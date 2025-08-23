#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import tkinter as tk
from mediator import Mediator 

def main():
    root = tk.Tk()
    root.title("Tetravex")
    mediator = Mediator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

