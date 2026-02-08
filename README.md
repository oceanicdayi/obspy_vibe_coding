# obspy_vibe_coding

ObsPy scripts for seismological data analysis and visualization.

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