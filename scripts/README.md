# fetch_iris_events_waveforms.py

簡短使用說明：

- 安裝依賴：
```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```
- 執行：
```bash
python scripts/fetch_iris_events_waveforms.py
```

常用選項：
- `--days N` : 查詢最近 N 天（預設 5）
- `--min-magnitude M` : 最小震級（預設 5.0）
- `--tw-only` : 只下載台灣 bounding box 內的觀測站波形
- `--before` / `--after` : 下載波形相對 origin 的時間範圍（秒）
- `--out` : 輸出資料夾（預設 `data/`）
 - `--first-only` : 只自動選擇並下載找到的第一個事件的波形（非互動）
 - `--max-files N` : 全部事件合計最多下載 N 個波形檔案（預設 0 = 不限制）

範例：只下載第一個事件且最多 5 個波形檔案
```bash
python scripts/fetch_iris_events_waveforms.py --days 5 --min-magnitude 5 --first-only --max-files 5 --out data_run --before 60 --after 120
```

只列出事件（不下載波形）：
```bash
python scripts/fetch_iris_events_waveforms.py --days 5 --min-magnitude 5 --no-waveforms
```

---

# plot_earthquake_map.py

Extract earthquake information and create seismicity maps.

## Quick Start

```bash
# Demo mode with synthetic data (no internet required)
python scripts/plot_earthquake_map.py --demo

# Fetch real earthquake data from last 7 days
python scripts/plot_earthquake_map.py
```

## Features

- Fetches earthquake data from USGS/IRIS FDSN services
- Creates global seismicity map with:
  - **Marker size** = Magnitude (larger = stronger)
  - **Marker color** = Depth (yellow = shallow, red = deep)
- Prints summary statistics and top earthquakes
- Demo mode with realistic synthetic data

## Command-Line Options

- `--days N` : Number of days to look back (default: 7)
- `--min-magnitude M` : Minimum magnitude (default: 4.0)
- `--output FILE` : Output PNG filename (default: earthquake_map.png)
- `--client NAME` : FDSN client - USGS or IRIS (default: USGS)
- `--demo` : Use synthetic demo data (no internet needed)

## Examples

```bash
# Last 14 days, magnitude 5.0+
python scripts/plot_earthquake_map.py --days 14 --min-magnitude 5.0

# Use IRIS data service and custom output
python scripts/plot_earthquake_map.py --client IRIS --output my_map.png

# Demo mode (synthetic data for testing)
python scripts/plot_earthquake_map.py --demo
```

## Troubleshooting

If you see network errors:
1. Try `--demo` mode to test without internet
2. Try `--client IRIS` instead of USGS
3. Check internet connection
