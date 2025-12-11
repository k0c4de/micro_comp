import cv2
import numpy as np
import multiprocessing
import time
import os

def video_process_loop(video_files, command_queue, window_name):
    """
    Standalone function for the video process.
    """
    print("Video Process Started")
    
    current_video_key = "pos"
    cap = cv2.VideoCapture(video_files[current_video_key])
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    running = True
    while running:
        # 1. Check for commands (non-blocking)
        while not command_queue.empty():
            try:
                cmd, val = command_queue.get_nowait()
                if cmd == "stop":
                    running = False
                elif cmd == "set_state":
                    if val in video_files and val != current_video_key:
                        current_video_key = val
                        cap.release()
                        cap = cv2.VideoCapture(video_files[current_video_key])
                        print(f"Switched video to: {current_video_key}")
            except:
                pass
        
        if not running:
            break

        # 2. Play Video
        ret, frame = cap.read()
        if not ret:
            # Loop back
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Resize for performance if needed (optional)
        frame = cv2.resize(frame, (782, 358))
        
        cv2.imshow(window_name, frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            running = False

    cap.release()
    cv2.destroyAllWindows()
    print("Video Process Stopped")

class VideoPlayer:
    def __init__(self):
        self.command_queue = multiprocessing.Queue()
        self.window_name = "Obedience Game"
        
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.video_files = {
            "pos": os.path.join(ROOT_DIR, "obedient.mov"),
            "neg": os.path.join(ROOT_DIR, "rebellious.mov")
        }
        
        self.process = multiprocessing.Process(
            target=video_process_loop, 
            args=(self.video_files, self.command_queue, self.window_name)
        )

    def start(self):
        self.process.start()

    def set_state(self, state):
        # Map common names to internal keys
        mapping = {"good": "pos", "bad": "neg", "obedient": "pos", "rebellious": "neg"}
        key = mapping.get(state, state)
        self.command_queue.put(("set_state", key))

    def stop(self):
        self.command_queue.put(("stop", None))
        self.process.join()