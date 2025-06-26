import pytest
import os

from biblecli.cli import CLIConfig
from biblecli.bible import BibleClient
from biblecli.utils import get_source_root


@pytest.fixture(scope='session', autouse=True)
def download_translations():
    for translation in ['BSB', 'KJV']:
        translation_exists = \
            os.path.isfile(f"{get_source_root()}/data/db/{translation}.db")
        if not translation_exists:
            bible = BibleClient(translation)
            bible.create_bible_db()
    
    default_translation = CLIConfig.get_default_translation()
    
    if default_translation is not 'BSB':
        CLIConfig.set_default_translation('BSB')
