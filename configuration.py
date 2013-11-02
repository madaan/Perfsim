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
        self.ARRIVAL_DIST = config.get('system', 'ARRIVAL_DIST')
        self.ARRIVAL_DIST_MEAN = config.get('system', 'ARRIVAL_DIST_RATE')

        '''
        {
        'server_0': {'service_dist': 'E', 'service_dist_rate': '.30'}, 
        'server_1': {'service_dist': 'D', 'service_dist_rate': '.20'}
        }
        '''
        self.server_config = {} #A dictionary of dictionaries, as shown above
        for section in config.sections()[1:]: #Skip the system
            self.server_config[section] = {}
            for option in config.options(section):
                self.server_config[section][option] = config.get(section, option)
        print self.server_config
    
if __name__ == '__main__':
    Config('perfsim.config')
