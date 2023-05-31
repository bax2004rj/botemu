from panda3d.core import *
from direct.showbase.ShowBase import ShowBase


loadPrcFileData("","load-file-type p3assimp")

class Core():
    def __init__(self,pandaInstance):
        floor = pandaInstance.loader.load_model("assets/VL-FIELD-TTILE-GRAY.obj",)
        floor.reparent_to(pandaInstance.render)