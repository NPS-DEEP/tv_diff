from PyQt5.QtWidgets import QMessageBox

"""Simple message box for simple popup warnings.
"""

def show_popup(parent, message):
    # raise RuntimeError("bad") # force fail for diagnostics
    mb = QMessageBox()
    mb.setText(message)
    mb.exec()

