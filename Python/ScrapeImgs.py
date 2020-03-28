from bs4 import BeautifulSoup
import requests, urllib
import re, os, logging

import DBmanage as DBm


def new_APOD_image_avail():
    """
        Checks wheather a new image is available on APOD web.
        TODO: Try except block on excessive requests
    """
    # Search for IMG_URL
    SOURCE_URL = "https://apod.nasa.gov/apod/"
    fuente = requests.get(SOURCE_URL).text
    sopa = BeautifulSoup(fuente, 'lxml')
    ref_img = sopa.find('img')
    if ref_img:
        img_link = ref_img.parent['href']  # ancor parent
        IMG_URL = SOURCE_URL + img_link
        IMG_NAME = IMG_URL.split('/')[-1]
        return (IMG_URL, IMG_NAME)


def download_APOD_img_to(IMGS_DIRECTORY, url_name_APOD):
    """
        Download it
    """
    # get main logger
    logger = logging.getLogger('wallpylog')

    DOWNLOAD_PATH = IMGS_DIRECTORY + os.sep + 'APOD'
    img_url, img_name = url_name_APOD
    try:
        urllib.request.urlretrieve(img_url, DOWNLOAD_PATH + os.sep + img_name)
        logger.info("... done downlading.")
    except urllib.error.HTTPError as e:  # SystemExit and KeyboardInterrupt wont be catched
        logger.exception("Image can't be accessible.")
    except Exception as e:
        msg = "Please refer to https://docs.python.org/3.7/library/urllib.error.html#module-urllib.error for error details."
        logger.exception(msg)


def try_APOD_download(DB_PATH, IMGS_DIRECTORY, url_name_APOD, TODAY):
    """ Download the APOD image from 'url_name_APOD' if it doesn't exists inside DB_PATH. """
    # get main logger
    logger = logging.getLogger('wallpylog')

    DOWNLOADED_IMG_PATH = IMGS_DIRECTORY + os.sep + 'APOD'
    DOWNLOADED_IMG_PATH += os.sep + url_name_APOD[1]
    # check if apod image path exists in db
    ImgInDB = DBm.APOD_img_in_DB(DB_PATH, url_name_APOD, IMGS_DIRECTORY)
    msg = f"New APOD image exists in DB (ImgInDB): {ImgInDB}"
    logger.debug(msg)
    # if new APOD image is not registered in DB
    if not ImgInDB:
        msg = f"Downloading new APOD image: '{url_name_APOD[1]}'..."
        logger.info(msg)
        download_APOD_img_to(IMGS_DIRECTORY, url_name_APOD)
        DBm.insert_single_record_to_DB(
            DB_PATH,
            {
                'fuente': 'APOD',
                'ruta': DOWNLOADED_IMG_PATH,
                'fecha_descarga': TODAY.strftime('%Y-%m-%d')  # YYYY-MM-DD
            })
    else:
        msg = "An APOD image will not be downloaded."
        logger.info(msg)


# def download_img_to(IMGS_DIRECTORY, source):
#     """
#         source can be: 'APOD' or 'Unsplash'. The subfolder is called the same.
#     """
#     DOWNLOAD_PATH = IMGS_DIRECTORY + os.sep + source
#     # check if APOD directory exists in IMGS_DIRECTORY
#     if not os_path.isdir(DOWNLOAD_PATH):
#         os.mkdir(DOWNLOAD_PATH)

#     # check for source to use
#     if source == 'APOD':
#         """
#             Once a day a new picture.
#         """
#         #
#         # Search for IMG_URL
#         SOURCE_URL = "https://apod.nasa.gov/apod/"
#         fuente = requests.get(SOURCE_URL).text
#         sopa = BeautifulSoup(fuente, 'lxml')
#         ref_img = sopa.find('img')
#         if ref_img:
#             img_link = ref_img.parent['href']  # ancor parent
#             IMG_URL = SOURCE_URL + img_link

#             # download img into folder if got one
#             IMG_NAME = IMG_URL.split('/')[-1]
#             urllib.request.urlretrieve(IMG_URL, DOWNLOAD_PATH + os.sep + IMG_NAME)

#     elif source == 'Unsplash':
#         """
#             All at once. If image already exists do nothing.
#         """
#         # def find_images_data(SOURCE_URL):
#         #     fuente = requests.get(SOURCE_URL).text
#         #     sopa = BeautifulSoup(fuente, 'lxml')
#         #     titulo = sopa.find(
#         #         'h2', text=re.compile('Download free HD background images'))
#         #     next_div = titulo.parent.find_next('div')
#         #     imgs_tags = next_div.findAll(
#         #         'img', src=re.compile('https://images.unsplash.com/photo-*'))
#         #     img_url_name = []
#         #     for img_tag in imgs_tags:
#         #         # convert url to the high resolution one
#         #         url = re.sub(r"(?<=w=)\d+(?=&q=\d+$)", '4000', img_tag['src'])
#         #         name = re.search(r"photo-[A-Za-z0-9]{13}-[A-Za-z0-9]{12}", url)
#         #         name = name.group(0) + '.jpg'
#         #         img_url_name.append((url, name))
#         #     return img_url_name

#         # #
#         # # Search for IMG_URL
#         # SOURCE_URL = "https://unsplash.com/backgrounds/desktop/hd"
#         # IMG_URL_NAME = find_images_data(SOURCE_URL)

#         # for url_img, img_name in IMG_URL_NAME:
#         #     # download only those that don't exist
#         #     if img_name not in os.listdir(DOWNLOAD_PATH):
#         #         urlrequest.urlretrieve(url_img,
#         #                                DOWNLOAD_PATH + os.sep + img_name)
#         #     else:
#         #         print(f"Image {img_name} already in path")
#         pass
