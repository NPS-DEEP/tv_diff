from PyQt5.QtWidgets import QMessageBox

"""Simple message box for simple popup warnings.
"""

def show_popup(parent, message):
    # debug zz=5/0
    mb = QMessageBox()
    mb.setText(message)
    mb.exec()

