import time
import sys
from managers.video_manager import VideoManager
from managers.outer_music_manager import OuterMusicManager
from config import STAGES, MAX_STAGES, STAGE_BUTTON_MAPPING, PIN_BUTTON_0, PIN_BUTTON_1

# Try importing GPIO
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("[GameManager] RPi.GPIO not found. Running in simulation mode (Keyboard).")

# Try importing Keyboard for simulation
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

class GameManager:
    def __init__(self):
        self.video_mgr = VideoManager()
        self.music_mgr = OuterMusicManager()
        
        self.current_stage = 0 # 0 means S0 (Start)
        self.state = "INIT" # INIT, INTRO, LOOP, RESULT, ENDING
        
        self.obey_count = 0
        self.rebel_count = 0
        
        self.running = True
        
        # Setup Input
        self._setup_input()

    def _setup_input(self):
        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PIN_BUTTON_0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(PIN_BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _check_input(self):
        """
        Returns:
            0: Button 0 pressed
            1: Button 1 pressed
            None: No input
        """
        # Check GPIO
        if GPIO_AVAILABLE:
            if GPIO.input(PIN_BUTTON_0) == GPIO.LOW:
                return 0
            if GPIO.input(PIN_BUTTON_1) == GPIO.LOW:
                return 1
        
        # Check Keyboard (Fallback/Debug)
        if KEYBOARD_AVAILABLE:
            if keyboard.is_pressed('0'):
                return 0
            if keyboard.is_pressed('1'):
                return 1
                
        return None

    def run(self):
        print("Game Started.")
        self.state = "S0_START"
        self._enter_state_s0()

        try:
            while self.running:
                self.update()
                time.sleep(0.05) # Tick rate
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.cleanup()

    def cleanup(self):
        self.video_mgr.stop()
        self.music_mgr.stop()
        if GPIO_AVAILABLE:
            GPIO.cleanup()

    def update(self):
        # Check if video finished
        video_finished = self.video_mgr.check_status()

        if self.state == "S0_START":
            if video_finished:
                self.current_stage = 1
                self._enter_stage_intro()

        elif self.state == "STAGE_INTRO":
            if video_finished:
                self._enter_stage_loop()

        elif self.state == "STAGE_LOOP":
            # Wait for input
            btn = self._check_input()
            if btn is not None:
                self._handle_input(btn)

        elif self.state == "STAGE_RESULT":
            if video_finished:
                self._next_stage()

        elif self.state == "ENDING":
            if video_finished:
                print("Game Over. Restarting...")
                # Reset
                self.obey_count = 0
                self.rebel_count = 0
                self.current_stage = 0
                self.state = "S0_START"
                self._enter_state_s0()

    # --- State Transitions ---

    def _enter_state_s0(self):
        print(">>> State: S0 (Start)")
        self.state = "S0_START"
        self.video_mgr.play("S0")
        self.music_mgr.play("S0") # Might be None

    def _enter_stage_intro(self):
        print(f">>> State: Stage {self.current_stage} Intro")
        self.state = "STAGE_INTRO"
        key = f"S{self.current_stage}_intro"
        self.video_mgr.play(key)
        self.music_mgr.play(key)

    def _enter_stage_loop(self):
        print(f">>> State: Stage {self.current_stage} Loop (Waiting for Input)")
        self.state = "STAGE_LOOP"
        key = f"S{self.current_stage}_loop"
        self.video_mgr.play(key, loop=True)
        # Music for loop? Usually continues from Intro or silence.
        # If we want to stop intro music:
        # self.music_mgr.stop() 
        # But usually BGM continues.

    def _handle_input(self, btn_index):
        # Determine if Obey or Rebel
        # Get mapping for current stage
        obey_btn = STAGE_BUTTON_MAPPING.get(self.current_stage, 0)
        
        is_obey = (btn_index == obey_btn)
        
        if is_obey:
            print("Input: OBEY")
            self.obey_count += 1
            result_type = "obey"
        else:
            print("Input: REBEL")
            self.rebel_count += 1
            result_type = "rebel"
            
        self._enter_stage_result(result_type)

    def _enter_stage_result(self, result_type):
        print(f">>> State: Stage {self.current_stage} Result ({result_type})")
        self.state = "STAGE_RESULT"
        key = f"S{self.current_stage}_{result_type}"
        self.video_mgr.play(key)
        self.music_mgr.play(key)

    def _next_stage(self):
        if self.current_stage < MAX_STAGES:
            self.current_stage += 1
            self._enter_stage_intro()
        else:
            self._enter_ending()

    def _enter_ending(self):
        print(">>> State: Ending")
        self.state = "ENDING"
        
        if self.obey_count >= self.rebel_count:
            ending_type = "good" # Obey -> Good?
        else:
            ending_type = "bad"
            
        print(f"Stats: Obey={self.obey_count}, Rebel={self.rebel_count} -> {ending_type}")
        
        key = f"Ending_{ending_type}"
        self.video_mgr.play(key)
        self.music_mgr.play(key)
