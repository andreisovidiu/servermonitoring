import os
import telebot
import psutil
import time
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

"""

Psutil package class to get system information

"""

class SystemInfoPrinter:
    def __init__(self):
        self.cpu_percentage = 0
        self.total_memory = 0
        self.available_memory = 0
        self.used_memory = 0
        self.memory_percentage = 0
        self.total_disk_space = 0
        self.used_disk_space = 0
        self.free_disk_space = 0
        self.disk_space_percentage = 0

    def update_system_info(self):
        self.cpu_percentage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        self.total_memory = memory.total
        self.available_memory = memory.available
        self.used_memory = memory.used
        self.memory_percentage = memory.percent
        disk_usage = psutil.disk_usage('/')
        self.total_disk_space = disk_usage.total
        self.used_disk_space = disk_usage.used
        self.free_disk_space = disk_usage.free
        self.disk_space_percentage = disk_usage.percent
        
    def print_system_info(self):
        print() # Blank space left just for aesthetic reasons
        print(f"CPU Usage: {self.cpu_percentage}%")
        print(f"Total Memory: {self.total_memory / (1024 ** 3):.2f} GB")
        print(f"Available Memory: {self.available_memory / (1024 ** 3):.2f} GB")
        print(f"Used Memory: {self.used_memory / (1024 ** 3):.2f} GB")
        print(f"Memory Usage: {self.memory_percentage}%")
        print(f"Total Disk Space: {self.total_disk_space / (1024 ** 3):.2f} GB")
        print(f"Used Disk Space: {self.used_disk_space / (1024 ** 3):.2f} GB")
        print(f"Free Disk Space: {self.free_disk_space / (1024 ** 3):.2f} GB")
        print(f"Disk Space Usage: {self.disk_space_percentage}%")

"""

Twilio and Telegram code implementation

"""

# load hidden .env variables
load_dotenv()

# Your Account SID and Auth Token from console.twilio.com
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)    

# Telegram 
bot = telebot.TeleBot(os.getenv('API_TOKEN'))

# TG channel id
target_chat_id = os.getenv('CHAT_ID')

# Alert messages for each case
cpu_message = 'CPU usage alert, check the server'
ram_message = 'RAM usage alert, check the server'
disk_message = 'DISK usage alert, check the server'

# .env constants
number1 = os.getenv('MY_NUMBER')
number2 = os.getenv('NUMBER2')
twilio_number = os.getenv('TWILIO_NUMBER')

"""

Main

"""

def main():

    info_printer = SystemInfoPrinter() # Object from class SystemInfoPrinter
    start_time = None

    while True:
        """ 
        If values are higher than a certain % for a certain amount of time 
        then send an alert message and repeat every minute/s 
        
        """
        info_printer.update_system_info()

        # CPU message
        if info_printer.cpu_percentage > 70:

            if start_time is None:
                    start_time = datetime.now()
                    print('start time inside the if loop', start_time)

            elapsed_time = datetime.now() - start_time
            print('elapsed time', elapsed_time)
            
            if elapsed_time.total_seconds() > 30:
                # TG bot message method
                bot.send_message(chat_id=target_chat_id, text=cpu_message)
                start_time = datetime.now() # Reset
        else:
            start_time = None

                # info_printer.print_system_info()

            # try:
            #     message = client.messages.create(
            #         to= number1,
            #         from_=twilio_number,
            #         body="ALERT CPU USAGE, check the server.")
            # except:
            #     bot.send_message(chat_id=target_chat_id, text='Cellphone message not sent, check twilio.com/console')
                

        """
        Errors are managed by the Twilio module 
        and by the try/except condition,
        check documentation or support for details
        https://www.twilio.com/docs/errors/21608
        
        """
        # Remove when implemented   
        time.sleep(5)
        info_printer.print_system_info()

if __name__ == "__main__":
    main()
