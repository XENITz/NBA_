# 🏀 NBA Data Analysis & Match Prediction System

A comprehensive NBA analytics tool that extracts live game data, analyzes player and team performance, and generates match predictions with probability insights.

## 🎯 What Can You Do?

- **📊 Get Today's NBA Games** - See all games scheduled for today
- **👤 Analyze Any Player** - Get recent stats and performance predictions
- **🏆 Predict Match Outcomes** - Win probabilities, expected scores, betting insights
- **📈 Track Team Performance** - Recent form, shooting efficiency, win rates
- **🎲 Fantasy Sports Help** - Player performance predictions and insights

## ⚡ Quick Start

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run interactive mode
python analyze.py

# 3. Try these commands:
> today                              # See today's games
> player LeBron James                # Analyze a player
> matchup Lakers vs Warriors         # Predict a game
```

**📖 [Read the Quick Start Guide](QUICK_START.md)** for step-by-step instructions.

## 📦 Installation

### Virtual Environment Setup
A virtual environment has been created with all dependencies:

```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Or use the convenience script
.\activate_env.ps1
```

### Installed Packages
- **nba-api** - Official NBA data API wrapper
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** & **seaborn** - Data visualization
- **requests** - HTTP requests
- **jupyter** - Interactive notebook environment

## 💻 Usage Examples

### 1. Interactive Mode (Easiest)
```powershell
python analyze.py
```

### 2. Command Line
```powershell
# Show today's games
python analyze.py today

# Analyze a player
python analyze.py player "Stephen Curry"

# Predict a matchup
python analyze.py matchup "Lakers" "Warriors" "LeBron James,Stephen Curry"
```

### 3. Run Example Analysis
```powershell
python main.py
```

### 4. Custom Python Script
```python
from main import NBADataExtractor
from prediction_model import AdvancedPredictor

extractor = NBADataExtractor()
predictor = AdvancedPredictor()

# Get today's games
games = extractor.get_todays_games()

# Analyze a player
stats = extractor.get_player_recent_stats("Kevin Durant")

# Predict a match
home = extractor.get_team_recent_performance("Celtics")
away = extractor.get_team_recent_performance("Bucks")
prediction = predictor.predict_match_outcome(home, away)
```

## 📊 Example Output

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
   Lakers: 115 | Warriors: 110
   Expected Point Spread: 5.0

📊 BETTING/FANTASY INSIGHTS:
  🔥 Expected to be a close game - potential for overtime
  📈 High-scoring game expected - good for Over bets
```

## 📁 Project Files

```
NBA_/
├── venv/                    # Virtual environment
├── main.py                  # Core data extraction & analysis
├── analyze.py               # Interactive CLI tool
├── prediction_model.py      # Advanced prediction algorithms
├── requirements.txt         # Python dependencies
├── activate_env.ps1        # Environment activation helper
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
└── USAGE_GUIDE.md          # Detailed documentation
```

## 🎓 Understanding Predictions

### Win Probability
Our model considers:
- **Recent Form (35%)** - Last 10 games win/loss record
- **Offensive Power (25%)** - Points per game
- **Shooting Efficiency (20%)** - FG% and 3P%
- **Home Court Advantage (15%)** - Home team boost
- **Key Player Impact (5%)** - Star player performance

### Confidence Levels
- **High**: >20% probability difference - clear favorite
- **Medium**: 10-20% difference - likely winner  
- **Low**: <10% difference - toss-up game

### Player Predictions
- 🔥 **GREAT GAME** - Expected 25+ points, high efficiency
- ✅ **GOOD GAME** - Expected 15-25 points, solid performance
- ⚠️ **AVERAGE GAME** - Expected 10-15 points, normal output
- ❌ **POOR GAME** - Expected <10 points, below average

## 🔧 Customization

### Adjust Prediction Weights
Edit `prediction_model.py`:
```python
self.weights = {
    'recent_form': 0.35,
    'offensive_power': 0.25,
    'shooting_efficiency': 0.20,
    'home_court': 0.15,
    'player_impact': 0.05
}
```

### Change Analysis Window
```python
# Analyze last 5 games instead of 10
stats = extractor.get_player_recent_stats("LeBron James", last_n_games=5)
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 3 steps
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive guide with examples
- **main.py** - View source code and examples
- **prediction_model.py** - Understand prediction algorithms

## ⚠️ Important Notes

1. **Player Names**: Use full official names (e.g., "LeBron James" not "LBJ")
2. **Team Names**: Use full names or common nicknames (e.g., "Lakers", "Warriors")
3. **NBA Season**: Works best during NBA season (October - June)
4. **API Limits**: Wait a few seconds between requests if you get errors
5. **Predictions**: Based on statistics - actual results may vary!

## 🚀 Next Steps

1. ✅ Environment is set up
2. ✅ All packages installed
3. ✅ Ready to analyze games!

**Try it now:**
```powershell
.\venv\Scripts\Activate.ps1
python analyze.py today
```

## 📄 License

This project is for educational and personal use. NBA data is property of the NBA.

---

**Built with ❤️ for NBA analytics and predictions**
