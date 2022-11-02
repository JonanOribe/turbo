from configparser import ConfigParser


def get_config_file_data():
    configFilePath:str =  '\\'.join(os.path.abspath(__file__).split('\\')[:3])
    config_file = configFilePath + '\\config.cfg'
    config = ConfigParser()
    return config,config_file