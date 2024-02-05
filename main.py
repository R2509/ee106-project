'''
Main file.
'''

from pathlib import Path
from re import X
import tkinter as tk
#from tkinter import ttk
#ttk.Button(win, text= "someShit", command=_AFunctionOrSmthn).pack()

dir_path = Path(__file__).parent.resolve()

class Placer:
    '''
    take arguments for .place() upon
    instantiation so that they don't
    need to be passed to .place() later.
    '''
    def __init__(
            self,
            element: tk.Button,
            x: int = 0,
            y: int = 0,
        ):
        self.element = element
        self.x = x
        self.y = y
    def place(self):
        '''
        Place the widget on the window.
        '''
        self.element.place(
            x = self.x,
            y = self.y,
        )

def create_button(
        x: int = 0,
        y: int = 0,
        text: str = 'TEXT',
        width: int = 5,
        height: int = 1,
    ):
    '''
    Create a `tkinter.Button` with
    the specified options.
    '''
    button = tk.Button(
        text = text,
        width = width,
        height = height,
    )
    return Placer(button, x=x, y=y)

## processes to be assigned 1 thread each

def getMean(k):
    return k






root = tk.Tk()
root.title("parallel processing engine")

button = create_button()
button.place()
root.mainloop()

