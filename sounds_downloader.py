#!/usr/bin/env python3
# ATBP Tools - Sounds Downloader
# Downloads all the available sounds from ATBP and (optionally) lists them.

from data import *
from sounds import *

SOUNDS_LIST_FILE = "ATBP_sounds_list.md"
SOUNDS_OUTPUT_DIR = "ATBP_sounds"

def main():
    """
        Fetches as complete a list of sounds it can and downloads them.
        
        Optionally creates a Markdown list of sounds.
    """

    # Prompt the user for the option to output a Markdown list of files.
    i = input("Output list of sounds (Y/N)? ")
    output_list = i in ("Y", "y", "yes", "YES", "Yes")
    
    # Run the program.
    print("Loading sounds list...")
    sounds_list = set(
        get_sounds_list(read_list_file("definitions")) +
        read_list_file("other_sounds")
    )
    if output_list:
        print("Writing sounds list...")
        output_sounds_list(sounds_list, SOUNDS_LIST_FILE)
    print("Saving sounds list...")
    download_sounds(sounds_list, SOUNDS_OUTPUT_DIR)
    
    # Wait for the user to exit.
    print("Complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()