#!/usr/bin/python3.11
 
import random
from tkinter import *
from tkinter import messagebox as msgbox
import tkinter.font as tkFont
import time
 
class MineSweeper:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mines = 0
        self.lifes = 0
        self.fonts = ("", 10, "bold")
        self.color_bg = "aliceblue"
        self.ask_settings()
        if not self.width * self.height * self.mines:
            return
        self.cell_width = 4
        self.cell_height = 2
        self.mine_board = [[False for i in range(self.width)] for j in range(self.height)]
        self.game_window = Tk()
        self.game_window.title("🐈")
        self.game_window.geometry(str(42 * self.width + 3) + "x" + str(44 * self.height + 3 + 22))
        self.game_window.configure(bg=self.color_bg)
        self.cells = self.set_cells()
        self.set_status_bar()
        self.game_over = False
        self.game_won = False
        self.is_first_loop = True
 
        self.game_window.mainloop()
 
 
    def open_cell_callback(self, _event: Event):
        if _event.widget["text"] == "🚩":
            return
        grid = _event.widget.grid_info()
        if self.is_first_loop:
            self.set_mines(grid["column"], grid["row"])
            self.print_mine_board()
            self.start_time = time.time()
            self.is_first_loop = False
 
        if self.mine_board[grid["row"]][grid["column"]]:
            if self.lifes > 1:
                self.lifes -= 1
                msgbox.showwarning("Oops", "You hit a mine\nLifes: " + str(self.lifes))
                label = Label(self.game_window,text="💥", width=self.cell_width, height=self.cell_height, font=self.fonts, bg=self.color_bg)
                label.grid(row=grid["row"], column=grid["column"])
                self.cells[grid["row"]][grid["column"]].destroy()
                self.cells[grid["row"]][grid["column"]] = label
                self.mines_left_label.configure(text="Mines left: " + str(int(self.mines_left_label.cget("text").split(": ")[1]) - 1))
                self.lifes_left_label.configure(text="Lifes left: " + str(int(self.lifes_left_label.cget("text").split(": ")[1]) - 1))
                return
 
            self.game_over = True
            self.show_answer()
            msgbox.showerror("Game Over", "You lose")
            self.game_window.destroy()
            return
        else:
            self.open_cell(grid["row"], grid["column"])
            if self.judge_win():
                self.game_won = True
                msgbox.showinfo("Clear", "You win")
                self.game_window.destroy()
 
 
    def flag_callback(self, _event: Event):
        if _event.widget["text"] == "🚩" :
            _event.widget.config(text=" ", font=self.fonts)
            self.mines_left_label.configure(text="Mines left: " + str(int(self.mines_left_label.cget("text").split(": ")[1]) + 1))
        else:
            _event.widget.config(text="🚩", font=self.fonts)
            self.mines_left_label.configure(text="Mines left: " + str(int(self.mines_left_label.cget("text").split(": ")[1]) - 1))
 
        self.game_window.update()
 
 
    def show_answer(self):
        for i in range(self.height):
            for j in range(self.width):
                if type(self.cells[i][j]) == Button:
                    self.show_cell(i, j)
 
 
    def show_cell(self, i: int, j: int):
        if self.cells[i][j].cget("text") == " ":
            if self.mine_board[i][j]:
                self.cells[i][j].configure(text="💣")
            else:
                self.cells[i][j].configure(text="😾")
 
        else:
            if not self.mine_board[i][j]:
                self.cells[i][j].configure(text="🐀")
 
 
    def set_status_bar(self):
        self.status_bar = Frame(self.game_window, width=42 * self.width, height=40, bg=self.color_bg)
        self.status_bar.grid(row=self.height, column=0, columnspan=self.width, sticky="W")
        self.mines_left_label = Label(self.status_bar, text="Mines left: " + str(self.mines), font=self.fonts, bg=self.color_bg)
        self.mines_left_label.grid(row=0, column=0)
        self.lifes_left_label = Label(self.status_bar, text="Lifes left: " + str(self.lifes), font=self.fonts, bg=self.color_bg)
        self.lifes_left_label.grid(row=0, column=1)
        self.time_label = Label(self.status_bar, text="Time: 0", font=self.fonts, bg=self.color_bg)
        self.time_label.grid(row=0, column=2)
        self.time_label.after(100, self.time_callback)
 
 
    def time_callback(self):
        self.time_label.after(100, self.time_callback)
        if self.is_first_loop:
            return
        if self.game_over:
            return
        if self.game_won:
            return
        now = time.time()
        self.time_label.configure(text="Time: " + str(int((now  - self.start_time) * 10) / 10))
 
 
    def open_cell(self, _x: int, _y: int):
        if type(self.cells[_x][_y]) == Label:
            return
        mines = self.count_mines(_x, _y)
        label = Label(self.game_window, text=mines if mines else "😻", width=self.cell_width, height=self.cell_height, font=self.fonts, bg=self.color_bg, fg=self.get_color(mines))
        label.grid(row=_x, column=_y)
        self.cells[_x][_y].destroy()
        self.cells[_x][_y] = label
        x = 0 if self.cells[_x][_y].cget("text") == "😻" else self.cells[_x][_y].cget("text")
        if not self.count_mines(_x, _y):
            for i in range(_y - 1, _y + 2):
                for j in range(_x - 1, _x + 2):
                    if i < 0 or j < 0 or i >= self.width or j >= self.height:
                        continue
                    self.open_cell(j, i)
 
 
    def judge_win(self) -> bool:
        for i in range(self.height):
            for j in range(self.width):
                if type(self.cells[i][j]) == Button and not self.mine_board[i][j]:
                    return False
 
        return True
 
 
    def get_color(self, _mines: int) -> str:
        #green -> yellow -> red
        match _mines:
            case 1:
                return "darkgreen"
            case 2:
                return "forestgreen"
            case 3:
                return "darkorange"
            case 4:
                return "orange"
            case 5:
                return "orangered"
            case 6:
                return "crimson"
            case 7:
                return "purple"
            case 8:
                return "saddlebrown"
            case _:
                return "black"
 
    def set_cells(self) -> []:
        cells = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                cell = Button(self.game_window,text=" ", width=self.cell_width, height=self.cell_height, font=self.fonts, bg=self.color_bg)
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", self.open_cell_callback)
                cell.bind("<Button-3>", self.flag_callback, add="+")
                row.append(cell)
 
            cells.append(row)
 
        return cells
 
 
    def count_mines(self, y, x) -> int:
        count = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                if self.mine_board[i][j]:
                    count += 1
 
        return count
 
 
    def ask_settings(self):
        self.setting_window = Tk()
        self.setting_window.title("🐈")
        self.setting_window.geometry("200x200")
 
        self.width_label = Label(self.setting_window, text="Width: ", font=self.fonts)
        self.width_label.place(x=0, y=0)
        self.width_txtbox = Entry(self.setting_window, font=self.fonts, width=5)
        self.width_txtbox.place(x=80, y=0)
        self.height_label = Label(self.setting_window, text="Height: ", font=self.fonts)
        self.height_label.place(x=0, y=30)
        self.height_txtbox = Entry(self.setting_window, font=self.fonts, width=5)
        self.height_txtbox.place(x=80, y=30)
        self.mines_label = Label(self.setting_window, text="Mines: ", font=self.fonts)
        self.mines_label.place(x=0, y=60)
        self.mines_txtbox = Entry(self.setting_window, font=self.fonts, width=5)
        self.mines_txtbox.place(x=80, y=60)
        self.lifes_label = Label(self.setting_window, text="Lifes: ", font=self.fonts)
        self.lifes_label.place(x=0, y=90)
        self.lifes_txtbox = Entry(self.setting_window, font=self.fonts, width=5 )
        self.lifes_txtbox.insert(0, "3")
        self.lifes_txtbox.place(x=80, y=90)
        self.settings_ok_button = Button(self.setting_window, text="OK", font=self.fonts, command=self.setting_window_func)
        self.settings_ok_button.place(y=120)
        self.setting_window.mainloop()
 
 
    def setting_window_func(self):
        if not self.width_txtbox.get() == "":
            self.width = int(self.width_txtbox.get())
 
        if not self.height_txtbox.get() == "":
            self.height = int(self.height_txtbox.get())
 
        if not self.mines_txtbox.get() == "":
            self.mines = int(self.mines_txtbox.get())
 
        if not self.lifes_txtbox.get() == "":
            self.lifes = int(self.lifes_txtbox.get())
 
        if not self.width * self.height * self.mines * self.lifes:
            return
        elif self.mines >= self.width * self.height - 9:
            msgbox.showerror("Error", "Too many mines")
            return
        elif self.lifes < 1:
            msgbox.showerror("Error", "Lifes must be biggar than 0")
            return
        else :
            msg = msgbox.askyesno("Confirm", "W*H: " + str(self.width) + " * " + str(self.height) + " Mines: " + str(self.mines) + " Lifes: " + str(self.lifes) + "\nAre you sure starting game with these settings?")
            if msg == True:
                self.setting_window.destroy()
                return
            else:
                return
 
 
    def print_mine_board(self):
        for i in range(self.height):
            for j in range(self.width):
                print(int(self.mine_board[i][j]), end=" ")
            print()
 
        print()
 
 
    def set_mines(self, _x: int, _y:int):
        for i in range(self.mines):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.is_in_forbitten_zone(_x, _y, x, y):
                    continue
 
                if not self.mine_board[y][x]:
                    self.mine_board[y][x] = True
                    break
 
 
    def is_in_forbitten_zone(self, _center_x: int, _center_y: int, _x: int, _y: int) -> bool:
        for i in range(_center_x - 1, _center_x + 2):
            for j in range(_center_y - 1, _center_y + 2):
                if i < 0 or i >= self.width or j < 0 or j >= self.height:
                    continue
 
                if i == _x and j == _y:
                    return True
 
        return False
 
 
if __name__ == "__main__":
    game = MineSweeper()
