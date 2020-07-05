import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = THIS_FOLDER + "/resource/"

res_dir = dict(
    CSS_MAIN=RES_FOLDER + "css/"
)

theme_prefs = dict(
    OUTLINE=5
)

button_labels = [
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
