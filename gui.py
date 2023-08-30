import tkinter as tk
from tkinter import ttk
from ttkbootstrap import tb
from ttkbootstrap.constants import *

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 400

def create_window():
    window = tk.Tk()
    window.title('Manager of times')
    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - WINDOW_WIDTH / 2)
    center_y = int(screen_height/2 - WINDOW_HEIGHT / 2)

    window.geometry(f'{WINDOW_HEIGHT}x{WINDOW_WIDTH}+{center_x}+{center_y}')
    window.resizable(False, False)

    return window


def create_buttons(window):
    button_anlegen = ttk.Button()

def main():
    window = create_window()
    window.mainloop()


if __name__ == '__main__':
    main()


