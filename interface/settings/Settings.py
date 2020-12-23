import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/resource/"

build_number = "20.12.4"
copyright_date = "2021"

menu_labels = [
    ["Doodle", True],
    ["Games", False],
    ["Messages", False],
    ["Photos", False],
    ["News", False],
    ["Timer", False],
    ["Calendar", False],
    ["Lists", False],
    ["Settings", False]
]

settings_menu_labels = [
    "General",
    "Theme",
    "Network",
    "Account",
    "About"
]

default_css_class = 'content-area'

settings_menu_background_classes_dict = {
    menu_labels[0][0]: 'content-box',
    menu_labels[1][0]: default_css_class,
    menu_labels[2][0]: default_css_class,
    menu_labels[3][0]: default_css_class,
    menu_labels[4][0]: default_css_class,
    menu_labels[5][0]: default_css_class,
    menu_labels[6][0]: default_css_class,
    menu_labels[7][0]: default_css_class,
    menu_labels[8][0]: default_css_class
}

# Default Settings & Preferences
default_menu = menu_labels[0][0]

res_dir = dict(
    ROOT=RES_FOLDER,
    CSS_MAIN=RES_FOLDER + "css/",
    BUTTON_IMAGES=RES_FOLDER + "button_images/",
    TEXTURES=RES_FOLDER + "textures/"
)

theme_prefs = dict(
    OUTLINE=5
)


def get_rpi_serial():
    # Extract serial from cpuinfo file
    cpuserial = "ERROR"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR"
    return cpuserial
