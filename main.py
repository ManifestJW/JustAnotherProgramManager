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
import colorlib
import threading
import customtkinter
import version
import webbrowser
import platform
import credits
import darkdetect
import mousescroll
import CTkMessagebox
import json
from CTkToolTip import *


customtkinter.set_appearance_mode(darkdetect.theme())

# Load commands from JSON file
def load_commands():
    with open('applications.json', 'r') as file:
        return json.load(file)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.commands_data = load_commands()

        # Colorlib
        global sysColor
        global sysColorAlt
        sysColor, sysColorAlt = colorlib.get_system_colors()  # Call the function from colorlib

        # dark color Var
        global colorBg
        if darkdetect.theme() == "Dark":
            colorBg = "#3a3a3a"
        else:
            colorBg = "#ffffff"

        global toggles
        toggles = []
        
        # Configure window properties
        self.title("Just Another Program Manager")  # Set the window title
        self.geometry(f"{1330}x{780}")  # Set the window size

        # Configure grid layout for the main application window
        self.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
        self.grid_columnconfigure((2, 3), weight=0)  # Fixed width for columns 2 and 3
        self.grid_rowconfigure((0, 1, 2), weight=1)  # Allow rows 0, 1, and 2 to expand

        # Create sidebar frame for navigation
        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")  # Position sidebar frame
        self.sidebarFrame.grid_rowconfigure(3, weight=1)  # Allow row 3 to expand

        # Add logo label to the sidebar
        self.logoLabel = customtkinter.CTkLabel(self.sidebarFrame, text="Just Another\nProgram Manager", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))  # Position logo label

        # Create buttons for navigation
        self.applicationsButton = customtkinter.CTkButton(self.sidebarFrame, text="Applications", command=self.appsView, fg_color=sysColor, hover_color=sysColorAlt)
        self.applicationsButton.grid(row=1, column=0, padx=20, pady=10)  # Position Applications button

        self.creditsButton = customtkinter.CTkButton(self.sidebarFrame, text="Credits", command=self.creditsView, fg_color=sysColor, hover_color=sysColorAlt)
        self.creditsButton.grid(row=4, column=0, padx=20, pady=10)  # Position Credits button

        # Display application version in the sidebar
        self.versionLabel = customtkinter.CTkLabel(self.sidebarFrame, text=version.appVersion, anchor="w", font=("Arial", 16, "bold"))
        self.versionLabel.grid(row=5, column=0, padx=20, pady=(10, 0))  # Position version label

        self.currentGameFrame = None  # Placeholder for the current game frame

        # Set default button states and initialize the main frame
        self.applicationsButton.configure(state="disabled")  # Disable Applications button initially
        self.currentGameFrame = self.createAppInstaller()  # Create the app installer frame
        self.currentGameFrame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")  # Position the frame

    # Function to check if any checkbox is checked
    def update_install_button_state(self, btn):
       # Check if any toggle is checked
       any_checked = any(toggle.get() for toggle in toggles)
       btn.configure(state=tk.NORMAL if any_checked else tk.DISABLED)


    def appsView(self):
        # Switch to the applications view
        self.applicationsButton.configure(state="disabled")  # Disable Applications button
        self.creditsButton.configure(state="enabled")  # Enable Credits button
        self.resetGameFrames()  # Reset any existing frames
        self.createGameFrame("App Installers")  # Create the app installers frame

    def creditsView(self):
        # Switch to the credits view
        self.applicationsButton.configure(state="enabled")  # Enable Applications button
        self.creditsButton.configure(state="disabled")  # Disable Credits button
        self.resetGameFrames()  # Reset any existing frames
        self.createGameFrame("Credits")  # Create the credits frame

    def resetGameFrames(self):
        # Remove any existing game-specific widgets from the main frame
        if self.currentGameFrame:
            self.currentGameFrame.destroy()  # Destroy the current game frame

    def createGameFrame(self, appType):
        # Create a new game frame based on the selected application type
        self.resetGameFrames()  # Reset existing frames

        if appType == "App Installers":
            self.currentGameFrame = self.createAppInstaller()  # Create app installer frame
        elif appType == "Credits":
            self.currentGameFrame = self.createCredits()  # Create credits frame
        
        self.currentGameFrame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")  # Position the new frame

    def createCredits(self):
        # Create the credits frame with tabs for different sections
        frame = customtkinter.CTkFrame(self, fg_color=("#ffffff", "#323232"))  # Create frame with light and dark mode colors
        tabview = customtkinter.CTkTabview(frame, width=2000, height=650, fg_color=("#ffffff", "#323232"), segmented_button_selected_hover_color=sysColorAlt, segmented_button_selected_color=sysColor)  # Create tab view
        tabview.pack(padx=20, pady=20)  # Pack the tab view into the frame
        tabview.add("Credits")  # Add Credits tab
        tabview.add("About")  # Add About tab
        tabview.add("License")  # Add License tab
        tabview.set("About")  # Set default tab to About

        # Add content to the License tab
        mitLicenseWidget = customtkinter.CTkLabel(tabview.tab("License"), width=80, height=20, text=credits.get_mit_license_text())
        mitLicenseWidget.pack(padx=10, pady=10)  # Pack the license text

        # Add content to the Credits tab
        creditsWidget = customtkinter.CTkLabel(tabview.tab("Credits"), width=80, height=20, text=credits.get_credits_text())
        creditsWidget.pack(padx=10, pady=10)  # Pack the credits text

        # Add content to the About tab
        aboutWidget = customtkinter.CTkLabel(tabview.tab("About"), width=80, height=20, text=credits.get_about_text())
        aboutWidget.pack(padx=10, pady=10)  # Pack the about text

        return frame  # Return the credits frame

    def createAppInstaller(self):
        # Create the app installer frame with various sections
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))  # Create frame with light and dark mode colors
        frame.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")  # Position the frame with padding
        
        for index, key in enumerate(self.commands_data.keys()):  # Loop through each key with an index
            self.createSection(frame, key, 1, index)  # Increment column index by 1 for each section

        # Create the Install Selected button above the frames
        self.parseButton = customtkinter.CTkButton(master=frame, command=self.parseDownloads, text="Install Selected", fg_color=sysColor, hover_color=sysColorAlt)
        self.parseButton.grid(row=0, column=0, padx=(5, 5), pady=(10, 5), sticky="w")  # Position Install Selected button
        self.update_install_button_state(self.parseButton)  # Call the method to initialize button state

        # Create the Update All Apps button next to Install Selected
        self.updateButton = customtkinter.CTkButton(master=frame, command=self.updateAllApps, text="Update ALL Apps", width=150, fg_color=sysColor, hover_color=sysColorAlt)
        self.updateButton.place(x=165, y=10)  # Position next to the Install Selected button

        return frame  # Return the app installer frame

    def createSection(self, frame, section_name, row, column):
        # Create a border frame for the section
        borderFrame = customtkinter.CTkFrame(frame, fg_color=sysColor, border_width=2, width=240, height=690)
        borderFrame.grid(row=row, column=column, padx=(5, 0), pady=(5, 5), sticky="nsew")
    
        sectionCanvas = customtkinter.CTkCanvas(borderFrame, bg=colorBg, width=210, height=690)
        sectionFrame = customtkinter.CTkFrame(sectionCanvas, fg_color=("#ffffff", "#3a3a3a"))
        sectionScrollbar = customtkinter.CTkScrollbar(borderFrame, orientation="vertical", command=sectionCanvas.yview, fg_color=("#ffffff", "#3a3a3a"), button_hover_color=sysColorAlt, button_color=sysColor)
        sectionScrollbar.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ns")
        sectionCanvas.configure(yscrollcommand=sectionScrollbar.set)
        sectionCanvas.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")
        sectionCanvas.create_window((0, 0), window=sectionFrame, anchor="nw")


        # Update the scroll region of the canvas when the frame is resized
        def update_scroll_region(event):
            sectionCanvas.configure(scrollregion=sectionFrame.bbox("all"))  # Update scroll region for each canvas
        
        # Bind resize events for each section frame
        sectionFrame.bind("<Configure>", update_scroll_region)
    
        mousescroll.bind_mouse_wheel(sectionCanvas)

        for key in self.commands_data.keys():  # Loop through each key
            self.createWidgets(sectionFrame, section_name)
            self.createCategoryLabel(sectionFrame, section_name.capitalize())

        return sectionCanvas, sectionFrame  # Return the canvas and frame for further use if needed

    def createCategoryLabel(self, frame, text):
        label = customtkinter.CTkLabel(frame, text=text, font=("Arial", 16, "bold"))
        label.place(x=5, y=5)  # Position label
        return label

    def createWidgets(self, frame, section_name):
        # Define the command list for the specific category
        browsers = [("", lambda: None, ["win32", "macos", "arch"])]
        for app in self.commands_data[section_name]:
            if self.detectDistro() == "macos":
                if self.commands_data[section_name][app]['macos-brew'] != "":
                    browsers.append((app, lambda: webbrowser.open(self.commands_data[section_name][app]['url'], new=2), "macos"))
            elif self.detectDistro() == "win32":
                if self.commands_data[section_name][app]['windows-winget'] != "":
                    browsers.append((app, lambda: webbrowser.open(self.commands_data[section_name][app]['url'], new=2), "win32"))
            elif self.detectDistro() == "arch":
                if self.commands_data[section_name][app]['archlinux-pacman-aur'] != "":
                    browsers.append((app, lambda: webbrowser.open(self.commands_data[section_name][app]['url'], new=2), "arch"))

        # Filter based on the current platform
        available_browsers = [
            (name, command) for name, command, platforms in browsers if self.detectDistro() in platforms
        ]

        # Sort the available browsers list alphabetically by the browser name
        available_browsers = sorted(available_browsers, key=lambda x: x[0].lower())

        for i, (name, command) in enumerate(available_browsers):
            goodName = name.replace(" ", "").replace(".", "").replace("+", "plus").lower()

            # Create the toggle checkbox for the application
            toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12, fg_color=sysColor, hover_color=sysColorAlt)
            toggle.grid(row=i + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding

            # Add the toggle to the list
            toggles.append(toggle)
            toggle.configure(command=lambda: self.update_install_button_state(self.parseButton))  # Bind the toggle to the update function

            # Create the button for the application
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color=sysColor, command=command, fg_color=("#ffffff", "#3a3a3a"), hover_color=("#ffffff", "#3a3a3a"), width=6)
            button.grid(row=i + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

        # Create dummy toggles and buttons for applications not available on the current platform
        for i, (name, command, _) in enumerate(browsers):
            if name not in [app[0] for app in available_browsers]:  # Check if the app is not in available_apps
                goodName = name.replace(" ", "").replace(".", "").replace("+", "plus").lower()

                # Create a dummy toggle checkbox for the unavailable app
                toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12, fg_color=sysColor, hover_color=sysColorAlt, state="disabled")
                toggle.grid(row=i + len(available_browsers) + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding

                # Add the toggle to the list
                toggles.append(toggle)
                toggle.configure(command=self.update_install_button_state)  # Bind the toggle to the update function

                # Create a dummy button for the unavailable app
                button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color=sysColor, command=command, fg_color=("#ffffff", "#3a3a3a"), hover_color=("#ffffff", "#3a3a3a"), width=6, state="disabled")
                button.grid(row=i + len(available_browsers) + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
                setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def executeCommands(self, commands, title="Terminal Output"):
        if not commands:
            return  # Exit if there are no commands to execute

        # Create a new window for terminal output
        terminalWindow = tk.Toplevel(self)
        terminalWindow.title(title)
        terminalWindow.geometry("600x400")

        terminalOutput = scrolledtext.ScrolledText(terminalWindow, wrap=tk.WORD)
        terminalOutput.pack(expand=True, fill='both')

        # Run the command in a separate thread
        def run_command():
            process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            # Unified function to read output and update terminal
            def update_terminal_output():
                for line in iter(process.stdout.readline, ''):
                    terminalOutput.configure(state='normal')
                    terminalOutput.insert(tk.END, line)
                    terminalOutput.yview(tk.END)  # Scroll to the bottom
                    terminalOutput.configure(state='disabled')

                for line in iter(process.stderr.readline, ''):
                    terminalOutput.configure(state='normal')
                    terminalOutput.insert(tk.END, line)
                    terminalOutput.yview(tk.END)  # Scroll to the bottom
                    terminalOutput.configure(state='disabled')

                process.stdout.close()
                process.stderr.close()
                process.wait()  # Wait for the process to finish
                terminalWindow.destroy()  # Close the terminal window
                self.updateButton.configure(state=tk.NORMAL)  # Re-enable the button after command execution

            # Start the terminal output update in a separate thread
            threading.Thread(target=update_terminal_output).start()

        # Start the command in a separate thread
        threading.Thread(target=run_command).start()


    def parseDownloads(self):       
        # Disable the button before executing commands
        self.parseButton.configure(state=tk.DISABLED)
        distro = self.detectDistro()  # Detect the operating system distribution
        commands = self.buildCommands(distro)  # Build the commands based on selected applications
        self.executeCommands(commands, title="Download Output")

    def detectDistro(self):
        if platform.system().lower() == "linux":
            with open('/etc/os-release') as f:
                osInfo = f.read().lower()
                if 'arch' in osInfo or 'manjaro' in osInfo or 'endeavouros' in osInfo:
                    return "arch"
                elif 'fedora' in osInfo or 'centos' in osInfo or 'rhel' in osInfo:
                    return "fedora"
                elif 'debian' in osInfo or 'ubuntu' in osInfo or 'linuxmint' in osInfo:
                    return "debian"
        elif platform.system().lower() == "windows":
            return "windows"
        elif platform.system().lower() == "darwin":
            return "macos"
        else:
            return "unknown"

    def buildCommands(self, distro):
        commands = ""
        def appendCommand(toggle, command):
            nonlocal commands
            if toggle.get() == 1:
                try:
                    commands += command
                except:
                    pass # is not on this OS
        # Example commands for brew and winget
        if distro == "macos":
            commands += "brew install --display-times "  # Initial command for Homebrew on macOS
        elif distro == "windows":
            commands += "winget install --accept-package-agreements --accept-source-agreements "  # Initial command for winget on Windows
        elif distro == "arch":
            commands += "yay -S --noconfirm "  # Initial command for yay on Arch

        categories = self.commands_data.keys()  # Get the first keys from the JSON

        for category in categories:
            for app in self.commands_data[category]:
                # Check if the keys exist before accessing them
                if self.detectDistro() == "win32":
                    if self.commands_data[category][app]['windows-winget'] != "":
                        appendCommand(getattr(self, f"{app.replace(' ', '').replace('.', '').replace('+', 'plus').lower()}Toggle"),
                                      self.commands_data[category][app]['windows-winget'])
                elif self.detectDistro() == "macos":
                    if self.commands_data[category][app]['macos-brew'] != "":
                        appendCommand(getattr(self, f"{app.replace(' ', '').replace('.', '').replace('+', 'plus').lower()}Toggle"),
                                      self.commands_data[category][app]['macos-brew'])
                elif self.detectDistro() == "arch":
                    if self.commands_data[category][app]['archlinux-pacman-aur'] != "":
                        appendCommand(getattr(self, f"{app.replace(' ', '').replace('.', '').replace('+', 'plus').lower()}Toggle"),
                                      self.commands_data[category][app]['archlinux-pacman-aur'])
                else:
                    pass
            
        return commands

    def updateAllApps(self):
        msg = CTkMessagebox.CTkMessagebox(title="Warning Message!", message="Are you sure you want to update every app!\nThis includes apps not listed here.",
                  icon="warning", option_1="Cancel", option_2="OK")
        if msg.get()=="OK":
            
            # Disable the button before executing commands
            self.updateButton.configure(state=tk.DISABLED)

            # Command to run
            if platform.system().lower() == "darwin":
                command = "brew upgrade"
            elif platform.system().lower() == "windows":
                command = "winget upgrade --all"
            else:
                command = "yay -Syyuu"

            self.executeCommands(command)

if __name__ == "__main__":
    app = App()
    app.mainloop()