import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.logger import Logger
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.widget import Widget
import logging
import logging.config
from datetime import datetime
import socket
import os
import argparse
import errno
import version
import sys
from mpf.system.utility_functions import Util
from mpfwiz.machinewizard import MachineWizard
from mpfwiz.mpf_wizard_ui import UIConfigTree, WizardUI


parser = argparse.ArgumentParser(description='Starts the mpf-wizard')

parser.add_argument("machine_path", help="Path of the machine folder.")

parser.add_argument("-c",
                    action="store", dest="configfile",
                    default="config", metavar='config_file',
                    help="The name of a config file to load. Default is "
                    "config.yaml. Multiple files can be used via a comma-"
                    "separated list (no spaces between)")

parser.add_argument("-v",
                    action="store_const", dest="loglevel", const=logging.DEBUG,
                    default=logging.INFO, help="Enables verbose logging to the"
                    " log file")

parser.add_argument("-V",
                    action="store_const", dest="consoleloglevel", const=logging.DEBUG,
                    default=logging.INFO,
                    help="Enables verbose logging to the console. Do NOT use on Windows platforms.  Must be also used with -v to work.")

parser.add_argument("-x",
                    action="store_const", dest="force_platform",
                    const='virtual', help="Forces the virtual platform to be "
                    "used for all devices")

parser.add_argument("-r",
                    action="store_true", dest="rebuild_cache",
                    help="Forces the config cache to be rebuilt")

parser.add_argument("-b",
                    action="store_false", dest="bcp", default=True,
                    help="Runs MPF without making a connection attempt to a "
                    "BCP Server")

parser.add_argument("-l",
                    action="store", dest="logfile", metavar='file_name',
                    default=os.path.join("logs", datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S-mpf-" + socket.gethostname() + ".log")),
                    help="The name (and path) of the log file")

parser.add_argument("-C",
                    action="store_true", dest="create",
                    help="Create a new machine if not found")

parser.add_argument("-N",
                    action="store", dest="mpfconfigfile",
                    default=os.path.join("mpf", "mpfconfig.yaml"),
                    metavar='config_file',
                    help="The MPF framework default config file. Default is "
                    "mpf/mpfconfig.yaml")

parser.add_argument("--version",
            action="version", version=version.version_str,
            help="Displays the MPF Wizard version info and exits")

args = parser.parse_args()
args.configfile = Util.string_to_list(args.configfile)

try:
    os.makedirs('logs')
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise


# logging config
dictLogConfig = { 
    'version': 1,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
        }
    },
    'handlers': { 
        'filelog': { 
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': args.logfile,
            'formatter': 'standard'
        },
        'consolelog': { 
            'class': 'logging.StreamHandler',
            'level': args.consoleloglevel,
            'formatter': 'standard',
            'stream' : 'ext://sys.stdout'
        }
    },
    'loggers': { 
        'mpf-wizard': { 
            'handlers': ['filelog','consolelog'],
            'level': args.loglevel
        },
        'machinewizard': { 
            'handlers': ['filelog','consolelog'],
            'level': args.loglevel
        },
        'mpf-wizard-ui': { 
            'handlers': ['filelog','consolelog'],
            'level': args.loglevel
        }
    }
}

logging.config.dictConfig(dictLogConfig)
mpflogger = logging.getLogger('mpf-wizard')
mpflogger.info('starting up the mpf-wizard')
mpflogger.debug('Command Line Arguments: ' + str(sys.argv))

class MPFWizardApp(App):
    icon = 'mpf-wizard_icon_256x256.png'
    title = "MPF Wizard v" + version.__version__
    
    def build(self):
        try:
            machine = MachineWizard(vars(args))
        except Exception as e:
            mpflogger.exception(e)
            App.get_running_app().Stop()
                
        #uct = UIConfigTree(machine.config_files)
        #return uct.getTreeViewAsFiles()

        #root = self.root
        wizardui = WizardUI(machine)
        return wizardui.getMainMenu()


if __name__ == '__main__':
    MPFWizardApp().run()