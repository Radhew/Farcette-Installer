# Farcette Installer
This is an automatic installer for DaThings's YouTube Poop mod for Arzette: The Jewel of Faramore. The normal process of installing isn't hard at all, but I figured it was a nice excuse to make a neat little mod manager for it.

### This is an unofficial, fanmade installer for the mod. Please do not bother DaThings about issues you may have when using the installer/manager. Instead, please use this page's issue tracker!

## Compiling
The mod manager itself is just a python script compiled with PyInstaller. It's been written to work both by compiling it that way, or running the script itself. Pillow is the only required dependency, along with the "files" folder. To add it to your python installation, use this command: ``pip install Pillow``

The installer is made with Inno Setup. When compiling, make sure to include all files in the project as they are in this repo. They're basically all (minus the readme.md) required.

Note: unzip.exe is a simple commandline extraction utility from StahlWorks. You can find it [here.](http://stahlworks.com/zip)
