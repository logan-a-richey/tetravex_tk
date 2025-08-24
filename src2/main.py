#!/usr/bin/env python3

import tkinter as tk 

from controller import Controller

def main():
    print("Running program ...")
    root = tk.Tk()
    root.title("Tetravex App")

    c = Controller(root)
    root.mainloop()
    print("Exiting program ...")


if __name__ == "__main__":
    main()

