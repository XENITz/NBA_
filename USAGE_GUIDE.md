# NBA Data Analysis & Match Prediction System

A comprehensive NBA analytics tool that uses the NBA API to extract game data, analyze player performance, and generate match predictions with probability insights.

## 🚀 Features

- **Live Game Data**: Fetch today's NBA games in real-time
- **Player Statistics**: Get detailed recent performance stats for any NBA player
- **Team Analysis**: Analyze team performance trends and statistics
- **Match Predictions**: Generate win probabilities based on multiple factors
- **Player Performance Predictions**: Predict if players will have great/good/average games
- **Betting Insights**: Get insights for fantasy sports and betting decisions

## 📦 Installation & Setup

### 1. Activate Virtual Environment

```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Or use the convenience script
.\activate_env.ps1
```

### 2. Verify Installation

All required packages are already installed:
- `nba-api` - NBA data access
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` & `seaborn` - Visualizations
- `jupyter` - Interactive notebooks

## 💻 Usage Examples

### Method 1: Interactive Mode (Recommended)

Run the interactive analyzer:

```powershell
python analyze.py
```

Then use commands like:
- `today` - Show today's games
- `player LeBron James` - Analyze a specific player
- `matchup Lakers vs Warriors` - Analyze a matchup

### Method 2: Command Line Arguments

**Show today's games:**
```powershell
python analyze.py today
```

**Analyze a specific player:**
```powershell
python analyze.py player "LeBron James"
python analyze.py player "Stephen Curry"
python analyze.py player "Kevin Durant"
```

**Analyze a matchup:**
```powershell
python analyze.py matchup "Lakers" "Warriors" "LeBron James,Stephen Curry"
```

### Method 3: Run Main Script

Run the example analysis in main.py:

```powershell
python main.py
```

This will:
1. Fetch today's games
2. Analyze example players (LeBron, Curry, Durant)
3. Generate a Lakers vs Warriors prediction
4. Save results to `match_analysis.json`

### Method 4: Custom Python Script

```python
from main import NBADataExtractor
from prediction_model import AdvancedPredictor

# Initialize
extractor = NBADataExtractor()
predictor = AdvancedPredictor()

# Get today's games
games = extractor.get_todays_games()

# Analyze a player
player_stats = extractor.get_player_recent_stats("LeBron James", last_n_games=10)

# Analyze a matchup
home_stats = extractor.get_team_recent_performance("Lakers")
away_stats = extractor.get_team_recent_performance("Warriors")
prediction = predictor.predict_match_outcome(home_stats, away_stats)

print(f"Winner: {prediction['favored_team']}")
print(f"Win Probability: {prediction['home_win_probability']}%")
```

## 📊 What You Can Predict

### Team Performance
- Win probability based on recent form
- Expected final scores
- Point spread predictions
- Home court advantage calculations

### Player Performance
- Expected point ranges
- Performance consistency ratings
- Great/Good/Average/Poor game predictions
- Impact on match outcomes

### Betting Insights
- Over/Under predictions for total points
- Close game indicators
- Strong favorite identification
- High/low scoring game predictions

## 🎯 Example Output

```
==================================================================
                  MATCH PREDICTION ANALYSIS
                   Warriors @ Lakers
==================================================================

🏆 PREDICTED WINNER: Lakers
   Confidence Level: Medium

📊 WIN PROBABILITIES:
   Los Angeles Lakers: 57.3%
   Golden State Warriors: 42.7%

🎯 PREDICTED FINAL SCORE:
   Los Angeles Lakers: 115
   Golden State Warriors: 110
   Expected Point Spread: 5.0

==================================================================
                  BETTING/FANTASY INSIGHTS
==================================================================
  🔥 Expected to be a close game - potential for overtime
  📈 High-scoring game expected - good for Over bets
```

## 📁 Project Structure

```
NBA_/
├── venv/                      # Virtual environment
├── main.py                    # Main data extraction script
├── analyze.py                 # Interactive analysis tool
├── prediction_model.py        # Advanced prediction algorithms
├── requirements.txt           # Python dependencies
├── activate_env.ps1          # Environment activation helper
├── match_analysis.json       # Saved analysis results
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── USAGE_GUIDE.md           # Detailed usage guide
```

## 🔧 Customization

### Adjust Prediction Weights

Edit `prediction_model.py` to change factor weights:

```python
self.weights = {
    'recent_form': 0.35,       # Team's recent win/loss record
    'offensive_power': 0.25,    # Points per game
    'shooting_efficiency': 0.20, # Field goal percentages
    'home_court': 0.15,         # Home court advantage
    'player_impact': 0.05       # Key player performance
}
```

### Change Number of Games Analyzed

In your scripts, adjust the `last_n_games` parameter:

```python
# Analyze last 5 games instead of 10
stats = extractor.get_player_recent_stats("LeBron James", last_n_games=5)
```

## 📝 Data Sources

This project uses the official NBA API through the `nba-api` Python package:
- Live game data
- Historical game logs
- Player statistics
- Team statistics
- Current season data

## ⚠️ Important Notes

1. **API Rate Limits**: The NBA API may have rate limits. If you get errors, add delays between requests.

2. **Player/Team Names**: Use full names or common abbreviations:
   - ✅ "LeBron James", "Lakers", "Golden State"
   - ❌ "LBJ", "LA", "GSW" (may not work)

3. **Current Season**: The tool automatically uses the current NBA season data.

4. **Data Accuracy**: Predictions are based on recent performance and statistical models. Actual outcomes may vary!

## 🎓 Understanding Predictions

### Confidence Levels
- **High**: >20% probability difference - clear favorite
- **Medium**: 10-20% difference - likely winner
- **Low**: <10% difference - toss-up game

### Performance Scores
- **70+**: Player expected to have a great game
- **50-70**: Good game expected
- **30-50**: Average performance
- **<30**: Below average expected

## 🤝 Contributing

Feel free to enhance the prediction models or add new features:
- Add more statistical factors
- Implement machine learning models
- Create visualization dashboards
- Add historical data analysis

## 📄 License

This project is for educational and personal use. NBA data is property of the NBA.

---

**Built with ❤️ for NBA analytics and predictions**
