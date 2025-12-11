import time
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(ROOT_DIR, "instruction_tts")

# 12/11 modified by k0c4de: Refactored into a class for integration
class GameLogic:
    def __init__(self, audio_engine):
        self.current_stage = 1
        self.max_stage = 4
        self.engine = audio_engine
        # 12/11 modified by k0c4de: Adjusted path to be relative to workspace root
        self.sound_folder = SOUND_DIR

    def play_audio(self, filename):
        """
        Play audio using the integrated AudioEngine
        """
        full_path = os.path.join(self.sound_folder, filename)
        print(f"正在播放: {full_path}")
        
        # 12/11 modified by k0c4de: Use engine to play TTS
        if os.path.exists(full_path):
            self.engine.play_tts(full_path)
            
            # Simulate blocking behavior of aplay
            # Wait for a short moment for the flag to set
            time.sleep(0.1)
            while self.engine.tts_playing:
                time.sleep(0.1)
        else:
            print(f"錯誤: 找不到檔案 {full_path}")

    def get_input(self):
        """
        Get input from user (Keyboard for debug, GPIO later)
        """
        # 12/11 modified by k0c4de: This can be overridden or replaced
        user_input = input("請輸入 1(服從) 或 0(反抗): ").strip()
        return user_input == '1'

    def run_stage(self):
        """
        Run one stage of the game
        """
        stage_str = f"0{self.current_stage}"

        # 1. Play Intro
        intro_file = f"intro_{stage_str}.wav"
        self.play_audio(intro_file)

        # 2. Get Input
        is_obedient = self.get_input()

        # 3. Update Music Engine Logic
        # 12/11 modified by k0c4de: Update background music based on input
        if is_obedient:
            self.engine.update_logic(1) # Good
        else:
            self.engine.update_logic(0) # Bad

        # 4. Play Feedback (Pos/Neg)
        if is_obedient:
            print("玩家服從 → 播 pos")
            voice_file = f"pos_{stage_str}.wav"
        else:
            print("玩家反抗 → 播 neg")
            voice_file = f"neg_{stage_str}.wav"

        self.play_audio(voice_file)

        # 5. Transition
        time.sleep(0.8)

        if self.current_stage < self.max_stage:
            self.current_stage += 1
        else:
            print("\n一輪結束 → 回到 Level 1\n")
            self.current_stage = 1
            time.sleep(1)
        
        return is_obedient # Return choice for other systems (e.g. screen)

# Keep the original main for testing if needed, but it won't work without engine
if __name__ == "__main__":
    print("This file is now a module. Run main.py instead.")
