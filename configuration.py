#sg
'''This script reads the configuration file, stored as perfsim.config
in the current directory. The values are then maintained as a state of the configuration object and can be retreived by the iterested module'''

import ConfigParser

class Config:

    def __init__(self, cfile):
        config = ConfigParser.ConfigParser()
        config.read('perfsim.config')
        #Read the system parameters :
        self.NUM_SERVER = int(config.get('system', 'NUM_SERVER'))


if __name__ == '__main__':
    Config('perfsim.config')
