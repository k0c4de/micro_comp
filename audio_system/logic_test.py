import time
import os

# === 遊戲階段設定 ===
current_stage = 1
max_stage = 4

# 音檔都放在 sound/ 資料夾
SOUND_FOLDER = "sound"

def play_audio(filename):
    """
    使用 aplay 播放 WAV 音檔（Raspberry Pi 內建）
    """
    full_path = os.path.join(SOUND_FOLDER, filename)
    print(f"正在播放: {full_path}")
    os.system(f"aplay -q {full_path}")   # -q 靜音模式，不輸出多餘字串


def get_keyboard_input():
    """
    使用鍵盤輸入 1(服從) / 0(反抗)
    """
    user_input = input("請輸入 1(服從) 或 0(反抗): ").strip()
    return user_input == '1'   # True = 服從，False = 反抗


def process_stage(is_obedient):
    """
    根據玩家是否服從，播放 pos_0X.wav 或 neg_0X.wav
    """
    global current_stage
    stage_str = f"0{current_stage}"

    if is_obedient:
        print("玩家服從 → 播 pos")
        voice_file = f"pos_{stage_str}.wav"
    else:
        print("玩家反抗 → 播 neg")
        voice_file = f"neg_{stage_str}.wav"

    # 播 pos 或 neg 音檔
    play_audio(voice_file)

    # === 過場延遲（避免太接近） ===
    time.sleep(0.8)

    # 下一階段
    if current_stage < max_stage:
        current_stage += 1
    else:
        print("\n一輪結束 → 回到 Level 1\n")
        current_stage = 1
        time.sleep(1)


# === 主程式 ===
if __name__ == "__main__":
    print("=== 黑盒教育遊戲：音訊播放版 ===\n")

    try:
        while True:
            stage_str = f"0{current_stage}"

            # 播本階段 intro
            intro_file = f"intro_{stage_str}.wav"
            play_audio(intro_file)

            # 玩家輸入
            is_obedient = get_keyboard_input()

            # 播 pos 或 neg 並切換階段
            process_stage(is_obedient)

            print("-" * 40)

    except KeyboardInterrupt:
        print("\n結束遊戲")
