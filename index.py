from helpers.base import render
from pages.menu import setup_menu
from main.root import get_root,setup_gui
from helpers.log import config_log


if __name__ == "__main__":
    config_log()

    root = get_root()

    setup_menu()

    setup_gui()
    
    render('home')

    root.mainloop()

