# Google Drive CLI Manager

This is a command-line interface (CLI) tool to manage Google Drive folders and files using the Google Drive API. You can browse your Google Drive, navigate into folders, select files, and upload/download files with ease.

## Features

- **Browse your Google Drive via CLI**
- **Navigate into folders**
- **Select specific files or folders**
- **Upload/Download functionality** via `Driver` class

## Authentication

This project requires Google Drive API credentials.

1. **Visit [Google Cloud Console](https://console.cloud.google.com/)**.
2. **Create a new project** and enable the Google Drive API for that project.
3. **Download your `credentials.json` file** from the Google Cloud Console and place it in the **root directory** of the project.
4. **Run the script** after placing the credentials.

> ⚠️ **Important:** Do not share your credentials or token files publicly, as they grant access to your Google Drive account.

## Setup

### Steps to Set Up Google Drive API

1. **Enable Google Drive API**:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Navigate to **API & Services > Library** and enable the **Google Drive API**.
   
2. **Download `credentials.json`**:
   - After enabling the API, go to **APIs & Services > Credentials**.
   - Under **OAuth 2.0 Client IDs**, click **Create Credentials**, and download the `credentials.json` file.

3. **Place the `credentials.json`** file in the root directory of your project.

### Running the Script

Once you’ve set up the Google Drive API credentials, run the script with the following steps:

1. Install the required dependencies (if you haven't already):

    ```bash
    pip install -r requirements.txt
    ```

2. Run the **CLI Interface** by executing the following command in the terminal:

    ```bash
    python cli_interface.py
    ```

## Available Commands

Here are the available commands for interacting with Google Drive:

- **`lsdir`** - List all files and folders in the current directory.
  
    ```bash
    lsdir
    ```

- **`chdir <folder_name>`** - Change directory to the specified folder.
  
    ```bash
    chdir my_folder
    ```

- **`updir`** - Go up one directory level.

    ```bash
    updir
    ```

- **`select <name>`** - Select a specific file or folder by its name.

    ```bash
    select my_file.txt
    ```

- **`upload <file_path>`** - Upload a file to the current directory in Google Drive.

    ```bash
    upload /path/to/local/file.txt
    ```

- **`download <file_name>`** - Download a file from Google Drive to the local machine.

    ```bash
    download my_file.txt
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Drive API** for providing access to Google Drive services.
- **Python `google-api-python-client`** library for easy interaction with Google APIs.

---

Let me know if you'd like further improvements or additions to the file!
