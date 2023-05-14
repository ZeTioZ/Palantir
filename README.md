# INFOB318 - Palantir Project

Acronym: Palantir <br>
Title: Palantir: an overlay for a RTS game <br>
Client(s) : Florent Rochet <br>
Student: Gentile Donato <br>

## Description
Palantir is an overlay for Age Of Empire II: Definitive Edition.
It allows to display information about the game in real time and get the best strategy and civilization to use against the opponents.
It uses image recognition and optical character recognition to read the game information and avoid triggering the anti-cheat system.
The overlay will display a step to step guide to help you win the game with the best strategy and civilization.

## Installation
- Clone the repository by running the following command in a console: `git clone https://github.com/UNamurCSFaculty/2223_INFOB318_Palantir.git`
- Run a console in the root folder
- Install the requirements with `pip install -r ./resources/requirements.txt`
- Run the palantir_main.py file from the src folder
- Enjoy

### You don't want to install the requirements?
- Download the binary files from the release page
- Extract the files
- Run the executable file named Palantir.exe
- (Optional) Create a shortcut of the executable file and move it to the desktop
- Enjoy

## Requirements
- [Python 3.6 or higher (Programming language)](https://www.python.org/downloads/)
- OpenCV 4.7.0.72 or higher (Image recognition)
- PyAutoGUI 0.9.53 or higher (Screen capture)
- wxPython 4.2.0 or higher (GUI)
- pywin32 306 or higher (Windows API)
- [Tesseract 4.0.0 or higher (Optical character recognition)](https://github.com/UB-Mannheim/tesseract/wiki)
- [Age Of Empire 2: Definitive Edition (Game)](https://www.ageofempires.com/games/aoeiide/)

## F.A.Q.
### How to install Tesseract?
- [Download the installer from the official website](https://github.com/UB-Mannheim/tesseract/wiki)
- Install the software
- Add the path to the Tesseract folder to the PATH environment variable
- Restart the computer
- Check if the installation was successful by running the following command in a console: `tesseract --version`

#### How to add the path to Tesseractr folder to the PATH environment variable
- In the search field of the start menu, type "Edit the system environment variables".
- In the System Properties window that you have just opened, click on "Environment Variables".
- In the User variables for... section, click on "Path" and then on "Edit".
- In the Edit Environment Variable window, click on "New".
- A new line will be added and selected. Click on "Browse".
- Select the root installation folder of Tesseract-OCR.
- Click "OK" three times.

### How to run the executable file?
- [Download the binary files from the release page](https://github.com/UNamurCSFaculty/2223_INFOB318_Palantir/releases)
- Extract the files
- Run the executable file named Palantir.exe
- (Optional) Create a shortcut of the executable file and move it to the desktop
- Enjoy
