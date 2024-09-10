import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# List of expected files in the folder
CAPTIONS_FILE = "captions.csv"
CAPTIONS_MOD_FILE = "captions_ytp.csv"
CAPTIONS_ORIG_FILE = "captions_original.csv"

LOCALE_FILE = "locale.csv"
LOCALE_MOD_FILE = "locale_ytp.csv"
LOCALE_ORIG_FILE = "locale_original.csv"

VIDEO_FOLDER = "video"
VIDEO_MOD_FOLDER = "video_ytp"
VIDEO_ORIG_FOLDER = "video_original"

GAME_EXE = "Arzette.exe"

# Files to be included in the compiled exe. Check frozen attr so that the script still works outside of pyinstaller
if getattr(sys, 'frozen', False):
    BACKGROUND_IMAGE_PATH = os.path.join(sys._MEIPASS, "files/Logo.png")
else:
    BACKGROUND_IMAGE_PATH = "files/Logo.png"

if getattr(sys, 'frozen', False):
    ICON_PATH = os.path.join(sys._MEIPASS, "files/favicon.ico")
else:
    ICON_PATH = "files/favicon.ico"
    
# Check for file access
def has_permission(path):
    try:
        # Poke the file
        if os.path.isfile(path):
            with open(path, 'r+'):
                pass
        # We currently don't need to check folders. It's all in the same directory, so we only need to poke one file. Leaving the functionality in for future reference
        elif os.path.isdir(path):
            return os.access(path, os.W_OK)
        return True
    except PermissionError:
        return False

# If access denied and not admin, that's probably the issue
def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("Error", "Access to the game folder, or one of the important game files, has been denied. Please run the mod manager as an administrator, or move the game folder somewhere else, like your desktop.\n\nIf all else fails, you can always install the mod manually. Check the installation page for instructions.")
    else: return

# Check for the files we're going to be modifying
def check_base_files():
    if not (os.path.exists(CAPTIONS_FILE) and 
            os.path.exists(LOCALE_FILE) and 
            os.path.exists(VIDEO_FOLDER)):
        messagebox.showerror("Error", "One or more expected files/folders for the game weren't found.\n\nAre you running the mod manager in Arzette's folder? It should be in the same place as the exe, along with whichever version of the mod you chose.")
        return False
    return True

# Check if the mod is enabled or disabled by looking at the inactive file names
def mod_enabled():
    return (os.path.exists(CAPTIONS_ORIG_FILE) and 
            os.path.exists(LOCALE_ORIG_FILE) and 
            os.path.exists(VIDEO_ORIG_FOLDER))

# Make sure Farcette exists in the folder
def check_for_mod():
    if not (os.path.exists(CAPTIONS_MOD_FILE) and 
            os.path.exists(LOCALE_MOD_FILE) and 
            os.path.exists(VIDEO_MOD_FOLDER)):
        messagebox.showerror("Error", "Critical files for the Farcette mod couldn't be found. Please reinstall the mod, or move the game to a different location on your computer.\nIf all else fails, check to see if your antivirus is interfering with the mod manager.")
        return False
    return True

# Make sure backups exist in the folder
def check_for_backups():
    if not (os.path.exists(CAPTIONS_ORIG_FILE) and 
            os.path.exists(LOCALE_ORIG_FILE) and 
            os.path.exists(VIDEO_ORIG_FOLDER)):
        messagebox.showerror("Error", "The original files for Arzette can no longer be found, rendering your game permanently pooped.\n\nIf you installed through Steam, you can restore your game by verifying the game files. Otherwise, please reinstall the game.")
        return False
    return True

