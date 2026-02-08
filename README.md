# obspy_vibe_coding

ObsPy scripts for seismological data analysis and visualization.

## 🤖 GitHub Copilot 使用指南

想知道如何使用 GitHub Copilot 來改進和擴展這個專案？查看以下文件：

- **[COPILOT_SUGGESTIONS.md](COPILOT_SUGGESTIONS.md)** - 詳細的功能建議和具體的 Copilot 提示詞範例
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - 專案架構說明和開發指南

這些文件包含：
- ✅ 立即可以開始的改進任務
- ✅ 中長期功能擴展建議  
- ✅ 具體的 Copilot Chat 提示詞範例
- ✅ 最佳實踐和學習資源

## Scripts

### plot_earthquake_map.py

Extract earthquake information from the last N days and plot seismicity on a map.

**Features:**
- Fetches earthquake data from USGS/IRIS FDSN services
- Plots global seismicity with magnitude-based marker sizes
- Color-coded depth visualization
- Generates summary statistics
- Demo mode with synthetic data

**Usage:**

```bash
# Fetch real earthquake data from last 7 days (M≥4.0)
python scripts/plot_earthquake_map.py

# Custom parameters
python scripts/plot_earthquake_map.py --days 14 --min-magnitude 5.0 --output my_map.png

# Use demo mode with synthetic data (no internet required)
python scripts/plot_earthquake_map.py --demo

# Use different FDSN client
python scripts/plot_earthquake_map.py --client IRIS
```

**Output:**
- PNG map file showing earthquake locations, magnitudes, and depths
- Console summary with statistics and top earthquakes

### fetch_iris_events_waveforms.py

Fetch recent earthquake events from IRIS and download waveform data.

**Usage:**
```bash
python scripts/fetch_iris_events_waveforms.py --days 5 --min-magnitude 5.0
```

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- obspy
- matplotlib
- numpy

## 📚 Documentation

- **[scripts/README.md](scripts/README.md)** - Detailed script usage documentation
- **[COPILOT_SUGGESTIONS.md](COPILOT_SUGGESTIONS.md)** - GitHub Copilot usage guide (建議和提示詞範例)
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Project structure for AI assistants

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or request features via Issues
- Submit Pull Requests for improvements
- Share your seismology analysis scripts
- Improve documentation

When contributing, consider using GitHub Copilot to help with:
- Writing tests for new features
- Generating documentation
- Code refactoring and optimization
- See [COPILOT_SUGGESTIONS.md](COPILOT_SUGGESTIONS.md) for ideas

## 📄 License

This project is open source. Please check with the repository owner for license details.