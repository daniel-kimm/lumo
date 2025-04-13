# image_retrieval.py
import torch
import clip
import numpy as np
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

load_dotenv()

class ImageRetriever:
    def __init__(self):
        # Load CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # Setup database connection
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    
    def encode_text(self, text):
        """Encode text prompt to CLIP embedding"""
        with torch.no_grad():
            text_encoded = self.model.encode_text(clip.tokenize([text]).to(self.device))
            return text_encoded.cpu().numpy().astype(np.float32)[0]
    
    def find_similar_images(self, text_prompt, num_images=16, domain=None, subcategory=None):
        """Find images similar to the text prompt"""
        # Get text embedding
        text_embedding = self.encode_text(text_prompt)
        
        # Prepare query conditions
        conditions = []
        params = [text_embedding.tobytes()]
        
        if domain:
            conditions.append("i.domain = %s")
            params.append(domain)
        
        if subcategory:
            conditions.append("i.subcategory = %s")
            params.append(subcategory)
        
        where_clause = " AND ".join(conditions) if conditions else ""
        if where_clause:
            where_clause = "WHERE " + where_clause
        
        # Query using embedding similarity
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = f"""
            SELECT 
                i.id, 
                i.domain, 
                i.subcategory, 
                i.urls,
                i.colors,
                i.tags,
                cosine_similarity(e.embedding, %s) as similarity
            FROM 
                image_embeddings e
            JOIN 
                images i ON e.id = i.id
            {where_clause}
            ORDER BY 
                similarity DESC
            LIMIT %s
            """
            
            # Add LIMIT parameter
            params.append(num_images)
            
            # Execute query
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Process results
            images = []
            for row in results:
                images.append({
                    'id': row['id'],
                    'domain': row['domain'],
                    'subcategory': row['subcategory'],
                    'urls': json.loads(row['urls']) if isinstance(row['urls'], str) else row['urls'],
                    'colors': json.loads(row['colors']) if isinstance(row['colors'], str) else row['colors'],
                    'tags': json.loads(row['tags']) if isinstance(row['tags'], str) else row['tags'],
                    'similarity': float(row['similarity'])
                })
                
            return images
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

# Example function to create a moodboard
def create_moodboard(prompt, num_images=16, domain=None):
    retriever = ImageRetriever()
    
    try:
        # Add modifiers to improve results
        enhanced_prompt = f"high quality, professional {prompt}"
        
        # Get images
        images = retriever.find_similar_images(
            enhanced_prompt, 
            num_images=num_images,
            domain=domain
        )
        
        # Print results
        print(f"Found {len(images)} images for prompt: '{prompt}'")
        for i, img in enumerate(images):
            print(f"{i+1}. {img['urls']['medium']} (similarity: {img['similarity']:.4f})")
            
        return images
        
    finally:
        retriever.close()

if __name__ == "__main__":
    # Example usage
    prompt = input("Enter your moodboard prompt: ")
    create_moodboard(prompt)