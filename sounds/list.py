# ATBP Tools
# Formats a list of sounds and outputs it.

from data import *

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
            markdown += "{}* [{}]({})\n".format("  " * (level - 1), i, SOUNDS_URL.format(parent + item))

    if not files:
        markdown += format_tree(tree["."], level + 1, True, parent)

    return markdown