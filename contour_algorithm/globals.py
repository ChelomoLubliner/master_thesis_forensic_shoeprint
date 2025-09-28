import os

OLD_DATASET = True



if OLD_DATASET:
    DATASET = 'contacts_data.txt'
    FOLDER = 'Images'
    LOCATIONS = 'locations_data.csv'
    W, H = 307, 395  # COL, ROW
else:
    DATASET = 'contacts_data_naomi_fast.txt'
    FOLDER = 'Images/'
    LOCATIONS = 'results_data_naomi_fast.txt'
    W, H = 255, 367

# Absolute paths for data directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'Data')
SHARED_DATA_PATH = os.path.join(PROJECT_ROOT, 'shared_data') + os.sep
PROCESSING_DATA_PATH = os.path.join(PROJECT_ROOT, 'shared_data', 'processing_data') + os.sep
IMAGES_PATH = os.path.join(PROJECT_ROOT, 'Images')




