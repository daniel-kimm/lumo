# main.py
import time
import random
from tqdm import tqdm
import argparse
from unsplash_client import UnsplashClient
from image_processor import ImageProcessor
from db_manager import DatabaseManager
from allocation import DOMAIN_ALLOCATION
from config import PHOTOS_PER_PAGE

def main():
    parser = argparse.ArgumentParser(description='Download and process images from Unsplash')
    parser.add_argument('--target', type=int, default=100000, help='Target number of images to collect')
    parser.add_argument('--check', action='store_true', help='Just check current counts')
    args = parser.parse_args()
    
    db_manager = DatabaseManager()
    
    # If just checking counts, display and exit
    if args.check:
        domain_counts = db_manager.get_domain_counts()
        total = db_manager.get_total_count()
        
        print(f"Total images: {total}")
        print("\nBreakdown by domain and subcategory:")
        current_domain = None
        domain_total = 0
        
        for domain, subcategory, count in domain_counts:
            if domain != current_domain:
                if current_domain:
                    print(f"  TOTAL: {domain_total}")
                print(f"\n{domain}:")
                current_domain = domain
                domain_total = 0
                
            domain_total += count
            print(f"  {subcategory}: {count}")
            
        if current_domain:
            print(f"  TOTAL: {domain_total}")
            
        return
    
    unsplash_client = UnsplashClient()
    image_processor = ImageProcessor(db_manager)
    
    # Track progress
    total_target = args.target
    processed_count = db_manager.get_total_count()
    
    print(f"Starting with {processed_count} images already processed")
    
    # Create a flat list of all subcategories with their allocation
    all_subcategories = []
    for domain, domain_data in DOMAIN_ALLOCATION.items():
        for subcategory, allocation in domain_data['subcategories'].items():
            all_subcategories.append({
                'domain': domain,
                'subcategory': subcategory,
                'allocation': allocation,
                'search_terms': domain_data['search_terms']
            })
    
    # Main processing loop
    pbar = tqdm(total=total_target, initial=processed_count)
    
    while processed_count < total_target:
        # Get current counts
        domain_counts = {}
        for domain, subcategory, count in db_manager.get_domain_counts():
            if domain not in domain_counts:
                domain_counts[domain] = {}
            domain_counts[domain][subcategory] = count
        
        # Prioritize subcategories that need more images
        subcategories_to_process = []
        for subcategory_data in all_subcategories:
            domain = subcategory_data['domain']
            subcategory = subcategory_data['subcategory']
            allocation = subcategory_data['allocation']
            
            current_count = domain_counts.get(domain, {}).get(subcategory, 0)
            if current_count < allocation:
                # Calculate priority (higher means more images needed)
                priority = (allocation - current_count) / allocation
                subcategories_to_process.append({
                    **subcategory_data,
                    'current_count': current_count,
                    'priority': priority
                })
        
        # Sort by priority (highest first)
        subcategories_to_process.sort(key=lambda x: x['priority'], reverse=True)
        
        if not subcategories_to_process:
            print("All allocations fulfilled!")
            break
            
        # Select a subcategory to process based on priority
        subcategory_data = subcategories_to_process[0]
        domain = subcategory_data['domain']
        subcategory = subcategory_data['subcategory']
        search_terms = subcategory_data['search_terms']
        
        # Pick a random search term from the domain
        search_term = random.choice(search_terms)
        
        # Determine page to fetch (random for diversity)
        max_page = 20  # Unsplash limitation
        page = random.randint(1, max_page)
        
        # Randomize orientation occasionally
        orientation = random.choice([None, 'landscape', 'portrait', 'squarish']) if random.random() < 0.3 else None
        
        # Fetch photos
        print(f"\nFetching for {domain}/{subcategory} using search term '{search_term}' (page {page})")
        photos = unsplash_client.search_photos(search_term, page=page, orientation=orientation)
        
        # Process each photo
        for photo in photos.get('results', []):
            if processed_count >= total_target:
                break
                
            result = image_processor.process_unsplash_photo(photo, domain, subcategory)
            if result:
                processed_count += 1
                pbar.update(1)
                
                # Rate limiting - pause between processing
                time.sleep(0.5)
    
    pbar.close()
    print(f"Completed processing {processed_count} images")

if __name__ == "__main__":
    main()