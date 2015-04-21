'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import os

from PySide import QtCore

def getLogDirectory():
    
    settings = QtCore.QSettings()
    fn = settings.fileName()
    app_dir, _ = os.path.splitext(fn)
    log_directory = os.path.join(app_dir, 'logs')
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    return log_directory
    
    
def getLogLocation():
    '''
    Set up location where log files will be stored (platform dependent).
    '''
    log_filename = 'logging_record.log'
    log_directory = getLogDirectory()
    
    logging_file_location = os.path.join(log_directory, log_filename)
    
    return logging_file_location
    
