# 🏀 NBA Prediction Tool - Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Run Interactive Mode
```powershell
python analyze.py
```

### Step 3: Use Commands
```
> today                              # See today's games
> player LeBron James                # Analyze player
> matchup Lakers vs Warriors         # Predict match
```

## Common Use Cases

### 🎯 Predict Tonight's Games

1. Check what games are on:
   ```powershell
   python analyze.py today
   ```

2. Pick a matchup and analyze it:
   ```powershell
   python analyze.py matchup "Lakers" "Warriors"
   ```

### 👤 Analyze Your Favorite Player

```powershell
python analyze.py player "Giannis Antetokounmpo"
```

This shows:
- Last 10 games averages
- Performance prediction for next game
- Consistency rating
- Expected point range

### 🏆 Full Match Analysis with Key Players

```powershell
python analyze.py matchup "Celtics" "Bucks" "Jayson Tatum,Giannis Antetokounmpo"
```

This provides:
- Win probability for each team
- Predicted final score
- Key player impact
- Betting insights

## Understanding the Output

### Win Probability
- **>60%**: Strong favorite
- **50-60%**: Slight favorite
- **<50%**: Underdog

### Confidence Levels
- **High**: Very confident in prediction
- **Medium**: Moderate confidence
- **Low**: Toss-up game

### Player Performance Predictions
- 🔥 **GREAT GAME**: Expect exceptional performance (25+ points)
- ✅ **GOOD GAME**: Solid performance expected (15-25 points)
- ⚠️ **AVERAGE GAME**: Normal performance (10-15 points)
- ❌ **POOR GAME**: Below average expected (<10 points)

## Tips for Best Results

1. **Use Full Names**: "LeBron James" not "LBJ"
2. **Team Abbreviations Work**: "Lakers", "Warriors", "Celtics"
3. **Check Today's Games First**: See who's actually playing
4. **Multiple Players**: Separate with commas, no spaces after comma
5. **Recent Form Matters**: Predictions based on last 5-10 games

## Example Workflow

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Check today's schedule
python analyze.py today

# 3. Pick an interesting matchup
python analyze.py matchup "Suns" "Lakers" "Kevin Durant,LeBron James"

# 4. Analyze a hot player
python analyze.py player "Luka Doncic"
```

## Troubleshooting

**Problem**: Player not found
- **Solution**: Use full official name: "Kevin Durant" not "KD"

**Problem**: Team not found
- **Solution**: Use full team name or common nickname: "Warriors" or "Golden State"

**Problem**: No games today
- **Solution**: NBA games aren't played every day. Try during NBA season (October-June)

**Problem**: API errors
- **Solution**: Wait a few seconds and try again. API has rate limits.

## What's Next?

- Modify `prediction_model.py` to adjust prediction factors
- Create your own custom analysis in a new Python file
- Export predictions to CSV for tracking accuracy
- Build a database of historical predictions

## Need Help?

- Check `USAGE_GUIDE.md` for detailed documentation
- Review `main.py` for code examples
- Look at `prediction_model.py` to understand algorithms

---

**Ready to predict some games? Let's go! 🚀**
