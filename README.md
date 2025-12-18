# Interactive Art Installation Project

## Overview
This project controls an interactive art installation using a Raspberry Pi. It manages video playback (HDMI/Headphones) and background music (Bluetooth) based on user input (Buttons).

## Architecture
- **GameManager**: Controls the flow of the game (FSM), handles input, and coordinates video and audio.
- **VideoManager**: Handles video playback using VLC.
- **OuterMusicManager**: Handles Bluetooth audio output using `sounddevice`.

## Setup

### 1. Hardware
- Raspberry Pi
- 2 Buttons connected to GPIO pins (Configured in `config.py`).
- Display (HDMI).
- Headphones (connected to Pi Audio Jack).
- Bluetooth Speaker (Paired and Trusted).

### 2. Software Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

**Important:**
- You must have **VLC Media Player** installed on the system.
  - On Raspberry Pi: `sudo apt-get install vlc`
- You need `libportaudio2` for sounddevice:
  - On Raspberry Pi: `sudo apt-get install libportaudio2`

### 3. Configuration
Edit `config.py` to set:
- `DEVICE_ID_BLUETOOTH`: The ID of your Bluetooth output device. Run `python -m sounddevice` to list devices.
- `PIN_BUTTON_0` / `PIN_BUTTON_1`: GPIO pins for buttons.
- `STAGE_BUTTON_MAPPING`: Which button corresponds to "Obey" for each stage.

### 4. Running
Run the main script:
```bash
python main.py
```

## File Structure
- `main.py`: Entry point.
- `config.py`: Configuration.
- `managers/`: Contains the logic modules.
- `bgm/`: Audio files.
- `deprecated/video/`: Video files (referenced in config).

## Notes
- The system uses `keyboard` module for simulation if `RPi.GPIO` is not available (Press '0' or '1').
- Ensure video files are in the correct paths as defined in `config.py`.
