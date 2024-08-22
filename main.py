from tkinter import *
from tkinter import messagebox
import random
import pandas
import math

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_word = {}
# ____________________ CSV ____________________ #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ____________________ BRAIN ____________________ #
def next_card():
    global current_word
    global flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(lang_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    flip_timer = window.after(3000, check)


def check():
    canvas.itemconfig(lang_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_word["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_img)


def is_known():
    to_learn.remove(current_word)

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
    

# ____________________ UI SETUP ____________________ #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, check)

canvas = Canvas(width=800, height=526)

back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=back_img)

canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)

lang_text = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="text", font=("Ariel", 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

# ____________________ BUTTONS ____________________ #
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
