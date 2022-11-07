# -*- coding: utf-8 -*-
#
#  ViewController.py
#  GraphicsGDGUI
#
#  Created by Full Name on 8/28/20.
#  Copyright (c) 2020 camila314. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import IBOutlet, IBAction, YES, NO, nil
import GGD2

from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from wand.api import library
import wand.color
import wand.image


from PIL import Image
import io
import numpy as np

from os.path import expanduser, join

class ViewController(NSViewController):
    label = IBOutlet()
    fileDisplay = IBOutlet()
    
    graphicSize = IBOutlet()
    blockDensity = IBOutlet()
    blockSize = IBOutlet()
    
    countLabel = IBOutlet()
    
    imagePreview = IBOutlet()
    
    drawBtn = IBOutlet()
    
    errCorrection = IBOutlet()

    def previewSVG(self):
        try:
            """drawing = svg2rlg(self.chosenFile.UTF8String())
            new_bites = io.BytesIO()
            renderPM.drawToFile(drawing,new_bites,fmt='png')"""
            with wand.image.Image() as imag:
                with wand.color.Color('transparent') as background_color:
                    library.MagickSetBackgroundColor(imag.wand,
                                                     background_color.resource)
                imag.read(filename=self.chosenFile.UTF8String())
                new_bites = io.BytesIO(imag.make_blob("png32"))
            
            im = Image.open(new_bites)
            im = im.crop(im.getbbox())
            im = im.resize((im.width*3, im.height*3))
            #im.thumbnail((133,133),Image.ANTIALIAS)
            im.save(join(expanduser("~"),".GGD2_prev.png"), format='PNG')
            
            img = NSImage.alloc().initWithContentsOfFile_(join(expanduser("~"),".GGD2_prev.png"))
            self.imagePreview.setImage_(img)
        except Exception, e:
            print(e)
        
        
    def viewDidLoad(self):
        paragraphStyle = NSMutableParagraphStyle.alloc().init()
        paragraphStyle.setAlignment_(NSTextAlignmentCenter)
        attributes = {NSStrokeWidthAttributeName: -3,NSForegroundColorAttributeName: NSColor.whiteColor(),NSStrokeColorAttributeName: NSColor.blackColor(),NSParagraphStyleAttributeName: paragraphStyle}
        str = NSAttributedString.alloc().initWithString_attributes_("GraphicsGD", attributes)
        self.label.setAttributedStringValue_(str)
        self.fileDisplay.setStringValue_("")
        self.level = None
        self.chosenFile = None
        self.drawBtn.setEnabled_(NO)
        
    @IBAction
    def onChooseFile_(self, sender):
        print("we choosing")
        openDlg = NSOpenPanel.openPanel()
        openDlg.setCanChooseFiles_(YES)
        openDlg.setCanChooseDirectories_(NO)
        openDlg.setAllowedFileTypes_(["svg"])
        
        if openDlg.runModal() == NSOKButton:
            files = openDlg.filenames()
            self.chosenFile = files.objectAtIndex_(0)
            print(self.chosenFile)
            self.fileDisplay.setStringValue_(self.chosenFile.UTF8String().split("/")[-1])
            self.previewSVG()
    
    def controlTextDidEndEditing_(self, notif):
        print("we ending")
        self.view().window().makeFirstResponder_(nil)
    @IBAction
    def generate_(self, sender):
        self.level = None
        if self.chosenFile and self.chosenFile.length()!=0:
            try:
                self.level = GGD2.ggd.generate(self.chosenFile.UTF8String(), 1.0/self.graphicSize.floatValue(), self.blockDensity.floatValue(), self.blockSize.floatValue(), self.errCorrection.state()==NSOffState)
                
                self.countLabel.setStringValue_("This graphic will contain %d blocks "%len(self.level.blocks))
            except:
                self.countLabel.setStringValue_("Error generating graphic")
        else:
            self.countLabel.setStringValue_("Select a graphics file")
        
        if self.level != None:
            self.drawBtn.setEnabled_(YES)
    @IBAction
    def onDraw_(self, sender):
        out = GGD2.msgport.uploadToGD(self.level)
        if out==1:
            self.countLabel.setStringValue_("An error occured while drawing")
        else:
            self.countLabel.setStringValue_("Successfully drew %d blocks"%len(self.level.blocks))
            
