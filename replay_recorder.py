#!/usr/bin/env python3
# ATBP Tools - Replay Recorder
# Sniffs network traffic for ATBP packets, and stores them in a replay format.

from replays import ReplayCreator

def main():
    """
        Listens for game network data and saves it in the replay format.
    """

    sniffer = ReplayCreator()
    print("Running...")
    try:
        sniffer.run()
    except KeyboardInterrupt:
        print("\r    ")
    
    # Wait for the user to exit.
    print("Complete.")
    input("Press Enter to exit...")
    
if __name__ == "__main__":
    main()