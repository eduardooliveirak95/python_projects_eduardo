# Smart Password Generator CLI

A professional command-line interface (CLI) tool built with Python to generate high-entropy, customizable passwords. This project features direct integration with **KeePass (.kdbx)** databases, allowing you to secure your credentials immediately after generation.

## Features

- **Keyword-Based Generation**: Create passwords based on a specific hint or service name.
- **High Security**: Uses Python's `secrets` module for cryptographically strong random numbers.
- **KeePass Integration**: Automatically save your new passwords into an existing `.kdbx` database.
- **Customizable Complexity**: Adjust password length and character sets to meet any security requirement.
- **User-Friendly CLI**: Interactive prompts for a seamless terminal experience.

### Prerequisites

* Python 3.8 or higher
* A KeePass database (optional, for saving passwords)


###INSTALL DEPENDENCIES (IMPORTANT):

py -m pip install --upgrade pip
pip install -r requirements.txt
