#!/usr/bin/env python3
# Replay Client
# Allows for the creation and playback of replays.

import sys
sys.path.append("..")

import traceback

from atbp.replays.recorder import ReplayRecorder
    

def record_replay(replay_path):
    """
        Starts recording a new replay.
    """
    
    recorder = ReplayRecorder(replay_path, True)
    print("Recorder started. Recording will begin once you enter a match.")
    try:
        recorder.run()
    except KeyboardInterrupt:
        print("Recording stopped.")
    print("Replay saved to " + replay_path)

def main():
    replay_path = input("Please enter the replay file's path (default: replay.atbp): ")
    if not replay_path:
        replay_path = "replay.atbp"
    record_replay(replay_path)

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit.")