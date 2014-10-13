ATBP-Tools
==========

**ATBP-Tools** is a suite of tools for use with [Adventure Time Battle Party](http://www.cartoonnetwork.com/games/adventuretime/adventure-time-battle-party/).

License: [WTFPL](http://www.wtfpl.net/) for the code; images are the property of Cartoon Network.

Tools
-----

These are the tools which have currently been developed:

* **Replay Player**: a web application for playing back replays. There is a demo available [here](http://lyros.net/atbp/replay_player_demo2/) (note that you can use the demo to play back any replay file, not just the demo replay).
* **Replay Recorder**: records matches for viewing later on the Replay Player. *Only available for Windows.*
* **Sounds Downloader**: downloads all known files to disk.

Installation
------------

*The Replay Recorder currently only works on Windows. If this is all you're looking for, consult the [Releases](https://github.com/Lyrositor/ATBP-Tools/releases) page.*

You'll need [Python 3.4](https://www.python.org/) (for convenience, make sure you select the option to install it to your PATH) as a base and the [latest version of ATBP-Tools](https://github.com/Lyrositor/ATBP-Tools/archive/master.zip). If you want to use the Replay Recorder, you'll also need [pydivert](https://github.com/ffalcinelli/pydivert) and [PyYAML](http://pyyaml.org/wiki/PyYAML). Then, launch the files in the `tools/` subdirectory to run the tools.

Known Bugs
----------

The following bugs are known; please don't report them unless you think you have information that can be used to fix them:

* **Replay Player:**
    * Champions and other creatures will jitter occasionally on-screen.