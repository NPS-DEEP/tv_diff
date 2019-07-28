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
        SettingsDialog.resize(578, 299)
        self.button_box = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.button_box.setGeometry(QtCore.QRect(190, 260, 301, 32))
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
        self.groupBox_3.setGeometry(QtCore.QRect(20, 70, 521, 181))
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 501, 151))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.use3_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.use3_cb.setText("")
        self.use3_cb.setObjectName("use3_cb")
        self.gridLayout.addWidget(self.use3_cb, 4, 1, 1, 1)
        self.use0_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.use0_cb.setText("")
        self.use0_cb.setObjectName("use0_cb")
        self.gridLayout.addWidget(self.use0_cb, 1, 1, 1, 1)
        self.use1_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.use1_cb.setText("")
        self.use1_cb.setObjectName("use1_cb")
        self.gridLayout.addWidget(self.use1_cb, 2, 1, 1, 1)
        self.slider0 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider0.setMaximum(255)
        self.slider0.setOrientation(QtCore.Qt.Horizontal)
        self.slider0.setObjectName("slider0")
        self.gridLayout.addWidget(self.slider0, 1, 3, 1, 1)
        self.use2_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.use2_cb.setText("")
        self.use2_cb.setObjectName("use2_cb")
        self.gridLayout.addWidget(self.use2_cb, 3, 1, 1, 1)
        self.use4_cb = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.use4_cb.setText("")
        self.use4_cb.setObjectName("use4_cb")
        self.gridLayout.addWidget(self.use4_cb, 5, 1, 1, 1)
        self.slider1 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider1.setMaximum(255)
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setObjectName("slider1")
        self.gridLayout.addWidget(self.slider1, 2, 3, 1, 1)
        self.slider2 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider2.setMaximum(255)
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setObjectName("slider2")
        self.gridLayout.addWidget(self.slider2, 3, 3, 1, 1)
        self.slider3 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider3.setMaximum(255)
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        self.slider3.setObjectName("slider3")
        self.gridLayout.addWidget(self.slider3, 4, 3, 1, 1)
        self.slider4 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider4.setMaximum(255)
        self.slider4.setOrientation(QtCore.Qt.Horizontal)
        self.slider4.setObjectName("slider4")
        self.gridLayout.addWidget(self.slider4, 5, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

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
        self.groupBox_3.setTitle(_translate("SettingsDialog", "Sensitivity"))
        self.label_5.setText(_translate("SettingsDialog", "Mode"))
        self.label_8.setToolTip(_translate("SettingsDialog", "Texture Vector Element"))
        self.label_8.setText(_translate("SettingsDialog", "Texture"))
        self.label_6.setText(_translate("SettingsDialog", "Mode Count"))
        self.label_9.setToolTip(_translate("SettingsDialog", "Enable this Texture"))
        self.label_9.setText(_translate("SettingsDialog", "Enable"))
        self.label_11.setToolTip(_translate("SettingsDialog", "Similarity Threshold"))
        self.label_11.setText(_translate("SettingsDialog", "Acceptance Threshold"))
        self.label_3.setText(_translate("SettingsDialog", "Standard Deviation"))
        self.label_7.setText(_translate("SettingsDialog", "Entropy"))
        self.label_4.setText(_translate("SettingsDialog", "Mean"))


