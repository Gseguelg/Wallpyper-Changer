from pathlib import Path
from datetime import datetime as dt
import sqlite3, os, logging


def create_db(DB_PATH):
    # database insertion
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    #
    # Cretate the main table
    with conn:  # commits automatically
        cur.execute("""
            CREATE TABLE imagenes (
                id INTEGER PRIMARY KEY,
                fuente TEXT,
                fecha_descarga TEXT,
                ruta TEXT UNIQUE)
            """)  # Ignores them that already exists
    conn.close()


def database_check_existance(DB_PATH, DB_NAME):
    """ If DB doesn't exists create it, otherwise do nothing. """
    # get main logger
    logger = logging.getLogger('wallpylog')

    if not os.path.isfile(DB_NAME):
        msg = f"... creating Database on {DB_PATH}"
        logger.info(msg)
        create_db(DB_PATH)
    else:
        msg = f"... already a DB at '{DB_PATH}'. Using it."
        logger.info(msg)


def insert_single_record_to_DB(DB_PATH, data):
    """ Update DB_PATH with NEW element DOWNLOAD_IMG_PATH """
    ruta = data['ruta']
    fuente = data['fuente']
    fecha_descarga = data['fecha_descarga']
    #
    # database insertion
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with conn:  # commits automatically
        cur.execute(
            """
            INSERT INTO imagenes (fuente, ruta, fecha_descarga)
            VALUES (?,?,?) """, (fuente, ruta, fecha_descarga))
    conn.close()


def APOD_img_in_DB(DB_PATH, url_name_APOD, IMGS_DIRECTORY):
    """
        IMGS_DIRECTORY is required to find the math value on DB.
    """
    _, img_name = url_name_APOD
    DOWNLOAD_PATH = IMGS_DIRECTORY + os.sep + 'APOD'
    DOWNLOAD_IMG_PATH = DOWNLOAD_PATH + os.sep + img_name

    # DB connection
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    #
    # query it
    cur.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM imagenes WHERE ruta=?
        )""", (DOWNLOAD_IMG_PATH, ))
    exists = cur.fetchone()[0]
    conn.close()
    #
    # finish
    if exists:
        return True


def get_random_img_from_db(DB_PATH):
    # DB connection
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    #
    # query it
    cur.execute("""
        SELECT ruta FROM imagenes
        ORDER BY RANDOM()
        LIMIT 1
    """)  # select first
    img_path = cur.fetchone()  # tuple
    conn.close()

    return img_path[0]


def check_db_imgs_path_existance(DB_PATH):
    """ Sanitize DB.
        All non existance 'ruta' records will be removed from db.
    """
    # get main logger
    logger = logging.getLogger('wallpylog')

    # DB connection
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # get all records
    cur.execute("SELECT * FROM imagenes")
    records = cur.fetchall()

    # for every record os.isfile(ruta)
    idxs_delete = list()
    for record in records:
        record_img_id = record[0]
        record_img_path = record[3]
        # if not exists save DB id on list
        if not os.path.isfile(record_img_path):
            logger.info(
                f"-> File '{record_img_path}' doesn't exists. Deleting record."
            )
            idxs_delete.append((record_img_id, ))

    # remove from DB using id
    if idxs_delete:
        with conn:  # auto commit
            cur.executemany("DELETE FROM imagenes WHERE id = ?", idxs_delete)

    conn.close()


#


def find_all_imgs_on(DIRECTORY, EXTENSIONS):
    """
        Returns a list with all full paths of especified extensions.
    """
    files = list()
    for e in EXTENSIONS:
        files.extend([str(path) for path in Path(DIRECTORY).rglob(e)])
    return files


def fill_db_from_local(IMGS_DIRECTORY, DB_PATH, files):
    """ Add all images path to DB_PATH DB from IMGS_DIRECTORY. """
    #
    # preprocess: add multiple values for each row as tuple.
    nfiles = len(files)
    filesdb = list(zip(["local"] * nfiles, files, files))  # list of tuples
    #
    # database insertion
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with conn:  # commits automatically
        cur.executemany(
            """
            INSERT INTO imagenes (fuente, ruta)
            SELECT ?, ?
            WHERE NOT EXISTS(
                SELECT 1 FROM imagenes WHERE ruta=?)
            """, filesdb)
    conn.close()


def synchronize_db(DB_PATH, IMGS_DIRECTORY, IMG_EXTENSIONS):
    """ Syncronize record values to file path images on IMGS_DIRECTORY. """
    check_db_imgs_path_existance(DB_PATH)
    files = find_all_imgs_on(IMGS_DIRECTORY, IMG_EXTENSIONS)
    # fill DB with local imgs paths
    fill_db_from_local(IMGS_DIRECTORY, DB_PATH, files)


def latest_APOD_download_date(DB_PATH):
    """ Returns a datetime object from DB, otherwise None. """
    # get main logger
    logger = logging.getLogger('wallpylog')

    msg = "Checking for new APOD online image..."
    logger.info(msg)  #####  DEBUG  ####

    # DB connection
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    #
    # query it
    cur.execute("""
        SELECT fecha_descarga FROM imagenes
        ORDER BY fecha_descarga DESC
        LIMIT 1
    """)  # select first
    fecha = cur.fetchone()[0]  # tuple
    conn.close()

    if fecha:
        UltimaFecha = dt.strptime(fecha, '%Y-%M-%d').date()
        msg = f"... latest download was at {UltimaFecha} 'YYYY-MM-DD'."
        logger.info(msg)
        return UltimaFecha
    else:
        msg = "... no record for latest APOD download."
        logger.info(msg)
