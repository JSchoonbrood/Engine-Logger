import configparser
import os

class Config():
    def __init__(self, directory, parent=None):
        self.directory = directory
        self.config_file = os.path.join(self.directory, 'Configuration.ini')
        self.config = configparser.ConfigParser()

    def locate_config(self):
        if os.path.isfile(self.config_file):
            return True
        else:
            return False

    def create_config(self):
        self.config['INTERFACE'] = {'TitleButtonSize' : 17,
                                    'ButtonSize' : 15,
                                    'TextSize' : 15,
                                    'HeaderSize' : 15}

        self.config['COSTS'] = {'Currency' : '£',
                                'ConsumerHourlyRate' : 50,
                                'TradeHourlyRate' : 30}
        
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def read_interface(self):
        print ("ToBeImplemented")

    def read_costs(self):
        print ("ToBeImplemented")

    def update_interface(self):
        print ("ToBeImplemented")

    def update_costs(self):
        print ("ToBeImplemented")
