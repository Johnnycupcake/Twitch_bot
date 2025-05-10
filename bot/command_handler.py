from bot.irc_client import send_message
from bot.twitch_api import load_tokens

tokens = load_tokens()

def handle_command(username, command, args, commands, sock, CHANNEL):
    try:
        if command in commands:
            response = commands[command].get('response', '').replace('{user}', username)
            send_message(sock, CHANNEL, response)


    except Exception as e:
        print(f"Error handling command '{command}': {e}")
        send_message(sock, CHANNEL, f"An error occurred while processing your command: {e}")