import uiHandler
import fileHandler
class updateWin():
    def __init__(self,screen,win,events):
        uiHandler.draw_text(screen,win.x,win.y,fileHandler.font_big,"Updates availiable")