OLD_DATASET = True
PATH = '' # we don't need PATH anymore because Data and Images folders are in the project.


if OLD_DATASET:
    DATASET = 'contacts_data.txt'
    FOLDER = 'Images/Old_Shoes/'
    LOCATIONS = 'locations_data.csv'
    W, H = 307, 395  # COL, ROW
else:
    DATASET = 'contacts_data_naomi_fast.txt'
    FOLDER = 'Images/New_Shoes/'
    LOCATIONS = 'results_data_naomi_fast.txt'
    W, H = 255, 367





