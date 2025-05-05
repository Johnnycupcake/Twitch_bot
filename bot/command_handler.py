from irc_client import send_message

def handle_command(username, command, args, commands, sock, CHANNEL):
    if command in commands:
        response = commands[command].get('response', '').replace('{user}', username)
        send_message(sock, CHANNEL, response)
    