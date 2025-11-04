"""
Advanced NBA Match Prediction Model
Analyzes multiple factors to predict match outcomes and player performance
"""

import json
from datetime import datetime

class AdvancedPredictor:
    """Enhanced prediction model with multiple factors"""
    
    def __init__(self):
        self.weights = {
            'recent_form': 0.25,           # Team's recent win/loss record
            'offensive_power': 0.18,        # Points per game
            'shooting_efficiency': 0.15,    # Field goal percentages
            'defensive_strength': 0.15,     # Points allowed / defensive rating
            'home_court': 0.12,             # Home court advantage
            'head_to_head': 0.10,           # Historical matchup performance
            'rest_advantage': 0.05,         # Fatigue / back-to-back factor
            'player_impact': 0.05           # Key player performance
        }
    
    def calculate_team_score(self, team_stats, defensive_stats=None, h2h_stats=None, rest_stats=None):
        """Calculate overall team score based on multiple factors"""
        score = 0
        
        # Recent form score (0-100)
        form_score = team_stats.get('win_percentage', 50)
        score += form_score * self.weights['recent_form']
        
        # Offensive power (normalized to 0-100, assuming 90-120 PPG range)
        ppg = team_stats.get('avg_points_scored', 105)
        offensive_score = min(100, max(0, (ppg - 90) / 30 * 100))
        score += offensive_score * self.weights['offensive_power']
        
        # Shooting efficiency (already in percentage)
        fg_pct = team_stats.get('avg_fg_pct', 45)
        fg3_pct = team_stats.get('avg_fg3_pct', 35)
        shooting_score = (fg_pct + fg3_pct) / 2
        score += shooting_score * self.weights['shooting_efficiency']
        
        # Defensive strength (inverse - lower points allowed is better)
        if defensive_stats:
            points_allowed = defensive_stats.get('avg_points_allowed', 110)
            # Normalize: 95-115 range, inverted (95 = best = 100 points, 115 = worst = 0 points)
            defensive_score = min(100, max(0, (115 - points_allowed) / 20 * 100))
            score += defensive_score * self.weights['defensive_strength']
        else:
            # Default defensive contribution
            score += 50 * self.weights['defensive_strength']
        
        # Head-to-head advantage
        if h2h_stats and h2h_stats.get('games_played', 0) > 0:
            h2h_score = h2h_stats.get('team1_win_pct', 50)
            score += h2h_score * self.weights['head_to_head']
        else:
            # Neutral if no H2H data
            score += 50 * self.weights['head_to_head']
        
        # Rest advantage
        if rest_stats:
            fatigue_factor = rest_stats.get('fatigue_factor', 0)
            # Convert fatigue to 0-100 scale (centered at 50)
            # -8 to +2 range -> 0 to 100 scale
            rest_score = 50 + (fatigue_factor * 5)
            score += rest_score * self.weights['rest_advantage']
        else:
            # Neutral rest
            score += 50 * self.weights['rest_advantage']
        
        return score
    
    def predict_match_outcome(self, home_team_stats, away_team_stats, key_players_stats=None, 
                            home_defensive_stats=None, away_defensive_stats=None,
                            h2h_stats=None, home_rest_stats=None, away_rest_stats=None):
        """Predict match outcome with confidence levels and advanced factors"""
        
        # Calculate base scores with new factors
        home_score = self.calculate_team_score(
            home_team_stats, 
            defensive_stats=home_defensive_stats,
            h2h_stats=h2h_stats,
            rest_stats=home_rest_stats
        )
        
        # For away team, invert H2H stats
        away_h2h_stats = None
        if h2h_stats and h2h_stats.get('games_played', 0) > 0:
            away_h2h_stats = {
                'games_played': h2h_stats['games_played'],
                'team1_win_pct': 100 - h2h_stats.get('team1_win_pct', 50)
            }
        
        away_score = self.calculate_team_score(
            away_team_stats,
            defensive_stats=away_defensive_stats,
            h2h_stats=away_h2h_stats,
            rest_stats=away_rest_stats
        )
        
        # Add home court advantage
        home_court_bonus = 7.5  # Points for home court advantage
        home_score += home_court_bonus * self.weights['home_court'] * 100
        
        # Adjust for key players if provided
        if key_players_stats:
            home_adjustment, away_adjustment = self._analyze_key_players(
                key_players_stats, 
                home_team_stats['team_name'],
                away_team_stats['team_name']
            )
            home_score += home_adjustment
            away_score += away_adjustment
        
        # Normalize to probabilities
        total_score = home_score + away_score
        home_win_prob = (home_score / total_score) * 100
        away_win_prob = (away_score / total_score) * 100
        
        # Determine confidence level
        prob_diff = abs(home_win_prob - away_win_prob)
        if prob_diff > 20:
            confidence = "High"
        elif prob_diff > 10:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Predicted score range
        home_predicted_score = self._predict_score(home_team_stats, home_win_prob)
        away_predicted_score = self._predict_score(away_team_stats, away_win_prob)
        
        return {
            'home_win_probability': round(home_win_prob, 2),
            'away_win_probability': round(away_win_prob, 2),
            'confidence': confidence,
            'favored_team': home_team_stats['team_name'] if home_win_prob > away_win_prob else away_team_stats['team_name'],
            'predicted_home_score': home_predicted_score,
            'predicted_away_score': away_predicted_score,
            'point_spread': abs(home_predicted_score - away_predicted_score)
        }
    
    def _analyze_key_players(self, players_stats, home_team, away_team):
        """Analyze impact of key players on the match"""
        home_adjustment = 0
        away_adjustment = 0
        
        for player_stat in players_stats:
            # Determine which team the player is on (simplified)
            # In a real implementation, you'd check actual team rosters
            player_impact = self._calculate_player_impact(player_stat)
            
            # This is a simplified version - you'd need to properly match players to teams
            # For now, we'll just add minimal impact
            home_adjustment += player_impact * 0.5
            away_adjustment += player_impact * 0.5
        
        return home_adjustment, away_adjustment
    
    def _calculate_player_impact(self, player_stats):
        """Calculate individual player's impact score"""
        if not player_stats:
            return 0
        
        # Weight different stats
        points_weight = 0.4
        efficiency_weight = 0.3
        all_around_weight = 0.3
        
        # Normalize stats
        points_score = min(100, (player_stats.get('avg_points', 0) / 35) * 100)
        efficiency_score = player_stats.get('avg_fg_pct', 45)
        all_around_score = (
            (player_stats.get('avg_rebounds', 0) / 12) * 30 +
            (player_stats.get('avg_assists', 0) / 10) * 30 +
            (player_stats.get('avg_steals', 0) / 2) * 20 +
            (player_stats.get('avg_blocks', 0) / 2) * 20
        )
        
        impact = (
            points_score * points_weight +
            efficiency_score * efficiency_weight +
            all_around_score * all_around_weight
        )
        
        return impact * self.weights['player_impact']
    
    def _predict_score(self, team_stats, win_probability):
        """Predict likely score for a team"""
        base_score = team_stats.get('avg_points_scored', 105)
        
        # Adjust based on win probability
        if win_probability > 60:
            adjustment = 3
        elif win_probability > 50:
            adjustment = 0
        else:
            adjustment = -3
        
        return round(base_score + adjustment)
    
    def predict_player_performance(self, player_stats):
        """Predict if a player will have a good/great/poor game"""
        if not player_stats:
            return None
        
        avg_points = player_stats.get('avg_points', 0)
        avg_fg_pct = player_stats.get('avg_fg_pct', 0)
        avg_plus_minus = player_stats.get('avg_plus_minus', 0)
        
        # Calculate consistency score from recent games
        recent_games = player_stats.get('recent_games', [])
        if recent_games and len(recent_games) > 2:
            recent_points = [game.get('PTS', 0) for game in recent_games[:5]]
            consistency = 100 - (max(recent_points) - min(recent_points)) / max(recent_points) * 100 if max(recent_points) > 0 else 0
        else:
            consistency = 50
        
        # Performance prediction
        performance_score = (
            (avg_points / 30 * 40) +  # Points component
            (avg_fg_pct) +             # Efficiency component
            (consistency * 0.20) +     # Consistency component
            ((avg_plus_minus + 10) / 20 * 20)  # Plus/minus component (normalized)
        )
        
        if performance_score > 70:
            prediction = "🔥 GREAT GAME Expected"
            confidence = "High"
        elif performance_score > 50:
            prediction = "✅ GOOD GAME Expected"
            confidence = "Medium"
        elif performance_score > 30:
            prediction = "⚠️ AVERAGE GAME Expected"
            confidence = "Medium"
        else:
            prediction = "❌ POOR GAME Expected"
            confidence = "Low"
        
        return {
            'player': player_stats.get('player_name'),
            'prediction': prediction,
            'confidence': confidence,
            'performance_score': round(performance_score, 2),
            'expected_points_range': f"{max(0, avg_points-5):.0f}-{avg_points+5:.0f}",
            'consistency_rating': f"{consistency:.0f}%"
        }


