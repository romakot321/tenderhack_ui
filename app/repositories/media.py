from pathlib import Path
from aiogram import types


class MediaRepository:
    assets_path = Path('assets/')

    def __init__(self):
        with open(self.assets_path / 'settings.png', 'rb') as f:
            self.settings_image = f.read()

    def get_settings_photo(self) -> types.BufferedInputFile:
        return types.BufferedInputFile(self.settings_image, 'settings.jpg')
