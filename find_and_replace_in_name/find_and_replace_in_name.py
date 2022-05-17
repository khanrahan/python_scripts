'''
Script Name: Find and Replace
Script Version: 1.1
Flame Version: 2019
Creation Date: 01.01.19
Update Date: 12.07.21

Description:

    Find and replace names
'''

from __future__ import print_function
from PySide2 import QtWidgets, QtCore
import re


folder_name = "Edit..."
action_name = "Find and Replace in Sequence Name"


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
        self.setStyleSheet("""QPushButton {color: #9a9a9a;                     
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
            self.setStyleSheet("""QLabel {color: #9a9a9a;                      
                                          border-bottom: 1px inset #282828;    
                                          font: 14px 'Discreet'}               
                                  QLabel:disabled {color: #6a6a6a}""")         
        elif label_type == 'background':                                       
            self.setAlignment(QtCore.Qt.AlignCenter)                           
            self.setStyleSheet("""QLabel {color: #9a9a9a;                      
                                          background-color: #393939;           
                                          font: 14px 'Discreet'}               
                                  QLabel:disabled {color: #6a6a6a}""")         
        elif label_type == 'outline':                                          
            self.setAlignment(QtCore.Qt.AlignCenter)                           
            self.setStyleSheet("""QLabel {color: #9a9a9a;                      
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
        self.setStyleSheet("""QLineEdit {color: #9a9a9a;                       
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


def replaceWildcards(string, pattern, replacement):
    """major influence from the below:
    https://stackoverflow.com/questions/65801340/wildcard-match-replace-and-or-multiple-string-wildcard-matching
    """
    
    splitPattern = re.split(r'([^*?$])', pattern)

    regex = ""

    for regexPiece in splitPattern:
        if regexPiece == "^":
            regex += "^"
        elif regexPiece == "*":
            regex += "\\S*"
        elif regexPiece == "?":
            regex += "\\S"
        elif regexPiece == "$":
            regex += "$"
        else:
            regex += "{}".format(re.escape(regexPiece))

    return re.sub(regex, replacement, string)


def main_window(selection):
    """ """

    def cancel_button():

        window.close()

    def ok_button():
        for item in selection:
            print ("*" * 10)

            seq_name = str(item.name)[(1):-(1)]
            print ('Start Name: ' + str(seq_name))

            find_me = str(find_entry.text())
            print ('Find Me: ' + str(find_me))

            replace_with_me = str(replace_entry.text())
            print ('Replace With Me: ' + str(replace_with_me))

            new_name = replaceWildcards(seq_name, find_me, replace_with_me)
            item.name = new_name
            print ('New Name: ' + str(new_name))

            print ("*" * 10)
            print ("\n")

        window.close()

    window = QtWidgets.QWidget()
    window.setMinimumSize(600, 130)
    window.setWindowTitle('Find and Replace in Sequence Name')
    window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.setStyleSheet('background-color: #272727')

    # Center window in linux

    resolution = QtWidgets.QDesktopWidget().screenGeometry()
    window.move((resolution.width() / 2) - (window.frameSize().width() / 2),
                (resolution.height() / 2) - (window.frameSize().height() / 2))

    # Labels

    find_label = FlameLabel('Find ', 'normal', window)
    replace_label = FlameLabel('Replace ', 'normal', window)

    # Entries
    find_entry = FlameLineEdit('', window)

    replace_entry = FlameLineEdit('', window)

    # Buttons
    ok_btn = FlameButton('Ok', ok_button, window)
    ok_btn.setStyleSheet('background: #732020') 

    cancel_btn = FlameButton('Cancel', cancel_button, window)

    # Layout
    gridbox01 = QtWidgets.QGridLayout()
    gridbox01.setVerticalSpacing(10)
    gridbox01.setHorizontalSpacing(10)

    gridbox01.addWidget(find_label, 0, 0)
    gridbox01.addWidget(find_entry, 0, 1)
    gridbox01.addWidget(replace_label, 1, 0)
    gridbox01.addWidget(replace_entry, 1, 1)

    hbox03 = QtWidgets.QHBoxLayout()
    hbox03.addStretch(1)
    hbox03.addWidget(cancel_btn)
    hbox03.addWidget(ok_btn)

    vbox = QtWidgets.QVBoxLayout()
    vbox.setMargin(20)
    vbox.addLayout(gridbox01)
    vbox.insertSpacing(2, 20)
    vbox.addLayout(hbox03)

    window.setLayout(vbox)

    window.show()

    return window

def scope_clip(selection):
    import flame

    for item in selection:
        if isinstance(item, flame.PyClip):
            return True
    return False

def scope_not_desktop(selection):
    import flame

    for item in selection:
        if not isinstance(item, flame.PyDesktop):
            return True
    return False

def get_media_panel_custom_ui_actions():

    return [
        {
            'name': folder_name,
            'actions': [
                {
                    'name': action_name,
                    'isVisible': scope_not_desktop,
                    'execute': main_window,
                    'minimumVersion': '2019'
                }
            ]
        }
    ]
