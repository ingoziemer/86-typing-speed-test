import tkinter
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import random

word_index = 0
position = 0
display_list = []

file = open("top_200_words.txt", "r")
data = file.read()
word_list = data.split("\n")
file.close()

correct_words = 0
wrong_words = 0
words_typed = 0
count = 60


def capture_entry(event):
    current_word = type_field.get()
    current_word = current_word[:-1] # deletes space at the end
    global word_index
    global position
    global correct_words
    global wrong_words
    global words_typed
    words_typed += 1
    # check if typed word matches given word
    # then change color to word to green or red (right or wrong)
    words_field.tag_add(current_word, f"1.{position}", f"1.{position + len(display_list[word_index])}")
    # first index means start from character zero
    # "end" means read until the end of text box
    if current_word == display_list[word_index]:
        words_field.tag_config(current_word, background="white", foreground="green")
        correct_words += 1
    else:
        words_field.tag_config(current_word, background="white", foreground="red")
        wrong_words += 1
    position = position + len(display_list[word_index]) + 1
    word_index += 1
    type_field.delete(0, END)
    # highlight next word
    words_field.tag_add("next", f"1.{position}", f"1.{position + len(display_list[word_index])}")
    words_field.tag_config("next", background="grey", foreground="white")

    if words_typed > 24:
        display_words(25)
        words_typed = 0


def countdown():
    global count
    if count == 60:
        timer_label.config(text=f"1:00")
    elif count >= 10:
        timer_label.config(text=f"0:{count}")
    elif 10 > count > 0:
        timer_label.config(text=f"0:0{count}")
    else:
        timer_label.config(text=f"0:00")
        type_field.config(state="disabled")
        calculate_wpm(correct_words, wrong_words)
        return
    count -= 1
    window.after(1000, countdown)


def calculate_wpm(correct, wrong):
    result = tkinter.Toplevel()
    result.wm_title("Result")
    result.config(padx=10, pady=10, width=150, height=50)
    correct_label = Label(result, text=f"Correct Words: {correct}")
    correct_label.grid(row=0, column=0)
    wrong_label = Label(result, text=f"Wrong Words: {wrong}")
    wrong_label.grid(row=1, column=0)


def display_words(number):
    for n in range(number):
        word = random.choice(word_list)
        words_field.insert(END, word + " ")
        display_list.append(word)

# ---------------- UI -------------- #
window = ThemedTk(theme="yaru")
window.title("Typing Speed Test")
window.config(padx=100, pady=100, width=1200, height=500)

words_field = Text(window)
words_field.config(height=10, width=100)

display_words(50)
words_field.grid(row=0, column=0, columnspan=2)

# highlight first word
first_word_length = len(display_list[0])
words_field.tag_add("start", "1.0", f"1.{first_word_length}")
words_field.tag_config("start", background="grey", foreground="white")

# Labels
timer_label = ttk.Label(text="1:00")
timer_label.grid(row=1, column=1)

# Entries
type_field = ttk.Entry()
type_field.grid(row=1, column=0)

window.bind("<space>", capture_entry)

# Buttons
start_button = ttk.Button(text="Start", command=countdown)
start_button.grid(column=0, row=2)

if __name__ == '__main__':
    window.mainloop()

# room for improvement:
## make countdown start when user starts typing in entry field instead of button
## make the words fit better in the rows
## capture correct and incorrect letters; count number of keypress
