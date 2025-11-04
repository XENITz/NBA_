# 📁 Project Organization Guide

## ✅ **Workspace Now Organized!**

Your NBA Prediction System has been restructured for better organization and maintainability.

---

## 📂 **Folder Structure**

### **`src/` - Source Code**
All Python modules live here:

- **`main.py`** - Core NBA data extraction
  - Fetches team and player stats
  - Handles API calls to NBA
  - Contains 3 new methods: head-to-head, rest days, defensive stats

- **`prediction_model.py`** - Prediction algorithms
  - 8-factor prediction model
  - Weight calculations
  - Confidence levels

- **`team_fallback_data.py`** - Backup data
  - Historical team averages
  - Used when API fails

- **`advanced_enhanced_predictor.py`** - Main predictor
  - Uses ALL features
  - Command-line interface
  - Complete analysis pipeline

- **`enhanced_predictor.py`** - Player availability predictor
  - Focuses on injury impact
  - Simpler than advanced version

- **`analyze.py`** - Quick analysis tool
  - CLI for fast predictions
  - Player and team analysis

---

### **`docs/` - Documentation**
All guides and documentation:

- **GETTING_STARTED.md** - Setup instructions
- **NEW_FEATURES_GUIDE.md** - Feature documentation
- **QUICK_START.md** - Quick reference
- **REAL_DATA_GUIDE.md** - Data sources info
- **USAGE_GUIDE.md** - Usage examples
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **PROJECT_SUMMARY.md** - Project overview
- **SYSTEM_READY.md** - System status

---

### **`tests/` - Test Files**
Testing scripts:

- **`test_api.py`** - API connectivity tests
- **`test_setup.py`** - Environment verification

---

### **`scripts/` - Utility Scripts**
Helper scripts:

- **`activate_env.ps1`** - Activate virtual environment (PowerShell)

---

### **`data/` - Data Storage**
Empty folder for:
- Generated reports
- Saved predictions
- Exported data
- Cache files (future use)

---

### **Root Directory**
Main access files:

- **`predict.py`** - 🎯 **Main entry point** for predictions
- **`quick_analyze.py`** - ⚡ Quick analysis interface
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Project overview
- **`.gitignore`** - Git ignore rules
- **`venv/`** - Virtual environment (unchanged)
- **`__pycache__/`** - Python cache (auto-generated)

---

## 🚀 **How to Use After Organization**

### **Option 1: Main Predictor (Recommended)**

```powershell
# Activate environment
.\venv\Scripts\Activate

# Run prediction with any two teams
python predict.py "Lakers" "Warriors"
python predict.py "Celtics" "Heat"
```

### **Option 2: Direct Module Access**

```powershell
# If you need to run modules directly
cd src
python -m advanced_enhanced_predictor "Lakers" "Warriors"
```

### **Option 3: Python Import**

```python
# In your own scripts
from src.main import NBADataExtractor
from src.prediction_model import AdvancedPredictor

extractor = NBADataExtractor()
predictor = AdvancedPredictor()
```

---

## 🔄 **What Changed?**

### **Before:**
```
NBA_/
├── main.py
├── prediction_model.py
├── advanced_enhanced_predictor.py
├── enhanced_predictor.py
├── analyze.py
├── team_fallback_data.py
├── test_api.py
├── test_setup.py
├── GETTING_STARTED.md
├── NEW_FEATURES_GUIDE.md
├── [8 more .md files]
└── ...
```
**Problem:** 20+ files in root directory - messy!

### **After:**
```
NBA_/
├── src/                    # All code here
├── docs/                   # All docs here
├── tests/                  # All tests here
├── scripts/                # Utilities here
├── data/                   # Future data storage
├── predict.py              # Main entry point
├── quick_analyze.py        # Quick tool
└── README.md               # Overview
```
**Solution:** Clean, organized, professional structure!

---

## ✅ **Benefits of New Structure**

### **1. Cleaner Root Directory**
- Only 5 important files visible
- Easy to find what you need
- Professional appearance

### **2. Logical Organization**
- Source code in `src/`
- Documentation in `docs/`
- Tests in `tests/`
- Clear separation of concerns

### **3. Better Imports**
- Package structure with `__init__.py`
- Can import: `from src.main import NBADataExtractor`
- More maintainable

### **4. Easier to Navigate**
- Know where to look for code vs docs
- Easier for collaboration
- Standard Python project structure

### **5. Scalability**
- Easy to add new modules
- Clear place for everything
- Ready for future growth

---

## 📝 **Import Path Updates**

All imports have been updated to work with the new structure:

**Old:**
```python
from main import NBADataExtractor
from prediction_model import AdvancedPredictor
```

**New:**
```python
from .main import NBADataExtractor
from .prediction_model import AdvancedPredictor
```

The wrapper scripts (`predict.py`, `quick_analyze.py`) handle the path automatically!

---

## 🎯 **Quick Reference**

### **To Run Predictions:**
```powershell
python predict.py "Team1" "Team2"
```

### **To Read Documentation:**
```powershell
# Open any file in docs/
code docs/NEW_FEATURES_GUIDE.md
code docs/QUICK_START.md
```

### **To Run Tests:**
```powershell
python tests/test_api.py
python tests/test_setup.py
```

### **To View Source Code:**
```powershell
# Open any module
code src/main.py
code src/advanced_enhanced_predictor.py
```

---

## 💡 **Tips**

1. **Always activate the virtual environment first:**
   ```powershell
   .\venv\Scripts\Activate
   ```

2. **Use `predict.py` for normal predictions** - it's the easiest way

3. **Check `docs/` for detailed guides** - everything is documented

4. **The `src/` folder is a Python package** - you can import from it

5. **Keep `data/` for any output files** you generate

---

## 🔧 **Future Enhancements**

With this structure, it's easy to add:

- **`src/models/`** - Machine learning models
- **`src/utils/`** - Utility functions
- **`src/api/`** - API wrappers
- **`config/`** - Configuration files
- **`logs/`** - Log files
- **`output/`** - Generated reports

---

## ✨ **Summary**

Your workspace is now:
- ✅ **Organized** - Everything has a place
- ✅ **Professional** - Standard Python structure
- ✅ **Maintainable** - Easy to find and update code
- ✅ **Scalable** - Ready to grow
- ✅ **Clean** - No clutter in root directory

**Everything still works the same, just better organized!** 🎉
