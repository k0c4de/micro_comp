import sounddevice as sd
import soundfile as sf
import os
import numpy as np
from config import BGM_FILES, DEVICE_ID_BLUETOOTH

class OuterMusicManager:
    def __init__(self):
        self.stream = None
        self.device_id = DEVICE_ID_BLUETOOTH
        print(f"[OuterMusicManager] Initialized with Device ID: {self.device_id}")

    def play(self, key):
        """
        Play audio file associated with key on the Bluetooth device.
        """
        path = BGM_FILES.get(key)
        if not path:
            # It's okay if some keys don't have BGM (e.g. S0)
            return
            
        if not os.path.exists(path):
            print(f"[OuterMusicManager] File not found: {path}")
            return

        # Stop any currently playing audio
        self.stop()

        try:
            # Read file
            data, fs = sf.read(path, dtype='float32')
            
            # Handle mono/stereo
            channels = data.shape[1] if data.ndim > 1 else 1
            
            # Define callback for stream
            # We use a closure to keep track of position
            position = 0
            
            def callback(outdata, frames, time, status):
                nonlocal position
                if status:
                    print(f"[OuterMusicManager] Stream Status: {status}")
                
                chunk_len = len(outdata)
                if position + chunk_len > len(data):
                    # End of file
                    remaining = len(data) - position
                    outdata[:remaining] = data[position:]
                    outdata[remaining:] = 0
                    raise sd.CallbackStop() # Stop stream
                else:
                    outdata[:] = data[position:position + chunk_len]
                    position += chunk_len

            # Start Stream
            self.stream = sd.OutputStream(
                samplerate=fs,
                device=self.device_id,
                channels=channels,
                callback=callback
            )
            self.stream.start()
            print(f"[OuterMusicManager] Playing: {key}")

        except Exception as e:
            print(f"[OuterMusicManager] Error playing {key}: {e}")

    def stop(self):
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"[OuterMusicManager] Error stopping: {e}")
            finally:
                self.stream = None
