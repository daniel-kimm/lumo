# db_manager.py
import psycopg2
import json
from psycopg2.extras import Json
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        self.create_tables()
        
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id UUID PRIMARY KEY,
                original_id TEXT,
                source TEXT,
                source_url TEXT,
                download_url TEXT,
                dimensions JSONB,
                image_hash TEXT UNIQUE,
                colors JSONB,
                urls JSONB,
                attribution JSONB,
                domain TEXT,
                subcategory TEXT,
                tags JSONB,
                date_imported TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_images_domain ON images(domain);
            CREATE INDEX IF NOT EXISTS idx_images_subcategory ON images(subcategory);
            CREATE INDEX IF NOT EXISTS idx_images_hash ON images(image_hash);
            """)
            self.connection.commit()
            
    def photo_exists(self, original_id):
        """Check if a photo with the given original ID exists"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM images WHERE original_id = %s)", (original_id,))
            return cursor.fetchone()[0]
            
    def hash_exists(self, image_hash):
        """Check if an image with the given hash exists"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM images WHERE image_hash = %s)", (image_hash,))
            return cursor.fetchone()[0]
            
    def store_image_metadata(self, metadata):
        """Store image metadata in the database"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO images (
                    id, original_id, source, source_url, download_url, 
                    dimensions, image_hash, colors, urls, attribution,
                    domain, subcategory, tags, date_imported
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    metadata['id'],
                    metadata['original_id'],
                    metadata['source'],
                    metadata['source_url'],
                    metadata['download_url'],
                    Json(metadata['dimensions']),
                    metadata['hash'],
                    Json(metadata['colors']),
                    Json(metadata['urls']),
                    Json(metadata['attribution']),
                    metadata['domain'],
                    metadata['subcategory'],
                    Json(metadata['tags']),
                    metadata['date_imported']
                )
            )
            self.connection.commit()
            
    def get_domain_counts(self):
        """Get counts of images by domain and subcategory"""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT domain, subcategory, COUNT(*) 
                FROM images 
                GROUP BY domain, subcategory
                ORDER BY domain, subcategory
            """)
            return cursor.fetchall()
            
    def get_total_count(self):
        """Get total count of images"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM images")
            return cursor.fetchone()[0]