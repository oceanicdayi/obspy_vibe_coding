# Copilot 指示（為此倉庫量身定制）

本檔案為協助 AI 編程 agent 能夠快速在此專案中開始工作的指引。

## 專案概述

這是一個 **Python 地震學資料分析專案**，使用 ObsPy 套件進行地震事件查詢、波形資料下載和地震活動性視覺化。

### 專案結構

```
obspy_vibe_coding/
├── scripts/
│   ├── plot_earthquake_map.py          # 地震活動性地圖繪製
│   ├── fetch_iris_events_waveforms.py  # IRIS 地震事件與波形下載
│   └── README.md                        # 腳本使用說明
├── requirements.txt                     # Python 依賴套件
├── README.md                            # 專案主要文件
└── .github/
    └── copilot-instructions.md         # 本檔案
```

### 核心依賴

- **obspy**: 地震學資料處理主要套件
- **matplotlib**: 資料視覺化
- **numpy**: 數值計算

### 環境設定

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
```

## GitHub Copilot 可以如何協助這個專案

### 1. 程式碼開發與增強

**新增分析功能**
- 使用 Copilot Chat 詢問：「如何新增地震 b-value 分析功能？」
- 讓 Copilot 幫助實作 Gutenberg-Richter 關係計算
- 新增震源機制解 (focal mechanism) 視覺化功能

**改善現有腳本**
- 在程式碼中加入註解請 Copilot 優化效能
- 使用 `/doc` 指令為函數生成完整的 docstring
- 請 Copilot 將重複的程式碼重構為可重用的函數

**範例提示詞**
```
# 在編輯器中選取函數後
/doc  # 自動生成 NumPy 風格的文件字串

# 在 Copilot Chat 中
請幫我優化 extract_earthquake_info 函數的效能
如何為 plot_seismicity_map 新增互動式地圖選項？
```

### 2. 測試框架建置

**使用 Copilot 建立測試**
```python
# 在新檔案 tests/test_earthquake_map.py 中，輸入：
# def test_fetch_earthquakes
# Copilot 會自動補全測試函數

# 或在 Chat 中詢問：
請為 plot_earthquake_map.py 中的所有函數建立 pytest 測試案例
如何模擬 FDSN Client 以避免在測試時真實下載資料？
```

**建議的測試結構**
```
tests/
├── __init__.py
├── test_plot_earthquake_map.py
├── test_fetch_waveforms.py
└── fixtures/
    └── sample_catalog.xml  # 測試用的範例資料
```

### 3. 資料處理與分析腳本

**新增實用工具**
- 地震目錄格式轉換（QuakeML, CSV, JSON）
- 波形資料前處理（去趨勢、濾波、重採樣）
- 震相自動辨識（P-wave, S-wave picking）

**Copilot 協助範例**
```python
# 開始輸入：
def convert_catalog_to_csv(catalog, output_file):
    """Convert ObsPy catalog to CSV format"""
    # Copilot 會自動建議完整實作

# 或使用 Chat
請幫我寫一個函數，將 ObsPy Catalog 轉換為 pandas DataFrame
如何實作自動震相辨識演算法？
```

### 4. 文件與註解

**改善文件品質**
- 使用 `/doc` 為每個函數生成詳細文件
- 讓 Copilot 撰寫 Jupyter notebook 教學範例
- 生成 API 參考文件

**範例工作流程**
1. 選取函數 → 輸入 `/doc` → Copilot 生成文件
2. 在 Chat 中：「請為這個專案寫一個入門教學 notebook」
3. 讓 Copilot 將複雜的演算法加上逐行註解

### 5. 錯誤處理與除錯

**使用 Copilot 改善錯誤處理**
```python
# 選取有可能失敗的程式碼區塊，在 Chat 中詢問：
請為這段程式碼新增完整的錯誤處理和使用者友善的錯誤訊息
如何處理網路連線逾時的情況？
```

**除錯協助**
- 貼上錯誤訊息到 Chat，詢問原因和解決方案
- 使用 `/fix` 指令讓 Copilot 自動修復常見問題
- 詢問最佳實踐：「ObsPy 中處理缺失資料的最佳方式是什麼？」

### 6. 效能優化

**詢問優化建議**
```
這個函數處理大型 catalog 時很慢，如何優化？
如何使用 numpy vectorization 加速計算？
是否應該使用平行處理來下載多個波形檔案？
```

### 7. 程式碼品質與風格

**使用 Copilot 改善程式碼品質**
- 請 Copilot 重構為更 Pythonic 的寫法
- 檢查是否符合 PEP 8 風格指南
- 新增型別提示 (type hints)

**範例**
```python
# 在 Chat 中
請將這段程式碼改寫為使用 pathlib 而不是 os.path
為所有函數新增 type hints
這段程式碼是否符合 PEP 8？請改善格式
```

### 8. 新功能建議

**Copilot 可以協助實作的功能**
- 即時地震通知系統
- 地震資料庫後端（SQLite/PostgreSQL）
- Web API 端點（使用 FastAPI/Flask）
- 地震預警系統模擬
- 多站點到時差分析
- 震央定位演算法
- 地動速度/加速度視覺化
- 與 Google Earth KML 匯出

**實作步驟範例**
```
# 在 Chat 中開始對話
我想新增一個 FastAPI 端點來查詢地震資料，請給我實作建議

