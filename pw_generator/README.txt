=====================================
  Password Generator
=====================================

A password generator with KeePass integration.
Generates secure passwords and saves them directly to a .kdbx database.


-------------------------------------
  REQUIREMENTS
-------------------------------------

- Python 3.8 or higher
- A KeePass .kdbx file (optional, only needed to save passwords)


-------------------------------------
  INSTALL
-------------------------------------

py -m pip install -r requirements.txt


-------------------------------------
  HOW TO RUN
-------------------------------------

1. Start the backend:
   py app.py

2. Open index.html in your browser.

Leave the terminal open while using the app.


-------------------------------------
  HOW TO USE
-------------------------------------

1. Enter a base word (optional), e.g. "amazon"
2. Adjust the length slider (4-64 characters)
3. Click "Gerar Password"
4. Fill in the KeePass fields if you want to save it
5. Click "Guardar" or "Gerar e Guardar" to do both at once


-------------------------------------
  BASE WORD SUBSTITUTIONS
-------------------------------------

  a -> @
  s -> $
  o -> 0
  i -> 1
  e -> 3

Example: "amazon" becomes "Am@z0n..." + random characters


-------------------------------------
  TROUBLESHOOTING
-------------------------------------

"pip not recognized"
  -> Use: py -m pip install -r requirements.txt

"py not recognized"
  -> Use: python -m pip install -r requirements.txt

"Cannot connect to server"
  -> Make sure app.py is running before opening the page

"KeePass file not found"
  -> Use the full path, e.g. C:\Users\you\passwords.kdbx


-------------------------------------
  FILES
-------------------------------------

  app.py           - Flask backend (API)
  index.html       - Web interface
  requirements.txt - Python dependencies
  README.txt       - This file
