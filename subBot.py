import os
import telebot
from telebot import types
import requests
import subprocess
import psutil  # For better process management
required_libraries = [
    'telebot',
    'requests',
    'psutil',
]

# Sub Bot Token

SUB_BOT_TOKEN = "7734600048:AAFazYkLSHvG5pqolD_Ro8qHjCapDuoSjlA"  # Replace with your sub bot's token

# Group Chat ID (must be an integer)
GROUP_CHAT_ID = -1002336551679  # Replace with your group chat ID (remove quotes and ensure it's an integer)
def install_missing_libraries():
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            os.system(f"pip install {lib}")
install_missing_libraries()
sub_bot_chat_id = SUB_BOT_TOKEN.split(":")[0]
# Initialize the sub bot
sub_bot = telebot.TeleBot(SUB_BOT_TOKEN)

def getIdPastebin(user):
    req = requests.get("https://pastebin.com/raw/QaKsZdCf")
    if req.status_code != 200:
        return ""  # Return empty string if the request fails

    for line in req.text.splitlines():  # Split text into lines
        try:
            us, chatid = line.strip().split(":")
            if us == user:
                return chatid
        except ValueError:
            # Skip lines that don't have the expected format
            continue

    return ""  # Return empty string if user is not found

@sub_bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message):
    if int(message.chat.id) == GROUP_CHAT_ID:
        text = message.text.strip()
        user = text.split(":")[1]  # Extract the user from the message
        chatid = getIdPastebin(user)  # Get the chatid associated with the user
        newText =f"{text.split(":")[0]}:{chatid}"
        if f":{sub_bot_chat_id}" in newText:

          if text.startswith("Start"):
            perform_start_action(message)
          elif text.startswith("Stop"):
            perform_stop_action(message)
          elif text.startswith("Update"):
            sub_bot.reply_to(message, "Send New Id:Token")
            sub_bot.register_next_step_handler(message, perform_update_action)
    else:
        sub_bot.send_message(message.chat.id, "This is not the permitted group!")



def perform_update_action(message):
    try:
        # Split the message into newId and newToken
        newId=message.text.split(":")[0]
        newToken=message.text.split(":")[1]


        # Define file paths
        file_path = "info.txt"  # Relative path (ensure it's correct)
        temp_file_path = "temp.txt"

        # Check if info.txt exists
        if not os.path.exists(file_path):
            sub_bot.reply_to(message, "info.txt file not found.")
            return

        # Open files using 'with' statement for proper handling
        with open(file_path, "r") as file, open(temp_file_path, "w") as fileWrite:
            for line in file:
                if line.startswith("Id"):
                    fileWrite.write(f"Id [{newId}]\n")
                elif line.startswith("Token"):
                    fileWrite.write(f"Token [{newToken}]\n")
                else:
                    fileWrite.write(line)

        # Replace info.txt with temp.txt
        os.remove(file_path)
        os.rename(temp_file_path, file_path)

        sub_bot.reply_to(message, "Update action performed.")
    except:
      sub_bot.reply_to(message, "Fiaa action Failed.")

def perform_start_action(message):
    try:
        # Provide the full path to omega.exe
        omega_path = "omega.exe"  # Replace with the full path if needed

        # Check if omega.exe is already running
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'omega.exe':
                sub_bot.reply_to(message, "omega.exe is already running.")
                return

        # Start omega.exe as a separate process
        subprocess.Popen(omega_path, shell=True)
        sub_bot.reply_to(message, "Successfully started omega.exe.")
    except Exception as e:
        sub_bot.reply_to(message, f"Failed to start omega.exe: {e}")

def perform_stop_action(message):
    try:
        # Find and kill all instances of omega.exe
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'omega.exe':
                proc.kill()  # Terminate the process
                killed = True

        if killed:
            sub_bot.reply_to(message, "Successfully stopped omega.exe.")
        else:
            sub_bot.reply_to(message, "omega.exe is not running.")
    except Exception as e:
        sub_bot.reply_to(message, f"Failed to stop omega.exe: {e}")

# Start polling
sub_bot.infinity_polling()