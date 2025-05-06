import socket
import ssl
import logging

def connect_to_twitch(server, port, token, nickname, channel):
    context = ssl.create_default_context()
    sock = socket.create_connection((server, port))
    sock = context.wrap_socket(sock, server_hostname=server)
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
    print(f"Connected to {channel} as {nickname}")
    return sock

def send_message(sock, channel, message):
    sock.send(f"PRIVMSG {channel} :{message}\r\n".encode('utf-8'))

def parse_message(msg):
    """Parse a raw IRC message to extract username and message content."""
    if 'PRIVMSG' not in msg:
        return None, None
    try:
        username = msg.split('!', 1)[0][1:]
        message = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]
        print(username, message)
        return username, message.strip()
    except Exception as e:
        logging.error(f"Error parsing message: {e}")
        return None, None