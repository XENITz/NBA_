"""
NBA Prediction System - Source Code Package

This package contains all the core modules for NBA game prediction:
- main: Core data extraction from NBA API
- prediction_model: Advanced prediction algorithms
- team_fallback_data: Historical team statistics
- analyze: Interactive CLI tool
- enhanced_predictor: Player availability analysis
- advanced_enhanced_predictor: Complete prediction with all features
"""

__version__ = "2.0.0"
__author__ = "NBA Prediction Team"

from .main import NBADataExtractor
from .prediction_model import AdvancedPredictor

__all__ = ['NBADataExtractor', 'AdvancedPredictor']
