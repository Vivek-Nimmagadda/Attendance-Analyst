# import base64
#
# from Crypto.Cipher import AES
#
#
# def encrypt(text):
#     encryption_suite = AES.new('This is a key123', AES.MODE_CFB, 'This is a key123')
#     cipher_text = encryption_suite.encrypt(text)
#     return cipher_text
#
#
# def decrypt(text):
#     decryption_suite = AES.new('This is a key123', AES.MODE_CFB, 'This is a key123')
#     plain_text = decryption_suite.decrypt(text)
#     return plain_text
#


from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16

PADDING = '{'

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# generate a random secret key
secret = "\xee\x9d\xcfx\xbc\x0b\xb3'\xad\xae\xd3\xfa\xa2;\xd5\x86"

# create a cipher object using the random secret
cipher = AES.new(secret)


def encode(str):
    global cipher
    encoded = EncodeAES(cipher, str)
    return encoded


def decode(str):
    global cipher
    decoded = DecodeAES(cipher, str)
    return decoded
