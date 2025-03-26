import glob
import os
import sys
from queue import Queue
import threading
import time
from colorama import Fore, init
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import pygame 
<<<<<<< Updated upstream
=======
import subprocess
import psutil  # Add this to your imports
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores files there
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize pygame mixer
pygame.mixer.init()

# Function for typewriting effect
def type_writer(text, color, delay=0.015):
    for char in text:
        sys.stdout.write(f"{color}{char}{Fore.RESET}")
        sys.stdout.flush()
        sleep(delay)
    print("\n")


# Update the sound file paths
sound_path = resource_path("build/spidy/mound/assets")  # Correct relative path

# Use os.path.join to build the full paths
spidy_sound = os.path.join(sound_path, "spidy_sound.mp3")
wake_up_spidy = os.path.join(sound_path, "wake_up_spidy.mp3")
start = os.path.join(sound_path, "start.mp3")
middle = os.path.join(sound_path, "middle.mp3")
dady_home = os.path.join(sound_path, "dady_home.mp3")
spidy_online = os.path.join(sound_path, "spidy_online.mp3")
hacker_mode = os.path.join(sound_path, "hacker_mode.mp3")
voice_mode = os.path.join(sound_path, "voice_mode.mp3")
notify_sound = os.path.join(sound_path, "xnotify.mp3")


