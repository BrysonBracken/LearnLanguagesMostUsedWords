import pandas
import tkinter as tk
import random

BACKGROUND_COLOR = "#373fff"
WHITE = "#FFFFFF"
FONT_LARGE = ("Ariel", 45, "bold")
FONT_LANGUAGE = ("Ariel", 30, "italic")
word_index_num = 0
display_language = 'Spanish'
spanish_dict = []
to_learn_dict = []
learning_mode = 'pending'
last_three_words = False


def most_frequent_words_app():
    # data process

    def load_learn_list():
        global spanish_dict
        global learning_mode
        try:
            with open("data/Spanish,English_to_learn.csv", encoding='UTF-8') as spanish_file:
                spanish_data = pandas.read_csv(spanish_file)
                spanish_dict = spanish_data.to_dict(orient="records")
                learning_mode = 'refresh'
        except FileNotFoundError:
            learning_mode = 'new words'
            try:
                with open("data/Spanish,English_personal.csv", encoding='UTF-8') as spanish_file:
                    spanish_data = pandas.read_csv(spanish_file)
                    spanish_dict = spanish_data.to_dict(orient="records")
            except FileNotFoundError:
                with open("data/Spanish,English.csv", encoding='UTF-8') as spanish_file:
                    spanish_data = pandas.read_csv(spanish_file)
                    spanish_dict = spanish_data.to_dict(orient="records")
        finally:
            word_button.config(text=f"{spanish_dict[0][display_language]}")
            language_button.config(text=f"{display_language}")

    def load_new_words():
        global to_learn_dict
        global spanish_dict
        global learning_mode
        to_learn_dict.extend(spanish_dict)
        with open("data/Spanish,English_personal.csv", encoding='UTF-8') as spanish_file:
            spanish_data = pandas.read_csv(spanish_file)
            spanish_dict = spanish_data.to_dict(orient="records")
            learning_mode = 'new words'

    # functions

    def word_known():
        global word_index_num
        global spanish_dict
        spanish_dict.pop(word_index_num)
        if learning_mode == 'refresh':
            spanish_data = pandas.DataFrame(spanish_dict)
            spanish_data.to_csv("data/Spanish,English_to_learn.csv", encoding='UTF-8')
        elif learning_mode == 'new words':
            spanish_data = pandas.DataFrame(spanish_dict)
            spanish_data.to_csv("data/Spanish,English_personal.csv", encoding='UTF-8')
        word_choice()

    def word_not_known():
        global to_learn_dict
        global spanish_dict
        global learning_mode
        if learning_mode == 'refresh':
            word_choice()
        elif learning_mode == 'new words':
            to_learn_dict.append(spanish_dict[word_index_num])
            spanish_data_to_learn = pandas.DataFrame(to_learn_dict)
            spanish_data_to_learn.to_csv("data/Spanish,English_to_learn.csv", encoding='UTF-8')
            spanish_dict.pop(word_index_num)
            spanish_data = pandas.DataFrame(spanish_dict)
            spanish_data.to_csv("data/Spanish,English_personal.csv", encoding='UTF-8')
            word_choice()

    def check_it():
        global learning_mode
        global last_three_words
        if learning_mode == 'new words':
            if len(spanish_dict) == 0:
                last_three_words = True
                load_learn_list()
        elif learning_mode == 'refresh' and len(spanish_dict) == 0 and last_three_words:
            word_button.config(text="You have learned everything!")
            word_button.grid(column=1, row=1, sticky="n")

    def word_choice():
        global word_index_num
        global display_language
        global learning_mode
        global last_three_words
        global spanish_dict
        check_it()
        display_language = 'Spanish'
        word_index_num = random.randint(0, len(spanish_dict) - 1)
        message = f"{spanish_dict[word_index_num][display_language]}"
        word_button.config(text=message)
        language_button.config(text=f"{display_language}")
        language_button.grid(column=1, row=0, sticky="s")
        word_button.grid(column=1, row=1, sticky="n")
        if learning_mode == 'refresh' and not last_three_words:
            if len(spanish_dict) <= 3:
                load_new_words()


    def switch_language():
        global display_language
        if display_language == 'Spanish':
            display_language = 'English'
        else:
            display_language = 'Spanish'
        word_button.config(text=f"{spanish_dict[word_index_num][display_language]}")
        language_button.config(text=f"{display_language}")

    # interface
    window = tk.Tk()
    window.title("Learn Most Frequent Words")
    window.iconbitmap("images/globe.ico")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    window.geometry("800x650")

    # buttons
    card_image = tk.PhotoImage(file="images/card_plain.png")
    card_button = tk.Button(image=card_image, highlightthickness=0, width=700, height=530, borderwidth=0,
                            bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR,
                            relief=tk.SUNKEN, command=switch_language)
    word_button = tk.Button(text="", highlightthickness=0,
                            font=FONT_LARGE, borderwidth=0, bg=WHITE, activebackground=WHITE, relief=tk.SUNKEN,
                            command=switch_language)
    language_button = tk.Button(text="", highlightthickness=0, font=FONT_LANGUAGE, borderwidth=0,
                                bg=WHITE, activebackground=WHITE, relief=tk.SUNKEN, command=switch_language)
    x_image = tk.PhotoImage(file="images/wrong_plain3.png")
    x_button = tk.Button(image=x_image, highlightthickness=0, borderwidth=0, height=100,
                         bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, command=word_not_known)
    check_image = tk.PhotoImage(file="images/right_plain2.png")
    check_button = tk.Button(image=check_image, highlightthickness=0, borderwidth=0, height=100,
                             bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, command=word_known)
    # labels
    know_it_label = tk.Label(text="Know it?", font=FONT_LARGE, bg=BACKGROUND_COLOR, foreground=WHITE)

    # placement
    card_button.grid(column=0, row=0, columnspan=3, rowspan=2)
    x_button.grid(column=0, row=2, sticky="w")
    check_button.grid(column=2, row=2, sticky="e")
    language_button.grid(column=1, row=0, sticky="s")
    word_button.grid(column=1, row=1, sticky="n")
    know_it_label.grid(column=1, row=2, pady=10)

    # layout
    window.rowconfigure(index=0, weight=3)
    window.rowconfigure(index=1, weight=3)
    window.rowconfigure(index=2, weight=1)

    window.columnconfigure(index=0, weight=1)
    window.columnconfigure(index=1, weight=1)
    window.columnconfigure(index=2, weight=1)

    load_learn_list()
    window.mainloop()


if __name__ == "__main__":
    most_frequent_words_app()
