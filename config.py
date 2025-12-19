import os

# Base Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(ROOT_DIR, "video") # Currently videos are here
BGM_DIR = os.path.join(ROOT_DIR, "bgm")

# Device IDs (Update these based on your hardware)
DEVICE_ID_HEADPHONE = 0 # Default output usually
DEVICE_ID_BLUETOOTH = 11

# Stage Settings
STAGES = [1, 2, 3]
MAX_STAGES = 3

# File Mappings
# Video Files (MP4)
VIDEO_FILES = {
    "S0": os.path.join(VIDEO_DIR, "S0.mp4"),
    
    "S1_intro": os.path.join(VIDEO_DIR, "S1_intro.mp4"),
    "S1_loop": os.path.join(VIDEO_DIR, "S1_loop.mp4"),
    "S1_obey": os.path.join(VIDEO_DIR, "S1_obey.mp4"),
    "S1_rebel": os.path.join(VIDEO_DIR, "S1_rebel.mp4"),
    
    "S2_intro": os.path.join(VIDEO_DIR, "S2_intro.mp4"),
    "S2_loop": os.path.join(VIDEO_DIR, "S2_loop.mp4"),
    "S2_obey": os.path.join(VIDEO_DIR, "S2_obey.mp4"),
    "S2_rebel": os.path.join(VIDEO_DIR, "S2_rebel.mp4"),
    
    "S3_intro": os.path.join(VIDEO_DIR, "S3_intro.mp4"),
    "S3_loop": os.path.join(VIDEO_DIR, "S3_loop.mp4"),
    "S3_obey": os.path.join(VIDEO_DIR, "S3_obey.mp4"),
    "S3_rebel": os.path.join(VIDEO_DIR, "S3_rebel.mp4"),
    
    "Ending_good": os.path.join(VIDEO_DIR, "Ending_obey.mp4"), # Assuming Obey -> Good
    "Ending_bad": os.path.join(VIDEO_DIR, "Ending_rebel.mp4"),   # Assuming Rebel -> Bad
}

# Bluetooth Audio Files (WAV/MP3)
# Mapping based on folder structure in bgm/
# bgm/1_S1_Intro/S1_Intro_out.mp3
BGM_FILES = {
    "S0": os.path.joint(BGM_DIR, "0_Start_intro", "Start_intro_int.mp3"),
    
    "S1_intro": os.path.join(BGM_DIR, "1_S1_Intro", "S1_Intro_out.mp3"),
    "S1_obey": os.path.join(BGM_DIR, "2_S1_Obey", "S1_Obey_out.mp3"),
    "S1_rebel": os.path.join(BGM_DIR, "3_S1_Rebel", "S1_Rebel_out.mp3"),
    
    "S2_intro": os.path.join(BGM_DIR, "4_S2_Intro", "S2_Intro_out.mp3"),
    "S2_obey": os.path.join(BGM_DIR, "5_S2_Obey", "S2_Obey_out.mp3"),
    "S2_rebel": os.path.join(BGM_DIR, "6_S2_Rebel", "S2_Rebel_out.mp3"),
    
    "S3_intro": os.path.join(BGM_DIR, "7_S3_Intro", "S3_Intro_out.mp3"),
    "S3_obey": os.path.join(BGM_DIR, "8_S3_Obey", "S3_Obey_out.mp3"),
    "S3_rebel": os.path.join(BGM_DIR, "9_S3_Rebel", "S3_Rebel_out.mp3"),
    
    "Ending_good": os.path.join(BGM_DIR, "10_Ending_Good", "Ending_Good_out.mp3"), # Verify filename
    "Ending_bad": os.path.join(BGM_DIR, "11_Ending_Bad", "Ending_Bad_out.mp3"),   # Verify filename
}

# Button Pins (BCM numbering for Raspberry Pi)
PIN_BUTTON_0 = 17 # Example
PIN_BUTTON_1 = 27 # Example

# Button Logic Mapping
# For each stage, define which button (0 or 1) corresponds to "Obey" (True)
# If button 0 is Obey, then button 1 is Rebel.
# Format: { Stage_Number: Button_Index_For_Obey }
STAGE_BUTTON_MAPPING = {
    1: 0, # Stage 1: Button 0 is Obey
    2: 1, # Stage 2: Button 1 is Obey
    3: 0  # Stage 3: Button 0 is Obey
}
