# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Unsplash API credentials
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_SECRET_KEY = os.getenv('UNSPLASH_SECRET_KEY')

# AWS credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Database credentials
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Image processing settings
IMAGE_SIZES = {
    'full': (1920, 1080),
    'medium': (1024, 768),
    'thumbnail': (256, 256)
}

# Rate limiting (to comply with Unsplash API limits)
RATE_LIMIT_PER_HOUR = 50
PHOTOS_PER_PAGE = 30