# Loader class to provide animation during the search
class Loader:
    def __init__(self, desc="Searching...", end="  Search Completed ✅", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

# Function to search for files with specified extensions
def spidy_lens_search_drive(query, drive, extensions, found_items, progress_queue, lock):
    total_items = 0
    files = []
    for ext in extensions:
        search_pattern = f"{drive}**/*{ext}"
        files.extend(glob.glob(search_pattern, recursive=True))
    total_items = len(files)
    
    # After counting files, push the total number of items to progress queue
    with lock:
        progress_queue.put(0)  # Start animation with 0 progress
        progress_queue.put(total_items)  # Set the total count for progress
    
    for file in files:
        if query.lower() in os.path.basename(file).lower():
            found_items.append(file)
        with lock:
            progress_queue.put(1)  # Increment progress for each file processed

# Main Search Function
def spidy_lens_search(query, extensions):
    drives = ['C:\\', 'D:\\', 'E:\\']
    found_items = []
    lock = threading.Lock()
    progress_queue = Queue()
    threads = []
    total_items = 0

    # Start search threads for each drive
    for drive in drives:
        thread = threading.Thread(target=spidy_lens_search_drive, args=(query, drive, extensions, found_items, progress_queue, lock))
        threads.append(thread)
        thread.start()
        total_items += 1  # Increase total_items for each drive processed

    # Start animation thread
    with Loader(f"Searching for '{query} {extensions}' on all drives..."):
        # Wait for threads to finish
        for thread in threads:
            thread.join()

    return found_items

# Updated play_sound function to match spidy.py
# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Main Function
def spidy_lens():
    sys.stdout.write("\r\n")
    sys.stdout.write("\r\n")
    welcome_message = (
            "╔══════════════════════ SPIDY LENS™ ══════════════════════╗\n"
            "║                                                         ║\n"
            "║            Welcome to Your Smart File Finder!           ║\n"
            "║       ──────── Type 'close lens' to exit ────────       ║\n"
            "║                                                         ║\n"
            "╚═════════════════════════════════════════════════════════╝"
        )
    type_writer(welcome_message, Fore.GREEN)  # Let type_writer apply the color
    sys.stdout.write("\r\n")

    while True:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        file_ext = input(f"{Fore.CYAN}Enter the file extension 🕷️: {Fore.RESET}")
        if file_ext.lower() == "close lens":
            type_writer("Closing SPIDY LENS...", Fore.RED)
            break
        
        query = input(f"{Fore.CYAN}Enter the file name or keyword: {Fore.RESET}")
        if query.lower() == "close lens":
            type_writer("Closing SPIDY LENS...", Fore.RED)
            break

        type_writer(f"Searching for '{query}' files with extension '{file_ext}'...", Fore.YELLOW)
=======
        # Input validation for file extension
        while True:
            file_ext = input(f"{Fore.CYAN}  🕷️ Enter the file extension : {Fore.RESET}").strip()
            if file_ext.lower() == "close lens":
                sys.stdout.write("\r\n")
                type_writer("  Closing SPIDY LENS...", Fore.RED)
                return
            if file_ext:
                break
            type_writer("Please enter a valid file extension!", Fore.RED)
            sys.stdout.write("\r\n")

=======
        # Input validation for file extension
        while True:
            file_ext = input(f"{Fore.CYAN}  🕷️ Enter the file extension : {Fore.RESET}").strip()
            if file_ext.lower() == "close lens":
                sys.stdout.write("\r\n")
                type_writer("  Closing SPIDY LENS...", Fore.RED)
                return
            if file_ext:
                break
            type_writer("Please enter a valid file extension!", Fore.RED)
            sys.stdout.write("\r\n")

>>>>>>> Stashed changes
        # Input validation for file name/keyword
        while True:
            query = input(f"{Fore.CYAN}  🕷️ Enter the file name or keyword : {Fore.RESET}").strip()
            if query.lower() == "close lens":
                type_writer("Closing SPIDY LENS...", Fore.RED)
                return
            if query and len(query) >= 1:
                break
            type_writer("Please enter a valid file name or keyword (at least 1 character)!", Fore.RED)
            sys.stdout.write("\r\n")

        type_writer(f"  Searching for '{query}' files with extension '{file_ext}'... ", Fore.YELLOW)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        found_items = spidy_lens_search(query, [file_ext])

        sys.stdout.write("\r\n")
        if found_items:
            thread1 = threading.Thread(target=play_sound, args=(notify_sound,))
            thread1.start()
            
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            type_writer(f"Found {len(found_items)} results:", Fore.GREEN)
            for item in found_items:
                print(item)
=======
=======
>>>>>>> Stashed changes
            type_writer(f"  Found {len(found_items)} results 🕷️:", Fore.GREEN)
            for idx, item in enumerate(found_items, 1):
                print(f"  {idx}. {item}")  # Indent results for alignment
                sys.stdout.write("\r\n")
                
                # Improved UI with consistent spacing and alignment
                action_prompt = (
                    f"{Fore.MAGENTA}┌─ Options for '{os.path.basename(item)}' 🕷️ ───────────────\n"  # Header with border
                    f"{Fore.YELLOW}│  [1] Open File          [2] Open Location          [3] Skip\n"  # Single-item options
                    f"{Fore.GREEN}│  [4] Open All Files     [5] Open All Locations     [6] Skip All\n"  # All-item options
                    f"{Fore.GREEN}│  [7] Close Lens\n"  # All-item options
                    f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────────\n"  # Footer border
                    f"{Fore.CYAN}  Enter your choice: "  # Prompt aligned with options
                )
                action = input(action_prompt + Fore.RESET).strip()

                if action == '1':  # Open single file
                    try:
                        if os.name == 'nt':  # Windows
                            os.startfile(item)
                        elif os.name == 'posix':  # Linux or macOS
                            subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', item])
                        type_writer(f"Opening '{item}'...", Fore.YELLOW)
                    except Exception as e:
                        type_writer(f"Error opening file: {e}", Fore.RED)
                elif action == '2':  # Open single location
                    try:
                        dir_path = os.path.dirname(item)
                        if os.name == 'nt':  # Windows
                            os.startfile(dir_path)
                        elif os.name == 'posix':  # Linux or macOS
                            subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', dir_path])
                        type_writer(f"Opening location of '{item}'...", Fore.YELLOW)
                    except Exception as e:
                        type_writer(f"Error opening location: {e}", Fore.RED)
                elif action == '3':  # Skip single item
                    type_writer("Skipping...", Fore.CYAN)
                elif action == '4':  # Open all files
                    for all_item in found_items:
                        try:
                            if os.name == 'nt':
                                os.startfile(all_item)
                            elif os.name == 'posix':
                                subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', all_item])
                            type_writer(f"Opening '{all_item}'...", Fore.YELLOW)
                        except Exception as e:
                            type_writer(f"Error opening file: {e}", Fore.RED)
                    break  # Exit loop after processing all
                elif action == '5':  # Open all locations
                    for all_item in found_items:
                        try:
                            dir_path = os.path.dirname(all_item)
                            if os.name == 'nt':
                                os.startfile(dir_path)
                            elif os.name == 'posix':
                                subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', dir_path])
                            type_writer(f"Opening location of '{all_item}'...", Fore.YELLOW)
                        except Exception as e:
                            type_writer(f"Error opening location: {e}", Fore.RED)
                    break  # Exit loop after processing all
                elif action == '6':  # Skip all remaining items
                    type_writer("  Skipping all remaining items...", Fore.CYAN)
                    type_writer(" All found locations:", Fore.GREEN)
                    for idx, all_item in enumerate(found_items, 1):  # Start numbering from 1
                        print(f"  {idx}. {all_item}")  # Numbered and indented
                    sys.stdout.write("\r\n")  # Extra line after locations
                    f"{Fore.MAGENTA}──────────────────────────────────────────────────────────\n"  # Footer border
                    break  # Exit loop without further processing
                elif action == '7':  # Close lens
                    type_writer(" Closing SPIDY LENS...", Fore.RED)
                    return
                else:  # Invalid input defaults to skip
                    type_writer("Invalid option, skipping...", Fore.CYAN)
                sys.stdout.write("\r\n")
>>>>>>> Stashed changes
        else:
            type_writer(f"No results found for '{query}' with extension '{file_ext}'.", Fore.RED)
            sys.stdout.write("\r\n")
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes

# Initialize colorama
init()

# Run the program
spidy_lens()