import socket
import ssl
import logging
import os
from bot.twitch_api import load_tokens

def connect_to_twitch(server, port, TOKEN, NICKNAME, CHANNEL):
    TOKEN = load_tokens()['access_token']
    TOKEN = "oauth:" + TOKEN
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((server, port))
        sock = context.wrap_socket(sock, server_hostname=server)
        sock.send(f"PASS {TOKEN}\r\n".encode('utf-8'))
        sock.send(f"NICK {NICKNAME}\r\n".encode('utf-8'))
        sock.send(f"JOIN {CHANNEL}\r\n".encode('utf-8'))
        print(f"Connected to {CHANNEL} as {NICKNAME}")
        print(sock)
        return sock
    except Exception as e:
        logging.error(f"Error connecting to Twitch: {e}")
        raise

def send_message(sock, CHANNEL, message):
    try:
        sock.send(f"PRIVMSG {CHANNEL} :{message}\r\n".encode('utf-8'))
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        raise

def parse_message(msg):
    """Parse a raw IRC message to extract username and message content."""
    if 'PRIVMSG' not in msg:
        print(msg)
    # try:
    #     username = msg.split('!', 1)[0][1:]
    #     message = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]
    #     print(username, message)
    #     return username, message.strip()
    # except Exception as e:
    #     logging.error(f"Error parsing message: {e}")
    #     return None, None