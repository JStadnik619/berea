import os


def get_source_root():
    return os.path.realpath(os.path.dirname(__file__))


def get_downloaded_translations():
    files = os.listdir(f"{get_source_root()}/data/db")
    
    downloaded_translations = []
    
    for file in files:
        if file.endswith('.db'):
            downloaded_translations.append(file[:-3])
    
    return downloaded_translations
