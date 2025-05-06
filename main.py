import os
import logging
from dotenv import load_dotenv
from bot.irc_client import connect_to_twitch, send_message, parse_message
from bot.json_loader import load_json, save_json
from bot.command_handler import handle_command

SERVER = 'irc.chat.twitch.tv'
PORT = 443

load_dotenv()
TOKEN = os.getenv('TMI_TOKEN')
NICKNAME = 'xtremetenticalcorn'
CHANNEL = '#xtremetenticalcorn'

sock = connect_to_twitch(SERVER, PORT, TOKEN, NICKNAME, CHANNEL)
commands = load_json('commands.json', default={})

while True:
    response = sock.recv(2048).decode('utf-8')
    if response.startswith('PING'):
        sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        continue

    username, message = parse_message(response)
    if username and message:
        split_msg = message.lower().split(' ', 1)
        command = split_msg[0]
        args = split_msg[1] if len(split_msg) > 1 else ''
        handle_command(username, command, args, commands, sock, CHANNEL)
