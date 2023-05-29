from direct.showbase.ShowBase import ShowBase


class botemu(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)


app = botemu()
app.run()