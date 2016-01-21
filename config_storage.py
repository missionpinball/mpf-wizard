"""Contains the various config storage classes"""
# config_storage.py
# Mission Pinball Framework Wizard
# Written by Brian Madden, Gabe Knuth & John Marsh
# Released under the MIT License. (See license info at the end of this file.)

from mpf.system.utility_functions import Util

class MPFConfigFile():
    
    def __init__(self, filename, config):
        self.filename = filename
        self.config = config
        self.child_files = dict()
        
    def add_child_file(self, child_file):
        self.child_files[child_file.filename] = child_file

    def get_merged_config(self):
        merged_config = self.config
        for key in self.child_files:
            merged_config = Util.dict_merge(merged_config, self.child_files[key].get_merged_config())
        
        return merged_config
            
# The MIT License (MIT)

# Copyright (c) 2013-2016 Brian Madden, Gabe Knuth and the AUTHORS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
