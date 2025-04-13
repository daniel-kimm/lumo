# image_embeddings.py
import os
import torch
import clip
from PIL import Image
import psycopg2
import numpy as np
import json
from tqdm import tqdm
from dotenv import load_dotenv
import io
import requests
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        # Load CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # Setup database connection
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # Create embeddings table if it doesn't exist
        self._create_embeddings_table()
        
    def _create_embeddings_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_embeddings (
                id UUID PRIMARY KEY REFERENCES images(id),
                embedding BYTEA NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_image_embeddings_id ON image_embeddings(id);
            """)
            self.conn.commit()
    
    def get_unprocessed_images(self, limit=100):
        """Get images that don't have embeddings yet"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT i.id, i.urls 
            FROM images i 
            LEFT JOIN image_embeddings e ON i.id = e.id 
            WHERE e.id IS NULL 
            LIMIT %s
            """, (limit,))
            return cursor.fetchall()
    
    def process_image(self, image_id, image_urls):
        """Generate embedding for a single image"""
        try:
            # Load image from medium size URL
            url = json.loads(image_urls)['medium']
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if needed (for PNG with alpha channel)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Preprocess and generate embedding
            image_input = self.preprocess(img).unsqueeze(0).to(self.device)
            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                embedding = image_features.cpu().numpy().astype(np.float32)
            
            # Save embedding to database
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO image_embeddings (id, embedding) VALUES (%s, %s)",
                    (image_id, embedding.tobytes())
                )
                self.conn.commit()
                
            return True
        except Exception as e:
            print(f"Error processing image {image_id}: {str(e)}")
            return False
    
    def process_batch(self, batch_size=100):
        """Process a batch of images"""
        images = self.get_unprocessed_images(batch_size)
        if not images:
            print("No unprocessed images found.")
            return 0
        
        print(f"Processing {len(images)} images...")
        successful = 0
        
        for image_id, image_urls in tqdm(images):
            if self.process_image(image_id, image_urls):
                successful += 1
        
        print(f"Successfully generated embeddings for {successful}/{len(images)} images.")
        return successful
    
    def get_embedding_stats(self):
        """Get statistics on embedding coverage"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM images")
            total_images = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM image_embeddings")
            total_embeddings = cursor.fetchone()[0]
            
            return {
                "total_images": total_images,
                "images_with_embeddings": total_embeddings,
                "completion_percentage": round(total_embeddings / total_images * 100, 2) if total_images > 0 else 0
            }

def main():
    generator = EmbeddingGenerator()
    
    # Print current stats
    stats = generator.get_embedding_stats()
    print(f"Current status: {stats['images_with_embeddings']}/{stats['total_images']} images have embeddings ({stats['completion_percentage']}%)")
    
    # Process all images in batches
    total_processed = 0
    while True:
        processed = generator.process_batch(batch_size=50)
        if processed == 0:
            break
        total_processed += processed
    
    print(f"Completed! Total processed this run: {total_processed}")
    
    # Final stats
    stats = generator.get_embedding_stats()
    print(f"Final status: {stats['images_with_embeddings']}/{stats['total_images']} images have embeddings ({stats['completion_percentage']}%)")

if __name__ == "__main__":
    main()