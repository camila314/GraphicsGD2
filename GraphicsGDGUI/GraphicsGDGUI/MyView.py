# -*- coding: utf-8 -*-
#
#  MyView.py
#  GraphicsGDGUI
#
#  Created by Full Name on 8/28/20.
#  Copyright (c) 2020 camila314. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet, nil
from Foundation import *
from AppKit import *

class MyView(NSView):
    def initWithFrame_(self, frame):
        self = super(MyView, self).initWithFrame_(frame)
        if self:
            # initialization code here
            pass
            
        return self

    def drawRect_(self, rect):
        # drawing code here
        try:
            img = NSImage.imageNamed_("Yeah")
            img.drawInRect_(rect)
            
            #print(self.layer().contents())
        except Exception, e:
            print(e)
        return
    def mouseDown_(self, yeah):
        self.window().makeFirstResponder_(nil)
