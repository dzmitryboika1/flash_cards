import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card_canvas.itemconfig(card_bg_image, image=card_front_image)
    card_canvas.itemconfig(french_title, text="French", fill="black")
    card_canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card_canvas.itemconfig(card_bg_image, image=card_back_image)
    card_canvas.itemconfig(french_title, text="English", fill="white")
    card_canvas.itemconfig(french_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data_frame = pandas.DataFrame(to_learn)
    data_frame.to_csv("data/words_to_learn", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

# Canvas
card_canvas = Canvas(width=800, height=526)
card_canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_bg_image = card_canvas.create_image(400, 265, image=card_front_image)
french_title = card_canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
french_word = card_canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
card_canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
