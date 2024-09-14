# ============================================
# JAPM (Just Another Program Manager)
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/14/2024
# License: MIT
# ============================================

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import queue
import threading
import customtkinter
import version
import webbrowser
import platform
import credits
from CTkToolTip import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Just Another Program Manager")
        self.geometry(f"{1330}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="JAPM", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.browsersButton = customtkinter.CTkButton(self.sidebar_frame, text="Applications", command=self.appsView)
        self.browsersButton.grid(row=1, column=0, padx=20, pady=10)

        self.creditsButton = customtkinter.CTkButton(self.sidebar_frame, text="Credits", command=self.creditsView)
        self.creditsButton.grid(row=4, column=0, padx=20, pady=10)
        
        self.versionLabel = customtkinter.CTkLabel(self.sidebar_frame, text=version.appVersion, anchor="w", font=("Arial", 14, "bold"))
        self.versionLabel.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.current_game_frame = None
    
        # set default values
        self.browsersButton.configure(state="disabled")
        self.current_game_frame = self.createAppInstaller()
        self.current_game_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")

    def appsView(self):
        self.browsersButton.configure(state="disabled")
        self.creditsButton.configure(state="enabled")
        self.reset_game_frames()
        self.create_game_frame("App Installers")

    def creditsView(self):
        self.browsersButton.configure(state="enabled")
        self.creditsButton.configure(state="disabled")
        self.reset_game_frames()
        self.create_game_frame("Credits")

    def reset_game_frames(self):
        # Reset the main frame to remove any existing game-specific widgets
        if self.current_game_frame:
            self.current_game_frame.destroy()

    def create_game_frame(self, game_name):
        # Create a new game frame based on the selected game_name
        self.reset_game_frames()

        if game_name == "App Installers":
            self.current_game_frame = self.createAppInstaller()
        elif game_name == "Utilities":
            self.current_game_frame = self.createUtilities()
        elif game_name == "Credits":
            self.current_game_frame = self.createCredits()
        self.current_game_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")

    def createCredits(self):
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))
        tabview = customtkinter.CTkTabview(frame, width=2000, height=650, fg_color=("#fcfcfc", "#323232"))
        tabview.pack(padx=20, pady=20)
        tabview.add("Credits")
        tabview.add("About")
        tabview.add("License")
        tabview.set("About")
        mit_license_widget = customtkinter.CTkLabel(tabview.tab("License"), width=80, height=20, text=(credits.get_mit_license_text()))
        mit_license_widget.pack(padx=10, pady=10)
        credits_widget = customtkinter.CTkLabel(tabview.tab("Credits"), width=80, height=20, text=(credits.get_credits_text()))
        credits_widget.pack(padx=10, pady=10)
        about_widget = customtkinter.CTkLabel(tabview.tab("About"), width=80, height=20, text=(credits.get_about_text()))
        about_widget.pack(padx=10, pady=10)
        return frame

    def createAppInstaller(self):
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))

        # Create a new frame for chat apps
        browser_frame = customtkinter.CTkFrame(frame, fg_color=("#e0e0e0", "#3a3a3a"))
        browser_frame.place(x=5, y=5)

        # Create buttons and checkboxes for browsers
        self.create_browser_widgets(browser_frame)

        # Create a new frame for chat apps
        chat_frame = customtkinter.CTkFrame(frame, fg_color=("#e0e0e0", "#3a3a3a"))
        chat_frame.place(x=220, y=5)
        self.create_chat_widgets(chat_frame)

        # Category Label
        self.browser_label = customtkinter.CTkLabel(browser_frame, text="Internet Browsers", font=("Arial", 18, "bold"))
        self.browser_label.place(x=5, y=5)

        self.chat_label = customtkinter.CTkLabel(chat_frame, text="Chat Apps", font=("Arial", 18, "bold"))
        self.chat_label.place(x=5, y=5)

        # Here for padding
        self.tabTag = customtkinter.CTkLabel(browser_frame, text="", font=("Arial", 18, "bold"))
        self.tabTag.grid(row=0, column=1, sticky="w", padx=5, pady=(10, 0)) 
        self.tabTag = customtkinter.CTkLabel(chat_frame, text="", font=("Arial", 18, "bold"))
        self.tabTag.grid(row=0, column=1, sticky="w", padx=5, pady=(10, 0)) 

        # Create and place the parseButton during the initialization
        self.parseButton = customtkinter.CTkButton(master=frame, command=self.parseDownloads, text="Download Programs")
        self.parseButton.place(x=1330 / 2 - 200, y=735)
        return frame

    def create_browser_widgets(self, frame):
        # Define browser options with their corresponding open functions
        browsers = [
            ("Arc", lambda: webbrowser.open('https://arc.net', new=2)),
            ("Brave", lambda: webbrowser.open('https://brave.com', new=2)),
            ("Chrome", lambda: webbrowser.open('https://www.google.com/chrome', new=2)),
            ("Chromium", lambda: webbrowser.open('https://www.chromium.org/Home/', new=2)),
            ("Edge", lambda: webbrowser.open('https://www.microsoft.com/en-us/edge', new=2)),
            ("Firefox", lambda: webbrowser.open('https://www.mozilla.org/en-US/firefox/new', new=2)),
            ("Floorp", lambda: webbrowser.open('https://floorp.app', new=2)),
            ("LibreWolf", lambda: webbrowser.open('https://librewolf.net', new=2)),
            ("Opera", lambda: webbrowser.open('https://www.opera.com', new=2)),
            ("Opera GX", lambda: webbrowser.open('https://www.opera.com/gx', new=2)),
            ("Orion", lambda: webbrowser.open('https://kagi.com/orion', new=2)),
            ("Thorium", lambda: webbrowser.open('https://thorium.rocks', new=2)),
            ("Tor", lambda: webbrowser.open('https://www.torproject.org/download', new=2)),
            ("Ungoogled Chromium", lambda: webbrowser.open('https://ungoogled-software.github.io/ungoogled-chromium-binaries', new=2)),
            ("Vivaldi", lambda: webbrowser.open('https://vivaldi.com', new=2)),
        ]

        for i, (name, command) in enumerate(browsers):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 14, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + len(browsers) + 1, column=0, sticky="w", pady=2, padx=(0, 0))
            
            toggle = customtkinter.CTkCheckBox(frame, text=name)
            toggle.grid(row=i + len(browsers) + 1, column=3, sticky="w", pady=2, padx=(0, 0))
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def create_chat_widgets(self, frame):
        # Define chat application options with invalid links
        chat_apps = [
            ("Discord", "https://invalid.discord.link"),
            ("Ferdium", "https://invalid.ferdium.link"),
            ("Guilded", "https://invalid.guilded.link"),
            ("TeamSpeak", "https://invalid.teamspeak.link"),
            ("Textual", "https://invalid.textual.link"),
            ("Google Chat", "https://invalid.googlechat.link"),
            ("Chatterino", "https://invalid.chatterino.link"),
            ("HexChat", "https://invalid.hexchat.link"),
            ("Jami", "https://invalid.jami.link"),
            ("Linphone", "https://invalid.linphone.link"),
            ("Element", "https://invalid.element.link"),
            ("Session", "https://invalid.session.link"),
            ("Signal", "https://invalid.signal.link"),
            ("Skype", "https://invalid.skype.link"),
            ("Slack", "https://invalid.slack.link"),
            ("Teams", "https://invalid.teams.link"),
            ("Telegram", "https://invalid.telegram.link"),
            ("Thunderbird", "https://invalid.thunderbird.link"),
        ]

        for i, (name, command) in enumerate(chat_apps):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 14, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + len(chat_apps) + 1, column=2, sticky="w", pady=2, padx=(0, 0))
            
            toggle = customtkinter.CTkCheckBox(frame, text=name)
            toggle.grid(row=i + len(chat_apps) + 1, column=3, sticky="w", pady=2, padx=(0, 0))
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def parseDownloads(self):
        # Disable the button before executing commands
        self.parseButton.configure(state=tk.DISABLED)
        distro = self.detect_distro()
        commands = self.build_commands(distro)

        if commands:
            # Create a new window for terminal output
            terminal_window = tk.Toplevel(self)
            terminal_window.title("Terminal Output")
            terminal_window.geometry("600x400")

            terminal_output = scrolledtext.ScrolledText(terminal_window, wrap=tk.WORD, background="#323232", foreground="#ffffff")
            terminal_output.pack(expand=True, fill='both')

            process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            # Function to read the output asynchronously
            def read_output(file, queue, lock):
                while True:
                    line = file.readline()
                    if not line:
                        break
                    with lock:
                        queue.put(line)

            # Set up queues and lock
            stdout_queue = queue.Queue()
            stderr_queue = queue.Queue()
            output_lock = threading.Lock()

            # Create file event handlers
            stdout_handler = threading.Thread(target=read_output, args=(process.stdout, stdout_queue, output_lock))
            stderr_handler = threading.Thread(target=read_output, args=(process.stderr, stderr_queue, output_lock))

            # Start file event handlers
            stdout_handler.start()
            stderr_handler.start()

            def check_output():
                with output_lock:
                    while not stdout_queue.empty():
                        terminal_output.configure(state='normal')
                        terminal_output.insert(tk.END, stdout_queue.get())
                        terminal_output.yview(tk.END)  # Scroll to the bottom
                        terminal_output.configure(state='disabled')

                    while not stderr_queue.empty():
                        terminal_output.configure(state='normal')
                        terminal_output.insert(tk.END, stderr_queue.get())
                        terminal_output.yview(tk.END)  # Scroll to the bottom
                        terminal_output.configure(state='disabled')

                if process.poll() is None:
                    # The process is still running, so check again after a short delay
                    terminal_output.after(100, check_output)
                else:
                    # Command finished, clean up
                    stdout_handler.join()
                    stderr_handler.join()

                    # Enable the button after command execution is complete
                    self.parseButton.configure(state=tk.NORMAL)

            # Start checking for output
            check_output()

    def detect_distro(self):
        if platform.system().lower() == "linux":
            with open('/etc/os-release') as f:
                os_info = f.read().lower()
                if 'arch' in os_info or 'manjaro' in os_info or 'endeavouros' in os_info:
                    return "arch"
                elif 'fedora' in os_info or 'centos' in os_info or 'rhel' in os_info:
                    return "fedora"
                elif 'debian' in os_info or 'ubuntu' in os_info or 'linuxmint' in os_info:
                    return "debian"
        elif platform.system().lower() == "windows":
            return "windows"
        elif platform.system().lower() == "darwin":
            return "macOS"
        else:
            return "unknown"

    def build_commands(self, distro):
        commands = ""
        def append_command(toggle, command_win, command_mac, command_arch):
            nonlocal commands
            if toggle.get() == 1:
                commands += command_win if distro == "windows" else command_mac if distro == "macOS" else command_arch if distro == "arch" else ""
            
        # Example commands for brew and winget
        if distro == "macOS":
            commands += "brew install --display-times "  # Initial command for Homebrew on macOS
        elif distro == "windows":
            commands += "winget install --accept-package-agreements --accept-source-agreements "  # Initial command for winget on Windows
        elif distro == "arch":
            commands += "yay -Syyuu --noconfirm "  # Initial command for yay on Arch

        append_command(self.arcToggle, "", "arc ", "")
        append_command(self.braveToggle, "Brave.Brave ", "brave-browser ", "brave-browser ")
        append_command(self.chromeToggle, "Google.Chrome ", "google-chrome ", "google-chrome ")
        append_command(self.chromiumToggle, "Hibbiki.Chromium ", "chromium ", "chromium ")
        append_command(self.edgeToggle, "Microsoft.Edge ", "microsoft-edge ", "microsoft-edge-stable-bin ")
        append_command(self.firefoxToggle, "Mozilla.Firefox ", "firefox ", "firefox ")
        append_command(self.floorpToggle, "Ablaze.Floorp ", "floorp ", "floorp-bin ")
        append_command(self.librewolfToggle, "LibreWolf.LibreWolf ", "librewolf ", "librewolf-bin ")
        append_command(self.operaToggle, "Opera.Opera ", "opera ", "opera ")
        append_command(self.operagxToggle, "Opera.OperaGX ", "opera-gx ", "")
        append_command(self.orionToggle, "", "orion ", "")
        append_command(self.thoriumToggle, "Alex313031.Thorium.AVX2 ", "alex313031-thorium ", "thorium-browser-bin ")
        append_command(self.torToggle, "TorProject.TorBrowser ", "tor-browser ", "tor-browser-bin ")
        append_command(self.ungoogledchromiumToggle, "eloston.ungoogled-chromium ", "eloston-chromium ", "ungoogled-chromium-bin")
        append_command(self.vivaldiToggle, "VivaldiTechnologies.Vivaldi ", "vivaldi ", "vivaldi")
        append_command(self.discordToggle, "Discord.Discord ", "discord ", "discord ")
        append_command(self.ferdiumToggle, "Ferdium.Ferdium ", "ferdium ", "ferdium-bin ")
        append_command(self.guildedToggle, "Guilded.Guilded ", "guilded ", "guilded ")
        append_command(self.teamspeakToggle, "TeamSpeakSystems.TeamSpeakClient ", "teamspeak-client ", "teamspeak ")

        if self.textualToggle.get() == 1 and distro != "windows":
            commands += "textual "

        if self.googleChatToggle.get() == 1 and distro != "macOS":
            commands += "squalou.google-chat-linux "

        append_command(self.chatterinoToggle, "ChatterinoTeam.Chatterino ", "chatterino ")

        if self.hexChatToggle.get() == 1 and distro == "windows":
            commands += "HexChat.HexChat "

        append_command(self.jamiToggle, "SFLinux.Jami ", "jami ")
        append_command(self.linPhoneToggle, "BelledonneCommunications.Linphone ", "linphone ")
        append_command(self.elementToggle, "Element.Element ", "element ")
        append_command(self.sessionToggle, "Oxen.Session ", "session ")
        append_command(self.signalToggle, "OpenWhisperSystems.Signal ", "signal ")
        append_command(self.skypeToggle, "Microsoft.Skype ", "skype ")
        append_command(self.slackToggle, "SlackTechnologies.Slack ", "slack ")
        append_command(self.teamsToggle, "Microsoft.Teams ", "microsoft-teams ")
        append_command(self.telegramToggle, "Telegram.TelegramDesktop ", "telegram ")
        append_command(self.thunderbirdToggle, "Mozilla.Thunderbird ", "thunderbird ")

        return commands

if __name__ == "__main__":
    app = App()
    app.mainloop()