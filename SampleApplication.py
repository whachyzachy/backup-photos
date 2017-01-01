import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo, QDateTime
import os
import logging
from datetime import *
import shutil


class App(QWidget):


    def __init__(self):
        super().__init__()
        self.title = 'Photo Import App'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 300
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.labelcurrent = QLabel()
        vertLayout = QVBoxLayout()

        tempButton = QPushButton('Choose Directory')
        tempButton.clicked.connect(self.handlePressed)
        vertLayout.addWidget(tempButton)
        vertLayout.addWidget(self.labelcurrent)
        self.labelcurrent.setText("No files copied yet...")


        self.setLayout(vertLayout)

        self.show()

    def handlePressed(self):
        dirname = QFileDialog.getExistingDirectory(self,'Open Directory With Pictures')
        print(dirname)
        print('Directory Name %s ' % dirname)

        currenttime = datetime.now()

        daysback = 30

        print('File is in directory %s' % dirname)
        recentlymodified = {}
        datesofpics = set()
        yearsofpics = set()

        filetypes = set(['.JPG','.xml','.MOV'])

        #topdir = '/home/jgibbs/TopDirTest/'
        topdir = '/media/windowsshare/Jason'

        for dirname, subdirs, files in os.walk(dirname):
            #print('directory %s ' % dirname)
            for file in files:
                try:
                    fullpath = os.path.join(dirname,file)
                    #print('full path %s ' % fullpath)

                    modtime = os.path.getmtime(fullpath)
                    moddatetime = datetime.fromtimestamp(modtime)


                    diff = currenttime - moddatetime

                    if (diff.days <= daysback):

                        filename_part, extension_part = os.path.splitext(file)

                        if (extension_part in filetypes):
                            recentlymodified[fullpath]=moddatetime
                            print ('diff days %s modified %s' % (diff.days,moddatetime.isoformat()))
                            datesofpics.add(moddatetime.date())
                            yearsofpics.add(moddatetime.year)

                except Exception as inst:
                    print('Exception type: %s file %s' % (type(inst),fullpath))

        print('DONE')

        for year_it in yearsofpics:
            full_year = os.path.join(topdir,str(year_it))
            if not os.path.exists(full_year):
                os.makedirs(full_year)

        for date_it in datesofpics:
            print('%s year and date %s' % (date_it.year,str(date_it)))

            full_date = os.path.join(topdir,str(date_it.year),str(date_it))
            if not os.path.exists(full_date):
                os.makedirs(full_date)


        totalcopied = 0
        for file, mod_time in recentlymodified.items():
            print('%s modded %s type %s' %(file,mod_time,type(mod_time)))
            print('year %s ' % mod_time.year)
            full_date = os.path.join(topdir, str(mod_time.year), str(mod_time.date()),os.path.basename(file))
            print('full_date %s' % full_date)
            if not os.path.exists(full_date):
                try:
                    self.labelcurrent.setText(file)
                    shutil.copyfile(file,full_date)
                    totalcopied = totalcopied + 1
                except Exception as inst:
                    print('Copy file exception %s for file %s' % (full_date,type(inst)))
        self.labelcurrent.setText("Copied %s files " % totalcopied)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
