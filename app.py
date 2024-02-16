import logging
import os
import telebot
import psutil
import time
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# load hidden .env variables
load_dotenv()

""" 

Logs settings 

"""

# Add path of the log file
log_path = os.getenv('LOG_PATH')
logging.basicConfig(filename=log_path, level=logging.WARNING,
    format='%(asctime)s:%(levelname)s:%(message)s')

"""

Psutil package class to get system information (CPU, MEMORY, DISK)

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
        self.total_memory = memory.total # Machine might have multiple RAM modules
        self.available_memory = memory.available
        self.used_memory = memory.used
        self.memory_percentage = memory.percent
        disk_usage = psutil.disk_usage('/')
        self.total_disk_space = disk_usage.total
        self.used_disk_space = disk_usage.used
        self.free_disk_space = disk_usage.free
        self.disk_space_percentage = disk_usage.percent
        
    def print_system_info(self):
        logging.warning(
            "\n"
            f"CPU Usage: {self.cpu_percentage}%, \n"
            f"Total Memory: {self.total_memory / (1024 ** 3):.2f} GB, \n"
            f"Available Memory: {self.available_memory / (1024 ** 3):.2f} GB, \n"
            f"Used Memory: {self.used_memory / (1024 ** 3):.2f} GB, \n"
            f"Memory Usage: {self.memory_percentage}%, \n"
            f"Total Disk Space: {self.total_disk_space / (1024 ** 3):.2f} GB, \n"
            f"Used Disk Space: {self.used_disk_space / (1024 ** 3):.2f} GB, \n"
            f"Free Disk Space: {self.free_disk_space / (1024 ** 3):.2f} GB, \n"
            f"Disk Space Usage: {self.disk_space_percentage}%"
            "\n"
        )

"""

Twilio and Telegram code implementation

"""

# Your Account SID and Auth Token from console.twilio.com
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)    

# Telegram 
bot = telebot.TeleBot(os.getenv('API_TOKEN'))

# TG channel id
target_chat_id = os.getenv('CHAT_ID')

# Alert messages for each case
cpu_message = 'Server has high CPU usage, try to look which processes are using the resources on the process tab.'
memory_message = 'Server has high Memory usage. Check out the process tab to see which process is using the most memory.'
disk_message = 'Server has high Disk usage, try to free up some disk space to clear this alert.'

# .env constants
number1 = os.getenv('MY_NUMBER')
number2 = os.getenv('NUMBER2')
twilio_number = os.getenv('TWILIO_NUMBER')

"""

Main

"""

def main():

    info_printer = SystemInfoPrinter() # Object from class SystemInfoPrinter
    cpu_start_time = None
    memory_start_time = None
    disk_start_time = None

    while True:
        """ 
        If values are higher than a certain % for a certain amount of time 
        then send an alert message and repeat every minute/s 
        
        """
        info_printer.update_system_info()

        """

        CPU ALARM

        """

        if info_printer.cpu_percentage > 75:

            if cpu_start_time is None:
                    cpu_start_time = datetime.now()

            elapsed_time = datetime.now() - cpu_start_time
            # print('CPU elapsed time', elapsed_time)

            if elapsed_time.total_seconds() > 30: # Seconds

                # Twilio message
                try:
                    message = client.messages.create(
                        to= number1,
                        from_=twilio_number,
                        body=cpu_message)
                except:
                    bot.send_message(chat_id=target_chat_id, text='Cellphone message not sent, check twilio.com/console')
                    logging.warning('Cellphone message not sent, check twilio.com/console')
                    
                # TG bot message
                bot.send_message(chat_id=target_chat_id, text=cpu_message)
                cpu_start_time = datetime.now() # Reset

                info_printer.print_system_info()

        else:
            cpu_start_time = None

        """
        
        MEMORY ALARM
        
        """

        if info_printer.memory_percentage > 85:

            if memory_start_time is None:
                    memory_start_time = datetime.now()

            elapsed_time = datetime.now() - memory_start_time
            # print('MEMORY elapsed time', elapsed_time)

            if elapsed_time.total_seconds() > 30: # Seconds

                # Twilio message
                try:
                    message = client.messages.create(
                        to= number1,
                        from_=twilio_number,
                        body=memory_message)
                except:
                    bot.send_message(chat_id=target_chat_id, text='Cellphone message not sent, check twilio.com/console')
                    logging.warning('Cellphone message not sent, check twilio.com/console')

                # TG bot message
                bot.send_message(chat_id=target_chat_id, text=memory_message)
                memory_start_time = datetime.now() # Reset

                info_printer.print_system_info()

        else:
            memory_start_time = None

        """ 
        
        DISK ALARM
        
        """

        if info_printer.disk_space_percentage > 85:

            if disk_start_time is None:
                    disk_start_time = datetime.now()

            elapsed_time = datetime.now() - disk_start_time
            # print('DISK elapsed time', elapsed_time)

            if elapsed_time.total_seconds() > 30: # Seconds

                # Twilio message
                try:
                    message = client.messages.create(
                        to= number1,
                        from_=twilio_number,
                        body=disk_message)
                except:
                    bot.send_message(chat_id=target_chat_id, text='Cellphone message not sent, check twilio.com/console')
                    logging.warning('Cellphone message not sent, check twilio.com/console')

                # TG bot message
                bot.send_message(chat_id=target_chat_id, text=disk_message)
                disk_start_time = datetime.now() # Reset

                info_printer.print_system_info()

        else:
            disk_start_time = None

        """
        Errors are managed by the Twilio module 
        and by the try/except condition,
        check documentation or support for details
        https://www.twilio.com/docs/errors/21608
        
        """
        # Remove when implemented, uncomment only for debug purposes   
        # time.sleep(3)
        # info_printer.print_system_info()

if __name__ == "__main__":
    main()
