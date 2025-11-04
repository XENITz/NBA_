"""
Quick Analysis Script - NBA Predictions

Simple interface for quick matchup analysis.

Usage:
    python quick_analyze.py matchup "Team1" "Team2"
    python quick_analyze.py player "Player Name"
    python quick_analyze.py today
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the analyzer
from src.analyze import main

if __name__ == "__main__":
    main()
