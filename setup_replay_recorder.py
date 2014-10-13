#!/usr/bin/env python3
# ATBP-Tools
# Setup script for the Replay Recorder.
# Make sure you have a lib/ folder with the required folders before running
# the setup.

from distutils.core import *
import os.path
import platform
import py2exe
import sys

sys.argv.append("py2exe")

if sys.maxsize > 2**32:
    lib = [
        "lib/x64/vcredist_x64.exe",
        "lib/x64/WinDivert.dll",
        "lib/x64/WinDivert64.sys"
    ]
else:
    lib = [
        "lib/x86/vcredist_x86.exe",
        "lib/x86/WinDivert.dll",
        "lib/x86/WinDivert32.sys",
    ]

setup(
    name="ReplayRecorder",
    description="Adventure Time Battle Party Replay Recorder",
    author="Lyrositor",
    version="1.0",
    license="WTFPL",

    packages=["atbp"],
    package_dir={
        "atbp": "atbp"
    },
    package_data={
        "atbp": ["atbp/data/*.txt"]
    },
    
    console=["tools/replay_recorder.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None,
    
    data_files=[
        ("", ["LICENSE.txt", "README.md"] + lib),
    ]
)

input("Press Enter to exit.")