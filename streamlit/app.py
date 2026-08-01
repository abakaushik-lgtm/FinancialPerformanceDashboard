"""
streamlit/app.py
Entry point wrapper for Streamlit application.
"""

import os
import sys

# Add parent directory to sys.path and run main app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from app import main

if __name__ == '__main__':
    # Launch main script logic
    pass
