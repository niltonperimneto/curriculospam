# CurriculoSpam: The "Please Hire Me" Automator

## What is this?
This is a script born of pure desperation. I am a History teacher, which means I am currently unemployed, broke, and questioning every life choice that led me here.

I have sent my CV to every school, and educational institution within a 500km radius. I have prayed to the LinkedIn and Gupy algorithm. I have offered to teach for charity. The result? Silence. The void. The deafening sound of my own inbox not pinging.

So, purely out of necessity (and the need to pay rent), I decided to automate the indignity of "circling back." This script scans my "Sent" folder for the keyword "curriculo", finds the recruiters who ghosted me, and sends them a polite follow-up reminding them that I exist and I am hungry.

## Features
- **Desperation Mining**: Scans the last 90 days of sent emails to find the people who ignored you.
- **Automated Pestering**: Sends a follow-up email so you don't have to type "Just checking in!" through tears.
- **Dignity Preservation (Optional)**: Includes a "Dry Run" mode so you can review the list of people who don't want you before you message them again.

## Requirements
- Python 3 (Because learning to code was my backup plan).
- A Gmail account.
- A **Google App Password** (Because using your real password is unsafe, unlike my financial situation).

## How to Run This Thing

### Linux
Open the Terminal and type:

```bash
# No need to install anything, it uses standard libraries.
# Unless you messed up your Python install, which wouldn't surprise me.
python3 curriculospam.py
```

### Windows
Open Command Prompt or PowerShell and type:

```cmd
python curriculospam.py
```
*Note: If `python` doesn't work, try `py`. If that doesn't work, ensure Python is in your PATH. If you don't know what that means, welcome to my world of confusion.*

## Configuration
Before running, open `curriculospam.py` and edit this section to match your specific level of qualification and despair:

```python
SUBJECT_LINE = "Follow-up: Candidatura Professor de História - Nilton Perim Neto"
```

## Disclaimer
I am not responsible if this gets you blacklisted from every HR department in the country. Use at your own risk. I'm just a teacher trying to survive.
