"""
Quick Setup Script
==================

Automated setup for EcoPackAI backend development environment.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import os
import sys
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def run_setup():
    """Run setup tasks"""
    
    print_header("EcoPackAI Backend Setup")
    
    # Check Python version
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"  Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Create necessary directories
    print("\n✓ Creating directories...")
    dirs = ['logs', 'data', 'models']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"  Created: {dir_name}/")
    
    # Check if .env exists
    print("\n✓ Checking environment configuration...")
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("  ⚠ .env not found")
            print("  → Copy .env.example to .env and configure your settings")
        else:
            print("  ❌ .env.example not found")
    else:
        print("  .env found")
    
    # Check database
    print("\n✓ Database setup...")
    print("  → Ensure PostgreSQL is running")
    print("  → Create database: createdb ecopackai_db")
    print("  → Run migrations or create tables")
    
    # Print next steps
    print_header("Setup Complete!")
    
    print("Next Steps:\n")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt\n")
    print("2. Configure environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your settings\n")
    print("3. Setup database:")
    print("   createdb ecopackai_db")
    print("   python -c \"from app import app, db; with app.app_context(): db.create_all()\"\n")
    print("4. Run application:")
    print("   python app.py\n")
    print("5. Run tests:")
    print("   pytest\n")
    print("6. View documentation:")
    print("   cat docs/BACKEND_INTEGRATION.md\n")
    
    print("=" * 60)
    print("For help: https://github.com/yourusername/EcoPackAI")
    print("=" * 60 + "\n")
    
    return True

if __name__ == '__main__':
    run_setup()