# We do this
def enable_mod():
    if not check_base_files():
        return
    if not check_for_mod():
        return
    if not has_permission(CAPTIONS_FILE):
        run_as_admin()

    try:
        if os.path.exists(CAPTIONS_FILE) and os.path.exists(CAPTIONS_MOD_FILE):
            os.rename(CAPTIONS_FILE, CAPTIONS_ORIG_FILE)
            os.rename(CAPTIONS_MOD_FILE, CAPTIONS_FILE)

        if os.path.exists(LOCALE_FILE) and os.path.exists(LOCALE_MOD_FILE):
            os.rename(LOCALE_FILE, LOCALE_ORIG_FILE)
            os.rename(LOCALE_MOD_FILE, LOCALE_FILE)

        if os.path.exists(VIDEO_FOLDER) and os.path.exists(VIDEO_MOD_FOLDER):
            os.rename(VIDEO_FOLDER, VIDEO_ORIG_FOLDER)
            os.rename(VIDEO_MOD_FOLDER, VIDEO_FOLDER)

        messagebox.showinfo("Success", "Mod enabled successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable mod: {e}\n\nTry moving the game somewhere else, like your desktop. If all else fails, you can always install the mod manually. Check the installation page for instructions.")
    update_buttons()

# We don't do this
def disable_mod():
    if not check_base_files():
        return
    if not has_permission(CAPTIONS_FILE):
        run_as_admin()

    try:
        if os.path.exists(CAPTIONS_ORIG_FILE) and os.path.exists(CAPTIONS_FILE):
            os.rename(CAPTIONS_FILE, CAPTIONS_MOD_FILE)
            os.rename(CAPTIONS_ORIG_FILE, CAPTIONS_FILE)

        if os.path.exists(LOCALE_ORIG_FILE) and os.path.exists(LOCALE_FILE):
            os.rename(LOCALE_FILE, LOCALE_MOD_FILE)
            os.rename(LOCALE_ORIG_FILE, LOCALE_FILE)

        if os.path.exists(VIDEO_ORIG_FOLDER) and os.path.exists(VIDEO_FOLDER):
            os.rename(VIDEO_FOLDER, VIDEO_MOD_FOLDER)
            os.rename(VIDEO_ORIG_FOLDER, VIDEO_FOLDER)

        messagebox.showinfo("Success", "Mod disabled successfully!\n\nIf you want to uninstall Farcette entirely, please run the uninstaller.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable mod: {e}\n\nIf this process worked before from a different location, try moving it back. If the error persists, you can manually restore your game by putting the original files back in place yourself. They should be in the root of your game folder, ending with '_original'.\n\nYou can also just reinstall the game.")
    update_buttons()

#Run Arzette from the mod manager. In the event of an error, make it clear that running the game through the manager isn't required
#Worth noting: Steam API files existing in the Arzette directory makes booting up the game this way take a decent amount of time. If you're testing the script, consider temporarily removing these files
def play_game():
    try:
        os.startfile(GAME_EXE)
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the game: {e}\n\nNote that you don't HAVE to run the game from here. If enabling the mod still succeeded, just run the game like normal. You'll know real fast if the mod's working or not. Trust me.")

# Update button states based on whether or not the mod is enabled
def update_buttons():
    if mod_enabled():
        enable_button.config(state="disabled")
        disable_button.config(state="normal")
    else:
        enable_button.config(state="normal")
        disable_button.config(state="disabled")

# Set up the window
def create_gui():
    window = tk.Tk()
    window.title("Farcette Mod Manager")
    
    window.iconbitmap(ICON_PATH)
    
    # I don't know how to make good windows sorry :(
    window.geometry("854x480")
    window.resizable(False, False)
    
    # The title drop from the installation video makes for a great background
    bg_image = Image.open(BACKGROUND_IMAGE_PATH)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    canvas = tk.Canvas(window, width=854, height=480)
    canvas.pack(fill="both", expand=True)
    
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    global enable_button, disable_button

    # Set up the buttons
    enable_button = tk.Button(window, text="Enable Mod", command=enable_mod)
    disable_button = tk.Button(window, text="Disable Mod", command=disable_mod)
    play_button = tk.Button(window, text="PLAY", height=5, width=20, command=play_game)
    
    # Place the buttons based on negative space in the background
    canvas.create_window(540, 280, anchor="nw", window=enable_button)
    canvas.create_window(640, 280, anchor="nw", window=disable_button)
    canvas.create_window(555, 320, anchor="nw", window=play_button)

    update_buttons()

    window.mainloop()

# Main entry point
if __name__ == "__main__":
    create_gui()