# Copilot 會提供：
1. 專案結構建議
2. 範例程式碼
3. 依賴套件清單
4. 測試方法
```

## 開發工作流程建議

### 使用 Copilot 的最佳實踐

1. **開始新功能前**
   - 在 Chat 中描述需求，請 Copilot 提供設計建議
   - 詢問是否有現成的 ObsPy 功能可以使用
   - 請 Copilot 列出需要的步驟

2. **編寫程式碼時**
   - 先寫清楚的函數簽名和 docstring，讓 Copilot 補全實作
   - 使用有意義的變數名稱，Copilot 會更準確
   - 逐步實作，每個小功能都先測試

3. **測試與除錯**
   - 請 Copilot 為每個函數生成測試案例
   - 遇到錯誤時，貼上完整的錯誤訊息和相關程式碼
   - 詢問最佳除錯策略

4. **文件撰寫**
   - 使用 `/doc` 快速生成文件
   - 請 Copilot 撰寫使用範例
   - 生成 CHANGELOG 和版本更新說明

### 常用 Copilot Chat 指令

- `/explain` - 解釋選取的程式碼
- `/doc` - 為選取的程式碼生成文件
- `/fix` - 修復選取程式碼中的問題
- `/tests` - 為選取的程式碼生成測試
- `/optimize` - 優化選取的程式碼效能

## 專案特定的注意事項

### ObsPy 特性
- ObsPy 使用 UTCDateTime 而非 Python 標準 datetime
- 深度單位是「公尺」需轉換為「公里」顯示
- FDSN 服務可能有速率限制，需加入適當的錯誤處理

### 程式碼風格
- 使用 Black 格式化工具（可請 Copilot 協助設定）
- 函數和變數名使用 snake_case
- 類別名使用 PascalCase
- 常數使用 UPPER_CASE

### 安全與隱私
- 避免在程式碼中硬編碼敏感資訊
- 使用環境變數或設定檔管理 API 金鑰
- 資料檔案放在 `.gitignore` 中以避免意外提交大檔案

## 快速啟動範例

### 執行現有腳本
```bash
# 1. 使用示範模式（不需網路）
python scripts/plot_earthquake_map.py --demo

# 2. 下載真實地震資料
python scripts/plot_earthquake_map.py --days 7 --min-magnitude 4.5

# 3. 查詢並下載波形資料
python scripts/fetch_iris_events_waveforms.py --days 5 --first-only --max-files 5
```

### 使用 Copilot 新增功能
```python
# 1. 建立新檔案 scripts/analyze_frequency.py
# 2. 開始輸入：
"""Analyze frequency content of seismic waveforms"""

from obspy import read
import matplotlib.pyplot as plt

def compute_spectrogram(stream, window_length=1.0):
    # Copilot 會自動建議實作

# 3. 在 Chat 中詢問：
# 「請幫我實作完整的頻譜分析腳本，包括短時傅立葉轉換和視覺化」
```

## 結語

GitHub Copilot 是強大的開發助手，特別適合用於：
- 快速原型開發
- 學習 ObsPy API 的新功能
- 自動生成重複性程式碼（測試、文件）
- 探索不同的實作方法

**記住**：Copilot 提供的建議需要人工審查，特別是在科學計算中，確保演算法的正確性非常重要。始終驗證生成的程式碼是否符合地震學原理和最佳實踐。

---

**最後更新**: 2026-02-08  
**維護者**: GitHub Copilot Agent
