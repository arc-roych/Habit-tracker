# 🛠️ How to Customize & Convert Habit Tracker to a Windows Executable

## **1️⃣ Customize the Python Code**

Before converting to `.exe`, you can tailor the Python program:

- Open `habit_tracker.py` in an editor (VS Code, Notepad++, etc.).

- Modify any sections you need (e.g., **habit list, UI layout, database structure**).

- Save your changes.

## **2️⃣ Install Dependencies**

Make sure you have Python and required libraries installed.

### ✅ Install Python (if not already installed)

Download and install Python from [python.org](https://www.python.org/downloads/).  

Ensure **Python is added to system PATH** during installation.

### ✅ Install Required Packages

Run:

```sh

pip install pyinstaller

3️⃣ Convert Python to an Executable (.exe)

Now, navigate to the project folder and run:

pyinstaller --onefile --windowed --icon=icon.ico habit_tracker.py


🔹 Explanation:

--onefile → Creates a single .exe file.

--windowed → Runs without a terminal window (for GUI apps).

--icon=icon.ico → (Optional) Adds an application icon.

4️⃣ Locate the Executable

After running the command, the .exe file will be inside the dist/ folder:

Habit-tracker/
├── dist/
│   ├── habit_tracker.exe  ✅ (Final Executable)
├── build/
├── habit_tracker.spec
├── habit_tracker.py

Move habit_tracker.exe to any folder and run it!

5️⃣ Handling Windows SmartScreen Warning

Since the .exe is unsigned, Windows may show a warning.

To bypass it:

Click "More info".

Click "Run anyway".


