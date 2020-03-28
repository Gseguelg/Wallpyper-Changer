import json, os, logging
from datetime import datetime as dt

from Config import CONFIG_FILE_NAME, LOG_LEVEL
import DBmanage as DBm


def load_config_file(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'r') as f:
        config_dict = json.load(f)
    return config_dict


def write_cache_activity(CACHE_FILE, CACHE_DATA=False):
    """
        Writes a CACHE_FILE with CACHE_DATA. If not CACHE_DATA
        is given then use default dict.
    """
    if not CACHE_DATA:
        # Default data
        load_variable = load_config_file(CONFIG_FILE_NAME)
        CACHE_DATA = load_variable['DEFAULT_CACHE_DATA']
    with open(CACHE_FILE, 'w') as f:
        # all no serialize strings are converted to strings
        json.dump(CACHE_DATA, f, default=str)


def read_cache_activity(CACHE_FILE):
    """ Read CACHE_FILE. If not exists creates with defaults. """
    if not os.path.isfile(CACHE_FILE):
        # Includes default values fron nested function
        write_cache_activity(CACHE_FILE)

    with open(CACHE_FILE, 'r') as f:
        CACHE_DATA = json.load(f)
        # convert to datetime object if possible
        if CACHE_DATA['LastRun']:
            CACHE_DATA['LastRun'] = dt.strptime(CACHE_DATA['LastRun'],
                                                '%Y-%m-%d %H:%M:%S.%f')
    return CACHE_DATA


def newLogger(Name, File=None, mode='a', OnlyFile=False, Level=logging.DEBUG):
    """ Returns a new logger 'Name' that outputs only to console by default. newLogger inheritate from root logger.

        Note 1: If only console are required, 'File' argument should be None.
        Note 2: If 'File' is not specified and 'OnlyFile' is True, a default file called '<running_file>.log' is used on current directory.

        INPUT
            Name (str): Name of the new logger.
        INPUT (optional)
            File (str, None): If specified log to console and to file path in appending (mode='a').
            mode (str): Specifies whether a new log should be appended to existing file (mode='a')
                or a new file should overwrite previous ones (mode='w').
            OnlyFile (bool): Whether output should go only to log file, otherwise also goes to console.
            
    """
    logger = logging.getLogger(Name)
    fmt = '[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s'
    frmt = logging.Formatter(fmt)

    if not File and OnlyFile:
        File = ''.join(__file__.split('.')[:-1]) + '.log'

    if File:
        filehandler = logging.FileHandler(File, mode=mode)
        filehandler.setFormatter(frmt)
        filehandler.setLevel(Level)
        logger.addHandler(filehandler)

    if not OnlyFile:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(Level)
        consolehandler.setFormatter(frmt)
        logger.addHandler(consolehandler)

    logger.setLevel(Level)
    return logger
