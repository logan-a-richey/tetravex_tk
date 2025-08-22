#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

# main gui application
from ui.app import App 

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()