def generate_betting_insights(prediction_data):
    """Generate insights for betting/fantasy purposes"""
    insights = []
    
    prob_diff = abs(prediction_data['home_win_probability'] - prediction_data['away_win_probability'])
    
    if prob_diff > 20:
        insights.append(f"⭐ Strong favorite: {prediction_data['favored_team']} ({prediction_data[prediction_data['favored_team'].lower().replace(' ', '_') + '_win_probability'] if 'home' in prediction_data else prediction_data['home_win_probability']}% win probability)")
    
    if prediction_data['point_spread'] < 5:
        insights.append("🔥 Expected to be a close game - potential for overtime")
    
    if prediction_data['predicted_home_score'] + prediction_data['predicted_away_score'] > 220:
        insights.append("📈 High-scoring game expected - good for Over bets")
    elif prediction_data['predicted_home_score'] + prediction_data['predicted_away_score'] < 200:
        insights.append("📉 Low-scoring game expected - defensive battle")
    
    return insights


if __name__ == "__main__":
    # Example usage
    predictor = AdvancedPredictor()
    
    # Example team stats (you would get these from main.py)
    home_stats = {
        'team_name': 'Lakers',
        'win_percentage': 60,
        'avg_points_scored': 112,
        'avg_fg_pct': 47.5,
        'avg_fg3_pct': 36.8
    }
    
    away_stats = {
        'team_name': 'Warriors',
        'win_percentage': 55,
        'avg_points_scored': 115,
        'avg_fg_pct': 46.2,
        'avg_fg3_pct': 38.5
    }
    
    prediction = predictor.predict_match_outcome(home_stats, away_stats)
    
    print("="*60)
    print("MATCH PREDICTION")
    print("="*60)
    print(f"Favored Team: {prediction['favored_team']}")
    print(f"Win Probability: {prediction['home_win_probability']}% vs {prediction['away_win_probability']}%")
    print(f"Confidence: {prediction['confidence']}")
    print(f"Predicted Score: {prediction['predicted_home_score']} - {prediction['predicted_away_score']}")
    print(f"Point Spread: {prediction['point_spread']:.1f}")
    
    insights = generate_betting_insights(prediction)
    print("\n📊 BETTING INSIGHTS:")
    for insight in insights:
        print(f"  {insight}")
