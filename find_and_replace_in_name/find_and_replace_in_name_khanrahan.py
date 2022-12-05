"""
Find & Replace in Name

URL:

    https://github.com/khanrahan/python_scripts/find_and_replace_in_name

Description:

    Perform find & replace on names of selected items.

Menus:

    Right-click selected clips on the Desktop --> Edit... -->  Find & Replace in Name

    Right-click selected clips in the Media Panel --> Edit...  --> Find & Replace in Name

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

from __future__ import print_function
from PySide2 import QtWidgets, QtCore

TITLE = "Find and Replace in Name"
VERSION_INFO = (0, 2, 0)
VERSION = ".".join([str(num) for num in VERSION_INFO])
TITLE_VERSION = "{} v{}".format(TITLE, VERSION)

MESSAGE_PREFIX = "[PYTHON HOOK]"

FOLDER_NAME = "Edit..."
ACTION_NAME = "Find and Replace in Name"


class FlameButton(QtWidgets.QPushButton):
    """
    Custom Qt Flame Button Widget
    To use:
    button = FlameButton('Button Name', do_when_pressed, window)
    """

    def __init__(self, button_name, do_when_pressed, parent_window, *args, **kwargs):
        super(FlameButton, self).__init__(*args, **kwargs)

        self.setText(button_name)
        self.setParent(parent_window)
        self.setMinimumSize(QtCore.QSize(110, 28))
        self.setMaximumSize(QtCore.QSize(110, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(do_when_pressed)
        self.setStyleSheet("""
            QPushButton {color: #9a9a9a;
                         background-color: #424142;
                         border-top: 1px inset #555555;
                         border-bottom: 1px inset black;
                         font: 14px 'Discreet'}
            QPushButton:pressed {color: #d9d9d9;
                                 background-color: #4f4f4f;
                                 border-top: 1px inset #666666;
                                 font: italic}
            QPushButton:disabled {color: #747474;
                                  background-color: #353535;
                                  border-top: 1px solid #444444;
                                  border-bottom: 1px solid #242424}
            QToolTip {color: black;
                      background-color: #ffffde;
                      border: black solid 1px}""")


class FlameLabel(QtWidgets.QLabel):
    """
    Custom Qt Flame Label Widget
    For different label looks set label_type as: 'normal', 'background', or 'outline'
    To use:
    label = FlameLabel('Label Name', 'normal', window)
    """

    def __init__(self, label_name, label_type, parent_window, *args, **kwargs):
        super(FlameLabel, self).__init__(*args, **kwargs)

        self.setText(label_name)
        self.setParent(parent_window)
        self.setMinimumSize(110, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        border-bottom: 1px inset #282828;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")
        elif label_type == 'background':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        background-color: #393939;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")
        elif label_type == 'outline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {color: #9a9a9a;
                        background-color: #212121;
                        border: 1px solid #404040;
                        font: 14px 'Discreet'}
                QLabel:disabled {color: #6a6a6a}""")


