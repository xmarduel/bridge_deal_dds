# Bridge deal generator with double dummy solver

A small python based program (GUI: PySide6)

The deals can be generated from so-called "templates" where for each hand (N/S/E/W) the following constraints can be specified

- specific cards
- number of points (or -1 for no constraint on points)
- distribution (for each color the number of cards or -1 for no constraints on the number of cards)

After a deal generation, the dds ("analyse") is called.
The double dummy solver is the one given by

- https://github.com/dds-bridge/dds

The source files are duplicated here, and there is a small python wrapper on it

# Python dependencies

- PySide6 (6.6.3)
- jinja2
- colorama

# Installation

Install all the source in a folder of your choice. Set a new environment variable "BRIDGE_DDS" to this installation folder. It contains, among others, the folders

- DDS
- DDS_WRAPPER
- DDS_DEAL_APP

Add the full path of the DDS_WRAPPER folder to your PYTHONPATH environment variable.

From the installation folder, cd to DDS_DEAL_APP and type:

> python bridgeUI.py

The GUI pops-up. The default template is loaded and push the button "Generate". But the DDS will certainly not work out of the box! Read the following.

# Windows - DDS

The dds.dll has to be properly loaded, i.e. the windows "Path" environment variable must contain the path to the MinGW standard libs. It has to be "%MINGW_HOME%\\bin",
where MINGW_HOME is the environment variable where your MinGW is installed:

To install MinGW, perform the following steps: from

- https://github.com/niXman/mingw-builds-binaries/releases

download and install the following package

- x86_64-13.2.0-release-win32-seh-msvcrt-rt_v11-rev0.7z

into the folder C:\MinGW64 for example (create it if neccessary). So in this example, MINGW_HOME is "C:\MinGW64\mingw64". Add the folder "C:\MinGW64\mingw64\bin" to your "Path" environment variable.

If you wish to compile the DDS library on your own, the make utility is needed: look for

- make-3.81-bin.zip
- make-3.81-dep.zip

Install them in C:\MinGW64\mingw-make and add this folder to your "Path" environment variable as well.

You are ready to compile de DDS source:

> cd DDS

> make

Then copy the resulting dds.dll and libdds.a into the DDS_WRAPPER folder.

# Apple - DDS

The dds.so has to be properly loaded. **_ TO COMPLETE _**

# Linux - DDS

Not even tried...
