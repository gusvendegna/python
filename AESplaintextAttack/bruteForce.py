from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64




iv = b'\0'*16

plainText = b'This is a top secret.'

targetCipher = '8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9'


with open('words_alpha.txt') as dic:
    for word in dic:
        if len(word) > 16:
            continue
        word = word.strip()
        key = bytes(word.ljust(16), encoding='utf-8')
      
        cipher = AES.new(key, AES.MODE_CBC, iv)

        cipherText = cipher.encrypt(pad(plainText, AES.block_size))

        if (bytes.fromhex(targetCipher) == cipherText):
            print("Key: " + word)
            break
        
        
