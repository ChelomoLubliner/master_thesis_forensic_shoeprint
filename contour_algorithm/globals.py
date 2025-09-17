import os

# Import environment variables from .env file
try:
    with open('../.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
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
PROCESSING_DATA_PATH = '../shared_data/processing_data/'





