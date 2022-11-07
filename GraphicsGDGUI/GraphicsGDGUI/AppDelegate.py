# -*- coding: utf-8 -*-
#
#  AppDelegate.py
#  GraphicsGDGUI
#
#  Created by Full Name on 8/28/20.
#  Copyright (c) 2020 camila314. All rights reserved.
#

from Foundation import *
from AppKit import *
import MyView
import objc

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
