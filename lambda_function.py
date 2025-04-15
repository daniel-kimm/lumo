# lambda_function.py
import json
import clip
import torch
import psycopg2
import psycopg2.extras
import numpy as np
import os
import boto3

# Load model at cold start (outside handler)
device = "cpu"  # Lambda doesn't have GPUs
model, preprocess = clip.load("ViT-B/32", device=device)

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        prompt = body.get('prompt')
        
        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Prompt is required'})
            }
            
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        
        # Get text embedding
        with torch.no_grad():
            text_encoded = model.encode_text(clip.tokenize([prompt]).to(device))
            text_embedding = text_encoded.cpu().numpy().astype(np.float32)[0]
        
        # Query similar images
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = """
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
            ORDER BY 
                similarity DESC
            LIMIT 16
            """
            
            cursor.execute(query, [text_embedding.tobytes()])
            results = cursor.fetchall()
            
            # Process results
            images = []
            for row in results:
                # Clean up the results
                images.append({
                    'id': row['id'],
                    'domain': row['domain'],
                    'subcategory': row['subcategory'],
                    'urls': json.loads(row['urls']) if isinstance(row['urls'], str) else row['urls'],
                    'colors': json.loads(row['colors']) if isinstance(row['colors'], str) else row['colors'],
                    'tags': json.loads(row['tags']) if isinstance(row['tags'], str) else row['tags'],
                    'similarity': float(row['similarity'])
                })
        
        # Generate color palette and suggested styles
        colorPalette = extract_colors(images)
        suggestedStyles = extract_styles(images)
        
        # Close database connection
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # For CORS
            },
            'body': json.dumps({
                'images': images,
                'colorPalette': colorPalette,
                'suggestedStyles': suggestedStyles
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Helper functions for extracting colors and styles
def extract_colors(images):
    # Same implementation as before
    all_colors = []
    for img in images:
        if img.get('colors'):
            all_colors.extend(img['colors'])
    
    # Count colors and get top 6
    color_count = {}
    for color in all_colors:
        color_count[color] = color_count.get(color, 0) + 1
    
    return sorted(color_count.keys(), key=lambda c: color_count[c], reverse=True)[:6]

def extract_styles(images):
    # Same implementation as before
    style_tags = set()
    style_keywords = ['vintage', 'modern', 'minimal', 'cinematic', 'abstract']
    
    for img in images:
        if img.get('tags'):
            for tag in img['tags']:
                if any(kw in tag.lower() for kw in style_keywords):
                    style_tags.add(tag)
    
    return list(style_tags)[:3]