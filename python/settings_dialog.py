# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(578, 335)
        self.button_box = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.button_box.setGeometry(QtCore.QRect(190, 290, 301, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.button_box.setObjectName("button_box")
        self.load_pb = QtWidgets.QPushButton(SettingsDialog)
        self.load_pb.setGeometry(QtCore.QRect(130, 20, 121, 36))
        self.load_pb.setObjectName("load_pb")
        self.save_pb = QtWidgets.QPushButton(SettingsDialog)
        self.save_pb.setGeometry(QtCore.QRect(270, 20, 121, 36))
        self.save_pb.setObjectName("save_pb")
        self.groupBox_3 = QtWidgets.QGroupBox(SettingsDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 70, 541, 201))
        self.groupBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_3.setStyleSheet("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 9px;\n"
"    margin-top: 0.5em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 501, 155))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.slider0 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider0.setMaximum(1000)
        self.slider0.setOrientation(QtCore.Qt.Horizontal)
        self.slider0.setObjectName("slider0")
        self.gridLayout.addWidget(self.slider0, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 7, 0, 1, 1)
        self.rejection_slider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.rejection_slider.setMaximum(1000)
        self.rejection_slider.setOrientation(QtCore.Qt.Horizontal)
        self.rejection_slider.setObjectName("rejection_slider")
        self.gridLayout.addWidget(self.rejection_slider, 7, 2, 1, 1)
        self.slider2 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider2.setMaximum(1000)
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setObjectName("slider2")
        self.gridLayout.addWidget(self.slider2, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.slider4 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider4.setMaximum(1000)
        self.slider4.setOrientation(QtCore.Qt.Horizontal)
        self.slider4.setObjectName("slider4")
        self.gridLayout.addWidget(self.slider4, 5, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.slider1 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider1.setMaximum(1000)
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setObjectName("slider1")
        self.gridLayout.addWidget(self.slider1, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.slider3 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider3.setMaximum(1000)
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        self.slider3.setObjectName("slider3")
        self.gridLayout.addWidget(self.slider3, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.button_box.accepted.connect(SettingsDialog.accept)
        self.button_box.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Texture Vector Threshold Settings"))
        self.load_pb.setToolTip(_translate("SettingsDialog", "Open saved settings"))
        self.load_pb.setText(_translate("SettingsDialog", "Load settings..."))
        self.save_pb.setText(_translate("SettingsDialog", "Save settings..."))
        self.groupBox_3.setTitle(_translate("SettingsDialog", "Settings"))
        self.label.setText(_translate("SettingsDialog", "Rejection threshold"))
        self.label_5.setText(_translate("SettingsDialog", "Mode weight"))
        self.label_3.setText(_translate("SettingsDialog", "Standard Deviation weight"))
        self.label_7.setText(_translate("SettingsDialog", "Entropy weight"))
        self.label_4.setText(_translate("SettingsDialog", "Mean weight"))
        self.label_6.setText(_translate("SettingsDialog", "Mode Count weight"))


