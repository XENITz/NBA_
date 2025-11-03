"""
Enhanced NBA Prediction with Player Lineup Consideration
Checks if key players are playing and adjusts predictions accordingly
"""

from main import NBADataExtractor
from prediction_model import AdvancedPredictor, generate_betting_insights
from nba_api.live.nba.endpoints import scoreboard
import time

class EnhancedPredictor(NBADataExtractor):
    """Enhanced predictor that considers player availability"""
    
    def __init__(self):
        super().__init__()
        self.predictor = AdvancedPredictor()
    
    def get_todays_matchups(self):
        """Get actual matchups happening today with player rosters"""
        print("\n" + "="*70)
        print("TODAY'S NBA GAMES WITH ROSTERS".center(70))
        print("="*70)
        
        try:
            board = scoreboard.ScoreBoard()
            games = board.games.get_dict()
            
            if not games:
                print("\n⚠️  No games scheduled for today.")
                return []
            
            matchups = []
            for game in games:
                matchup = {
                    'game_id': game['gameId'],
                    'status': game['gameStatusText'],
                    'home_team': game['homeTeam']['teamName'],
                    'home_city': game['homeTeam']['teamCity'],
                    'away_team': game['awayTeam']['teamName'],
                    'away_city': game['awayTeam']['teamCity'],
                }
                
                matchups.append(matchup)
                
                print(f"\n🏀 {matchup['away_city']} {matchup['away_team']} @ "
                      f"{matchup['home_city']} {matchup['home_team']}")
                print(f"   Status: {matchup['status']}")
            
            return matchups
            
        except Exception as e:
            print(f"❌ Error fetching today's games: {e}")
            return []
    
    def analyze_with_injuries(self, home_team, away_team, key_players_status=None):
        """
        Analyze matchup considering player injuries/availability
        
        key_players_status format:
        {
            'home': [
                {'name': 'Player Name', 'playing': True/False, 'impact': 'high'/'medium'/'low'}
            ],
            'away': [...]
        }
        """
        print("\n" + "="*70)
        print(f"ENHANCED MATCH ANALYSIS: {away_team} @ {home_team}".center(70))
        print("="*70)
        
        # Get team stats
        home_stats = self.get_team_recent_performance(home_team, last_n_games=10)
        away_stats = self.get_team_recent_performance(away_team, last_n_games=10)
        
        if not home_stats or not away_stats:
            print("❌ Unable to fetch team data.")
            return None
        
        # Check player status if provided
        home_adjustment = 0
        away_adjustment = 0
        
        if key_players_status:
            print(f"\n{'='*70}")
            print("PLAYER AVAILABILITY ANALYSIS".center(70))
            print("="*70)
            
            # Analyze home team players
            if 'home' in key_players_status:
                print(f"\n{home_stats['team_name']} Key Players:")
                for player in key_players_status['home']:
                    status_icon = "✅" if player['playing'] else "❌"
                    status_text = "PLAYING" if player['playing'] else "OUT"
                    
                    print(f"  {status_icon} {player['name']}: {status_text}")
                    
                    if not player['playing']:
                        # Reduce team strength if star player is out
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
        
        # Get base prediction
        prediction = self.predictor.predict_match_outcome(home_stats, away_stats)
        
        # Adjust for player availability
        if home_adjustment != 0 or away_adjustment != 0:
            print(f"\n{'='*70}")
            print("ADJUSTING FOR PLAYER AVAILABILITY".center(70))
            print("="*70)
            
            print(f"\nTeam Strength Adjustments:")
            print(f"  {home_stats['team_name']}: {home_adjustment:+d}%")
            print(f"  {away_stats['team_name']}: {away_adjustment:+d}%")
            
            # Recalculate probabilities with adjustments
            home_prob = prediction['home_win_probability'] + home_adjustment
            away_prob = prediction['away_win_probability'] + away_adjustment
            
            # Normalize
            total = home_prob + away_prob
            home_prob = (home_prob / total) * 100
            away_prob = (away_prob / total) * 100
            
            prediction['home_win_probability'] = round(home_prob, 2)
            prediction['away_win_probability'] = round(away_prob, 2)
            prediction['favored_team'] = home_stats['team_name'] if home_prob > away_prob else away_stats['team_name']
            
            # Adjust predicted scores
            if home_adjustment < 0:
                prediction['predicted_home_score'] += home_adjustment // 2
            if away_adjustment < 0:
                prediction['predicted_away_score'] += away_adjustment // 2
            
            prediction['point_spread'] = abs(prediction['predicted_home_score'] - prediction['predicted_away_score'])
            
            print(f"\n✨ ADJUSTED PREDICTION:")
        else:
            print(f"\n{'='*70}")
            print("FINAL PREDICTION".center(70))
            print("="*70)
        
        # Display prediction
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
        
        return prediction


def main_example():
    """Example usage of enhanced predictor"""
    predictor = EnhancedPredictor()
    
    # Show today's games
    predictor.get_todays_matchups()
    
    # Example: Predict Lakers vs Warriors with player status
    print("\n" + "="*70)
    print("EXAMPLE: Lakers vs Warriors with Player Availability")
    print("="*70)
    
    player_status = {
        'home': [  # Lakers
            {'name': 'LeBron James', 'playing': True, 'impact': 'high'},
            {'name': 'Anthony Davis', 'playing': True, 'impact': 'high'},
        ],
        'away': [  # Warriors
            {'name': 'Stephen Curry', 'playing': True, 'impact': 'high'},
            {'name': 'Klay Thompson', 'playing': False, 'impact': 'medium'},  # Example injury
        ]
    }
    
    predictor.analyze_with_injuries('Lakers', 'Warriors', player_status)


if __name__ == "__main__":
    main_example()
