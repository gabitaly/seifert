#!/usr/bin/env python3

__author__="gabriele.giambartolomei@desy.de"
__date__ ="June, 2015, 10:56 AM"
__copyright__="Copyright (c) 2010-2015 European XFEL GmbH Hamburg. All rights reserved."

from karabo.configurator import Configurator
from GeSeifertXray import *

if __name__ == "__main__":
    device = Configurator(PythonDevice).create("GeSeifertXray", Hash("Logger.priority", "DEBUG", "deviceId", "GeSeifertXrayMain_0"))
    device.run()
