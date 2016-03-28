import sys
sys.path.append('C:\Anaconda3\Lib\site-packages')
import os
import argparse
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QRadioButton, QComboBox, QCheckBox
from random import randint


class Widget(QWidget):

    vocab = None    # will store vocab for class
    progress = None # will store progress into lesson
    sel = None      # Stores current selection from vocab
    eLanguage = None# True/False for determining which language to type in

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Русский Язык Учитель')  # Setting the application window title
        
        self.primary_layout = QVBoxLayout() # Hold all HBox layouts
        self.h_layout_0 = QHBoxLayout()
        self.h_layout_1 = QHBoxLayout()
        self.h_layout_2 = QHBoxLayout()
        self.mSelect = QComboBox() # for selecting a module...
        
        # populating the combobox...
        modules = os.listdir("Modules/")
        for item in modules:
            self.mSelect.addItem(item.replace('.txt', ''))
            print(item)
        
        # setting up default module loaded
        self.vocab = []
        defaultModule = open("Modules/"+modules[0], encoding="utf-8")
        for line in defaultModule:
            words = line.split("\t")
            self.vocab.append((words[0], words[1].replace("\n", "")))
        defaultModule.close()
		
        self.progress = 1						# initializing the user's 'progress'
        self.sel = randint(1, len(self.vocab)-1)# Setting the initial vocab selection to something random
        
        #self.h_layout_0.addWidget(self.lSelect)
        self.h_layout_0.addWidget(self.mSelect)
        self.mSelect.activated[str].connect(self.loadModule)
        
        ### h_layout_1 contents...
        self.russian = QLineEdit()
        self.russian.setText(self.vocab[self.sel][0])
        self.russian.setFixedWidth(200)
        self.russian.returnPressed.connect(self.enter_pressed)
        self.russian_label = QtGui.QLabel('Russian')
        self.h_layout_1.addWidget(self.russian_label)
        self.h_layout_1.addWidget(self.russian)
        
        ### h_layout_2 contents...
        self.english = QLineEdit()
        self.english.setFixedWidth(200)
        self.english.returnPressed.connect(self.enter_pressed)
        self.url_label = QtGui.QLabel('English')
        self.h_layout_2.addWidget(self.url_label)
        self.h_layout_2.addWidget(self.english)

        # Finishing...
        self.status_bar = QtGui.QStatusBar(self)
        
		# Adding the sublayouts to the primary layout
        self.primary_layout.addLayout(self.h_layout_0)
        self.primary_layout.addLayout(self.h_layout_1)
        self.primary_layout.addLayout(self.h_layout_2)

		# Instantiating the progress bar
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setMinimum(1)
        self.progressbar.setMaximum(100)
        
        self.lSelect = QCheckBox("Type Russian") # for selecting the entry language
        self.lSelect.stateChanged.connect(self.changeInputLanguage)
        self.primary_layout.addWidget(self.lSelect)
        self.primary_layout.addWidget(self.progressbar)
        self.setLayout(self.primary_layout)
        
        self.progressbar.setValue(self.progress)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
     
	
    def changeInputLanguage(self):
        if self.lSelect.isChecked():
            self.russian.setText("")
            self.english.setText(self.vocab[self.sel][1])
        else:
            self.english.setText("")
            self.russian.setText(self.vocab[self.sel][0])

   
    def enter_pressed(self):
        
        if self.lSelect.isChecked(): # we are checking the russian entry
            if self.vocab[self.sel][0] == self.russian.text():
                self.progress = self.progress + 1
            elif self.progress > 0:
                self.progress = self.progress - 1
            self.sel = randint(1, len(self.vocab)-1)
            self.progressbar.setValue(self.progress)
            self.russian.setText("")
            self.english.setText(self.vocab[self.sel][1])
            
        else: # we are checking the English entered...
            if self.vocab[self.sel][1] == self.english.text():
                self.progress = self.progress + 1
            elif self.progress > 0:
                self.progress = self.progress - 1
        
            self.sel = randint(1, len(self.vocab)-1)
            self.progressbar.setValue(self.progress)
            self.english.setText("")
            self.russian.setText(self.vocab[self.sel][0])
    
    def loadModule(self, text):
        self.vocab = []
        selectedModule = open("Modules/"+text+".txt", encoding="utf-8")
        for line in selectedModule:
            words = line.split("\t")
            self.vocab.append((words[0], words[1].replace("\n", "")))
        
        if self.lSelect.isChecked(): # we are checking the russian entry
            self.sel = randint(1, len(self.vocab)-1)
            self.progressbar.setValue(self.progress)
            self.russian.setText("")
            self.english.setText(self.vocab[self.sel][1])
            self.progress = 0
            self.progressbar.setValue(self.progress)
        else:    
            self.english.setText("")
            self.progress = 0
            self.progressbar.setValue(self.progress)
            self.sel = randint(1, len(self.vocab)-1)
            self.russian.setText(self.vocab[self.sel][0])
        selectedModule.close()
        

if __name__ == '__main__':
  app = QApplication(sys.argv)
  widget = Widget()
  widget.show()

  sys.exit(app.exec_())  
