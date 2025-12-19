import sounddevice as sd
import soundfile as sf
import os
import time
import numpy as np
from config import INNER_BGM_FILES, DEVICE_ID_HEADPHONE, DEVICE_NAME_HEADPHONE, INNER_BGM_VOLUME, INNER_BGM_DELAY, TARGET_SAMPLE_RATE

class InnerMusicManager:
    def __init__(self):
        self.stream = None
        self.device_id = self._find_device()
        print(f"[InnerMusicManager] Initialized with Device ID: {self.device_id}")

    def _find_device(self):
        """Find device ID by name."""
        try:
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if DEVICE_NAME_HEADPHONE.lower() in dev['name'].lower():
                    print(f"[InnerMusicManager] Found Headphone Device: {dev['name']} (ID: {i})")
                    return i
            
            print(f"[InnerMusicManager] Warning: Device matching '{DEVICE_NAME_HEADPHONE}' not found. Using default ID {DEVICE_ID_HEADPHONE}.")
            return DEVICE_ID_HEADPHONE
        except Exception as e:
            print(f"[InnerMusicManager] Error querying devices: {e}")
            return DEVICE_ID_HEADPHONE

    def play(self, key):
        """
        Play audio file associated with key on the Bluetooth device.
        """
        path = INNER_BGM_FILES.get(key)
        if not path:
            return
            
        if not os.path.exists(path):
            print(f"[InnerMusicManager] File not found: {path}")
            return

        # Stop any currently playing audio
        self.stop()

        try:
            # Read file
            data, fs = sf.read(path, dtype='float32')
            
            # Downsample if needed
            if fs > TARGET_SAMPLE_RATE:
                step = int(fs / TARGET_SAMPLE_RATE)
                if step > 1:
                    data = data[::step]
                    fs = int(fs / step)
                    # print(f"[InnerMusicManager] Downsampled to {fs} Hz")

            # Apply Volume
            data = data * INNER_BGM_VOLUME
            
            # Handle mono/stereo
            channels = data.shape[1] if data.ndim > 1 else 1
            
            # Calculate delay samples
            delay_samples = int(INNER_BGM_DELAY * fs) if INNER_BGM_DELAY > 0 else 0
            
            # Define callback for stream
            # We use a closure to keep track of position
            # Start position is negative if there is a delay
            position = -delay_samples
            
            def callback(outdata, frames, time, status):
                nonlocal position
                if status:
                    print(f"[InnerMusicManager] Stream Status: {status}")
                
                chunk_len = len(outdata)
                
                # Fill with zeros initially
                outdata.fill(0)
                
                # Calculate indices
                start_idx = position
                end_idx = position + chunk_len
                
                # If we are completely in the delay period (end_idx <= 0), outdata remains 0
                
                # If we are crossing from delay to data or fully in data
                if end_idx > 0:
                    # Determine where in outdata to start writing data
                    out_offset = 0
                    data_start = 0
                    
                    if start_idx < 0:
                        # We are crossing the boundary
                        out_offset = -start_idx # Skip the delay part in outdata
                        data_start = 0
                    else:
                        # We are fully in data
                        out_offset = 0
                        data_start = start_idx
                    
                    # Determine how much data to copy
                    # Available space in outdata from out_offset
                    space_left = chunk_len - out_offset
                    
                    # Available data remaining
                    data_left = len(data) - data_start
                    
                    if data_left <= 0:
                        # End of file reached previously or exactly now
                        raise sd.CallbackStop()
                    
                    # Amount to copy is min of space left and data left
                    copy_len = min(space_left, data_left)
                    
                    if copy_len > 0:
                        outdata[out_offset:out_offset+copy_len] = data[data_start:data_start+copy_len]
                    
                    # If we finished the file in this chunk
                    if copy_len < space_left:
                         raise sd.CallbackStop()

                position += chunk_len

            # Start Stream
            self.stream = sd.OutputStream(
                samplerate=fs,
                device=self.device_id,
                channels=channels,
                callback=callback,
                latency='high' # Increase latency to prevent underflow
            )
            self.stream.start()
            print(f"[InnerMusicManager] Playing: {key} (Delay: {INNER_BGM_DELAY}s, Rate: {fs}Hz)")

        except Exception as e:
            print(f"[InnerMusicManager] Error playing {key}: {e}")

    def stop(self):
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"[InnerMusicManager] Error stopping: {e}")
            finally:
                self.stream = None
