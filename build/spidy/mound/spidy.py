import time
import os
import pygame
import sys
from colorama import init, Fore
import random
import threading
import glob
from queue import Queue
from colorama import Fore
from queue import Queue
from threading import Lock
import psutil  
import threading
import random
from colorama import Fore
import subprocess

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores files there
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize pygame mixer
pygame.mixer.init()

# Initialize colorama
init()

# ASCII Art for branding
from termcolor import colored
def print_spidy_art():
    spidy_art1 = """
    
    
    
    
    
   ▄████████    ▄███████▄  ▄█  ████████▄  ▄██   ▄        
  ███    ███   ███    ███ ███  ███   ▀███ ███   ██▄      
  ███    █▀    ███    ███ ███▌ ███    ███ ███▄▄▄███      
  ███          ███    ███ ███▌ ███    ███ ▀▀▀▀▀▀███      
▀███████████ ▀█████████▀  ███▌ ███    ███ ▄██   ███      
         ███   ███        ███  ███    ███ ███   ███      
   ▄█    ███   ███        ███  ███   ▄███ ███   ███      
 ▄████████▀   ▄████▀      █▀   ████████▀   ▀█████▀        
 
 
"""
    spidy_art2 = """
    
    
    
                                                     ⠀⠀⢀⡟⢀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠈⣧⠀⠀
                                                     ⠀⠀⣼⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⢸⡆⠀
⠀⢰⣿⠀⠻⠧⣤⡴⣦⣤⣤⣤⣠⡶⣤⣤⠾⠗⠈⣿⠀
⠀⠺⣷⡶⠖⠛⣩⣭⣿⣿⣿⣿⣿⣯⣭⡙⠛⠶⣶⡿⠃
⠀⠀⠀⢀⣤⠾⢋⣴⠟⣿⣿⣿⡟⢷⣬⠙⢷⣄⠀⠀⠀
⢀⣠⡴⠟⠁⠀⣾⡇⠀⣿⣿⣿⡇⠀⣿⡇⠀⠙⠳⣦⣀
⢸⡏⠀⠀⠀⠀⢿⡇⠀⢸⣿⣿⠁⠀⣿⡇⠀⠀⠀⠈⣿
⠀⣷⠀⠀⠀⠀⢸⡇⠀⠀⢻⠇⠀⠀⣿⠇⠀⠀⠀⠀⣿
⠀⢿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡏
⠘⡇⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⡾⠀
                                                        ⠀⠀⠹⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⢰⠁⠀
                                                        ⠀⠀⠀⠁⠀⠀⠀⠈⢇⠀⠀⠀⠀⡞⠀⠀⠀⠀⠁⠀⠀

"""
 #Ensure both arts have the same number of lines by padding with empty lines
    lines_spidy_art1 = spidy_art1.split('\n')
    lines_spidy_art2 = spidy_art2.split('\n')

    max_lines = max(len(lines_spidy_art1), len(lines_spidy_art2))

    # Pad the shorter art with empty lines
    while len(lines_spidy_art1) < max_lines:
        lines_spidy_art1.append("")
    while len(lines_spidy_art2) < max_lines:
        lines_spidy_art2.append("")

    # Margin to be added (e.g., 10 spaces)
    margin = 35

    # Add margin only to spidy_art1
    lines_spidy_art1 = [(" " * margin) + line for line in lines_spidy_art1]

    # Create a shorter horizontal border with alternating colors
    horizontal_border = ""
    for i in range(156):  # Length of border, set to 150 characters
        if i % 2 == 0:
            horizontal_border += colored("═", "blue")
        else:
            horizontal_border += colored("═", "red")

    # Print the shorter horizontal border at the top
    print(horizontal_border)

    # Printing the two Spidy Art side by side with a horizontal blue and red border
    for line1, line2 in zip(lines_spidy_art1, lines_spidy_art2):
        print(f"{colored(line1, 'blue')}{colored(line2, 'red')}")

    # Print the shorter horizontal border at the bottom
    print(horizontal_border)


