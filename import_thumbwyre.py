#!/usr/bin/env python3
import os
import sqlite3

DB_FILE = 'backend.db'
SOURCE_DIR = 'thumbwyre'

def import_thumbwyre_files():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    count = 0
    for filename in os.listdir(SOURCE_DIR):
        filepath = os.path.join(SOURCE_DIR, filename)
        
        if os.path.isfile(filepath):
            # Extract title and category from filename
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            if ext in ['.mp3', '.mp4']:
                # Clean up filename for title
                title = name.replace('_', ' ').replace('(0)', '').strip()
                
                # Determine category and set default author
                if ext == '.mp3':
                    category = 'music'
                    author = 'wyreDev'
                else:  # .mp4
                    category = 'video'
                    author = 'wyreDev'
                
                description = f"{len(title)} seconds · Just now"
                src = f"{SOURCE_DIR}/{filename}"
                
                try:
                    cursor.execute(
                        'INSERT INTO videos(title, author, description, src, category) VALUES (?, ?, ?, ?, ?)',
                        (title, author, description, src, category)
                    )
                    count += 1
                    print(f'✓ Added: {title}')
                except sqlite3.IntegrityError:
                    print(f'⊘ Already exists: {title}')
                except Exception as e:
                    print(f'✗ Error adding {title}: {e}')
    
    conn.commit()
    conn.close()
    
    print(f'\n✅ Import complete! Added {count} files to database.')

if __name__ == '__main__':
    import_thumbwyre_files()
