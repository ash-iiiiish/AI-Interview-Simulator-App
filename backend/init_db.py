"""
Database initialization script.
Run this once to create all tables in PostgreSQL.

Usage:
    cd backend
    python init_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import engine, Base
import models  # noqa: F401 — import to register models

def init_database():
    print("🔧 Initializing database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        print("\nTables created:")
        for table in Base.metadata.sorted_tables:
            print(f"  → {table.name}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
