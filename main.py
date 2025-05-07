import os
from dotenv import load_dotenv
from bot.irc_client import connect_to_twitch, send_message, parse_message
from bot.json_loader import load_json, save_json
from bot.command_handler import handle_command



SERVER = 'irc.chat.twitch.tv'
PORT = 443

load_dotenv()
TOKEN = os.getenv('TMI_TOKEN')
NICKNAME = 'xtremetenticalbot'
CHANNEL = '#xtremetenticalcorn'

sock = connect_to_twitch(SERVER, PORT, TOKEN, NICKNAME, CHANNEL)
try:
    commands = load_json(os.path.join('config', 'commands.json'))
except FileNotFoundError:
    commands = {}

while True:
        
    response = sock.recv(2048).decode('utf-8')
    if response.startswith('PING'):
        sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        continue

    username, message = parse_message(response)
    print(response)
    if username and message:
        try:
            split_msg = message.split(' ', 1)
            command = split_msg[0]
            print(command)
            args = split_msg[1] if len(split_msg) > 1 else ''
            handle_command(username, command, args, commands, sock, CHANNEL)
        except Exception as e:
            print(f"Error processing message: {e}")