def get_network_speed():
    """Measure network speed using speedtest-cli, with psutil as fallback."""
    try:
        import speedtest  # Requires 'pip install speedtest-cli'
        type_writer("Measuring SPIDY Server Speed... (10-20 seconds)", Fore.MAGENTA, delay=0.01)
        st = speedtest.Speedtest()
        st.get_best_server()  # Find the best server for accurate results
        download_speed = st.download() / 1_000_000  # Convert bits/sec to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert bits/sec to Mbps
        unit = "Mbps"
        return download_speed, upload_speed, unit
    except ImportError:
        type_writer("⚠️ Speedtest module not found, falling back to usage monitoring (install with 'pip install speedtest-cli')", Fore.RED)
        net_io_start = psutil.net_io_counters()
        start_bytes_sent = net_io_start.bytes_sent
        start_bytes_recv = net_io_start.bytes_recv
        
        type_writer("Measuring current usage... (5 seconds)", Fore.YELLOW, delay=0.01)
        time.sleep(5)
        
        net_io_end = psutil.net_io_counters()
        end_bytes_sent = net_io_end.bytes_sent
        end_bytes_recv = net_io_end.bytes_recv
        
        upload_bytes = end_bytes_sent - start_bytes_sent
        download_bytes = end_bytes_recv - start_bytes_recv
        
        upload_bits_per_sec = (upload_bytes * 8) / 5
        download_bits_per_sec = (download_bytes * 8) / 5
        
        if download_bits_per_sec >= 1_000_000:
            download_speed = download_bits_per_sec / 1_000_000
            upload_speed = upload_bits_per_sec / 1_000_000
            unit = "Mbps"
        else:
            download_speed = download_bits_per_sec / 1_000
            upload_speed = upload_bits_per_sec / 1_000
            unit = "kbps"
        
        return download_speed, upload_speed, unit
    except Exception as e:
        type_writer(f"⚠️ Network Error: {e}. Check your connection or firewall.", Fore.RED)
        return 0, 0, "Mbps"


# High-end Linux-style loader animation with progress bar and unique colors
def linux_loader_animation():
    loading_text = "System Initializing..."
    total_steps = 50  # Number of steps to simulate the system loading
    bar_length = 50  # Length of the progress bar
    spinner = ['|', '/', '-', '\\']
    count = 0

    for step in range(total_steps):
        progress = int((step / total_steps) * bar_length)
        bar = "█" * progress + " " * (bar_length - progress)
        
        # Customizing the colors for different parts
        sys.stdout.write(f"\r{colored(loading_text, 'yellow')} "
                         f"[{colored(bar, 'white')}] "
                         f"{colored(str(step * 2) + '%', 'green')} "
                         f"{colored(spinner[count % 4], 'green')}")
        sys.stdout.flush()
        time.sleep(0.1)
        count += 1

    sys.stdout.write("\r" + " " * 80 + "\r")  # Clear the line after completion
    
    # Different color for the completion text and progress bar
    print(f"{colored(loading_text, 'yellow')} "
          f"[{colored('█████████████████████████', 'white')}] "
          f"{colored('100% Complete', 'green')}")


# Call the function to print ASCII art
print_spidy_art()

# Call the Linux-style loader animation after the ASCII art
print("\n")
linux_loader_animation()

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
appa_sound_path = os.path.join(sound_path, "Appa lu.mp3")


# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Random Spidy Quotes
spidy_quotes = [
    "I am your friendly neighborhood Spidy! 🕷️",
    "With great power comes great responsibility! ⚡",
    "Web-slinging through the streets...💨",
    "I’m always watching... 😏",
    "Spidy is always ready for action! 🔥"
]

# Function to get a random Spidy quote
def get_random_spidy_quote():
    return random.choice(spidy_quotes)

# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")
        



# Function to play the sound (Make sure 'dady_home' is a valid path to a sound file)
def play_daddy_home_sound():
    play_sound(dady_home)  # Make sure 'dady_home' is the correct sound file
    
def appa_sound():
    play_sound(appa_appa)

# Function to simulate the typing effect
def type_daddy_home_message():
    type_writer("Daddy is Home Wake Up Spidy 🔥😏", random.choice([Fore.RED, Fore.YELLOW, Fore.LIGHTCYAN_EX]))
    
def type_appa():
    type_writer("hehe 😁", random.choice([Fore.YELLOW, Fore.LIGHTCYAN_EX]))

# Function to play the sound (Make sure to define the play_sound function)
def play_sound(sound):
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function for the typewriter effect (Ensure this is defined)
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

