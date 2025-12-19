import vlc
import os
import time
from config import VIDEO_FILES, DEVICE_ID_HEADPHONE, DEVICE_NAME_HEADPHONE, VIDEO_VOLIME, TARGET_SAMPLE_RATE

class VideoManager:
    def __init__(self):
        # Initialize VLC instance
        # --no-xlib is often recommended for Linux/Pi to avoid threading issues with X11
        self.instance = vlc.Instance("--no-xlib --quiet")
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(int(VIDEO_VOLIME * 100))
        # self.player.set_fullscreen(True) # [DEMO] enable this while demo
        
        # Set Audio Output Device
        self.audio_device_id = None
        self._set_audio_output()
        
        self.current_key = None
        self.is_looping = False
        self.finished = False
        
        # Setup Event Callback
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end_reached)

    def _set_audio_output(self):
        """
        Attempt to set the audio output device based on DEVICE_NAME_HEADPHONE.
        """
        try:
            mods = self.player.audio_output_device_enum()
            if mods:
                target_device = None
                found_devices = []
                
                current = mods
                while current:
                    dev_id = current.contents.device
                    dev_desc = current.contents.description.decode('utf-8') if current.contents.description else ""
                    found_devices.append((dev_id, dev_desc))
                    
                    # Check for name match
                    if DEVICE_NAME_HEADPHONE.lower() in dev_desc.lower():
                        target_device = dev_id
                    
                    current = current.contents.next
                
                vlc.libvlc_audio_output_device_list_release(mods)
                
                if target_device:
                    print(f"[VideoManager] Setting Audio Device to: {target_device}")
                    self.audio_device_id = target_device
                    self.player.audio_output_device_set(None, target_device)
                else:
                    print(f"[VideoManager] Warning: Device matching '{DEVICE_NAME_HEADPHONE}' not found.")
                    print(f"[VideoManager] Available devices: {found_devices}")
                    # Fallback to default (don't set anything, let VLC decide)
            else:
                print("[VideoManager] No audio output devices found.")
                
        except Exception as e:
            print(f"[VideoManager] Error setting audio device: {e}")

    def _on_end_reached(self, event):
        """Callback when video finishes."""
        # print("Video finished event received.")
        if self.is_looping:
            # Restart video
            # We need to be careful calling play from callback. 
            # A safer way is to set time to 0 and play.
            # Or just let the main loop handle it if we expose 'finished' and 'is_looping'
            # But here we want seamless-ish looping.
            
            # Option 1: Seek to 0 and play (might work)
            # self.player.set_media(self.player.get_media())
            # self.player.play()
            
            # Option 2: Just set finished = True and let GameManager restart it? 
            # That causes a black blink.
            
            # Option 3: Use VLC's input-repeat option (better done at init or media creation)
            # But we want to toggle looping per video.
            
            # Let's try seeking to start.
            # Note: This callback is from a different thread.
            pass
            
        self.finished = True

    def check_status(self):
        """
        Check if video is finished.
        If looping and finished, restart it.
        """
        if self.finished:
            if self.is_looping:
                self.player.set_position(0.0)
                self.player.play()
                self.finished = False
                return False
            return True
        return False

    def play(self, video_key, loop=False):
        """
        Play a video by key defined in config.
        """
        path = VIDEO_FILES.get(video_key)
        if not path:
            print(f"[VideoManager] Error: Key '{video_key}' not found in config.")
            return
        
        if not os.path.exists(path):
            print(f"[VideoManager] Error: File not found at {path}")
            return

        print(f"[VideoManager] Playing: {video_key} (Loop: {loop})")
        
        self.current_key = video_key
        self.is_looping = loop
        self.finished = False
        
        media = self.instance.media_new(path)
        self.player.set_media(media)
        
        # Re-apply audio device to ensure it persists across videos
        if self.audio_device_id:
            self.player.audio_output_device_set(None, self.audio_device_id)
            
        self.player.play()

        self.is_looping = loop
        self.finished = False

        media = self.instance.media_new(path)
        
        if loop:
            # Add option to loop indefinitely
            media.add_option("input-repeat=65535")
        
        self.player.set_media(media)
        self.player.play()
        
        # Wait a bit for it to start
        time.sleep(0.1)

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def check_status(self):
        """
        Call this in the main loop to check status.
        Returns True if the current video has finished (and is not looping).
        """
        # If looping, it never "finishes" in the sense of moving to next state
        if self.is_looping:
            return False
            
        # Check if finished flag was set by callback
        if self.finished:
            return True
            
        # Double check with player state (sometimes callback is missed)
        state = self.player.get_state()
        if state == vlc.State.Ended:
            self.finished = True
            return True
            
        return False
