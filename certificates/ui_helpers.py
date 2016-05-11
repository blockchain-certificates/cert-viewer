import binascii
import sys


unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')


def obfuscate_email_display(email):
    """Hides parts of email before displaying"""
    hidden_email_parts = email.split("@")
    hidden_email = hidden_email_parts[0][:2] + ("*" * (len(hidden_email_parts[0]) - 2)) + "@" + hidden_email_parts[1]
    return hidden_email
