#!/usr/bin/env python3
# ATBP-Tools
# Setup script for the tools
# Make sure you have a lib/ folder with the required folders before running
# the setup.

from setuptools import setup, find_packages
import glob
import os
import platform
import py2exe
import sys

if sys.maxsize > 2**32:
    ARCH="x64"
    LIB = [
        "lib/x64/vcredist_x64.exe",
        "lib/x64/WinDivert.dll",
        "lib/x64/WinDivert64.sys"
    ]
else:
    ARCH="x86"
    LIB = [
        "lib/x86/vcredist_x86.exe",
        "lib/x86/WinDivert.dll",
        "lib/x86/WinDivert32.sys",
    ]

VERSION = "1.0"

setup(
    name="ATBP-Tools",
    description="A collection of tools for use with Adventure Time Battle Party.",
    author="Lyrositor",
    version=VERSION,
    license="WTFPL",
    url="https://github.com/Lyrositor/ATBP-Tools",

    packages=find_packages(exclude="tools"),
    install_requires=["pydivert", "PyYAML"],
    
    console=["tools/replay_recorder.py", "tools/sounds_downloader.py"],
    options={"py2exe": {"bundle_files": 1, "optimize": 2}},
    zipfile=None,
    
    data_files=[
        ("", ["LICENSE.txt", "README.md"] + LIB),
        (
            os.path.join("atbp", "data"),
            glob.glob(os.path.join("atbp", "data", "*.txt"))
        )
    ]
)

input("Press Enter to exit.")