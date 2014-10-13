#!/usr/bin/env python3
# Replay Recorder
# Allows for the creation of replays.

import traceback

from atbp.replays.recorder import ReplayRecorder

def record_replay():
    """
        Starts recording a new replay.
    """
    
    # Get the replay path.
    replay_path = input("Please enter the replay file's path (default: replay.atbp): ")
    if not replay_path:
        replay_path = "replay.atbp"
    
    # Start recording.
    recorder = ReplayRecorder(replay_path, True)
    print("Recorder started. Recording will begin once you enter a match.")
    try:
        recorder.run()
    except KeyboardInterrupt:
        print("Recording stopped. Close the window to stop recording.")
    print("Replay saved to " + replay_path)

def main():
    try:
        record_replay()
    except:
        traceback.print_exc()
    finally:
        input("Press Enter to exit.")
    
if __name__ == "__main__":
    main()