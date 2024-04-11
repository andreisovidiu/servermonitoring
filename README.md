# Summary
Servermonitoring is Python script that monitors CPU, RAM and DISK SPACE values of Linux/Unix operating systems.
It alerts the user through a Telegram message and a Twilio cellphone message once the values are breached.

## Instructions

### Create a .env file with your data

```
# Telegram
API_TOKEN= "YOUR_API_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Twilio
ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN  = "YOUR_AUTH_TOKEN"
TWILIO_NUMBER = "YOUR_TWILIO_NUMBER"
RECIPIENTS = ["RECIPIENTS_NUMBER"]

# OS
LOG_PATH = "LOG_PATH/monitor.log"
```

### Install dependencies

```
pipenv install
```

### Install supervisord (optional)
Install Supervisord, a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.

Supervisord useful cmd commands:
```
supervisorctl reread
supervisorctl update
supervisorctl
supervisorctl restart all
supervisorctl stop all
supervisorctl start all
truncate -s 0 filename # empty log file
ps aux | grep supervisor
kill -9 PID 
```
Resources: <br>
http://supervisord.org/ <br>
https://www.youtube.com/watch?v=eX7D40y9qv8&t=505s

