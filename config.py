import os

# Base Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(ROOT_DIR, "video") # Currently videos are here
BGM_DIR = os.path.join(ROOT_DIR, "bgm")

# Device IDs (Update these based on your hardware)
DEVICE_ID_HEADPHONE = 0 # Default output usually
DEVICE_ID_BLUETOOTH = 10

# Device Names (Partial match)
DEVICE_NAME_HEADPHONE = "Built-in" # Look for "Headphones" or "bcm2835" or "Built-in"
DEVICE_NAME_BLUETOOTH = "Tronsmart" # Look for "Blue" or your speaker name

# BGM Volume (0.0 to 1.0)
OUTER_BGM_VOLUME = 1.0
INNER_BGM_VOLUME = 0.03
VIDEO_VOLIME = 0.5

# Target Sample Rate
TARGET_SAMPLE_RATE = 22050

# BGM Delay (Seconds)
# Positive value delays the start
INNER_BGM_DELAY = 0.0
OUTER_BGM_DELAY = 0.6

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
    "S0": os.path.join(BGM_DIR, "0_Start_intro", "Start_intro_out.mp3"),
    
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

# Inner Audio Files (WAV/MP3) - For Headphones
INNER_BGM_FILES = {
    "S0": os.path.join(BGM_DIR, "0_Start_intro", "Start_intro_in.mp3"),
    
    "S1_intro": os.path.join(BGM_DIR, "1_S1_Intro", "S1_Intro_in.mp3"),
    "S1_obey": os.path.join(BGM_DIR, "2_S1_Obey", "S1_Obey_in.mp3"),
    "S1_rebel": os.path.join(BGM_DIR, "3_S1_Rebel", "S1_Rebel_in.mp3"),
    
    "S2_intro": os.path.join(BGM_DIR, "4_S2_Intro", "S2_Intro_in.mp3"),
    "S2_obey": os.path.join(BGM_DIR, "5_S2_Obey", "S2_Obey_int.mp3"),
    "S2_rebel": os.path.join(BGM_DIR, "6_S2_Rebel", "S2_Rebel_in.mp3"),
    
    "S3_intro": os.path.join(BGM_DIR, "7_S3_Intro", "S3_Intro_in.mp3"),
    "S3_obey": os.path.join(BGM_DIR, "8_S3_Obey", "S3_Obey_in.mp3"),
    "S3_rebel": os.path.join(BGM_DIR, "9_S3_Rebel", "S3_Rebel_in.mp3"),
    
    "Ending_good": os.path.join(BGM_DIR, "10_Ending_Good", "Ending_Good_in.mp3"), 
    "Ending_bad": os.path.join(BGM_DIR, "11_Ending_Bad", "Ending_Bad_in.mp3"),   
}

# Button Pins (BCM numbering for Raspberry Pi)
PIN_BUTTON_0 = 4 # Example
PIN_BUTTON_1 = 17 # Example

# Button Logic Mapping
# For each stage, define which button (0 or 1) corresponds to "Obey" (True)
# If button 0 is Obey, then button 1 is Rebel.
# Format: { Stage_Number: Button_Index_For_Obey }
STAGE_BUTTON_MAPPING = {
    1: 0, # Stage 1: Button 0 is Obey
    2: 1, # Stage 2: Button 1 is Obey
    3: 0  # Stage 3: Button 0 is Obey
}