class FlameLineEdit(QtWidgets.QLineEdit):
    """
    Custom Qt Flame Line Edit Widget
    Main window should include this: window.setFocusPolicy(QtCore.Qt.StrongFocus)
    To use:
    line_edit = FlameLineEdit('Some text here', window)
    """

    def __init__(self, text, parent_window, *args, **kwargs):
        super(FlameLineEdit, self).__init__(*args, **kwargs)

        self.setText(text)
        self.setParent(parent_window)
        self.setMinimumHeight(28)
        self.setMinimumWidth(110)
        # self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""
            QLineEdit {color: #9a9a9a;
                       background-color: #373e47;
                       selection-color: #262626;
                       selection-background-color: #b8b1a7;
                       font: 14px 'Discreet'}
            QLineEdit:focus {background-color: #474e58}
            QLineEdit:disabled {color: #6a6a6a;
                                background-color: #373737}
            QToolTip {color: black;
                      background-color: #ffffde;
                      border: black solid 1px}""")


class FlameListWidget(QtWidgets.QListWidget):
    """
    Custom Qt Flame List Widget
    To use:
    list_widget = FlameListWidget(window)
    """

    def __init__(self, parent_window, *args, **kwargs):
        super(FlameListWidget, self).__init__(*args, **kwargs)

        self.setMinimumSize(500, 250)
        self.setParent(parent_window)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # only want 1 selection possible.  no multi selection.
        #self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setSpacing(3)
        self.setAlternatingRowColors(True)
        self.setUniformItemSizes(True)
        self.setStyleSheet("""
            QListWidget {color: #9a9a9a;
                         background-color: #2a2a2a;
                         alternate-background-color: #2d2d2d;
                         outline: none;
                         font: 14px "Discreet"}
            QListWidget::item:selected {color: #d9d9d9;
                                        background-color: #474747}""")


class FlameTokenPushButton(QtWidgets.QPushButton):
    '''
    Custom Qt Flame Token Push Button Widget v2.1

    button_name: Text displayed on button [str]
    token_dict: Dictionary defining tokens. {'Token Name': '<Token>'} [dict]
    token_dest: LineEdit that token will be applied to [object]
    button_width: (optional) default is 150 [int]
    button_max_width: (optional) default is 300 [int]

    Usage:

        token_dict = {'Token 1': '<Token1>', 'Token2': '<Token2>'}
        token_push_button = FlameTokenPushButton('Add Token', token_dict, token_dest)
    '''

    def __init__(self, button_name, token_dict, token_dest, button_width=110, button_max_width=300):
        super(FlameTokenPushButton, self).__init__()
        from functools import partial

        self.setText(button_name)
        self.setMinimumHeight(28)
        self.setMinimumWidth(button_width)
        self.setMaximumWidth(button_max_width)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""
            QPushButton {color: rgb(154, 154, 154);
                         background-color: rgb(45, 55, 68);
                         border: none;
                         font: 14px "Discreet";
                         padding-left: 6px;
                         text-align: left}
            QPushButton:hover {border: 1px solid rgb(90, 90, 90)}
            QPushButton:disabled {color: rgb(106, 106, 106);
                                  background-color: rgb(45, 55, 68);
                                  border: none}
            QPushButton::menu-indicator {subcontrol-origin: padding;
                                         subcontrol-position: center right}
            QToolTip {color: rgb(170, 170, 170);
                      background-color: rgb(71, 71, 71);
                      border: 10px solid rgb(71, 71, 71)}""")

        def token_action_menu():

            def insert_token(token):
                for key, value in token_dict.items():
                    if key == token:
                        token_name = value
                        token_dest.insert(token_name)

            for key, value in token_dict.items():
                token_menu.addAction(key, partial(insert_token, key))

        token_menu = QtWidgets.QMenu(self)
        token_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        token_menu.setStyleSheet("""
            QMenu {color: rgb(154, 154, 154);
                   background-color: rgb(45, 55, 68);
                   border: none; font: 14px "Discreet"}
            QMenu::item:selected {color: rgb(217, 217, 217);
                                  background-color: rgb(58, 69, 81)}""")

        self.setMenu(token_menu)

        token_action_menu()


class FindReplace(object):
    """Find and replace in name for selected objects in Flame. """

    def __init__(self, selection):
        self.selection = selection

        self.find = ""
        self.replace = ""

        self.names = [item.name.get_value() for item in selection]
        self.names_new = [self.replace_wildcards(item, self.find, self.replace)
                          for item in self.names]

        self.message(TITLE_VERSION)
        self.message("Script called from {}".format(__file__))

        self.tool_tip_find = ("<p><b>Find</b></p>\n"
                              "Accepts the following wildcards:<br>"
                              "* = match any number of characters<br>"
                              "? = match a single character<br>"
                              "^ = match start<br>"
                              "$ = match end<br>")

        self.wildcards = {"Match All": "*", "Match Any": "?", "Match Start": "^",
            "Match End": "$"}
        self.main_window()


    @staticmethod
    def message(string):
        """Print message to shell window and append global MESSAGE_PREFIX."""

        print(" ".join([MESSAGE_PREFIX, string]))


    @staticmethod
    def replace_wildcards(string, pattern, replacement):
        """major influence from the below:
        https://stackoverflow.com/questions/65801340/wildcard-match-replace-and-or-multiple-string-wildcard-matching
        """

        import re

        split_pattern = re.split(r'([^*?$])', pattern)

        regex = ""

        for regex_piece in split_pattern:
            if regex_piece == "^":
                regex += "^"
            elif regex_piece == "*":
                regex += "\\S*"
            elif regex_piece == "?":
                regex += "\\S"
            elif regex_piece == "$":
                regex += "$"
            else:
                regex += "{}".format(re.escape(regex_piece))

        return re.sub(regex, replacement, string)


    def update_find(self):
        """ """

        # the below .encode is necessary because otherwise it will return unicode
        # and PyClip.name.set_value() does not take unicode
        self.find = self.find_line_edit.text().encode("ascii", "ignore")

        self.names_new = [self.replace_wildcards(item, self.find, self.replace)
                          for item in self.names]
        self.list_scroll.clear()
        self.list_scroll.addItems(self.names_new)

        if not self.find:
            self.list_scroll.clear()
            self.list_scroll.addItems(self.names)  # return to starting state


    def update_replace(self):
        """ """

        # the below .encode is necessary because otherwise it will return unicode
        # and PyClip.name.set_value() does not take unicode
        self.replace = self.replace_line_edit.text().encode("ascii", "ignore")

        if self.find:
            self.names_new = [self.replace_wildcards(item, self.find, self.replace)
                              for item in self.names]
            self.list_scroll.clear()
            self.list_scroll.addItems(self.names_new)


    def update_names(self):
        """Change names of the PyClips to the clean names, skip if unnecesary.

        Relies on 3 lists:
            self.selection = PyClip objects
            self.names = name of the PyClip objects
            self.names_clean = cleaned up names of the above
        """

        for num, clip in enumerate(self.selection):
            if self.names[num] == self.names_new[num]:
                self.message("Skipping {}. No change to name.".format(self.names[num]))
                continue

            clip.name.set_value(self.names_new[num])
            self.message("Renamed {} to {}".format(self.names[num],
                                                   self.names_new[num]))


    def main_window(self):
        """ """

        def ok_button():

            self.update_names()
            self.window.close()
            self.message("Done!")

        def cancel_button():

            self.window.close()
            self.message("Cancelled!")

        self.window = QtWidgets.QWidget()
        self.window.setMinimumSize(800, 130)
        self.window.setWindowTitle(TITLE_VERSION)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.setStyleSheet('background-color: #272727')

        # Center window in linux
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.window.move((resolution.width() / 2) - (self.window.frameSize().width() / 2),
                    (resolution.height() / 2) - (self.window.frameSize().height() / 2))

        # Labels
        self.find_label = FlameLabel('Find ', 'normal', self.window)
        self.replace_label = FlameLabel('Replace ', 'normal', self.window)

        # Line Edits
        self.find_line_edit = FlameLineEdit('', self.window)
        self.find_line_edit.setToolTip(self.tool_tip_find)
        self.find_line_edit.setToolTipDuration(999999)

        self.find_line_edit_frequents = ["-RSZ_Result"]
        self.find_line_edit_completer = QtWidgets.QCompleter(self.find_line_edit_frequents)
        self.find_line_edit.setCompleter(self.find_line_edit_completer)
        self.find_line_edit.textChanged.connect(self.update_find)

        self.replace_line_edit = FlameLineEdit(self.replace, self.window)
        self.replace_line_edit.textChanged.connect(self.update_replace)

        # Token Push Button
        self.token_push_button = FlameTokenPushButton('Wildcards', self.wildcards,
                self.find_line_edit)

        # Buttons
        self.ok_btn = FlameButton('Ok', ok_button, self.window)
        self.ok_btn.setStyleSheet('background: #732020')

        self.cancel_btn = FlameButton('Cancel', cancel_button, self.window)

        # List
        self.list_scroll = FlameListWidget(self.window)
        self.list_scroll.addItems(self.names)

        # Layout
        self.gridbox1 = QtWidgets.QGridLayout()
        self.gridbox1.setVerticalSpacing(10)
        self.gridbox1.setHorizontalSpacing(10)

        self.gridbox1.addWidget(self.find_label, 0, 0)
        self.gridbox1.addWidget(self.find_line_edit, 0, 1)
        self.gridbox1.addWidget(self.token_push_button, 0, 2)
        self.gridbox1.addWidget(self.replace_label, 1, 0)
        self.gridbox1.addWidget(self.replace_line_edit, 1, 1)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addSpacing(50)
        self.hbox1.addWidget(self.list_scroll)
        self.hbox1.addSpacing(50)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.cancel_btn)
        self.hbox2.addWidget(self.ok_btn)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setMargin(20)
        self.vbox.addLayout(self.gridbox1)
        self.vbox.insertSpacing(1, 20)
        self.vbox.addLayout(self.hbox1)
        self.vbox.insertSpacing(3, 20)
        self.vbox.addLayout(self.hbox2)

        self.window.setLayout(self.vbox)

        self.window.show()

        return self.window

def scope_not_desktop(selection):
    import flame

    for item in selection:
        if not isinstance(item, flame.PyDesktop):
            return True
    return False

def get_media_panel_custom_ui_actions():

    return [{ 'name': FOLDER_NAME,
              'actions': [{'name': ACTION_NAME,
                           'isVisible': scope_not_desktop,
                           'execute': FindReplace,
                           'minimumVersion': '2019'}]
           }]
