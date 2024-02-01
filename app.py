import os
import telebot
import psutil
import time
from twilio.rest import Client
from dotenv import load_dotenv

############################################################################################

"""Psutil package implementation to get system information"""

# Get CPU usage
cpu_percentage = psutil.cpu_percent(interval=1)  # Interval is in seconds

# Get memory (RAM) usage
memory = psutil.virtual_memory()
total_memory = memory.total
available_memory = memory.available
used_memory = memory.used
memory_percentage = memory.percent
    
# Get disk usage
disk_usage = psutil.disk_usage('/')
total_disk_space = disk_usage.total
used_disk_space = disk_usage.used
free_disk_space = disk_usage.free
disk_space_percentage = disk_usage.percent

# Print values function
def print_system_info():

    # Print the obtained system information (using formatted strings to display GB values)
    print() # Blank space left just for aesthetic reasons
    print(f"CPU Usage: {cpu_percentage}%")

    print(f"Total Memory: {total_memory / (1024 ** 3):.2f} GB")
    print(f"Available Memory: {available_memory / (1024 ** 3):.2f} GB")
    print(f"Used Memory: {used_memory / (1024 ** 3):.2f} GB")
    print(f"Memory Usage: {memory_percentage}%")

    print(f"Total Disk Space: {total_disk_space / (1024 ** 3):.2f} GB")
    print(f"Used Disk Space: {used_disk_space / (1024 ** 3):.2f} GB")
    print(f"Free Disk Space: {free_disk_space / (1024 ** 3):.2f} GB")
    print(f"Disk Space Usage: {disk_space_percentage}%")

############################################################################################

"""Twilio + Telegram bot code implementation"""

# load hidden .env variables
load_dotenv()

# Your Account SID and Auth Token from console.twilio.com
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)    

# Telegram 
bot = telebot.TeleBot(os.getenv('API_TOKEN'))

# /start and /help messages handling
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

# TG channel id
target_chat_id = os.getenv('CHAT_ID')

# Alert messages for each case
cpu_message = 'CPU usage alert, check the server'
ram_message = 'RAM usage alert, check the server'
disk_message = 'DISK usage alert, check the server'

# Loop that checks for messages
# bot.infinity_polling()

# Initial time 
start_time = time.time()

number1 = os.getenv('MY_NUMBER')
number2 = os.getenv('NUMBER2')
twilio_number = os.getenv('TWILIO_NUMBER')

def main():
    while True:

        """ 
        If values are higher than a
        certain % for a certain amount of time 
        then send an alert message and repeat
        every minute/s 
        
        """
        
        elapsed_time = time.time() - start_time

        # Constant var
        time_passed = 20 # Value in seconds

        # List of INDIPENDENT conditions
        # CPU message
        if cpu_percentage > 80 and elapsed_time > time_passed: 
                # message = client.messages.create(
                #     to= number1,
                #     from_=twilio_number,
                #     body="ALERT CPU USAGE!")
                
                # TG bot message method
                bot.send_message(chat_id=target_chat_id, text=cpu_message)
                print_system_info()

        # Memory message
        if memory_percentage > 1 and elapsed_time > time_passed:
            message = client.messages.create(
                to= number1,
                from_=twilio_number,
                body="ALERT MEMORY USAGE!")
            
            # TG bot message method
            bot.send_message(chat_id=target_chat_id, text=ram_message)
            print_system_info()
            
        # Disk message
        if disk_space_percentage > 80 and elapsed_time > time_passed:
            # message = client.messages.create(
            #     to= number1,
            #     from_=twilio_number,
            #     body="ALERT DISK USAGE!")
            
            # TG bot message method
            bot.send_message(chat_id=target_chat_id, text=disk_message)
            print_system_info()
            
        """
        Errors are managed by the Twilio module,
        check documentation or support for details
        https://www.twilio.com/docs/errors/21608
        
        """
            
        time.sleep(time_passed) 

if __name__ == "__main__":
    main()
