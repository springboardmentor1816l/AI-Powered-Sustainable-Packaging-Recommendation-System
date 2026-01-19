"""
Run EcoPackAI Application
==========================

Simplified startup script with automatic fallback to SQLite if PostgreSQL is unavailable.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import os
import sys
from pathlib import Path

def main():
    """Start the application with appropriate configuration"""
    
    print("\n" + "=" * 60)
    print("  EcoPackAI - Starting Application")
    print("=" * 60 + "\n")
    
    # Set environment to development by default
    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'development'
        print("✓ Environment: development")
    
    # Check if PostgreSQL is available, otherwise use SQLite
    if not os.environ.get('DATABASE_URL'):
        # Use SQLite as fallback for easy development
        db_path = Path(__file__).parent / 'dev_database.db'
        os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
        print(f"✓ Database: SQLite (fallback)")
        print(f"  Location: {db_path}")
    else:
        print(f"✓ Database: {os.environ['DATABASE_URL'].split('@')[0]}")
    
    # Disable auth for development
    if not os.environ.get('REQUIRE_AUTH'):
        os.environ['REQUIRE_AUTH'] = 'False'
        print("✓ Authentication: Disabled (development mode)")
    
    # Use simple cache for development
    if not os.environ.get('CACHE_TYPE'):
        os.environ['CACHE_TYPE'] = 'SimpleCache'
        print("✓ Cache: SimpleCache (in-memory)")
    
    print("\n" + "-" * 60)
    print("Starting Flask development server...")
    print("-" * 60 + "\n")
    
    # Import and run the app
    try:
        from app import app, db
        
        # Create tables if using SQLite
        if 'sqlite' in os.environ.get('DATABASE_URL', ''):
            with app.app_context():
                try:
                    db.create_all()
                    print("✓ Database tables created/verified\n")
                except Exception as e:
                    print(f"⚠ Database initialization skipped: {e}\n")
        
        # Start the server
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 Server starting on http://localhost:{port}")
        print(f"📖 API Documentation: http://localhost:{port}/api/v1/docs")
        print(f"💚 Health Check: http://localhost:{port}/health\n")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True
        )
        
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
