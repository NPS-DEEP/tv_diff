#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication
from browser_main_window import BrowserMainWindow
from show_popup import show_popup

# main
if __name__=="__main__":
    parser = ArgumentParser(
                   description="TV file similarity browser.")
    parser.add_argument("-i", "--index", type=int,
                        help="The index of the first file to compare with.")

    args = parser.parse_args()

    # create the "application" and the main window
    application = QApplication(sys.argv)
    browser_main_window = BrowserMainWindow()

    # start the GUI
    browser_main_window.w.show()

    # maybe select an index
    if args.index:
        try:
            browser_main_window.browser_change_manager.change_node_record1(
                           browser_main_window.all_nodes[args.index-1])
        except IndexError as e:
            show_popup(browser_main_window.w, "Invalid node index ignored.")

    sys.exit(application.exec_())

