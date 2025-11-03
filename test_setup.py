"""
Test script to verify NBA prediction system is working correctly
Run this to make sure everything is set up properly
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("="*60)
    print("Testing Module Imports...")
    print("="*60)
    
    modules = [
        ('nba_api', 'NBA API'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests'),
        ('json', 'JSON'),
        ('datetime', 'Datetime')
    ]
    
    failed = []
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name:20} - OK")
        except ImportError as e:
            print(f"❌ {display_name:20} - FAILED: {e}")
            failed.append(module_name)
    
    return len(failed) == 0


def test_project_files():
    """Test if all project files exist"""
    print("\n" + "="*60)
    print("Testing Project Files...")
    print("="*60)
    
    import os
    
    required_files = [
        'main.py',
        'analyze.py',
        'prediction_model.py',
        'requirements.txt',
        'README.md'
    ]
    
    failed = []
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename:25} - EXISTS")
        else:
            print(f"❌ {filename:25} - MISSING")
            failed.append(filename)
    
    return len(failed) == 0


def test_nba_api_connection():
    """Test if NBA API is accessible"""
    print("\n" + "="*60)
    print("Testing NBA API Connection...")
    print("="*60)
    
    try:
        from nba_api.stats.static import players
        
        # Try to get players list
        all_players = players.get_players()
        
        if all_players and len(all_players) > 0:
            print(f"✅ NBA API Connected - Found {len(all_players)} players")
            
            # Show a few example players
            print("\nExample players found:")
            for player in all_players[:5]:
                print(f"   - {player['full_name']}")
            
            return True
        else:
            print("❌ NBA API returned no data")
            return False
            
    except Exception as e:
        print(f"❌ NBA API connection failed: {e}")
        return False


def test_data_extraction():
    """Test if data extraction works"""
    print("\n" + "="*60)
    print("Testing Data Extraction...")
    print("="*60)
    
    try:
        from main import NBADataExtractor
        
        extractor = NBADataExtractor()
        print("✅ NBADataExtractor initialized")
        
        # Test finding a player
        player = extractor.get_player_by_name("LeBron James")
        if player:
            print(f"✅ Player search works - Found: {player['full_name']}")
        else:
            print("⚠️  Player search returned None (might be OK if player retired)")
        
        # Test finding a team
        team = extractor.get_team_by_name("Lakers")
        if team:
            print(f"✅ Team search works - Found: {team['full_name']}")
        else:
            print("❌ Team search failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data extraction test failed: {e}")
        return False


def test_prediction_model():
    """Test if prediction model works"""
    print("\n" + "="*60)
    print("Testing Prediction Model...")
    print("="*60)
    
    try:
        from prediction_model import AdvancedPredictor
        
        predictor = AdvancedPredictor()
        print("✅ AdvancedPredictor initialized")
        
        # Create test data
        home_stats = {
            'team_name': 'Test Home Team',
            'win_percentage': 60,
            'avg_points_scored': 112,
            'avg_fg_pct': 47.5,
            'avg_fg3_pct': 36.8
        }
        
        away_stats = {
            'team_name': 'Test Away Team',
            'win_percentage': 55,
            'avg_points_scored': 108,
            'avg_fg_pct': 46.2,
            'avg_fg3_pct': 35.5
        }
        
        prediction = predictor.predict_match_outcome(home_stats, away_stats)
        
        if prediction and 'home_win_probability' in prediction:
            print("✅ Prediction model works")
            print(f"   Test prediction: {prediction['favored_team']} "
                  f"({prediction['home_win_probability']}% vs {prediction['away_win_probability']}%)")
            return True
        else:
            print("❌ Prediction model returned invalid data")
            return False
            
    except Exception as e:
        print(f"❌ Prediction model test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("NBA PREDICTION SYSTEM - VERIFICATION TEST")
    print("="*60 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Project Files", test_project_files),
        ("NBA API Connection", test_nba_api_connection),
        ("Data Extraction", test_data_extraction),
        ("Prediction Model", test_prediction_model)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} - {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your NBA prediction system is ready to use!")
        print("\nNext steps:")
        print("  1. Run: python analyze.py today")
        print("  2. Try: python analyze.py player 'LeBron James'")
        print("  3. Test: python analyze.py matchup 'Lakers' 'Warriors'")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  - Make sure virtual environment is activated")
        print("  - Run: pip install -r requirements.txt")
        print("  - Check internet connection for API access")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
