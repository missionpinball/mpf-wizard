from kivy.uix.label import Label
from kivy.uix.treeview import TreeView, TreeViewLabel
import logging
import sys


class RawConfigTree(object):



    def __init__(self, configdict):
        self.rawdict = configdict
        self.log = logging.getLogger('mpf-wizard-ui')
        self.log.info('Rendering Config Dict As TreeView')
        
        try:
            tv = TreeView()
            
            for key in self.rawdict:
                if isinstance(self.rawdict[key], dict):
                    newnode = tv.add_node(TreeViewLabel(text=key))
                    self._addNodesToTree(tv, newnode, self.rawdict[key])
                else:
                    newnode = tv.add_node(TreeViewLabel(text=key + ':' + str(self.rawdict[key])))

            self.treeview = tv
        except:
            e = sys.exc_info()[0]
            self.log.exception("Error: %s" % e )
            raise
            
    def _addNodesToTree(self, tree_view, parent_node, value):
        
        if isinstance(value, dict):
            for key in value:
                if isinstance(value[key], dict):
                    newnode = tree_view.add_node(TreeViewLabel(text=key), parent_node)
                    self._addNodesToTree(tree_view, newnode, value[key])
                else:
                    newnode = tree_view.add_node(TreeViewLabel(text=key + ':' + str(value[key])), parent_node)
                    
    
# The MIT License (MIT)

# Copyright (c) 2013-2016 Brian Madden, Gabe Knuth and John Marsh

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
