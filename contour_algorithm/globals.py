import os

# Import environment variables from .env file

# Get the absolute path to the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_file = os.path.join(project_root, '.env')

try:
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    print(f"Warning: .env file not found at {env_file}")
    pass

# Configuration via environment variables
# Default to old dataset if not specified
DATASET = os.getenv('DATASET')
FOLDER = os.getenv('FOLDER')
LOCATIONS = os.getenv('LOCATIONS')
W = int(os.getenv('W'))  # COL
H = int(os.getenv('H'))  # ROW

# Snake initialization parameters (dataset-specific)
SNAKE_Y_CENTER = int(os.getenv('SNAKE_Y_CENTER'))
SNAKE_Y_RADIUS = int(os.getenv('SNAKE_Y_RADIUS'))
SNAKE_X_CENTER = int(os.getenv('SNAKE_X_CENTER'))
SNAKE_X_RADIUS = int(os.getenv('SNAKE_X_RADIUS'))

# Location file format parameters
LOCATIONS_HAS_HEADER = os.getenv('LOCATIONS_HAS_HEADER').lower() == 'true'
LOCATIONS_SEPARATOR = os.getenv('LOCATIONS_SEPARATOR')
LOCATIONS_SCALE_FACTOR = float(os.getenv('LOCATIONS_SCALE_FACTOR'))

# Processing data paths
PROCESSING_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared_data', 'processing_data') + os.sep

# Absolute paths for data directories  
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'Data')
SHARED_DATA_PATH = os.path.join(PROJECT_ROOT, 'shared_data')
IMAGES_PATH = os.path.join(PROJECT_ROOT, 'Images')





