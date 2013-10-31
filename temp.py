#sg

import ConfigParser
config = ConfigParser.ConfigParser()
config.read('perfsim.config')
#Read the system parameters :
self.NUM_SERVER = int(config.get('system', 'NUM_SERVER'))




