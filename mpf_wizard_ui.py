from kivy.uix.label import Label
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from ruamel.yaml.comments import CommentedSeq
import logging
import sys
from config_storage import MPFConfigFile

class MainMenu(TabbedPanel):
    pass

class WizardUI(object):
    def __init__(self, machine):
        self.machine = machine
        
    def getMainMenu(self):
        menu = MainMenu()

        tree = UIConfigTree(self.machine.config_files)
        menu.ids.tab_filetreeview.add_widget(tree.getTreeViewAsFiles())
        menu.ids.tab_mergedtreeview.add_widget(tree.getMergedTreeView())

        switches = self.machine.getSwitches()
        menu.ids.tab_switches.add_widget(UISwitchPanel(self.machine.config_files))
        
        return menu
        
class UIConfigTree(object):
    
    def __init__(self, config_files):
        self.config_files = config_files
        self.log = logging.getLogger('mpf-wizard-ui')
        
        self.label_font_size = '12sp'
        
        self.filename_label_color = ListProperty()
        self.filename_label_color = [181,91,0,1]
        
        self.key_label_color = ListProperty()
        self.key_label_color = [255,255,255,1]
                
    def getMergedTreeView(self):
        try:
            tv = TreeView(hide_root=True)
            tv.size_hint = 1, None
            tv.bind(minimum_height = tv.setter('height'))
            
            for key in self.config_files:
                merged_dict = self.config_files[key].get_merged_config()
            
            for key in merged_dict:
                if isinstance(merged_dict[key], dict):
                    newnode = tv.add_node(TreeViewLabel(text=str(key), font_size=self.label_font_size, color=self.key_label_color))
                    self._addNodeToMergedTreeView(tv, newnode, merged_dict[key])
                else:
                    newnode = tv.add_node(TreeViewLabel(text=str(key) + ':' + str(merged_dict[key]), font_size=self.label_font_size, color=self.key_label_color))
            
            scv = ScrollView(pos = (0, 0), bar_width = 10)
            scv.add_widget(tv)
            return scv

        except:
            e = sys.exc_info()[0]
            self.log.exception("Error: %s" % e )
            raise
        
    def _addNodeToMergedTreeView(self, tree_view, parent_node, config):
        for key in config:
            if isinstance(config[key], dict):
                newnode = tree_view.add_node(TreeViewLabel(text=str(key), font_size=self.label_font_size, color=self.key_label_color), parent_node)
                self._addNodeToMergedTreeView(tree_view, newnode, config[key])
            else:
                newnode = tree_view.add_node(TreeViewLabel(text=str(key) + ':' + str(config[key]), font_size=self.label_font_size, color=self.key_label_color), parent_node)
        
        
    def getTreeViewAsFiles(self):
        try:
            tv = TreeView(hide_root=True)
            tv.size_hint = 1, None
            tv.bind(minimum_height = tv.setter('height'))
            
            for key in self.config_files:
                newnode = tv.add_node(TreeViewLabel(text=self.config_files[key].filename, font_size=self.label_font_size, color=self.filename_label_color))
                
                for child_filename in self.config_files[key].child_files:
                    self._addFileNodeToFileTreeView(tv, newnode, self.config_files[key].child_files[child_filename])
                    
                for configkey in self.config_files[key].config:
                    if isinstance(self.config_files[key].config[configkey], dict):
                        self._addDictNodeToFileTreeView(tv, newnode, configkey, self.config_files[key].config[configkey])
                    else:
                        tv.add_node(TreeViewLabel(text=str(configkey) + ':' + str(self.config_files[key].config[configkey]), font_size=self.label_font_size, color=self.key_label_color), newnode)
                                
            scv = ScrollView(pos = (0, 0), bar_width = 10)
            scv.add_widget(tv)
            return scv
        except:
            e = sys.exc_info()[0]
            self.log.exception("Error: %s" % e )
            raise
            
    def _addFileNodeToFileTreeView(self, tree_view, parent_node, config_file):
        newnode = tree_view.add_node(TreeViewLabel(text=config_file.filename, font_size=self.label_font_size, color=self.filename_label_color), parent_node)

        for child_filename in config_file.child_files:
            self._addNodeToFileTreeView(tree_view, newnode, config_file.child_files[child_filename])
    
        for configkey in config_file.config:
            if isinstance(config_file.config[configkey], dict):
                self._addDictNodeToFileTreeView(tree_view, newnode, configkey, config_file.config[configkey])
            else:
                tree_view.add_node(TreeViewLabel(text=str(configkey) + ':' + str(config_file.config[configkey]), font_size=self.label_font_size, color=self.key_label_color), newnode)


    def _addDictNodeToFileTreeView(self, tree_view, parent_node, configkey, config):
        newnode = tree_view.add_node(TreeViewLabel(text=str(configkey), font_size=self.label_font_size, color=self.key_label_color), parent_node)
        
        for key in config:
            if isinstance(config[key], dict):
                self._addDictNodeToFileTreeView(tree_view, newnode, key, config[key])
            else:
                tree_view.add_node(TreeViewLabel(text='[color=#00EBDB]' + str(key) + ':[/color][color=#FFADC9]' + str(config[key]) + '[/color]', font_size=self.label_font_size, color=self.key_label_color, markup=True), newnode)
        
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
