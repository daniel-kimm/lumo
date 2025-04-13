# unsplash_client.py
import time
import random
import requests
from config import UNSPLASH_ACCESS_KEY, RATE_LIMIT_PER_HOUR, PHOTOS_PER_PAGE

class UnsplashClient:
    def __init__(self):
        self.api_key = UNSPLASH_ACCESS_KEY
        self.base_url = "https://api.unsplash.com"
        self.request_timestamps = []
        
    def _respect_rate_limit(self):
        """Ensure we don't exceed Unsplash API rate limits"""
        current_time = time.time()
        # Remove timestamps older than 1 hour
        self.request_timestamps = [ts for ts in self.request_timestamps if current_time - ts < 3600]
        
        if len(self.request_timestamps) >= RATE_LIMIT_PER_HOUR:
            wait_time = 3600 - (current_time - self.request_timestamps[0]) + 1
            print(f"Rate limit approached. Waiting {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            
        self.request_timestamps.append(time.time())
        
    def search_photos(self, query, page=1, per_page=PHOTOS_PER_PAGE, orientation=None):
        """Search for photos with given query and pagination"""
        self._respect_rate_limit()
        
        try:
            # Add some randomness to the query to increase diversity
            if random.random() < 0.3 and " " in query:
                terms = query.split()
                query = " ".join(random.sample(terms, max(1, len(terms) - 1)))
            
            # Build the request parameters
            params = {
                'query': query,
                'page': page,
                'per_page': per_page,
                'client_id': self.api_key,
            }
            
            if orientation:
                params['orientation'] = orientation
                
            # Make the request
            response = requests.get(
                f"{self.base_url}/search/photos",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error searching photos for '{query}': {str(e)}")
            time.sleep(5)  # Wait before retrying
            return {"results": []}
        
    def get_photo_data(self, photo_id):
        """Get detailed data for a specific photo"""
        self._respect_rate_limit()
        
        try:
            response = requests.get(
                f"{self.base_url}/photos/{photo_id}",
                params={'client_id': self.api_key},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting photo data for ID {photo_id}: {str(e)}")
            return None