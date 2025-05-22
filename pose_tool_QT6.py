'''
Name: pose_tool.py
Description: Simple tool to load and save poses in Autodesk Maya using .json files.
Author: Joar Engberg 2022
Updated to Qt6 by: Patatifique
'''

import json
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from collections import OrderedDict
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtGui, QtWidgets

def maya_main_window():
    # Return the Maya main window as QMainWindow
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)

class PoseToolWindow(QtWidgets.QDialog):
    pose_folder_path = None
    
    def __init__(self):
        super(PoseToolWindow, self).__init__(maya_main_window())
        self.setWindowTitle("Simple Pose Tool")
        self.setWindowIcon(QtGui.QIcon(":character.svg"))
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowType.WindowContextHelpButtonHint)
        self.resize(200, 80)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.WindowType.Tool)
 
    def create_ui_widgets(self):
        self.text_label = QtWidgets.QLabel("Save/load pose from/to selected controllers or joints:")
        self.save_button = QtWidgets.QPushButton("Save pose ...")
        self.load_button = QtWidgets.QPushButton("Load pose ...")

    def create_ui_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.load_button)
        main_layout.addStretch()
 
    def create_ui_connections(self):
        self.save_button.clicked.connect(self.save_pose_dialog)
        self.load_button.clicked.connect(self.load_pose_dialog)

    def pose_folder_dialog(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select pose folder path", "")
        if folder_path:
            self.pose_folder_path = folder_path

    def save_pose_dialog(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save pose file", self.pose_folder_path, "Pose file (*.json);;All files (*.*)")
        if file_path:
            self.save_pose(file_path)
            print(f"Saved pose: {file_path}")

    def load_pose_dialog(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load pose file", self.pose_folder_path, "Pose file (*.json);;All files (*.*)")
        if file_path:
            self.load_pose(file_path)
            print(f"Loaded pose: {file_path}")

    def save_pose(self, pose_path):
        controllers = cmds.ls(sl=True)
        controller_dict = OrderedDict()

        for ctrl in controllers:
            attr_dict = OrderedDict()
            keyable_attr_list = cmds.listAttr(ctrl, keyable=True, unlocked=True) or []

            for attr in keyable_attr_list:
                attr_value = cmds.getAttr(f"{ctrl}.{attr}")
                attr_dict[attr] = attr_value

            controller_dict[ctrl] = attr_dict

        with open(pose_path, "w") as jsonFile:
            json.dump(controller_dict, jsonFile, indent=4)

    def load_pose(self, file_path):
        with open(file_path, "r") as jsonFile:
            pose_data = json.load(jsonFile)
        
        self.active_controls = []
        for ctrl, input_attrs in pose_data.items():
            if cmds.objExists(ctrl):
                for attr, value in input_attrs.items():
                    cmds.setAttr(f"{ctrl}.{attr}", value)
                self.active_controls.append(ctrl)

def start():
    global pose_tool_ui
    try:
        pose_tool_ui.close()
        pose_tool_ui.deleteLater()
    except:
        pass
    pose_tool_ui = PoseToolWindow()
    pose_tool_ui.show()

if __name__ == "__main__":
    start()