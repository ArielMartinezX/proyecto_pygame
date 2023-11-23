import json

SCR_HEIGHT = 600
SCR_WIDTH = 800
CONFIG_FILE_PATH = './configs/config.json'
FPS = 60
DEBUG = False

def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)