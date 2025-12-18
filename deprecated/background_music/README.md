# 第一階段：環境與檔案準備

在 Raspberry Pi 的桌面建立資料夾，命名為 `audio_project`。

## 1. 準備音訊檔案
- 將製作好的 21 個 `.wav` 檔放入 `audio_project`。
- 格式要求：副檔名為 `.wav`，且所有檔案的長度（秒數）與採樣率（Sample Rate）必須完全一致。
- 命名規則：
    - `base.wav`（主旋律）
    - `good_1.wav` … `good_10.wav`（好聽音樂，1 最弱，10 最強）
    - `bad_1.wav` … `bad_10.wav`（不好聽音效，1 最弱，10 最強）

## 2. 安裝必要的軟體
打開終端機（Terminal），依序執行以下指令：

```bash
# 更新套件清單
sudo apt-get update

# 安裝 PortAudio（音訊驅動）
sudo apt-get install libportaudio2

# 安裝 Python 音訊處理套件
pip3 install sounddevice soundfile numpy
```

# 第二階段：找出硬體 ID

1. 插上有線耳機（3.5mm）。
2. 連接藍牙喇叭並確定已配對/連線。
3. 在 `audio_project` 資料夾建立 `check.py`，內容如下：

```python
# check.py
import sounddevice as sd
print(sd.query_devices())
```

4. 在終端機執行：

```bash
python3 check.py
```

5. 記下清單中對應的編號（ID）：
- 耳機（Headphones）前的數字（例如 `1`）
- 藍牙喇叭（你的喇叭名稱）前的數字（例如 `2`）

# 第三階段：完整程式碼（main.py）

在 `audio_project` 建立 `main.py`，將完整程式碼貼上，並務必在檔案最上方將 `DEVICE_ID` 修改為你查到的數字（耳機或喇叭的裝置 ID）。

# 第四階段：執行與測試步驟

確認：
- 耳機已插入 3.5mm 孔。
- 藍牙喇叭已連線。
- `audio_project` 內有 21 個 WAV 檔。
- `main.py` 中的 `DEVICE_ID` 已正確設定。

執行：

```bash
python3 main.py
```

操作與聆聽：
- 程式啟動後，兩邊應該都會聽到 base 音樂。
- 在鍵盤輸入 `1` 並按 Enter：耳機變豐富（加入好音樂），喇叭變吵雜（加入壞音效）。
- 在鍵盤輸入 `0` 並按 Enter：數值往回扣，剛剛加入的音樂會逐步消失。
- 繼續輸入 `0` 到負數：耳機變吵雜（加入壞音效），喇叭變豐富（加入好音樂）。

# 第五階段：如果聲音不同步（跑拍）

以 Base 音樂的節奏（鼓聲）為準：
- 若耳機比喇叭快（聽到：咚..咚）：打開 `main.py`，找到 `BLUETOOTH_LATENCY_OFFSET = 0.3`，調大此數值（例如 `0.4` 或 `0.5`）。
- 若耳機比喇叭慢：調小此數值（例如 `0.1` 或 `0`）。
- 每次修改後重啟 `main.py` 測試同期性。
