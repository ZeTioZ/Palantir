import cProfile

import wx

from frames.main_frame import PalantirFrame

app = wx.App()
main_frame = PalantirFrame(None, 'Palantir')
cProfile.run(app.MainLoop())
