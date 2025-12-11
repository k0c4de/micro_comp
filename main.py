import time
import sys
import threading
from background_music import music
from instruction_system import logic_test
from video.video_player import VideoPlayer

# ==========================================
# Main Program
# ==========================================
def main():

    # 1. Start Audio System
    print("Initializing Audio System...")
    try:
        stream_phones, stream_bt = music.start_streams()
        stream_phones.start()
        stream_bt.start()
        print("Audio Streams Started.")
    except Exception as e:
        print(f"Error starting audio: {e}")
        print("Please check device IDs in background_music/music.py")
        return

    # 2. Initialize Game Logic
    game = logic_test.GameLogic(music.engine)

    # 3. Initialize Video Player
    video_player = VideoPlayer()
    video_player.start()

    try:
        while True:
            # Run one stage
            result = game.run_stage()
            
            # Update Video State based on result
            if result: # Obedient -> Good
                video_player.set_state("good")
            else: # Rebellious -> Bad
                video_player.set_state("bad")
            
            print("-" * 40)

    except KeyboardInterrupt:
        print("\nStopping System...")
    finally:
        # Cleanup
        stream_phones.stop()
        stream_bt.stop()
        stream_phones.close()
        stream_bt.close()
        video_player.stop()
        print("System Shutdown.")

if __name__ == "__main__":
    main()
