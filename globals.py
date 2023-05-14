OLD_DATASET = False


PATH = '' # don't need path because Images and Data folder are in the project
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





