"""
Quick analysis script for NBA predictions
Run this to analyze specific matchups and players
"""

from main import NBADataExtractor
from prediction_model import AdvancedPredictor, generate_betting_insights
import sys

def analyze_matchup(home_team, away_team, key_players=None):
    """Analyze a specific matchup with predictions"""
    print("\n" + "="*70)
    print(f"NBA MATCH ANALYSIS: {away_team} @ {home_team}".center(70))
    print("="*70)
    
    extractor = NBADataExtractor()
    predictor = AdvancedPredictor()
    
    # Get team stats
    home_stats = extractor.get_team_recent_performance(home_team, last_n_games=10)
    away_stats = extractor.get_team_recent_performance(away_team, last_n_games=10)
    
    if not home_stats or not away_stats:
        print("❌ Unable to fetch team data. Check team names.")
        return
    
    # Get player stats if provided
    player_stats = []
    if key_players:
        print(f"\n{'='*70}")
        print("KEY PLAYERS ANALYSIS".center(70))
        print("="*70)
        
        for player_name in key_players:
            stats = extractor.get_player_recent_stats(player_name, last_n_games=5)
            if stats:
                player_stats.append(stats)
                
                # Player performance prediction
                player_prediction = predictor.predict_player_performance(stats)
                if player_prediction:
                    print(f"\n{player_prediction['player']}:")
                    print(f"  {player_prediction['prediction']}")
                    print(f"  Expected Points: {player_prediction['expected_points_range']}")
                    print(f"  Consistency: {player_prediction['consistency_rating']}")
                    print(f"  Confidence: {player_prediction['confidence']}")
    
    # Generate match prediction
    print(f"\n{'='*70}")
    print("ADVANCED MATCH PREDICTION".center(70))
    print("="*70)
    
    prediction = predictor.predict_match_outcome(home_stats, away_stats, player_stats)
    
    print(f"\n🏆 PREDICTED WINNER: {prediction['favored_team']}")
    print(f"   Confidence Level: {prediction['confidence']}")
    print(f"\n📊 WIN PROBABILITIES:")
    print(f"   {home_stats['team_name']}: {prediction['home_win_probability']}%")
    print(f"   {away_stats['team_name']}: {prediction['away_win_probability']}%")
    print(f"\n🎯 PREDICTED FINAL SCORE:")
    print(f"   {home_stats['team_name']}: {prediction['predicted_home_score']}")
    print(f"   {away_stats['team_name']}: {prediction['predicted_away_score']}")
    print(f"   Expected Point Spread: {prediction['point_spread']:.1f}")
    
    # Betting insights
    insights = generate_betting_insights(prediction)
    if insights:
        print(f"\n{'='*70}")
        print("BETTING/FANTASY INSIGHTS".center(70))
        print("="*70)
        for insight in insights:
            print(f"  {insight}")
    
    print(f"\n{'='*70}")
    print("ANALYSIS COMPLETE".center(70))
    print("="*70 + "\n")


def quick_player_analysis(player_name):
    """Quick analysis of a single player"""
    print("\n" + "="*70)
    print(f"PLAYER ANALYSIS: {player_name}".center(70))
    print("="*70)
    
    extractor = NBADataExtractor()
    predictor = AdvancedPredictor()
    
    stats = extractor.get_player_recent_stats(player_name, last_n_games=10)
    
    if not stats:
        print(f"❌ Could not find player: {player_name}")
        return
    
    # Performance prediction
    prediction = predictor.predict_player_performance(stats)
    
    if prediction:
        print(f"\n{'='*70}")
        print("PERFORMANCE PREDICTION".center(70))
        print("="*70)
        print(f"\n{prediction['prediction']}")
        print(f"\nExpected Points Range: {prediction['expected_points_range']}")
        print(f"Consistency Rating: {prediction['consistency_rating']}")
        print(f"Performance Score: {prediction['performance_score']}/100")
        print(f"Confidence: {prediction['confidence']}")
    
    # Recent games trend
    print(f"\n{'='*70}")
    print("RECENT GAMES PERFORMANCE".center(70))
    print("="*70)
    
    recent_games = stats.get('recent_games', [])[:5]
    if recent_games:
        print("\nLast 5 Games:")
        for i, game in enumerate(recent_games, 1):
            print(f"\n  Game {i}: {game.get('MATCHUP', 'N/A')}")
            print(f"    Date: {game.get('GAME_DATE', 'N/A')}")
            print(f"    Points: {game.get('PTS', 0)}")
            print(f"    Rebounds: {game.get('REB', 0)} | Assists: {game.get('AST', 0)}")
            print(f"    FG%: {game.get('FG_PCT', 0)*100:.1f}% | +/-: {game.get('PLUS_MINUS', 0):+.0f}")
    
    print(f"\n{'='*70}\n")


def show_todays_games():
    """Show all games scheduled for today"""
    print("\n" + "="*70)
    print("TODAY'S NBA GAMES".center(70))
    print("="*70)
    
    extractor = NBADataExtractor()
    games = extractor.get_todays_games()
    
    if not games:
        print("\n⚠️ No games scheduled for today or unable to fetch game data.")
    
    print("\n" + "="*70 + "\n")


def interactive_mode():
    """Interactive mode for custom queries"""
    print("\n" + "="*70)
    print("NBA PREDICTION TOOL - INTERACTIVE MODE".center(70))
    print("="*70)
    print("\nCommands:")
    print("  1. Analyze matchup: matchup [home_team] vs [away_team]")
    print("  2. Analyze player: player [player_name]")
    print("  3. Show today's games: today")
    print("  4. Exit: quit")
    print("="*70)
    
    while True:
        user_input = input("\n> ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit' or user_input.lower() == 'exit':
            print("\n👋 Thanks for using NBA Prediction Tool!")
            break
        
        elif user_input.lower() == 'today':
            show_todays_games()
        
        elif user_input.lower().startswith('player '):
            player_name = user_input[7:].strip()
            quick_player_analysis(player_name)
        
        elif user_input.lower().startswith('matchup '):
            # Parse matchup command
            parts = user_input[8:].split(' vs ')
            if len(parts) == 2:
                home_team = parts[1].strip()
                away_team = parts[0].strip()
                
                # Ask for key players
                key_input = input("Enter key players to analyze (comma-separated, or press Enter to skip): ").strip()
                key_players = [p.strip() for p in key_input.split(',')] if key_input else None
                
                analyze_matchup(home_team, away_team, key_players)
            else:
                print("❌ Invalid format. Use: matchup [away_team] vs [home_team]")
        
        else:
            print("❌ Unknown command. Type 'quit' to exit or use one of the commands above.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'today':
            show_todays_games()
        
        elif command == 'player' and len(sys.argv) > 2:
            player_name = ' '.join(sys.argv[2:])
            quick_player_analysis(player_name)
        
        elif command == 'matchup' and len(sys.argv) > 3:
            # Format: python analyze.py matchup "Lakers" "Warriors" "LeBron James,Stephen Curry"
            home_team = sys.argv[2]
            away_team = sys.argv[3]
            key_players = sys.argv[4].split(',') if len(sys.argv) > 4 else None
            analyze_matchup(home_team, away_team, key_players)
        
        else:
            print("❌ Invalid command.")
            print("Usage:")
            print("  python analyze.py today")
            print("  python analyze.py player 'LeBron James'")
            print("  python analyze.py matchup 'Lakers' 'Warriors' 'LeBron James,Stephen Curry'")
    
    else:
        # Run interactive mode
        interactive_mode()
