"""
Migration script to add reset_token and reset_token_expires columns to users table
"""
import sqlite3

def migrate():
    conn = sqlite3.connect('techstudy.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'reset_token' not in columns:
            print("Adding reset_token column...")
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
            print("✓ reset_token column added")
        else:
            print("reset_token column already exists")
        
        if 'reset_token_expires' not in columns:
            print("Adding reset_token_expires column...")
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP")
            print("✓ reset_token_expires column added")
        else:
            print("reset_token_expires column already exists")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
