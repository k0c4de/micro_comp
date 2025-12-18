import vlc
import os
import time
from config import VIDEO_FILES

class VideoManager:
    def __init__(self):
        # Initialize VLC instance
        # --no-xlib is often recommended for Linux/Pi to avoid threading issues with X11
        self.instance = vlc.Instance("--no-xlib --quiet")
        self.player = self.instance.media_player_new()
        self.player.set_fullscreen(True)
        
        self.current_key = None
        self.is_looping = False
        self.finished = False
        
        # Setup Event Callback
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end_reached)

    def _on_end_reached(self, event):
        """Callback when video finishes."""
        # print("Video finished event received.")
        if self.is_looping:
            # If looping, restart the video
            # Note: This might have a slight gap. 
            # For seamless looping, one might need a playlist or specific VLC options.
            # But re-playing here is the simplest logic.
            # We need to do this in a thread-safe way or just let the main loop handle it?
            # Calling play() from callback might be risky in some VLC versions.
            # Safer to set a flag and let the main loop restart it, 
            # OR use media options for looping.
            pass 
        self.finished = True

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
