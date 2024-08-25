3D Print Cost Calculator User Manual
1. Introduction
3D Print Cost Calculator is an intuitive application designed to help you accurately calculate the cost of 3D-printed parts. By allowing you to input various parameters such as part weight, print time, material costs, and profit margin, the application provides a comprehensive breakdown of the total production cost.

2. Installation
2.1 System Requirements
Operating System: Windows 7 or later (32-bit or 64-bit) or Linux
Disk Space: Approximately 50 MB of free disk space
2.2 Installing the Application on Windows
Download the Installer: Download the installer 3dCalculatorSetup.exe from [the download link].
Run the Installer: Double-click the installer and follow the on-screen instructions.
Installation Directory: By default, the application will be installed in C:\Program Files (x86)\3DPrintCalculator.
Launch the Application: After successful installation, you can start the application from the Start menu or via the desktop shortcut.
2.3 Installing the Application on Linux
For Linux users, the application can be run directly from the Python script provided. No installation is required.

Ensure Dependencies: Ensure that Python 3 and PyQt5 are installed on your system.
Run the Application: Open a terminal, navigate to the directory containing print_calculator.py, and run the following command:
bash
Copy code
python3 print_calculator.py
3. Usage
3.1 Main Tab
Select Material: Choose a material from the list of available materials.
Weight (grams): Enter the part weight in grams.
Print Time (hours): Enter the print time in hours (rounded up to the nearest whole hour).
Profit Margin (%): Enter the desired profit margin as a percentage.
Additional Cost (BGN) [optional]: If there are additional costs for creating the model, enter them here.
Click the Calculate Cost button to calculate the total cost. The result will be displayed at the bottom of the screen.

3.2 Settings Tab
Printer Price (BGN): Enter the printer's price.
Electricity Price (BGN per kWh): Enter the electricity cost per kilowatt-hour.
Material Name: Enter the name of a new material you wish to add.
Material Price per kg (BGN): Enter the material price per kilogram.
Managing Materials:

Add Material: Click to add the new material to the list.
Edit Material: To modify an existing material, select it from the list, make the necessary changes, and click Edit Material.
Delete Material: To remove a material, select it from the list and click Delete Material.
Click Save Settings to save all the settings.

3.3 Settings Storage
Windows Version:
All settings are saved in a JSON file located in the AppData directory of your user profile. These settings will be automatically loaded the next time the application is launched.

Linux Version:
For Linux users, the settings are also saved in a JSON file. This file, named settings.json, is stored in the same directory where the application script (print_calculator.py) is located. Each time the application is launched, it will load these settings automatically from the JSON file.
