# -*- coding: utf-8 -*-
#
#  main.py
#  GraphicsGDGUI
#
#  Created by Full Name on 8/28/20.
#  Copyright (c) 2020 camila314. All rights reserved.
#

# import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import AppDelegate
import ViewController

# pass control to AppKit
AppHelper.runEventLoop()
