# GitHub Copilot 使用建議 - ObsPy Vibe Coding 專案

本文件提供具體的建議，說明如何使用 GitHub Copilot 來增強和改進這個地震學資料分析專案。

## 📋 目錄

1. [立即可以開始的任務](#立即可以開始的任務)
2. [中期改善建議](#中期改善建議)
3. [長期擴展方向](#長期擴展方向)
4. [具體的 Copilot 提示詞範例](#具體的-copilot-提示詞範例)

---

## 🚀 立即可以開始的任務

### 1. 建立完整的測試套件

**現況**: 專案目前沒有測試檔案  
**目標**: 使用 pytest 建立全面的單元測試和整合測試

**Copilot 協助步驟**:
```bash
# 1. 建立 tests 目錄結構
mkdir -p tests/fixtures

# 2. 在新檔案 tests/test_plot_earthquake_map.py 中，輸入：
import pytest
from scripts.plot_earthquake_map import fetch_earthquakes, extract_earthquake_info

# 3. 讓 Copilot 自動補全測試案例
def test_fetch_earthquakes_demo():
    """Test fetching earthquakes in demo mode"""
    # Copilot 會建議完整的測試邏輯
```

**Copilot Chat 提示詞**:
```
請為 plot_earthquake_map.py 中的所有函數建立完整的 pytest 測試案例。
包括：
1. 單元測試（每個函數獨立測試）
2. 模擬 (mock) FDSN Client 以避免網路請求
3. 測試錯誤處理情境
4. 測試 demo 模式功能
```

### 2. 新增型別提示 (Type Hints)

**現況**: 程式碼缺少型別標註  
**目標**: 為所有函數新增完整的型別提示

**Copilot Chat 提示詞**:
```
請為 plot_earthquake_map.py 中的所有函數新增完整的型別提示。
使用 typing 模組中的適當型別，例如 Optional, List, Dict 等。
確保與 ObsPy 的型別相容。
```

**範例**:
```python
from typing import Dict, List, Optional
from obspy.core.event import Catalog

def extract_earthquake_info(catalog: Catalog) -> Dict[str, List]:
    """Extract relevant information from earthquake catalog."""
    # ... 實作
```

### 3. 改善錯誤處理和使用者訊息

**Copilot Chat 提示詞**:
```
請檢查 fetch_iris_events_waveforms.py，改善所有的錯誤處理。
確保：
1. 所有可能的例外都被正確捕獲
2. 錯誤訊息對使用者友善且具有指導性
3. 使用 logging 模組記錄除錯資訊
4. 加入重試邏輯處理網路暫時性錯誤
```

### 4. 新增設定檔支援

**目標**: 使用 YAML 或 TOML 設定檔取代命令列參數

**Copilot Chat 提示詞**:
```
請幫我建立一個 config.yaml 範本和讀取設定檔的功能。
設定應包括：
- FDSN 客戶端設定（預設服務、超時時間、重試次數）
- 地圖繪製設定（輸出格式、DPI、色彩配置）
- 資料查詢預設值（天數、最小震級）
請使用 pyyaml 或 tomli 套件。
```

### 5. 程式碼重構和模組化

**Copilot Chat 提示詞**:
```
請將 plot_earthquake_map.py 重構為更模組化的結構：
1. 將資料獲取邏輯分離到 data_fetcher.py
2. 將視覺化邏輯分離到 visualizer.py
3. 將資料處理邏輯分離到 data_processor.py
4. 建立一個 utils.py 存放共用函數
請保持向後相容性，原有的 plot_earthquake_map.py 仍可作為 CLI 工具執行。
```

---

## 🔄 中期改善建議

### 6. 建立 Jupyter Notebook 教學範例

**Copilot Chat 提示詞**:
```
請建立一個 Jupyter notebook (examples/earthquake_analysis_tutorial.ipynb)，
包含以下內容：
1. 專案簡介和環境設定
2. 基本地震資料查詢範例
3. 自訂地圖視覺化
4. 波形資料分析範例
5. 進階分析（震央分布、深度統計、時序分析）
使用真實資料和 demo 模式作為範例。
```

### 7. 新增資料匯出功能

**功能需求**:
- 匯出地震目錄為 CSV、JSON、GeoJSON
- 匯出為 Google Earth KML 格式
- 匯出統計報告為 Markdown 或 HTML

**Copilot Chat 提示詞**:
```
請新增一個 exporter.py 模組，包含以下函數：
1. catalog_to_csv(catalog, output_file) - 匯出為 CSV
2. catalog_to_geojson(catalog, output_file) - 匯出為 GeoJSON
3. catalog_to_kml(catalog, output_file) - 匯出為 KML
4. generate_html_report(earthquake_data, output_file) - 生成 HTML 報告
確保處理各種邊緣情況和缺失資料。
```

### 8. 實作資料快取機制

**Copilot Chat 提示詞**:
```
請實作一個簡單的資料快取系統：
1. 使用 SQLite 儲存已查詢的地震事件
2. 避免重複下載相同時間範圍的資料
3. 提供 --no-cache 選項強制重新下載
4. 加入快取過期機制（預設 24 小時）
請使用標準函式庫或輕量級套件。
```

### 9. 新增互動式地圖

**Copilot Chat 提示詞**:
```
請使用 folium 或 plotly 建立互動式地震地圖：
1. 滑鼠懸停顯示地震詳細資訊
2. 可縮放和拖曳的地圖
3. 圖層控制（深度、震級、時間範圍）
4. 匯出為獨立的 HTML 檔案
請建立新檔案 scripts/plot_interactive_map.py
```

### 10. 波形資料視覺化與分析

**Copilot Chat 提示詞**:
```
請建立 scripts/analyze_waveforms.py，包含以下功能：
1. 讀取已下載的波形資料
2. 繪製三分量波形（垂直、南北、東西）
3. 計算並繪製頻譜圖 (spectrogram)
4. 執行帶通濾波和訊號處理
5. 自動震相辨識（P 波和 S 波）
6. 批次處理多個波形檔案
使用 ObsPy 的內建功能和最佳實踐。
```

---

## 🎯 長期擴展方向

### 11. 建立 Web API 服務

**Copilot Chat 提示詞**:
```
請使用 FastAPI 建立一個地震資料查詢 API：

端點設計：
- GET /api/earthquakes?days=7&min_mag=4.0 - 查詢地震
- GET /api/earthquakes/{event_id} - 取得單一事件詳情
- GET /api/earthquakes/stats - 統計資訊
- GET /api/waveforms/{event_id} - 取得波形資料清單

請包含：
1. 完整的 OpenAPI 文件
2. 請求驗證和錯誤處理
3. 速率限制
4. CORS 設定
5. Docker 部署設定
```

### 12. 即時地震監控系統

**Copilot Chat 提示詞**:
```
請設計一個即時地震監控腳本 scripts/monitor_earthquakes.py：
1. 定期輪詢 FDSN 服務檢查新地震
2. 偵測到新地震時發送通知（email/Slack/Telegram）
3. 自動生成地圖和報告
4. 使用 SQLite 記錄所有事件
5. 支援背景執行和日誌記錄
6. 提供狀態檢查和健康監控端點
```

### 13. 地震預警系統模擬

**Copilot Chat 提示詞**:
```
請建立一個地震預警系統模擬器 scripts/eew_simulator.py：
1. 模擬 P 波和 S 波傳播
2. 計算不同地點的預警時間
3. 視覺化波前傳播動畫
4. 評估預警系統效能
5. 匯出模擬結果報告
使用真實的地震速度模型和地球物理參數。
```

### 14. 機器學習整合

**Copilot Chat 提示詞**:
```
請設計一個 ML 模組用於：
1. 地震規模預測（基於早期 P 波訊號）
2. 地震序列分類（主震、前震、餘震）
3. 異常偵測（辨識非天然地震事件）
請使用 scikit-learn 或 PyTorch，並提供訓練範例。
```

### 15. 資料視覺化儀表板

**Copilot Chat 提示詞**:
```
請使用 Streamlit 或 Dash 建立互動式儀表板：
1. 即時地震地圖更新
2. 統計圖表（震級分布、深度分布、時間序列）
3. 互動式查詢介面
4. 波形資料瀏覽器
5. 匯出功能
6. 深色/淺色主題切換
請建立 dashboard/app.py
```

---

## 💡 具體的 Copilot 提示詞範例

### 程式碼生成範例

#### 範例 1: 新增功能
```
# 在新檔案中輸入註解，讓 Copilot 生成程式碼：

# Function to calculate Gutenberg-Richter b-value
# Input: list of magnitudes
# Output: b-value, a-value, and R-squared
def calculate_b_value(magnitudes):
    # Copilot 會自動補全實作
```

#### 範例 2: 優化現有程式碼
```
# 在 Copilot Chat 中：
請優化這個函數的效能：
[貼上 extract_earthquake_info 函數]

建議使用：
1. NumPy 向量化操作
2. 列表推導式取代迴圈
3. 減少不必要的函數呼叫
```

#### 範例 3: 新增文件
```
# 選取函數後在編輯器中輸入：
/doc

# 或在 Chat 中：
請為這個函數撰寫完整的 NumPy 風格文件字串，包括：
- 簡短描述
- 詳細說明
- 參數說明（含型別）
- 回傳值說明
- 使用範例
- 注意事項
```

### 問題解決範例

#### 範例 4: 除錯協助
```
# 在 Chat 中貼上錯誤訊息：
我執行 python scripts/plot_earthquake_map.py 時遇到以下錯誤：
[錯誤訊息]

請說明錯誤原因並提供解決方案。
```

#### 範例 5: 學習 API
```
# 在 Chat 中詢問：
ObsPy 中如何：
1. 讀取 miniSEED 格式的波形資料？
2. 套用帶通濾波？
3. 計算震相到時？
請提供程式碼範例。
```

### 架構設計範例

#### 範例 6: 設計新功能
```
# 在 Chat 中：
我想新增一個功能，可以比較不同時間段的地震活動性。
請提供：
1. 功能設計建議
2. 所需的函數清單
3. 資料結構設計
4. 視覺化方案
5. 範例程式碼架構
```

---

## 🎓 學習資源和最佳實踐

### 使用 Copilot 學習 ObsPy

**提示詞範例**:
```
請給我一個完整的 ObsPy 快速入門教學，涵蓋：
1. 地震目錄查詢
2. 波形資料下載和處理
3. 震相辨識
4. 訊號處理（濾波、重採樣）
5. 資料視覺化
每個主題請提供程式碼範例和說明。
```

### 程式碼審查和品質改善

**提示詞範例**:
```
請審查 [檔案名稱] 並提供改善建議：
1. 程式碼風格和 PEP 8 合規性
2. 效能瓶頸
3. 潛在的 bug 或邊緣情況
4. 安全性問題
5. 測試覆蓋率不足的部分
6. 文件完整性
```

---

## 📝 結語

這份文件提供了大量使用 GitHub Copilot 改進此專案的具體建議。你可以：

1. **從簡單的開始**: 先完成「立即可以開始的任務」
2. **循序漸進**: 逐步實作中期和長期功能
3. **靈活調整**: 根據實際需求修改建議
4. **保持學習**: 使用 Copilot 作為學習 ObsPy 和地震學的工具

記住：
- ✅ Copilot 是輔助工具，最終程式碼品質仍需人工審查
- ✅ 科學計算中演算法正確性至關重要
- ✅ 始終驗證計算結果並與已知數據對照
- ✅ 適當的測試是確保程式碼品質的關鍵

**開始使用**: 選擇一個任務，打開 Copilot Chat，開始對話！

---

**文件版本**: 1.0  
**最後更新**: 2026-02-08  
**貢獻者**: 歡迎提交 issue 或 PR 改進這份文件
