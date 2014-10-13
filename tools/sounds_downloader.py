#!/usr/bin/env python3
# Sounds Downloader
# Downloads all known sound files.

import traceback

from atbp.data import *
from atbp.resources.sounds import *

URLS = get_data("urls")

def output_sounds_list(sounds_list, output_path):
    """
        Formats the provided sounds list and outputs it.
    """

    # Convert the sound names to a simple tree-like structure.
    tree = {}
    for sound in sounds_list:
        bits = sound.split("/")
        folder = tree
        for b in bits[:-1]:
            if b not in folder:
                folder[b] = {}
            folder = folder[b]
        if "." not in folder:
            folder["."] = []
        folder["."].append(bits[-1])

    # Format the tree structure in Markdown.
    markdown = format_tree(tree)
    try:
        with open(output_path, "w") as f:
            f.write(markdown)
    except (IOError, OSError):
        print("Failed to write the list of URLs.")

def format_tree(tree, level=0, files=False, parent=""):
    """
        Formats a file tree-like structure.
    """

    markdown = ""

    for item in sorted(tree):
        if item == ".":
            continue
        i = item.replace("_", "\_")  # Sanitize the name for Markdown.
        if not files:
            markdown += "  " * level + "* **" + i + "**\n"
            markdown += format_tree(tree[item], level + 1, False, parent + item + "/")
        else:
            markdown += "{}* [{}]({})\n".format("  " * (level - 1), i, URLS["root"] + URLS["sounds"].format(parent + item))

    if not files:
        markdown += format_tree(tree["."], level + 1, True, parent)

    return markdown

def sounds_downloader():
    # Prompt the user for the download folder path.
    download_path = input("Please enter the download folder path (default: ATBP_sounds): ")
    if not download_path:
        download_path = "ATBP_sounds"

    # Prompt the user for the option to output a Markdown list of files.
    i = input("Output list of sounds (Y/N)? ")
    output_list = i in ("Y", "y", "yes", "YES", "Yes")
    if output_list:
        list_path = input("Please enter the sounds list's path (default: ATBP_sounds_list.md): ")
        if not list_path:
            list_path = "ATBP_sounds_list.md"

    # Get a list of sound files.
    print("Loading sounds list...")
    sounds_list = get_all_sounds()
    if output_list:
        print("Writing sounds list...")
        output_sounds_list(sounds_list, list_path)

    # Download them all.
    print("Downloading sounds...")
    download_sounds(sounds_list, download_path)

    print("Complete.")

def main():
    try:
        sounds_downloader()
    except:
        traceback.print_exc()
    finally:
        input("Press Enter to exit.")

if __name__ == "__main__":
    main()