spidy_quotes = [
    "I am your friendly neighborhood Spidy! 🕷️",
    "With great power comes great responsibility! ⚡",
    "Web-slinging through the streets...💨",
    "I’m always watching... 😏",
    "Spidy is always ready for action! 🔥"
]

# Function to simulate typing effect
def type_writer(text, color=Fore.GREEN, delay=0.02, end_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if end_line:
        print()  # To move to the next line if needed

# Function to play sound
def play_sound(sound):
    if not os.path.isfile(sound):
        print(f"Error: Sound file {sound} not found!")
        return
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the sound to finish
            time.sleep(1)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to get a random Spidy quote
def get_random_spidy_quote():
    return random.choice(spidy_quotes)

# Welcome Spidynal Forever
def spidy_online_system():
    print(Fore.CYAN)
    threading.Thread(target=play_sound, args=(spidy_online,)).start()
    type_writer("🔥 SPIDYNAL V2.0 SYSTEM ONLINE 💀🕸️", Fore.LIGHTCYAN_EX)
    type_writer("[🤝] GPT Private Server Connected...", Fore.MAGENTA)
    type_writer("[💀] Spidynal Security System ONLINE...", Fore.RED)
    type_writer("✅ DADDY IS HOME WAKE UP SPIDY!", Fore.YELLOW)

# Hacker Mode Activation
def hacker_mode_activation():
    threading.Thread(target=play_sound, args=(hacker_mode,)).start()
    type_writer("[💀] SPIDYNAL DARK HACKER MODE ACTIVATED...", Fore.RED)
    for i in range(5):
        type_writer(random.choice(spidy_quotes), random.choice([Fore.RED, Fore.CYAN, Fore.YELLOW]))
        time.sleep(0.5)

# Voice System
def voice_mode_system():
    threading.Thread(target=play_sound, args=(voice_mode,)).start()
    type_writer("🎙️ SPIDYNAL VOICE SYSTEM ONLINE...", Fore.LIGHTCYAN_EX)
    time.sleep(2)
    type_writer("Hello Daddy... Welcome back to your Private AI 🔥😏💀", Fore.YELLOW)

# Play 'DADDY HOME' sound and display message
def play_daddy_home_sound():
    play_sound(dady_home)  # Make sure 'dady_home' is the correct sound file

def type_daddy_home_message():
    type_writer("Daddy is Home Wake Up Spidy 🔥😏", random.choice([Fore.RED, Fore.YELLOW, Fore.LIGHTCYAN_EX]))


# Print ASCII Art with color
def print_ascii_art():
    print(Fore.CYAN )

# Play sound in background using threading
def play_start_sound():
    play_sound(start)

# Run both the ASCII art and sound concurrently
thread1 = threading.Thread(target=print_ascii_art)
thread2 = threading.Thread(target=play_start_sound)

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

time.sleep(1)  # Add a small delay after both actions have completed

# Display system startup message
# Function to play sound in a separate thread
def play_middle_sound():
    play_sound(wake_up_spidy)

# Run both the sound and type_writer concurrently
thread1 = threading.Thread(target=play_middle_sound)
thread2 = threading.Thread(target=type_writer, args=("SPIDYNAL SYSTEM ONLINE 🕸️", Fore.CYAN))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

time.sleep(2)
# Function to play the sound for middle
def play_middle_sound():
    play_sound(middle)

# Run both the sound and type_writer concurrently
thread1 = threading.Thread(target=play_middle_sound)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
thread2 = threading.Thread(target=type_writer, args=("[🤝] Connecting to ~SPIDY Private Server...", Fore.MAGENTA))

# Start both threads
=======
thread2 = threading.Thread(target=type_writer, args=("Connecting to ~SPIDY Private Server...", Fore.MAGENTA))
>>>>>>> Stashed changes
=======
thread2 = threading.Thread(target=type_writer, args=("Connecting to ~SPIDY Private Server...", Fore.MAGENTA))
>>>>>>> Stashed changes
=======
thread2 = threading.Thread(target=type_writer, args=("Connecting to ~SPIDY Private Server...", Fore.MAGENTA))
>>>>>>> Stashed changes
thread1.start()
thread2.start()
thread1.join()
thread2.join()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
type_writer("✅ SPIDY SYSTEM ACTIVATED..!", Fore.GREEN)
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

# Add network speed display here with the debug-enabled function
download_speed, upload_speed, unit = get_network_speed()
type_writer(f"SPIDINAL Speed - Download: {download_speed:.2f} {unit} | Upload: {upload_speed:.2f} {unit} 🌐", Fore.CYAN)

type_writer("SPIDY SYSTEM ACTIVATED..!", Fore.GREEN)


<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
# Function to play the exit sound and print the exit message
def exit_sequence():
    # Thread to play the exit sound
    thread1 = threading.Thread(target=play_sound, args=(spidy_sound,))
    # Thread to start the typewriter effect for exit message
    thread2 = threading.Thread(target=type_writer, args=("SPIDY BROZ SYSTEM OFFLINE 😴", Fore.YELLOW))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    
    

# Play the intro sound in a separate thread
# thread = threading.Thread(target=play_sound, args=(middle,))
# thread.start()

while True:
    
    # Get command input from user with a dynamic typing effect
   
    type_writer(" ", Fore.LIGHTCYAN_EX)
    type_writer("SPIDYNAL™ 🕷️: ", Fore.CYAN, delay=0.02, end_line=False)
    command = input()

    import threading

# Assuming you are in the main command loop
    if command.lower() == "wake up":
        # Start both the sound and the typewriter effect concurrently using threads
        thread1 = threading.Thread(target=play_daddy_home_sound)
        thread2 = threading.Thread(target=type_daddy_home_message)

        # Start both threads
        thread1.start()
        thread2.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()


    elif command.lower() == "whats today":
        # Display a random Spidy quote and change color
        type_writer(get_random_spidy_quote(), random.choice([Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.MAGENTA]))
        
    elif command.lower() == "appa lu":
        thread1 = threading.Thread(target=play_sound, args=(appa_sound_path,))
        thread2 = threading.Thread(target=type_appa)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        
    elif command.lower() == "spidy hacks":
        hacker_mode_activation()
            
    elif command.lower() == "spidynal voice":
        voice_mode_system()
        
    elif command.lower() == "whats today":
        # Display a random Spidy quote
        type_writer(get_random_spidy_quote(), random.choice([Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.MAGENTA]))


    elif command.lower() == "spidy lens":
        spidy_lens_path = resource_path("build/spidy/mound/spidyLens.py")
        if os.path.exists(spidy_lens_path):
            subprocess.run(["python", spidy_lens_path])
        else:
            type_writer("Error: spidyLens.py not found!", Fore.RED)

    elif command.lower() == "spidy lens global":
        spidy_lens_global_path = resource_path("build/spidy/mound/spidyLensGlobal.py")
        if os.path.exists(spidy_lens_global_path):
            subprocess.run(["python", spidy_lens_global_path])
        else:
            type_writer("Error: spidyLensGlobal.py not found!", Fore.RED)

    elif command.lower() == "exit":
        exit_sequence()
        break  # Exit the loop after the exit sequence is completed
    
    elif command.lower() == "spidynal speed":
        download_speed, upload_speed, unit = get_network_speed()
        box_width = 50
        speed_text = f"Download: {download_speed:.2f} {unit} | Upload: {upload_speed:.2f} {unit}"
        padding = (box_width - len(speed_text) - 4) // 2
        
        # Top border
        top_border = colored("╔" + "═" * (box_width - 2) + "╗", "cyan")
        type_writer(top_border, delay=0.01)
        
        # Content line
        content = colored("║", "cyan") + " " * padding + speed_text + " " * (box_width - len(speed_text) - 2 - padding) + colored("║", "cyan")
        type_writer(f"🌐 Network Speed - {content}", delay=0.01)
        
        # Bottom border (fixed typo)
        bottom_border = colored("╚" + "═" * (box_width - 2) + "╝", "cyan")
        type_writer(bottom_border, delay=0.01)  # Note: Should be bottom_border, not custom_border
    
    elif command.lower() == "fuck":
            type_writer("what's fuck huh?", Fore.GREEN)
            
    elif command.lower() == "fuck you":
            type_writer("fuck you bitch.., you mother fucker..! 🖕🏻", Fore.GREEN)

    elif command.lower() == "help":
            type_writer("Commands here: wake up, spidy lens, spidy hacks, whats today, exit, help || and more secrets...", Fore.GREEN)
        

    else:
        # Randomly change the color for an "Invalid Command"
        invalid_colors = [Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.LIGHTCYAN_EX]
        type_writer(f"Invalid Command... Try Again 😏", random.choice(invalid_colors))
