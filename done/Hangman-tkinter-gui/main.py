import random
import re
import string
import time
from queue import Queue
from threading import Thread
import numpy
from tkinter import *

import tkinter as tk
from tkinter import ttk
from functools import *


class Hangman:
    _buttons = [0] * 26  # Array with buttons that contains all the letters
    chosen_word = ''  # the word chosed randomly
    root = ''
    canv = ''
    printed_word = ''
    final_test = ''
    lives = 6
    hearts = numpy.empty((6, 3))
    reset_button=0
    paintLetter=''

    def __init__(self, prm):
        self.root = prm
        self.canv = Canvas(self.root, width=800, height=400)
        self.canv.pack()
        # pole
        self.canv.create_line((70, 300, 70, 50), (70, 50, 200, 50), (200, 50, 200, 70))
        self.canv.create_line(40, 300, 100, 300)
        self.canv.create_text(110, 15, text="Lives :",font=2)

        self.reset_button = Button(self.root, text="Reset", width=5, command=partial(self.reset))
        self.reset_button.place(x=750, y=350)

        self.choseRandWord()
        self.buildButtons()
        self.paintLines()
        self.paintLives()
        self.paintMan()



    def buildButtons(self):  # Print the buttons with the searchFunction incorporate
        nrAsc = ord('a')
        for i in range(26):
            x = 500
            y = 200
            asc = chr(nrAsc)
            self._buttons[i] = Button(self.root, text="" + asc.upper() + "", width=3, command=partial(self.searchLetter, asc))
            if 0 <= i < 8:
                self._buttons[i].place(x=x + i * 29, y=y)
            elif 8 <= i < 16:
                j = i - 8
                self._buttons[i].place(x=x + j * 29, y=y + 25)
            elif 16 <= i < 24:
                j = i - 16
                self._buttons[i].place(x=x + j * 29, y=y + 50)
            else:
                j = i - 24
                self._buttons[i].place(x=x + 87 + j * 29, y=y + 75)
            nrAsc += 1
    def reset(self):

        for i in range(len(self.chosen_word)):
            self.paintLetter = tk.Label(root, text="  ", font=('', 15))
            self.paintLetter.place(x=i * 30 + 2, y=318)
        self.choseRandWord()
        self.printed_word=['']*len(self.chosen_word)
        self.canv.delete("all")

        self.canv.create_line((70, 300, 70, 50), (70, 50, 200, 50), (200, 50, 200, 70))
        self.canv.create_line(40, 300, 100, 300)
        self.canv.create_text(110, 15, text="Tries :", font=2)

        self.buildButtons()
        self.lives = 6

        self.paintLives()
        self.paintLines()


    def choseRandWord(self):  # randomly chose a word
        word_list = open("Words", "r").read().strip(' ').split(' ')
        num = random.randint(0, len(word_list) - 1)
        self.chosen_word = word_list[num]
        self.printed_word = [''] * len(self.chosen_word)

    def searchLetter(self, asc):  # search the letter in word ; if it's found, destroy the button and print the letter
        index = ord(asc)  # conversion char -> number
        index -= ord('a')
        self._buttons[index].destroy()  # destroy the button that represents the letter in the array
        if asc in self.chosen_word:
            for find in re.finditer(asc, self.chosen_word):  # find the duplicates
                print(find.start())
                self.printed_word[find.start()] = asc
        else:
            self.lives -= 1
            if self.lives == 0:
                self.canv.create_text(600,100 , text="You lost !",font=('','20','bold'))
                self.canv.create_text(600, 150, text="Your word was : " + str(self.chosen_word), font=('', '15', ''))
                for i in range(26):
                    if (self._buttons[i] != None):
                        self._buttons[i].destroy()

        self.showLetters()
        self.paintMan()


        self.final_test = ''.join(
            [str(item) for item in self.printed_word])  # conversion from list of chars to a string

        if self.chosen_word == self.final_test:
            self.canv.create_text(600, 100, text="You Won !", font=('', '20', 'bold'))
            for i in range(26):
                if (self._buttons[i] != None):
                    self._buttons[i].destroy()


    def paintLives(self):
        for i in range(6):
            self.hearts[i][0] = self.canv.create_arc(160 + i * 25, 5, 171 + i * 25, 15, start=0, extent=180,
                                                     fill="black",tag="heart0"+str(i))
            self.hearts[i][1] = self.canv.create_arc(150 + i * 25,5, 161 + i * 25, 15, start=0, extent=180,
                                                     fill="black",tag="heart1"+str(i))
            self.hearts[i][2] = self.canv.create_polygon((149 + i * 25, 10, 160 + i * 25, 25),
                                                         (160 + i * 25, 25, 172 + i * 25, 10), fill="black",tags="heart2"+str(i))

    def paintMan(self):
        match self.lives:
            case 5:
                self.canv.create_oval(180, 70, 220, 110, fill="black")
                self.canv.delete("heart05", "heart15", "heart25")
            case 4:
                self.canv.create_line(200, 110, 200, 190)
                self.canv.delete("heart04", "heart14", "heart24")
            case 3:
                self.canv.create_line(200, 110, 230, 150)  # hands
                self.canv.delete("heart03", "heart13", "heart23")
            case 2:
                self.canv.create_line(200, 110, 170, 150)
                self.canv.delete("heart02", "heart12", "heart22")
            case 1:
                self.canv.create_line(200, 190, 230, 230)  # legs
                self.canv.delete("heart01", "heart11", "heart21")
            case 0:
                self.canv.create_line(200, 190, 170, 230)
                self.canv.delete("heart00","heart10","heart20")

    def paintLines(self):
        for i in range(len(self.chosen_word)):
            self.canv.create_line(i * 30, 350, 20 + i * 30, 350, width=5)  # fill='red', dash=(10,5), width=2

    def showLetters(self):
        for i in range(len(self.chosen_word)):
            self.paintLetter = tk.Label(root, text="" + self.printed_word[i] + "", font=('', 15))
            self.paintLetter.place(x=i * 30 + 2, y=318)

        #  horizontal = Frame(root, bg='blue', height=1, width=70)
        #  horizontal.place(x=50, y=30)
        pass

    #  B = Button(root, text="Afiseaza", command=lambda: print(a.public_chars))


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x400")
    root.resizable(False, False)
    root.title("Hangman")

    I = tk.Label(root, text="Text \n initial")
    I.configure(text="Text modificat")
    # I.grid(row=0,column=0)
    # char = Text(root, width=100, height=1)

    game = Hangman(root)
    root.mainloop()
