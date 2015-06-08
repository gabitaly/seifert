#!/usr/bin/env python

__author__="gabriele.giambartolomei@desy.de"
__date__ ="June, 2015, 10:56 AM"
__copyright__="Copyright (c) 2010-2015 European XFEL GmbH Hamburg. All rights reserved."

import time
import sys
from karabo.device import *


@KARABO_CLASSINFO("GeSeifertXray", "1.3")
class GeSeifertXray(PythonDevice):

    @staticmethod
    def expectedParameters(expected):
        '''
        This static method is needed as a part of the factory/configuration system.
        @param expected Will contain the description of the device expected parameters.
        NOTE: parenthesis () are used for allowing to switch off interpreter indentation rule.
        '''
        (
        )

    def __init__(self, configuration):
        # always call PythonDevice constructor first!
        super(GeSeifertXray,self).__init__(configuration)
        # Define the first function to be called after the constructor has finished
        self.registerInitialFunction(self.initialization)
        # Initialize here your member variables...

    def initialization(self):
        '''
        This method will be called after the constructor.
        if you need methods that can be callable from another device or GUI
        you may register them here:
        self.KARABO_SLOT(self.myslot1)
        self.KARABO_SLOT(self.myslot2)
        ...
        Corresponding methods (myslot1, myslot2, ...) should be defined in this class
        '''
        
    # Put here your slots 


# This entry used by device server
if __name__ == "__main__":
    launchPythonDevice()
