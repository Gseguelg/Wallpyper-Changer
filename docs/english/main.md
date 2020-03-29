# How to download
1. Download the code or clone it.
    * If not sure which, just download it and unzip it where you want to install it (can be any folder).
    * To download <kbd>Click</kbd> on *Clone or download* -> *Download ZIP*. A pop up window to download will appear.

# Requirements

#### Python libraries
**Walpyper Changer** runs on python and depends on the following libraries:
* pathlib
* datetime
* sqlite3
* logging
* os
* json
* BeautifulSoup
* requests
* urllib
* ctypes

A fresh installation on [Anacoda][1] is enough for that. Take a look to [My Coding Adventure][2] for a cheatsheet on how to install python.

#### Create a json config

On installation directory it's neccesary to create new file called `config.json` inside `./Python` directory. Fill it with the following content.


```json
{
    "IMGS_DIRECTORY": "C:\\Users\\<USERNAME>\\Pictures\\Saved Pictures",
    "DB_NAME": "images_path.db",
    "IMG_EXTENSIONS": [
        "*.jpg",
        "*.png"
    ],
    "CACHE_NAME": ".wallpyper.cache",
    "DEFAULT_CACHE_DATA": {
        "LastRun": null,
        "NewApodAvail": true
    }
}
```

* Set `"IMGS_DIRECTORY"` to the folder path where your wallpaper images are saved.
* It's possible to replace `<USERNAME>` with your user name in order to use default images folder and subfolders.

# Installation
Installation requires the use of **windows tasks scheduler** and **python 3** accesible by path.

1. [Download it](#How-to-download).
2. Check for [requirements](#Requirements).
3. Open the folder **Wallpyper-Changer-master** and double click on the _batch file_ `create_task.bat`. A file called `Wallpyper_task.xml` should be created.
4. Open **windows tasks scheduler** and search for the option _**import task**_. Click it.
5. Once a pop-up dialog appears click on accept.
6. Your task is ready to be **Wallpyper Changer** every 5 minutes after user logging.

# Troubleshoot
The file `<installation path>/Python/wallpyper.log` logs most actions done by **Wallpyper Changer**. Take a look to this file and post and issue with it.

[1]: https://www.anaconda.com/
[2]: https://github.com/Gseguelg/My-Coding-Adventure/wiki/Python