import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import threading
import sys

# ==========================================
# 1. 設定區域 (請修改這裡！)
# ==========================================

# 【重要】請填入剛剛查到的裝置 ID
DEVICE_ID_HEADPHONE = 1  # 改成您的耳機 ID
DEVICE_ID_BLUETOOTH = 2  # 改成您的藍牙喇叭 ID

# 藍牙延遲補償 (秒)
# 因為藍牙通常比較慢，我們要讓耳機「等」一下
# 如果耳機聲音比喇叭快，請把這個數字調大 (例如 0.3, 0.4)
BLUETOOTH_LATENCY_OFFSET = 0.3 

# 檔案名稱設定
FILE_BASE = "base.wav"
FILES_GOOD = [f"good_{i}.wav" for i in range(1, 11)]
FILES_BAD = [f"bad_{i}.wav" for i in range(1, 11)]

# ==========================================
# 2. 載入音訊 (Loading)
# ==========================================
print("正在載入音訊檔案 (WAV) 到記憶體，請稍候...")

def load_audio(filename):
    try:
        data, samplerate = sf.read(filename, dtype='float32')
        # 如果是單聲道，轉成立體聲
        if data.ndim == 1:
            data = np.column_stack((data, data))
        return data, samplerate
    except Exception as e:
        print(f"錯誤：找不到檔案 {filename} 或格式錯誤。")
        sys.exit(1)

# 載入 Base
base_data, fs = load_audio(FILE_BASE)
track_length = len(base_data)

# 載入 Layers
good_data_list = [load_audio(f)[0] for f in FILES_GOOD]
bad_data_list = [load_audio(f)[0] for f in FILES_BAD]

# 驗證長度
for d in good_data_list + bad_data_list:
    if len(d) != track_length:
        print("警告：有音訊檔案長度不一致！可能會導致播放錯亂。")

print(f"載入完成。取樣率: {fs}, 長度: {track_length} frames")

# ==========================================
# 3. 核心邏輯引擎 (Audio Engine)
# ==========================================
class AudioEngine:
    def __init__(self):
        # 狀態變數：-10 (最壞) ~ 0 (原始) ~ +10 (最好)
        self.current_level = 0 
        self.lock = threading.Lock()

    def update_logic(self, input_val):
        """ 
        控制核心：
        Input 1 -> 數值 +1 (往好音樂走)
        Input 0 -> 數值 -1 (往壞音效走)
        """
        with self.lock:
            if input_val == 1:
                # 往正向移動，最大不超過 10
                if self.current_level < 10:
                    self.current_level += 1
                    print(f"[Input 1]往好方向推 -> 目前數值: {self.current_level}")
                else:
                    print("[Input 1]已達最好狀態 (10)，無法再增加")
            
            elif input_val == 0:
                # 往負向移動，最小不低於 -10
                if self.current_level > -10:
                    self.current_level -= 1
                    print(f"[Input 0]往壞方向推 -> 目前數值: {self.current_level}")
                else:
                    print("[Input 0]已達最壞狀態 (-10)，無法再增加")

    def get_mix_chunk(self, start_frame, frames, mode):
        """
        即時合成音訊片段
        mode: 'HEADPHONE' (正常) 或 'SPEAKER' (相反)
        """
        # 計算循環播放的索引位置
        indices = np.arange(start_frame, start_frame + frames) % track_length
        
        # 1. 基礎音軌
        mix = base_data[indices].copy()
        
        with self.lock:
            level = self.current_level

        # 2. 解析數值 (-10 ~ 10) 決定要疊加什麼
        # 先計算出標準邏輯下該播幾層 Good 或 Bad
        if level > 0:
            standard_good = level
            standard_bad = 0
        elif level < 0:
            standard_good = 0
            standard_bad = abs(level)
        else:
            standard_good = 0
            standard_bad = 0

        # 3. 根據裝置模式分配 (相反邏輯在這裡執行)
        if mode == 'HEADPHONE':
            # 耳機：忠實呈現
            active_good_layers = standard_good
            active_bad_layers = standard_bad
        else:
            # 喇叭：邏輯完全相反
            # 當耳機播好音樂時，喇叭播對應數量的壞音效
            # 當耳機播壞音效時，喇叭播對應數量的好音樂
            active_good_layers = standard_bad
            active_bad_layers = standard_good

        # 4. 執行疊加 (使用 numpy 加速運算)
        for i in range(active_good_layers):
            mix += good_data_list[i][indices]
            
        for i in range(active_bad_layers):
            mix += bad_data_list[i][indices]

        # 5. 防止爆音 (Clipping Protection)
        max_val = np.max(np.abs(mix))
        if max_val > 1.0:
            mix /= max_val
            
        return mix

engine = AudioEngine()

# ==========================================
# 4. 串流回呼 (Callbacks) & 同步控制
# ==========================================
start_time = time.time()

def callback_headphone(outdata, frames, time_info, status):
    # 耳機回呼：負責有線耳機，包含人工延遲
    if status: print(f"Headphone: {status}")
    
    # 計算目前播放時間 (扣掉延遲補償，讓耳機晚一點播)
    current_time = time.time() - start_time - BLUETOOTH_LATENCY_OFFSET
    
    if current_time < 0:
        outdata.fill(0) # 時間還沒到，輸出靜音
        return

    frame_idx = int(current_time * fs)
    data = engine.get_mix_chunk(frame_idx, frames, 'HEADPHONE')
    outdata[:] = data

def callback_bluetooth(outdata, frames, time_info, status):
    # 藍牙回呼：負責藍牙喇叭，直接播放
    if status: print(f"BT: {status}")
    
    current_time = time.time() - start_time
    frame_idx = int(current_time * fs)
    
    data = engine.get_mix_chunk(frame_idx, frames, 'SPEAKER')
    outdata[:] = data

# ==========================================
# 5. 主程式啟動
# ==========================================
if __name__ == "__main__":
    print("\n=== 系統啟動 ===")
    print(f"有線耳機 ID: {DEVICE_ID_HEADPHONE}")
    print(f"藍牙喇叭 ID: {DEVICE_ID_BLUETOOTH}")
    print("輸入 '1' 增加好感度，輸入 '0' 減少好感度 (按 Enter 確認)")
    print("按 Ctrl+C 結束程式")
    print("================\n")

    try:
        # 同時開啟兩個音訊串流
        stream_phones = sd.OutputStream(
            device=DEVICE_ID_HEADPHONE, channels=2, samplerate=fs, 
            callback=callback_headphone, blocksize=2048
        )
        stream_bt = sd.OutputStream(
            device=DEVICE_ID_BLUETOOTH, channels=2, samplerate=fs, 
            callback=callback_bluetooth, blocksize=2048
        )

        with stream_phones, stream_bt:
            while True:
                # 等待使用者輸入 (模擬感測器)
                # 未來您可以將這裡替換成 GPIO 的讀取程式碼
                user_input = input(">> 輸入指令 (1/0): ")
                
                if user_input.strip() == "1":
                    engine.update_logic(1)
                elif user_input.strip() == "0":
                    engine.update_logic(0)
                else:
                    print("無效輸入，請輸入 1 或 0")

    except KeyboardInterrupt:
        print("\n程式結束")
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        print("提示：請確認裝置 ID 是否正確，或藍牙是否已斷線。")