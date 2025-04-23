## Authentication
This project requires Google Drive API credentials.

- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Create a project, enable Drive API, and download your `credentials.json`
- Place it in the root directory before running the script

> ⚠️ Do not share your credentials or token file publicly.

# Google Drive CLI Manager

This is a command-line interface tool to manage Google Drive folders and files using the Google Drive API.

## Features

- Browse your Google Drive via CLI
- Navigate into folders
- Select specific files or folders
- Upload/Download functionality (via `Driver` class)

## Setup

1. Enable Google Drive API on your [Google Cloud Console](https://console.cloud.google.com/).
2. Download `credentials.json` and place it in the root directory.
3. Run `cli_interface.py`.

```bash

python cli_interface.py

lsdir - List all files and folders

chdir <folder_name> - Change directory

updir - Go up one directory

select <name> - Select a file or folder