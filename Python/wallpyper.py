from datetime import datetime as dt
import ctypes, os, logging

from Config import CONFIG_FILE_NAME, LOG_LEVEL
import ManageFiles as MFs
import DBmanage as DBm
import ScrapeImgs as ScrpIMGs


def set_wallpaper(FULL_PATH_IMG):
    """
        Updates de system parameter in order to set a wallpaper background.
        Source: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
    """
    """
        BOOL SystemParametersInfoW(
            UINT  uiAction,
            UINT  uiParam,
            PVOID pvParam,
            UINT  fWinIni
            );
    """
    SPI_SETDESKWALLPAPER = 0x0014  # hex for 20 dec
    uiParam = 0  # 0 if not indicated
    fWinIni = 0x0003  # permanent (SPIF_UPDATEINIFILE)
    # fWinIni = 0x0000  # temporarely
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, uiParam,
                                               FULL_PATH_IMG, fWinIni)


if __name__ == "__main__":
    # create logger be called by functions
    logger = MFs.newLogger('wallpylog', Level=LOG_LEVEL, File='wallpyper.log')

    #
    # variables
    WORKING_DIRECTORY = os.getcwd()
    CONFIG_FILE_PATH = WORKING_DIRECTORY + os.sep + CONFIG_FILE_NAME
    load_variable = MFs.load_config_file(CONFIG_FILE_PATH)
    IMGS_DIRECTORY = load_variable['IMGS_DIRECTORY']
    IMG_EXTENSIONS = load_variable['IMG_EXTENSIONS']
    DB_NAME = load_variable['DB_NAME']
    DB_PATH = WORKING_DIRECTORY + os.sep + DB_NAME
    CACHE_NAME = load_variable['CACHE_NAME']
    CACHE_PATH = WORKING_DIRECTORY + os.sep + CACHE_NAME

    NOW = dt.now()
    TODAY = NOW.date()
    CACHE_DATA = MFs.read_cache_activity(CACHE_PATH)

    logger.debug(f"TODAY: {TODAY}")

    #

    msg = f"Checking Database '{DB_NAME}' existance..."
    logger.info(msg)
    DBm.database_check_existance(DB_PATH, DB_NAME)
    logger.info("... done checking DB.")

    msg = f"Synchronizing '{DB_NAME}' with respect to '{IMGS_DIRECTORY}' and subfolders..."
    logger.info(msg)
    DBm.synchronize_db(DB_PATH, IMGS_DIRECTORY, IMG_EXTENSIONS)
    logger.info("... done syncronizing.")  #####  DEBUG  ####

    # look for latest APOD img downloaded recorded in DB
    LastDownload = DBm.latest_APOD_download_date(DB_PATH)
    logger.debug(f"LastDownload: {LastDownload}")

    # keep trying on every run. WATCH OUT for ip bans! (5 min it's ok)
    if LastDownload != TODAY:  # Also None is accepted to start the try
        # web scrapped for image url
        url_name_APOD = ScrpIMGs.new_APOD_image_avail()
        msg = f"New APOD image url: {url_name_APOD[0]}"
        logger.debug(msg)
        msg = f"New APOD image name: {url_name_APOD[1]}"
        logger.debug(msg)

        # Is there and URL and name? (tuple)
        if url_name_APOD:
            ScrpIMGs.try_APOD_download(DB_PATH, IMGS_DIRECTORY, url_name_APOD,
                                       TODAY)

    # set an image as wallpaper on time interval
    if True:
        msg = "Changing desktop wallpaper..."
        logger.info(msg)  #####  DEBUG  ####

        FULL_PATH_IMG = DBm.get_random_img_from_db(DB_PATH)
        msg = f"New desktop img from: {FULL_PATH_IMG}"
        logger.debug(msg)
        set_wallpaper(FULL_PATH_IMG)
        logger.info("... wallpaper changed.")  #####  DEBUG  ####

    # Updates some CACHE_DATA values
    CACHE_DATA['LastRun'] = NOW
    MFs.write_cache_activity(CACHE_PATH, CACHE_DATA)
