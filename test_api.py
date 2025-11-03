"""Test script to check what NBA data is actually available"""

from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.endpoints import teamgamelog, leaguegamefinder
from nba_api.stats.static import teams
import time

print("="*60)
print("NBA API DATA AVAILABILITY TEST")
print("="*60)

# Test 1: Today's games
print("\n1. Testing Live Scoreboard API...")
try:
    board = scoreboard.ScoreBoard()
    games = board.games.get_dict()
    print(f"✅ Found {len(games)} games today")
    
    if games:
        print("\nToday's games:")
        for g in games[:3]:
            away = g['awayTeam']['teamTricode']
            home = g['homeTeam']['teamTricode']
            status = g['gameStatusText']
            print(f"  {away} @ {home} - {status}")
            
            # Try to get boxscore for recent game data
            try:
                game_id = g['gameId']
                time.sleep(1)
                box = boxscore.BoxScore(game_id=game_id)
                print(f"  ✅ Boxscore available for {game_id}")
                
                # Check if we can get team stats
                if hasattr(box, 'home_team_stats'):
                    print(f"  ✅ Team stats available")
                break
            except Exception as e:
                print(f"  ⚠️ Boxscore not available: {str(e)[:50]}")
except Exception as e:
    print(f"❌ Live API failed: {e}")

# Test 2: Recent team games using LeagueGameFinder
print("\n2. Testing LeagueGameFinder for recent games...")
try:
    lakers = [t for t in teams.get_teams() if 'Lakers' in t['full_name']][0]
    
    time.sleep(1)
    gamefinder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=lakers['id'],
        season_nullable='2024-25',
        season_type_nullable='Regular Season'
    )
    games_df = gamefinder.get_data_frames()[0]
    print(f"✅ Found {len(games_df)} Lakers games in 2024-25")
    
    if len(games_df) > 0:
        print("\nRecent games:")
        for idx, game in games_df.head(3).iterrows():
            print(f"  {game['GAME_DATE']}: {game['MATCHUP']} - {game['WL']}")
            
except Exception as e:
    print(f"❌ LeagueGameFinder failed: {str(e)[:100]}")

# Test 3: Try different season formats
print("\n3. Testing different season formats...")
seasons_to_try = ['2024-25', '2023-24', '2024']

lakers = [t for t in teams.get_teams() if 'Lakers' in t['full_name']][0]

for season in seasons_to_try:
    try:
        time.sleep(1)
        gamelog = teamgamelog.TeamGameLog(
            team_id=lakers['id'],
            season=season,
            season_type_all_star='Regular Season'
        )
        df = gamelog.get_data_frames()[0]
        print(f"  Season '{season}': {len(df)} games found")
        
        if len(df) > 0:
            latest = df.iloc[0]
            print(f"    Latest game: {latest['GAME_DATE']} - {latest['MATCHUP']}")
    except Exception as e:
        print(f"  Season '{season}': Error - {str(e)[:60]}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
