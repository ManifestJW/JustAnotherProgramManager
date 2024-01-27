# ============================================
# Program Master
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 1/25/2024
# License: MIT
# ============================================

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import queue
import threading
import customtkinter
import version
import platform
import credits
from functions import *
from CTkToolTip import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Program Manager")
        self.geometry(f"{1330}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Program Master", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.browsersButton = customtkinter.CTkButton(self.sidebar_frame, text="App Installers", command=self.browsersView)
        self.browsersButton.grid(row=1, column=0, padx=20, pady=10)

        self.utilitiesButton = customtkinter.CTkButton(self.sidebar_frame, text="Utilities", command=self.UtilitiesView)
        self.utilitiesButton.grid(row=2, column=0, padx=20, pady=10)

        self.creditsButton = customtkinter.CTkButton(self.sidebar_frame, text="Credits", command=self.creditsView)
        self.creditsButton.grid(row=4, column=0, padx=20, pady=10)
        
        self.versionLabel = customtkinter.CTkLabel(self.sidebar_frame, text=f"Version: {version.appVersion}", anchor="w", font=("Arial", 14, "bold"))
        self.versionLabel.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.current_game_frame = None  # To keep track of the currently displayed game frame
    
        # set default values
        self.browsersButton.configure(state="disabled")
        self.current_game_frame = self.createAppInstaller()
        self.current_game_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")


    def browsersView(self):
        self.browsersButton.configure(state="disabled")
        self.utilitiesButton.configure(state="enabled")
        self.creditsButton.configure(state="enabled")
        self.reset_game_frames()
        self.create_game_frame("App Installers")

    def UtilitiesView(self):
        self.browsersButton.configure(state="enabled")
        self.utilitiesButton.configure(state="disabled")
        self.creditsButton.configure(state="enabled")
        self.reset_game_frames()
        self.create_game_frame("Utilities")

    def creditsView(self):
        self.browsersButton.configure(state="enabled")
        self.utilitiesButton.configure(state="enabled")
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
        mit_license_widget = customtkinter.CTkLabel(tabview.tab("License"), width=80, height=20, text=(get_mit_license_text()))
        mit_license_widget.pack(padx=10, pady=10)
        credits_widget = customtkinter.CTkLabel(tabview.tab("Credits"), width=80, height=20, text=(get_credits_text()))
        credits_widget.pack(padx=10, pady=10)
        about_widget = customtkinter.CTkLabel(tabview.tab("About"), width=80, height=20, text=(get_about_text()))
        about_widget.pack(padx=10, pady=10)
        return frame

    def createAppInstaller(self):
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))

        # Category Label
        self.label = customtkinter.CTkLabel(frame, text="Internet Browsers", font=("Arial", 25, "bold"))
        self.label.place(x=5, y=5)

        # Here for padding
        self.header_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 25, "bold"))
        self.header_label.grid(row=0, column=1, sticky="w", padx=5, pady=(10, 0))  # Adjusted row to 0 and added pady

        # Create Arc
        if platform.system().lower() == "darwin":
            self.label = customtkinter.CTkLabel(frame, text="Arc", font=("Arial", 16, "bold"))
            self.label.grid(row=1, column=2, sticky="w")  # Adjusted column to 2
            self.arcToggle = customtkinter.CTkCheckBox(frame, text=None)
            self.arcToggle.grid(row=1, column=1)
            icon = create_image_icon(frame, "assets/arc.png", 1, 1)

        # Create Brave
        self.label = customtkinter.CTkLabel(frame, text="Brave", font=("Arial", 16, "bold"))
        self.label.grid(row=2, column=2, sticky="w")  # Adjusted column to 2
        self.braveToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.braveToggle.grid(row=2, column=1)
        icon = create_image_icon(frame, "assets/brave.png", 2, 1)

        # Create Chrome
        self.label = customtkinter.CTkLabel(frame, text="Chrome", font=("Arial", 16, "bold"))
        self.label.grid(row=3, column=2, sticky="w")  # Adjusted column to 2
        self.chromeToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.chromeToggle.grid(row=3, column=1)
        icon = create_image_icon(frame, "assets/googleChrome.png", 3, 1)

        # Create Chromium
        self.label = customtkinter.CTkLabel(frame, text="Chromium", font=("Arial", 16, "bold"))
        self.label.grid(row=4, column=2, sticky="w")  # Adjusted column to 2
        self.chromiumToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.chromiumToggle.grid(row=4, column=1)
        icon = create_image_icon(frame, "assets/chromium.png", 4, 1)

        # Create Edge
        self.label = customtkinter.CTkLabel(frame, text="Edge", font=("Arial", 16, "bold"))
        self.label.grid(row=5, column=2, sticky="w")  # Adjusted column to 2
        self.edgeToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.edgeToggle.grid(row=5, column=1)
        icon = create_image_icon(frame, "assets/edge.png", 5, 1)

        # Create Firefox
        self.label = customtkinter.CTkLabel(frame, text="Firefox", font=("Arial", 16, "bold"))
        self.label.grid(row=6, column=2, sticky="w")  # Adjusted column to 2
        self.firefoxToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.firefoxToggle.grid(row=6, column=1)
        icon = create_image_icon(frame, "assets/firefox.png", 6, 1)

        # Create Floorp
        self.label = customtkinter.CTkLabel(frame, text="Floorp", font=("Arial", 16, "bold"))
        self.label.grid(row=7, column=2, sticky="w")  # Adjusted column to 2
        self.floorpToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.floorpToggle.grid(row=7, column=1)
        icon = create_image_icon(frame, "assets/floorp.png", 7, 1)

        # Create LibreWolf
        self.label = customtkinter.CTkLabel(frame, text="LibreWolf", font=("Arial", 16, "bold"))
        self.label.grid(row=8, column=2, sticky="w")  # Adjusted column to 2
        self.libreWolfToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.libreWolfToggle.grid(row=8, column=1)
        icon = create_image_icon(frame, "assets/libreWolf.png", 8, 1)

        # Create Opera
        self.label = customtkinter.CTkLabel(frame, text="Opera", font=("Arial", 16, "bold"))
        self.label.grid(row=9, column=2, sticky="w")  # Adjusted column to 2
        self.operaToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.operaToggle.grid(row=9, column=1)
        icon = create_image_icon(frame, "assets/opera.png", 9, 1)

        # Create Opera GX
        self.label = customtkinter.CTkLabel(frame, text="Opera GX", font=("Arial", 16, "bold"))
        self.label.grid(row=10, column=2, sticky="w")  # Adjusted column to 2
        self.operaGXToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.operaGXToggle.grid(row=10, column=1)
        icon = create_image_icon(frame, "assets/operaGX.png", 10, 1)

        # Create Thorium
        self.label = customtkinter.CTkLabel(frame, text="Thorium AVX2", font=("Arial", 16, "bold"))
        self.label.grid(row=11, column=2, sticky="w")  # Adjusted column to 2
        self.thoriumToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.thoriumToggle.grid(row=11, column=1)
        icon = create_image_icon(frame, "assets/thorium.png", 11, 1)

        # Create Tor
        self.label = customtkinter.CTkLabel(frame, text="Tor", font=("Arial", 16, "bold"))
        self.label.grid(row=12, column=2, sticky="w")  # Adjusted column to 2
        self.torToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.torToggle.grid(row=12, column=1)
        icon = create_image_icon(frame, "assets/tor.png", 12, 1)

        # Create Ungoogled Chromium
        self.label = customtkinter.CTkLabel(frame, text="Ungoogled", font=("Arial", 16, "bold"))
        self.label.grid(row=13, column=2, sticky="w")  # Adjusted column to 2
        self.ungoogledToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.ungoogledToggle.grid(row=13, column=1)
        icon = create_image_icon(frame, "assets/chromium.png", 13, 1)

        # Create Vivaldi
        self.label = customtkinter.CTkLabel(frame, text="Vivaldi", font=("Arial", 16, "bold"))
        self.label.grid(row=14, column=2, sticky="w")  # Adjusted column to 2
        self.vivaldiToggle = customtkinter.CTkCheckBox(frame, text=None)
        self.vivaldiToggle.grid(row=14, column=1)
        icon = create_image_icon(frame, "assets/vivaldi.png", 14, 1)

        # Text widget for displaying output
        self.output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=161, height=7)
        self.output_text.place(x=5, y=625)
    
        # Create and place the parseButton during the initialization
        self.parseButton = customtkinter.CTkButton(master=frame, command=self.parseDownloads, text="Download Programs")
        self.parseButton.place(x=1330 / 2 - 200, y=735)
        return frame

    def parseDownloads(self):
        # Disable the button before executing commands
        self.parseButton.configure(state=tk.DISABLED)
        
        if platform.system().lower() == "windows":
            commands = "winget install "
        else:
            commands = "brew install "

        if self.arcToggle.get() == 1:
            if platform.system().lower() == "windows":
                pass
            else:
                commands = commands + "arc "

        if self.braveToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Brave.Brave "
            else:
                commands = commands + "brave-browser "
    
        if self.chromeToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Google.Chrome "
            else:
                commands = commands + "google-chrome "

        if self.chromiumToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Hibbiki.Chromium "
            else:
                commands = commands + "chromium " 

        if self.edgeToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Microsoft.Edge "
            else:
                commands = commands + "microsoft-edge "

        if self.firefoxToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Mozilla.Firefox "
            else:
                commands = commands + "firefox "

        if self.floorpToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Ablaze.Floorp "
            else:
                commands = commands + "floorp "

        if self.libreWolfToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "LibreWolf.LibreWolf "
            else:
                commands = commands + "librewolf "

        if self.operaToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Opera.Opera "
            else:
                commands = commands + "opera "

        if self.operaGXToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Opera.OperaGX "
            else:
                commands = commands + "opera-gx "

        if self.thoriumToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "Alex313031.Thorium.AVX2 "
            else:
                commands = commands + "alex313031-thorium "

        if self.ungoogledToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "eloston.ungoogled-chromium "
            else:
                commands = commands + "eloston-chromium "

        if self.vivaldiToggle.get() == 1:
            if platform.system().lower() == "windows":
                commands = commands + "VivaldiTechnologies.Vivaldi "
            else:
                commands = commands + "vivaldi "

        def execute_command():
            if commands:
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
                            self.output_text.configure(state='normal')
                            self.output_text.insert(tk.END, stdout_queue.get())
                            self.output_text.yview(tk.END)  # Scroll to the bottom
                            self.output_text.configure(state='disabled')

                        while not stderr_queue.empty():
                            self.output_text.configure(state='normal')
                            self.output_text.insert(tk.END, stderr_queue.get())
                            self.output_text.yview(tk.END)  # Scroll to the bottom
                            self.output_text.configure(state='disabled')

                    if process.poll() is None:
                        # The process is still running, so check again after a short delay
                        self.output_text.after(100, check_output)
                    else:
                        # Command finished, clean up
                        stdout_handler.join()
                        stderr_handler.join()

                        # Enable the button after command execution is complete
                        self.parseButton.configure(state=tk.NORMAL)

                # Start checking for output
                check_output()

        # Start executing commands
        execute_command()

if __name__ == "__main__":
    app = App()
    app.mainloop()
