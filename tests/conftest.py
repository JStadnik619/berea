import pytest

from biblecli.cli import CLIConfig
from biblecli.bible import BibleClient


# monkeypatch and tmp_path require function scope
@pytest.fixture(scope='function')
def app_data_path(monkeypatch, tmp_path):
    """Use a temporary directory for storing mutable app data (translations or config).
    """
    def mock_get_app_data_path(subdir):
        path = tmp_path + '/biblecli'
        if subdir:
           path += f"/{subdir}"
        return path
    
    monkeypatch.setattr('biblecli.utils.get_app_data_path', mock_get_app_data_path)


# TODO: define helpers.translation_exists()


# monkeypatch and tmp_path require function scope
@pytest.fixture(scope='function', autouse=True)
def download_translations(app_data_path):
    for translation in ['BSB', 'KJV']:
        bible = BibleClient(translation)
        bible.create_bible_db()
    
    default_translation = CLIConfig.get_default_translation()
    
    if default_translation != 'BSB':
        CLIConfig.set_default_translation('BSB')
