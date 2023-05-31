#Basic core loading
import cores.overUnder.CoreLoader as core
#Panda3d
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

class botemu(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        coreInstance = core(self)

app = botemu()
app.run()