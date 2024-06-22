# Bridge deal generator with double dummy solver

A small python based program (GUI: PySide6)

The deals can be generated from so-called "templates" where for each hand (N/S/E/W) the following constraints can be specified
  - specific cards
  - number of points (or -1 for no constraint on points)
  - distribution (for each color the number of cards or -1 for no constraints on the number of cards)

After a deal generation, the dds ("analyse") is called.
The double dummy solver is the one given by xxx.

Windows
=======

The dds.dll has to be properly loaded, i.e. the windows "path" environment variable must contain the path to the mingw64 standard libs. It has to be "C:\\MinGW64\\mingw64\\bin". 

The DDS library has been compiled from sources in linked with these libraries (DDS source files are also given). 
In case of you do not have these libraries in this path, you won't be able to utilise the DDS analyser.

To compile on your own the dss.dll, you have to install MinGW. I got it from
- https://github.com/niXman/mingw-builds-binaries/releases

and downloaded/installed (in C:\\MinGW64) the x86_64-13.2.0-release-win32-seh-msvcrt-rt_v11-rev0.7z package. 
The DDS was compiled without the boost library to avoid extra dependencies.

The make utility was also needed: look for
- make-3.81-bin.zip
- make-3.81-dep.zip

Apple
=====

The dds.so has to be properly loaded.  *** TO COMPLETE ***


