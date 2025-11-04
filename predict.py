"""
NBA Prediction System - Main Entry Point

Usage:
    python predict.py "HomeTeam" "AwayTeam"
    
Examples:
    python predict.py "Lakers" "Warriors"
    python predict.py "Celtics" "Heat"
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Add src to path so imports work
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    # Now run the predictor
    from advanced_enhanced_predictor import main
    main()
