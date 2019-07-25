#!/usr/bin/env python3

#############
# Installer #
#############

# Steps:
# 1. Get user's TF2 directory
# 2. Copy info about TF2 dir into config.py
# 3. Run 'pip install -r requirements.txt' 
# 4. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
# 5. Ensure that the program runs in background and runs on startup (pythonw for windows, nohup python & for linux)

# Step 1: