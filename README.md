# Telegram Autojoiner
This script is designed to listen to channels for time-sensitive Telegram invite links to join them automatically.

## Prerequisites
1. [Python3](https://www.python.org/downloads/)

## Environment Variables
```
API_ID=<From API Development Tools from https://my.telegram.org>
API_HASH=<From API Development Tools from https://my.telegram.org>
PHONE_NUMBER=<Phone number of account used to listen and join group>
NOTIFICATION_CHANNEL_ADMIN_USER=<Phone number of account used to publish to notification channel>
CHANNEL_LINK=<Telegram link to channel to listen to>
NOTIFICATION_CHANNEL_LINK=<Telegram link to channel to publish notification to>
```

## How to Run
1. Set up virtual environment for pip installations (optional)
```
python3 -m venv venv
```

This command creates a virtual environment called `venv`.

2. Activate virtual environment (optional, but required if you did step 1)
```
On Linux/MacOS (Unix shells): source ./venv/bin/activate
On Windows (Command Prompt): .\venv\Scripts\activate
On Windows (Powershell): .\venv\Scripts\Activate.ps1
```

3. Install dependencies
```
python3 -m pip install -r requirements.txt
```

4. Run the script
```
python3 autojoiner.py
```

When running the script for the first time, the script will try to create a session for both the target Telegram account and the admin Telegram account (for notification channel). To successfully login, a verification code from Telegram is required. This is only done once. Subsequently, it is cached as a `<phone number>.session` file, and `notification.session` for the notification account.

## Pointers
### Process does not run in the background if terminal is closed
Running the script following step 4 requires the shell to be open throughout its lifespan. Closing the shell will stop the process. To run it in the background, consider using background commands like `nohup`:
```
nohup python3 autojoiner.py &
```
This will allow the script to continue running even after the terminal is closed. Note that this might result in loss of logs.

### Loss of logs when running as background process
To keep track of the script's output, you can pipe the logs to a file:
```
nohup python3 autojoiner.py > autojoiner.log 2>&1 &
```
This will save the output and errors to `autojoiner.log`.