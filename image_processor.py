import os
import uuid
import requests
import io
from PIL import Image, ImageOps
from io import BytesIO
import boto3
from datetime import datetime
import hashlib
from tqdm import tqdm
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET_NAME, IMAGE_SIZES

class ImageProcessor:
    def __init__(self, db_manager):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        self.bucket_name = S3_BUCKET_NAME
        self.db_manager = db_manager
        self.temp_dir = 'temp_images'
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def _download_image(self, url):
        """Download image from URL"""
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            return BytesIO(response.content)
        except Exception as e:
            print(f"Error downloading image from {url}: {str(e)}")
            return None
    
    def _compute_image_hash(self, image_data):
        """Compute MD5 hash of image data for deduplication"""
        return hashlib.md5(image_data.getvalue()).hexdigest()
            
    def _resize_image(self, image, size):
        """Resize image while maintaining aspect ratio"""
        return ImageOps.fit(image, size, Image.LANCZOS)
    
    def _extract_colors(self, image, num_colors=6):
        """Extract dominant colors from image"""
        try:
            image = image.copy()
            image.thumbnail((100, 100))
            
            # Convert to small size for faster processing
            result = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
            result = result.convert('RGB')
            palette = result.getcolors(num_colors)
            
            # Sort colors by frequency (descending)
            palette.sort(reverse=True)
            
            colors = []
            for count, color in palette:
                hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                percentage = count / (100 * 100)
                colors.append({
                    'hex': hex_color,
                    'percentage': percentage
                })
                
            return colors
        except Exception as e:
            print(f"Error extracting colors: {str(e)}")
            return []
    
    def process_unsplash_photo(self, photo_data, domain, subcategory):
        """
        Process a photo from Unsplash:
        1. Download the image
        2. Create different sizes
        3. Extract metadata (colors, dimensions)
        4. Upload to S3
        5. Store metadata in database
        """
        try:
            photo_id = photo_data['id']
            photo_url = photo_data['urls']['raw']
            
            # Skip if already in database
            if self.db_manager.photo_exists(photo_id):
                return None
                
            # Download the image
            image_data = self._download_image(photo_url)
            if not image_data:
                return None
                
            # Check for duplicates using image hash
            image_hash = self._compute_image_hash(image_data)
            if self.db_manager.hash_exists(image_hash):
                return None
                
            # Open the image with PIL
            image = Image.open(image_data)
            
            # Extract image metadata
            width, height = image.size
            aspect_ratio = width / height
            colors = self._extract_colors(image)
            
            # Create a unique filename
            unique_id = str(uuid.uuid4())
            
            # Create different sizes and upload to S3
            s3_urls = {}
            
            for size_name, dimensions in IMAGE_SIZES.items():
                resized = self._resize_image(image, dimensions)
                
                # Save to temporary file
                temp_file = os.path.join(self.temp_dir, f"{unique_id}_{size_name}.jpg")
                resized.save(temp_file, "JPEG", quality=85)
                
                # Upload to S3
                s3_key = f"{domain}/{subcategory}/{size_name}/{unique_id}.jpg"
                self.s3_client.upload_file(
                    temp_file,
                    self.bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': 'image/jpeg'}
                )
                
                # Generate S3 URL
                s3_urls[size_name] = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
                
                # Remove temporary file
                os.remove(temp_file)
            
            # Prepare metadata for database
            metadata = {
                'id': unique_id,
                'original_id': photo_id,
                'source': 'unsplash',
                'source_url': photo_data['links']['html'],
                'download_url': photo_url,
                'dimensions': {
                    'width': width,
                    'height': height,
                    'aspect_ratio': aspect_ratio
                },
                'hash': image_hash,
                'colors': colors,
                'urls': s3_urls,
                'attribution': {
                    'name': photo_data['user']['name'],
                    'username': photo_data['user']['username'],
                    'link': photo_data['user']['links']['html']
                },
                'domain': domain,
                'subcategory': subcategory,
                'tags': [tag for tag in photo_data.get('tags', []) if 'title' in tag],
                'date_imported': datetime.now().isoformat()
            }
            
            # Store in database
            self.db_manager.store_image_metadata(metadata)
            
            return metadata
            
        except Exception as e:
            print(f"Error processing photo {photo_data.get('id', 'unknown')}: {str(e)}")
            return None
