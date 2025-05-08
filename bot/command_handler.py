from bot.irc_client import send_message
from bot.twitch_api import get_access_token, get_stream_info, get_user_id, get_followers

def handle_command(username, command, args, commands, sock, CHANNEL):
    try:
        if command in commands:
            response = commands[command].get('response', '').replace('{user}', username)
            send_message(sock, CHANNEL, response)
        elif command == '!uptime':
            token = get_access_token()
            user_id = get_user_id(token)
            uptime = get_stream_info(token, user_id)
            send_message(sock, CHANNEL, uptime)
        elif command == '!followers':
            token = get_access_token()
            user_id = get_user_id(token)
            followers = get_followers(token, user_id)
            send_message(sock, CHANNEL, followers)


    except Exception as e:
        print(f"Error handling command '{command}': {e}")
        send_message(sock, CHANNEL, f"An error occurred while processing your command: {e}")