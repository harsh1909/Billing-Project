from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot ,QRect
import page1
from PyQt5.QtGui import QFont

font = QFont("aerial",10,0,False)
#("family",size,weight,itallics or not)
       
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100,100,1200,600)
        self.setWindowTitle("Home")
        self.statusBar().showMessage('Message in statusbar.')
        
        
        self.home = page1.home_page(self)
        
        self.setFont(font)
        self.setCentralWidget(self.home)
        self.show()
        #self.showMaximized()

           

        



if __name__=="__main__":
    appctxt = ApplicationContext()
    app = QApplication(sys.argv)
    
    soft = main_window()
    
    sys.exit(appctxt.app.exec_())

