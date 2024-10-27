import requests
import base64
import hashlib
import Crypto
import Crypto.Cipher.AES
import Crypto.Random
import Crypto.Util.Padding
import cfscrape

class AESGibberish:
    def __init__(self):
        # Code by drake-mer on github
        # https://github.com/drake-mer/gibberish-aes-python/tree/master

        pass

    def rawEncrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        """Return the padded cipher text with the default blocksize of 16."""
        return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv=iv).encrypt(
            Crypto.Util.Padding.pad(plaintext, 16)
        )


    def rawDecrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        return Crypto.Util.Padding.unpad(
            Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv=iv).decrypt(ciphertext),
            16
        )


    def openSSLKey(self, password: str, salt: bytes):
        salted_password = password.encode('utf-8') + salt
        hash_1 = hashlib.md5(salted_password).digest()
        hash_2 = hashlib.md5(hash_1 + salted_password).digest()
        hash_3 = hashlib.md5(hash_2 + salted_password).digest()
        return (hash_1 +  hash_2, hash_3)


    def enc(self, plaintext: str, password: str):
        salt = Crypto.Random.get_random_bytes(8)
        return base64.b64encode(
            b'Salted__' + salt + self.rawEncrypt(plaintext.encode('utf-8'), * self.openSSLKey(password, salt))
        )


    def dec(self, ciphertext: str, password: str):
        ciphertext = base64.b64decode(ciphertext)
        salt = ciphertext[8:16]
        ciphertext = ciphertext[16:]
        return self.rawDecrypt(ciphertext, * self.openSSLKey(password, salt))

class Privnote:
    def __init__(self):
        # Original by abkrn on github made for node js
        # I've converted it to python
        # https://github.com/abrkn/privnote

        self.aes = AESGibberish()
        self.cipher = "aes-256-cbc"
        self.base_url = "https://privnote.com/"
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.scraper = cfscrape.create_scraper(sess=self.session)
    
    def decrypt(self, data, password):
        return self.aes.dec(data, password)

    def read(self, link):
        code = link.split("privnote.com/")[1].split(" ")[0]
        code, password = code.split("#")

        resp = self.scraper.delete(self.base_url + code, headers=self.headers)
        data = resp.json()
        
        if "destroyed" not in data:
            return False, "Invalid privnote link."
        elif "data" not in data and "destroyed" in data:
            return False, "Privnote has already been read."
        else:
            encyrpted = data["data"]
            decrypted = self.decrypt(encyrpted, password)
            return True, decrypted.decode("utf-8")
    
if __name__ == "__main__":
    privnote = Privnote()
    link = input("Enter the privnote link: ")
    print(privnote.read(link))