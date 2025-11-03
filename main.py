from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguegamefinder, playergamelog, commonplayerinfo, teamgamelog
from nba_api.stats.static import players, teams
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import numpy as np
from team_fallback_data import get_team_fallback_stats

class NBADataExtractor:
    """Extract and analyze NBA game and player data for predictions"""
    
    def __init__(self):
        self.all_players = players.get_players()
        self.all_teams = teams.get_teams()
        
    def get_todays_games(self):
        """Get all games scheduled for today"""
        print("\n" + "="*60)
        print("FETCHING TODAY'S NBA GAMES")
        print("="*60)
        
        try:
            board = scoreboard.ScoreBoard()
            games_data = board.games.get_dict()
            
            if not games_data:
                print("No games scheduled for today.")
                return []
            
            todays_games = []
            for game in games_data:
                game_info = {
                    'game_id': game['gameId'],
                    'game_status': game['gameStatusText'],
                    'home_team': game['homeTeam']['teamName'],
                    'home_team_city': game['homeTeam']['teamCity'],
                    'home_score': game['homeTeam']['score'],
                    'away_team': game['awayTeam']['teamName'],
                    'away_team_city': game['awayTeam']['teamCity'],
                    'away_score': game['awayTeam']['score'],
                }
                todays_games.append(game_info)
                
                print(f"\n🏀 {game_info['away_team_city']} {game_info['away_team']} ({game_info['away_score']}) "
                      f"vs {game_info['home_team_city']} {game_info['home_team']} ({game_info['home_score']})")
                print(f"   Status: {game_info['game_status']}")
            
            return todays_games
        except Exception as e:
            print(f"Error fetching today's games: {e}")
            return []
    
    def get_player_by_name(self, player_name):
        """Find player by name"""
        player = [p for p in self.all_players if player_name.lower() in p['full_name'].lower()]
        return player[0] if player else None
    
    def get_team_by_name(self, team_name):
        """Find team by name"""
        team = [t for t in self.all_teams if team_name.lower() in t['full_name'].lower() 
                or team_name.lower() in t['nickname'].lower()]
        return team[0] if team else None
    
    def get_player_recent_stats(self, player_name, last_n_games=10):
        """Get player's recent performance stats using REAL current season data"""
        print(f"\n{'='*60}")
        print(f"FETCHING RECENT STATS FOR: {player_name}")
        print("="*60)
        
        player = self.get_player_by_name(player_name)
        if not player:
            print(f"Player '{player_name}' not found.")
            return None
        
        print(f"   📊 Fetching REAL current season data for {player['full_name']}...")
        
        try:
            time.sleep(0.6)  # Rate limiting
            
            # Try current season first
            gamelog = playergamelog.PlayerGameLog(
                player_id=player['id'],
                season='2024-25',
                season_type_all_star='Regular Season'
            )
            df = gamelog.get_data_frames()[0]
            
            if df.empty:
                print(f"   ⚠️  No current season data, trying 2023-24...")
                time.sleep(0.6)
                gamelog = playergamelog.PlayerGameLog(
                    player_id=player['id'],
                    season='2023-24',
                    season_type_all_star='Regular Season'
                )
                df = gamelog.get_data_frames()[0]
                season_used = "2023-24"
            else:
                season_used = "2024-25"
            
            if df.empty:
                print(f"❌ No recent games found for {player['full_name']}")
                return None
            
            # Get most recent games
            df = df.head(last_n_games)
            print(f"   ✅ Found {len(df)} recent games in season {season_used}")
            
        except Exception as e:
            print(f"   ❌ API Error: {str(e)[:80]}")
            return None
        
        # Calculate averages
        try:
            stats = {
                'player_name': player['full_name'],
                'games_played': len(df),
                'avg_points': df['PTS'].mean(),
                'avg_rebounds': df['REB'].mean(),
                'avg_assists': df['AST'].mean(),
                'avg_steals': df['STL'].mean(),
                'avg_blocks': df['BLK'].mean(),
                'avg_fg_pct': df['FG_PCT'].mean() * 100,
                'avg_fg3_pct': df['FG3_PCT'].mean() * 100,
                'avg_ft_pct': df['FT_PCT'].mean() * 100,
                'avg_plus_minus': df['PLUS_MINUS'].mean(),
                'recent_games': df[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST', 'FG_PCT', 'PLUS_MINUS']].to_dict('records')
            }
            
            print(f"\n📊 {stats['player_name']} - Last {stats['games_played']} Games (Season {season_used}):")
            print(f"   Points: {stats['avg_points']:.1f} | Rebounds: {stats['avg_rebounds']:.1f} | Assists: {stats['avg_assists']:.1f}")
            print(f"   FG%: {stats['avg_fg_pct']:.1f}% | 3P%: {stats['avg_fg3_pct']:.1f}% | FT%: {stats['avg_ft_pct']:.1f}%")
            print(f"   +/-: {stats['avg_plus_minus']:+.1f}")
            
            return stats
        except Exception as e:
            print(f"Error processing player stats: {e}")
            return None
    
    def get_team_recent_performance(self, team_name, last_n_games=10):
        """Get team's recent performance using REAL current season data"""
        print(f"\n{'='*60}")
        print(f"FETCHING TEAM PERFORMANCE: {team_name}")
        print("="*60)
        
        team = self.get_team_by_name(team_name)
        if not team:
            print(f"Team '{team_name}' not found.")
            print(f"Available teams include: Lakers, Warriors, Celtics, Heat, Bucks, etc.")
            return None
        
        # Use LeagueGameFinder - this works for current season!
        print(f"   📊 Fetching REAL current season data for {team['full_name']}...")
        
        try:
            time.sleep(0.6)  # Rate limiting
            
            # LeagueGameFinder works for 2024-25 season
            gamefinder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team['id'],
                season_nullable='2024-25',
                season_type_nullable='Regular Season'
            )
            
            games_df = gamefinder.get_data_frames()[0]
            
            if games_df.empty:
                print(f"   ⚠️  No games found for current season, trying last season...")
                time.sleep(0.6)
                gamefinder = leaguegamefinder.LeagueGameFinder(
                    team_id_nullable=team['id'],
                    season_nullable='2023-24',
                    season_type_nullable='Regular Season'
                )
                games_df = gamefinder.get_data_frames()[0]
                season_used = "2023-24"
            else:
                season_used = "2024-25"
            
            if games_df.empty:
                print(f"⚠️  No recent games found for {team['full_name']}")
                print(f"   Using historical/fallback data...")
                return get_team_fallback_stats(team_name)
            
            # Get most recent games
            df = games_df.head(last_n_games)
            print(f"   ✅ Found {len(games_df)} total games in season {season_used}")
            print(f"   📈 Analyzing last {len(df)} games")
            
        except Exception as e:
            print(f"   ❌ API Error: {str(e)[:80]}")
            print(f"   Using fallback data...")
            return get_team_fallback_stats(team_name)
        
        # Process the data
        try:
            wins = df['WL'].value_counts().get('W', 0)
            losses = df['WL'].value_counts().get('L', 0)
            
            stats = {
                'team_name': team['full_name'],
                'games_played': len(df),
                'wins': wins,
                'losses': losses,
                'win_percentage': (wins / len(df)) * 100 if len(df) > 0 else 0,
                'avg_points_scored': df['PTS'].mean(),
                'avg_points_allowed': df['PTS'].mean(),  # Note: would need opponent data for accurate allowed points
                'avg_fg_pct': df['FG_PCT'].mean() * 100,
                'avg_fg3_pct': df['FG3_PCT'].mean() * 100,
                'avg_rebounds': df['REB'].mean(),
                'avg_assists': df['AST'].mean(),
                'recent_games': df[['GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'FG_PCT', 'FG3_PCT', 'PLUS_MINUS']].to_dict('records')
            }
            
            print(f"\n🏆 {stats['team_name']} - Last {stats['games_played']} Games (Season {season_used}):")
            print(f"   Record: {stats['wins']}-{stats['losses']} ({stats['win_percentage']:.1f}% Win Rate)")
            print(f"   Avg Points: {stats['avg_points_scored']:.1f}")
            print(f"   FG%: {stats['avg_fg_pct']:.1f}% | 3P%: {stats['avg_fg3_pct']:.1f}%")
            print(f"   Rebounds: {stats['avg_rebounds']:.1f} | Assists: {stats['avg_assists']:.1f}")
            
            return stats
        except Exception as e:
            print(f"Error processing team stats: {e}")
            return None
    
    def get_head_to_head_history(self, team1_name, team2_name, last_n_games=5):
        """
        Get head-to-head matchup history between two teams
        Returns: wins, losses, avg point differential, recent trends
        """
        print(f"\n{'='*60}")
        print(f"HEAD-TO-HEAD HISTORY: {team1_name} vs {team2_name}")
        print("="*60)
        
        team1 = self.get_team_by_name(team1_name)
        team2 = self.get_team_by_name(team2_name)
        
        if not team1 or not team2:
            print(f"❌ Could not find one or both teams")
            return None
        
        try:
            time.sleep(0.6)
            
            # Get all games for team1 in recent seasons
            gamefinder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team1['id'],
                season_nullable='2024-25',
                season_type_nullable='Regular Season'
            )
            
            games_df = gamefinder.get_data_frames()[0]
            
            if games_df.empty:
                print(f"   ⚠️  No current season data, checking 2023-24...")
                time.sleep(0.6)
                gamefinder = leaguegamefinder.LeagueGameFinder(
                    team_id_nullable=team1['id'],
                    season_nullable='2023-24',
                    season_type_nullable='Regular Season'
                )
                games_df = gamefinder.get_data_frames()[0]
            
            # Filter for games against team2
            team2_abbreviations = [team2['abbreviation']]
            h2h_games = games_df[games_df['MATCHUP'].str.contains(team2['abbreviation'], na=False)]
            
            if h2h_games.empty:
                print(f"   ⚠️  No recent head-to-head games found")
                return {
                    'games_played': 0,
                    'team1_wins': 0,
                    'team2_wins': 0,
                    'avg_point_diff': 0,
                    'recent_games': []
                }
            
            # Get most recent matchups
            h2h_games = h2h_games.head(last_n_games)
            
            # Calculate stats
            team1_wins = len(h2h_games[h2h_games['WL'] == 'W'])
            team2_wins = len(h2h_games[h2h_games['WL'] == 'L'])
            
            # Calculate average point differential (positive = team1 winning by more)
            h2h_games['POINT_DIFF'] = h2h_games['PLUS_MINUS']
            avg_point_diff = h2h_games['POINT_DIFF'].mean()
            
            stats = {
                'games_played': len(h2h_games),
                'team1_wins': team1_wins,
                'team2_wins': team2_wins,
                'team1_win_pct': (team1_wins / len(h2h_games) * 100) if len(h2h_games) > 0 else 0,
                'avg_point_diff': avg_point_diff,
                'recent_games': h2h_games[['GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'PLUS_MINUS']].to_dict('records')
            }
            
            print(f"   📊 Last {len(h2h_games)} meetings:")
            print(f"   {team1['full_name']}: {team1_wins} wins ({stats['team1_win_pct']:.1f}%)")
            print(f"   {team2['full_name']}: {team2_wins} wins")
            print(f"   Avg Point Differential: {avg_point_diff:+.1f} (favors {team1_name if avg_point_diff > 0 else team2_name})")
            
            # Show recent trend
            if len(h2h_games) >= 3:
                recent_3 = h2h_games.head(3)
                recent_wins = len(recent_3[recent_3['WL'] == 'W'])
                if recent_wins >= 2:
                    print(f"   🔥 {team1_name} won {recent_wins} of last 3 meetings!")
                elif recent_wins <= 1:
                    print(f"   🔥 {team2_name} won {3-recent_wins} of last 3 meetings!")
            
            return stats
            
        except Exception as e:
            print(f"   ❌ Error fetching head-to-head data: {str(e)[:80]}")
            return None
    
    def get_rest_days(self, team_name):
        """
        Calculate days of rest since last game
        Returns: number of rest days and fatigue factor
        """
        team = self.get_team_by_name(team_name)
        if not team:
            return None
        
        try:
            time.sleep(0.6)
            
            gamefinder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team['id'],
                season_nullable='2024-25',
                season_type_nullable='Regular Season'
            )
            
            games_df = gamefinder.get_data_frames()[0]
            
            if games_df.empty or len(games_df) < 2:
                return {
                    'rest_days': 3,
                    'is_back_to_back': False,
                    'fatigue_factor': 0,
                    'note': 'Insufficient data'
                }
            
            # Get last 2 games
            games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])
            games_df = games_df.sort_values('GAME_DATE', ascending=False)
            
            last_game = games_df.iloc[0]['GAME_DATE']
            second_last_game = games_df.iloc[1]['GAME_DATE']
            
            # Calculate days between games
            days_since_last = (datetime.now() - last_game).days
            days_between_last_two = (last_game - second_last_game).days
            
            is_back_to_back = days_between_last_two <= 1
            
            # Fatigue factor calculation
            # Back-to-back: -8%, 1 day rest: -3%, 2 days: 0%, 3+ days: +2%
            if days_since_last == 0:
                fatigue_factor = -8  # Playing today, was back-to-back
            elif days_since_last == 1:
                fatigue_factor = -3
            elif days_since_last == 2:
                fatigue_factor = 0
            else:
                fatigue_factor = 2  # Well rested
            
            return {
                'rest_days': days_since_last,
                'is_back_to_back': is_back_to_back,
                'fatigue_factor': fatigue_factor,
                'last_game_date': last_game.strftime('%Y-%m-%d'),
                'days_between_last_two': days_between_last_two
            }
            
        except Exception as e:
            print(f"   ⚠️  Error calculating rest days: {str(e)[:80]}")
            return None
    
    def get_team_defensive_stats(self, team_name, last_n_games=10):
        """
        Get defensive statistics for a team
        Returns: points allowed, opponent FG%, defensive rating
        """
        team = self.get_team_by_name(team_name)
        if not team:
            return None
        
        try:
            time.sleep(0.6)
            
            gamefinder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team['id'],
                season_nullable='2024-25',
                season_type_nullable='Regular Season'
            )
            
            games_df = gamefinder.get_data_frames()[0]
            
            if games_df.empty:
                return None
            
            # Get recent games
            df = games_df.head(last_n_games)
            
            # Calculate defensive stats
            # Note: LeagueGameFinder doesn't directly give opponent stats
            # We approximate by using PLUS_MINUS and own PTS
            avg_points_scored = df['PTS'].mean()
            avg_plus_minus = df['PLUS_MINUS'].mean()
            
            # Approximate opponent points (team PTS - PLUS_MINUS = opponent PTS)
            df['OPP_PTS'] = df['PTS'] - df['PLUS_MINUS']
            avg_points_allowed = df['OPP_PTS'].mean()
            
            # Defensive efficiency (lower is better)
            defensive_rating = avg_points_allowed
            
            defensive_stats = {
                'avg_points_allowed': avg_points_allowed,
                'defensive_rating': defensive_rating,
                'avg_point_differential': avg_plus_minus,
                'games_analyzed': len(df)
            }
            
            return defensive_stats
            
        except Exception as e:
            print(f"   ⚠️  Error calculating defensive stats: {str(e)[:80]}")
            return None
    
    def generate_match_prediction_insights(self, home_team, away_team, key_players=None):
        """Generate insights for match prediction"""
        print(f"\n{'='*60}")
        print(f"MATCH PREDICTION ANALYSIS")
        print(f"{away_team} @ {home_team}")
        print("="*60)
        
        # Get team stats
        home_stats = self.get_team_recent_performance(home_team)
        away_stats = self.get_team_recent_performance(away_team)
        
        if not home_stats or not away_stats:
            print("Unable to generate prediction - missing team data")
            return None
        
        insights = {
            'home_team': home_stats,
            'away_team': away_stats,
            'key_players_stats': []
        }
        
        # Analyze key players if provided
        if key_players:
            print(f"\n{'='*60}")
            print("KEY PLAYERS ANALYSIS")
            print("="*60)
            
            for player_name in key_players:
                player_stats = self.get_player_recent_stats(player_name, last_n_games=5)
                if player_stats:
                    insights['key_players_stats'].append(player_stats)
        
        # Generate prediction insights
        print(f"\n{'='*60}")
        print("PREDICTION INSIGHTS")
        print("="*60)
        
        # Win percentage comparison
        home_win_prob = home_stats['win_percentage']
        away_win_prob = away_stats['win_percentage']
        
        # Home court advantage (typically 3-5%)
        home_advantage = 5
        adjusted_home_prob = home_win_prob + home_advantage
        
        total = adjusted_home_prob + away_win_prob
        normalized_home_prob = (adjusted_home_prob / total) * 100
        normalized_away_prob = (away_win_prob / total) * 100
        
        print(f"\n🎯 WIN PROBABILITY (Based on Recent Form + Home Court):")
        print(f"   {home_stats['team_name']}: {normalized_home_prob:.1f}%")
        print(f"   {away_stats['team_name']}: {normalized_away_prob:.1f}%")
        
        # Offensive comparison
        print(f"\n⚡ OFFENSIVE POWER:")
        print(f"   {home_stats['team_name']}: {home_stats['avg_points_scored']:.1f} PPG")
        print(f"   {away_stats['team_name']}: {away_stats['avg_points_scored']:.1f} PPG")
        
        # Shooting efficiency
        print(f"\n🎯 SHOOTING EFFICIENCY:")
        print(f"   {home_stats['team_name']}: FG {home_stats['avg_fg_pct']:.1f}% | 3P {home_stats['avg_fg3_pct']:.1f}%")
        print(f"   {away_stats['team_name']}: FG {away_stats['avg_fg_pct']:.1f}% | 3P {away_stats['avg_fg3_pct']:.1f}%")
        
        # Key factors
        print(f"\n🔑 KEY FACTORS:")
        if home_stats['wins'] > away_stats['wins']:
            print(f"   ✓ {home_stats['team_name']} has better recent form ({home_stats['wins']}-{home_stats['losses']} vs {away_stats['wins']}-{away_stats['losses']})")
        else:
            print(f"   ✓ {away_stats['team_name']} has better recent form ({away_stats['wins']}-{away_stats['losses']} vs {home_stats['wins']}-{home_stats['losses']})")
        
        if home_stats['avg_fg_pct'] > away_stats['avg_fg_pct']:
            print(f"   ✓ {home_stats['team_name']} shooting more efficiently")
        else:
            print(f"   ✓ {away_stats['team_name']} shooting more efficiently")
        
        print(f"   ✓ Home court advantage favors {home_stats['team_name']}")
        
        insights['prediction'] = {
            'home_win_probability': normalized_home_prob,
            'away_win_probability': normalized_away_prob,
            'favored_team': home_stats['team_name'] if normalized_home_prob > normalized_away_prob else away_stats['team_name']
        }
        
        return insights
    
    def save_analysis_to_file(self, data, filename):
        """Save analysis data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"\n✅ Analysis saved to {filename}")
        except Exception as e:
            print(f"Error saving analysis: {e}")


def main():
    """Main execution function"""
    extractor = NBADataExtractor()
    
    # 1. Get today's games
    todays_games = extractor.get_todays_games()
    
    # 2. Example: Analyze specific players
    print("\n" + "="*60)
    print("EXAMPLE ANALYSIS")
    print("="*60)
    
    # Analyze key players (change these names to current players you want to analyze)
    key_players = ["LeBron James", "Stephen Curry", "Kevin Durant"]
    player_stats = []
    
    for player_name in key_players:
        stats = extractor.get_player_recent_stats(player_name, last_n_games=5)
        if stats:
            player_stats.append(stats)
    
    # 3. Example: Predict a specific matchup
    # Change these team names to teams that will play soon
    prediction = extractor.generate_match_prediction_insights(
        home_team="Lakers",
        away_team="Warriors",
        key_players=["LeBron James", "Stephen Curry"]
    )
    
    # 4. Save analysis
    if prediction:
        extractor.save_analysis_to_file(prediction, 'match_analysis.json')
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()