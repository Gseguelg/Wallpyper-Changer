# ¿Cómo descargar?
1. Descarga el código o clonalo.
    * Si no estás seguro, descargalo y descomprimelo en una carpeta donde se instalará (puede ser cualquier carpeta).
    * Para descargar <kbd>Click</kbd> en *Clone or download* -> *Download ZIP*. Una ventana emergente para descargar apacerá.

# Requisitos

#### Bibliotecas Python
**Walpyper Changer** corre en python y depende de las siguientes bibliotecas:
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

Una instalación predeterminada de [Anacoda][1] tiene todo lo necesario. Hecha una mirada a [My Coding Adventure][2] para revisar una hoja de resumen para instalar python.

#### Crea el archivo de configuración json

En el directorio de installación es necesario crear una nuevo archivo llamado `config.json` bajo el directorio `./Python`. El archivo debe contener lo siguiente.

```json
{
    "IMGS_DIRECTORY": "C:\\Users\\<NombreUsuario>\\Pictures\\Saved Pictures",
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

* Configura `"IMGS_DIRECTORY"` como la ruta de la carpeta que contiene las images a usar como fondos de escritorio.
* Es posible reemplazar `<NombreUsuario>` con tu nombre de usuario para mantener la carpeta de imagenes predeterminada y sus subcarpetas.

# Instalación
Installación requiere usar el **Programador de tareas de windows** y **python 3** accesible desde el path.

1. [Descargalo](#How-to-download).
2. Revisa los [requisitos](#Requisitos).
3. Abre la carpeta **Wallpyper-Changer-master** y dale double click al _archivo batch_ `create_task.bat`. Un nuevo archivo llamado `Wallpyper_task.xml` debería ser creado.
4. Abre el **Programador de tareas de windows** y busca la opción _**importar tarea**_. Hazle click.
5. Una vez aparezca una ventana emergente dale aceptar.
6. Tu tarea está lista para ejecutar **Wallpyper Changer** cada 5 minutes después de iniciar sesión.

# Solucionar problemas
El archivo `<directorio isntalacion>/Python/wallpyper.log` registra la mayoria de las acciones hechas por **Wallpyper Changer**. Dale una revisada y crea una _issue_ en esta página de github con el resultado del archivo de registro.

[1]: https://www.anaconda.com/
[2]: https://github.com/Gseguelg/My-Coding-Adventure/wiki/Python