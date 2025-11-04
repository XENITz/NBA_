"""
ADVANCED NBA PREDICTOR with ALL NEW FEATURES
- Head-to-Head History
- Rest Days / Fatigue Factor
- Defensive Stats
- Player Availability
- Enhanced Prediction Algorithm
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import NBADataExtractor
from prediction_model import AdvancedPredictor
from nba_api.live.nba.endpoints import scoreboard
import time

class SuperPredictor(NBADataExtractor):
    """Ultimate predictor with all advanced features"""
    
    def __init__(self):
        super().__init__()
        self.predictor = AdvancedPredictor()
    
    def comprehensive_matchup_analysis(self, home_team, away_team, key_players_status=None):
        """
        Complete matchup analysis with ALL factors:
        - Recent team performance
        - Head-to-head history
        - Rest days / fatigue
        - Defensive stats
        - Player availability
        """
        print("\n" + "="*80)
        print(f"🏀 COMPREHENSIVE MATCHUP ANALYSIS: {away_team} @ {home_team} 🏀".center(80))
        print("="*80)
        
        # 1. Get basic team stats
        print("\n" + "="*80)
        print("📊 STEP 1: TEAM PERFORMANCE ANALYSIS".center(80))
        print("="*80)
        
        home_stats = self.get_team_recent_performance(home_team, last_n_games=10)
        away_stats = self.get_team_recent_performance(away_team, last_n_games=10)
        
        if not home_stats or not away_stats:
            print("❌ Unable to fetch team data.")
            return None
        
        # 2. Get head-to-head history
        print("\n" + "="*80)
        print("🔄 STEP 2: HEAD-TO-HEAD HISTORY".center(80))
        print("="*80)
        
        h2h_stats = self.get_head_to_head_history(home_team, away_team, last_n_games=5)
        
        # 3. Check rest days for both teams
        print("\n" + "="*80)
        print("😴 STEP 3: REST & FATIGUE ANALYSIS".center(80))
        print("="*80)
        
        print(f"\n{home_stats['team_name']}:")
        home_rest = self.get_rest_days(home_team)
        if home_rest:
            print(f"   Rest Days: {home_rest['rest_days']}")
            print(f"   Back-to-Back: {'YES ⚠️' if home_rest['is_back_to_back'] else 'NO ✅'}")
            print(f"   Fatigue Factor: {home_rest['fatigue_factor']:+d}%")
            if home_rest['fatigue_factor'] < 0:
                print(f"   ⚠️  Team may be fatigued!")
            elif home_rest['fatigue_factor'] > 0:
                print(f"   ✅ Team is well-rested!")
        
        print(f"\n{away_stats['team_name']}:")
        away_rest = self.get_rest_days(away_team)
        if away_rest:
            print(f"   Rest Days: {away_rest['rest_days']}")
            print(f"   Back-to-Back: {'YES ⚠️' if away_rest['is_back_to_back'] else 'NO ✅'}")
            print(f"   Fatigue Factor: {away_rest['fatigue_factor']:+d}%")
            if away_rest['fatigue_factor'] < 0:
                print(f"   ⚠️  Team may be fatigued!")
            elif away_rest['fatigue_factor'] > 0:
                print(f"   ✅ Team is well-rested!")
        
        # 4. Get defensive stats
        print("\n" + "="*80)
        print("🛡️  STEP 4: DEFENSIVE ANALYSIS".center(80))
        print("="*80)
        
        print(f"\n{home_stats['team_name']} Defense:")
        home_defense = self.get_team_defensive_stats(home_team, last_n_games=10)
        if home_defense:
            print(f"   Points Allowed: {home_defense['avg_points_allowed']:.1f} PPG")
            print(f"   Defensive Rating: {home_defense['defensive_rating']:.1f}")
            print(f"   Point Differential: {home_defense['avg_point_differential']:+.1f}")
        
        print(f"\n{away_stats['team_name']} Defense:")
        away_defense = self.get_team_defensive_stats(away_team, last_n_games=10)
        if away_defense:
            print(f"   Points Allowed: {away_defense['avg_points_allowed']:.1f} PPG")
            print(f"   Defensive Rating: {away_defense['defensive_rating']:.1f}")
            print(f"   Point Differential: {away_defense['avg_point_differential']:+.1f}")
        
        # 5. Player availability analysis
        home_adjustment = 0
        away_adjustment = 0
        
        if key_players_status:
            print("\n" + "="*80)
            print("⭐ STEP 5: PLAYER AVAILABILITY ANALYSIS".center(80))
            print("="*80)
            
            # Analyze home team players
            if 'home' in key_players_status:
                print(f"\n{home_stats['team_name']} Key Players:")
                for player in key_players_status['home']:
                    status_icon = "✅" if player['playing'] else "❌"
                    status_text = "PLAYING" if player['playing'] else "OUT"
                    
                    print(f"  {status_icon} {player['name']}: {status_text}")
                    
                    if not player['playing']:
                        impact_values = {'high': -10, 'medium': -5, 'low': -2}
                        adjustment = impact_values.get(player.get('impact', 'medium'), -5)
                        home_adjustment += adjustment
                        print(f"     Impact: {player.get('impact', 'medium').upper()} "
                              f"(Team strength {adjustment:+d}%)")
            
            # Analyze away team players
            if 'away' in key_players_status:
                print(f"\n{away_stats['team_name']} Key Players:")
                for player in key_players_status['away']:
                    status_icon = "✅" if player['playing'] else "❌"
                    status_text = "PLAYING" if player['playing'] else "OUT"
                    
                    print(f"  {status_icon} {player['name']}: {status_text}")
                    
                    if not player['playing']:
                        impact_values = {'high': -10, 'medium': -5, 'low': -2}
                        adjustment = impact_values.get(player.get('impact', 'medium'), -5)
                        away_adjustment += adjustment
                        print(f"     Impact: {player.get('impact', 'medium').upper()} "
                              f"(Team strength {adjustment:+d}%)")
        
        # 6. Generate advanced prediction
        print("\n" + "="*80)
        print("🎯 STEP 6: ADVANCED PREDICTION CALCULATION".center(80))
        print("="*80)
        
        # Get base prediction with all factors
        prediction = self.predictor.predict_match_outcome(
            home_stats, 
            away_stats,
            home_defensive_stats=home_defense,
            away_defensive_stats=away_defense,
            h2h_stats=h2h_stats,
            home_rest_stats=home_rest,
            away_rest_stats=away_rest
        )
        
        # Apply player availability adjustments
        if home_adjustment != 0 or away_adjustment != 0:
            print(f"\n📝 Adjusting for player availability...")
            print(f"   {home_stats['team_name']}: {home_adjustment:+d}%")
            print(f"   {away_stats['team_name']}: {away_adjustment:+d}%")
            
            home_prob = prediction['home_win_probability'] + home_adjustment
            away_prob = prediction['away_win_probability'] + away_adjustment
            
            total = home_prob + away_prob
            home_prob = (home_prob / total) * 100
            away_prob = (away_prob / total) * 100
            
            prediction['home_win_probability'] = round(home_prob, 2)
            prediction['away_win_probability'] = round(away_prob, 2)
            prediction['favored_team'] = home_stats['team_name'] if home_prob > away_prob else away_stats['team_name']
        
        # 7. Display final prediction
        print("\n" + "="*80)
        print("🏆 FINAL PREDICTION".center(80))
        print("="*80)
        
        print(f"\n{'='*80}")
        print(f"📊 WIN PROBABILITIES:")
        print(f"   {home_stats['team_name']}: {prediction['home_win_probability']:.2f}%")
        print(f"   {away_stats['team_name']}: {prediction['away_win_probability']:.2f}%")
        
        print(f"\n🎯 PREDICTED FINAL SCORE:")
        print(f"   {home_stats['team_name']}: {prediction['predicted_home_score']}")
        print(f"   {away_stats['team_name']}: {prediction['predicted_away_score']}")
        print(f"   Point Spread: {prediction['point_spread']:.1f}")
        
        print(f"\n🏆 PREDICTED WINNER: {prediction['favored_team']}")
        print(f"   Confidence Level: {prediction['confidence']}")
        
        # 8. Key factors summary
        print(f"\n{'='*80}")
        print("🔑 KEY FACTORS CONSIDERED:".center(80))
        print("="*80)
        
        print(f"\n✅ Recent Form (25% weight):")
        print(f"   {home_stats['team_name']}: {home_stats['wins']}-{home_stats['losses']} ({home_stats['win_percentage']:.1f}%)")
        print(f"   {away_stats['team_name']}: {away_stats['wins']}-{away_stats['losses']} ({away_stats['win_percentage']:.1f}%)")
        
        print(f"\n⚔️  Offensive Power (18% weight):")
        print(f"   {home_stats['team_name']}: {home_stats['avg_points_scored']:.1f} PPG")
        print(f"   {away_stats['team_name']}: {away_stats['avg_points_scored']:.1f} PPG")
        
        if home_defense and away_defense:
            print(f"\n🛡️  Defensive Strength (15% weight):")
            print(f"   {home_stats['team_name']}: {home_defense['avg_points_allowed']:.1f} allowed")
            print(f"   {away_stats['team_name']}: {away_defense['avg_points_allowed']:.1f} allowed")
        
        if h2h_stats and h2h_stats.get('games_played', 0) > 0:
            print(f"\n🔄 Head-to-Head (10% weight):")
            print(f"   Last {h2h_stats['games_played']} meetings: {h2h_stats['team1_wins']}-{h2h_stats['team2_wins']}")
            print(f"   Point diff: {h2h_stats['avg_point_diff']:+.1f} (favors {home_team if h2h_stats['avg_point_diff'] > 0 else away_team})")
        
        if home_rest and away_rest:
            print(f"\n😴 Rest Advantage (5% weight):")
            rest_diff = home_rest['fatigue_factor'] - away_rest['fatigue_factor']
            if rest_diff > 3:
                print(f"   ✅ {home_stats['team_name']} has rest advantage ({home_rest['rest_days']} vs {away_rest['rest_days']} days)")
            elif rest_diff < -3:
                print(f"   ✅ {away_stats['team_name']} has rest advantage ({away_rest['rest_days']} vs {home_rest['rest_days']} days)")
            else:
                print(f"   ➖ Similar rest levels ({home_rest['rest_days']} vs {away_rest['rest_days']} days)")
        
        print(f"\n🏠 Home Court Advantage (12% weight):")
        print(f"   ✅ {home_stats['team_name']} playing at home")
        
        if key_players_status:
            print(f"\n⭐ Player Impact (5% weight):")
            if home_adjustment < 0:
                print(f"   ⚠️  {home_stats['team_name']} affected by injuries ({home_adjustment:+d}%)")
            if away_adjustment < 0:
                print(f"   ⚠️  {away_stats['team_name']} affected by injuries ({away_adjustment:+d}%)")
            if home_adjustment == 0 and away_adjustment == 0:
                print(f"   ✅ All key players available")
        
        print("\n" + "="*80)
        print("✨ ANALYSIS COMPLETE ✨".center(80))
        print("="*80)
        
        return {
            'home_team': home_stats,
            'away_team': away_stats,
            'head_to_head': h2h_stats,
            'home_rest': home_rest,
            'away_rest': away_rest,
            'home_defense': home_defense,
            'away_defense': away_defense,
            'prediction': prediction
        }


def main():
    """
    Main function - accepts command line arguments for custom team matchups
    
    Usage:
        python advanced_enhanced_predictor.py "HomeTeam" "AwayTeam"
        
    Examples:
        python advanced_enhanced_predictor.py "Lakers" "Warriors"
        python advanced_enhanced_predictor.py "Bucks" "Celtics"
        python advanced_enhanced_predictor.py "Pacers" "Heat"
    """
    import sys
    
    predictor = SuperPredictor()
    
    # Check if command line arguments are provided
    if len(sys.argv) >= 3:
        # User provided team names via command line
        home_team = sys.argv[1]
        away_team = sys.argv[2]
        
        print("\n" + "="*80)
        print(f"CUSTOM MATCHUP PREDICTION".center(80))
        print("="*80)
        print(f"Analyzing: {away_team} @ {home_team}")
        
        result = predictor.comprehensive_matchup_analysis(
            home_team=home_team,
            away_team=away_team
        )
        
        if result:
            print(f"\n✅ Analysis complete for {away_team} @ {home_team}!")
        else:
            print(f"\n⚠️  Could not complete analysis. Please check team names.")
            print(f"   Examples: Lakers, Warriors, Celtics, Heat, Bucks, Pacers")
    
    else:
        # No arguments provided - run default examples
        print("\n" + "="*80)
        print("ℹ️  NO TEAMS SPECIFIED - RUNNING DEFAULT EXAMPLES".center(80))
        print("="*80)
        print("\nUsage: python advanced_enhanced_predictor.py \"HomeTeam\" \"AwayTeam\"")
        print("Example: python advanced_enhanced_predictor.py \"Lakers\" \"Warriors\"\n")
        
        # Example 1: Basic prediction
        print("\n" + "="*80)
        print("EXAMPLE 1: BASIC ADVANCED PREDICTION".center(80))
        print("="*80)
        
        result = predictor.comprehensive_matchup_analysis(
            home_team="Lakers",
            away_team="Warriors"
        )
        
        # Example 2: Different matchup
        print("\n\n" + "="*80)
        print("EXAMPLE 2: DIFFERENT MATCHUP".center(80))
        print("="*80)
        
        result = predictor.comprehensive_matchup_analysis(
            home_team="Celtics",
            away_team="Heat"
        )
        
        print("\n🎉 Demo Complete!")
        print("\n💡 TIP: Run with team names to analyze any matchup!")
        print("   Example: python advanced_enhanced_predictor.py \"Bucks\" \"Pacers\"")


if __name__ == "__main__":
    main()
