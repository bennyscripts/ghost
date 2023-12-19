alphabet = list("abcdefghijklmnopqrstuvwxyz 1234567890!@£$%^&*()_+€#")
alphabet.append("{space}")
char_to_num = lambda char : alphabet.index(char) + 1
num_to_char = lambda num : alphabet[num - 1]

def encrypt(string, key):
    encrypted = []
    string.replace(" ", "{SPACE}")

    for word in string.split():
        for char in list(word):
            num = char_to_num(char)
            
            for _ in range(key):
                num = (num * 3) - 5
            
            encrypted.append(num)

    return "-".join([str(item) for item in encrypted])

def decrypt(cipher, key):
    new_cipher = [int(item) for item in cipher.split("-")]
    decrypted = []

    for num in new_cipher:
        word = ""

        for _ in range(key):
            num = int((num + 5) / 3)

        word += num_to_char(num)
        decrypted.append(word)

    return "".join(decrypted)

@ghost.command(name="encrypt", description="Encrypt some text.", usage="[text]")
async def encrypt_cmd(ctx, *, text):
    await ctx.send(encrypt(text, 5))

@ghost.command(name="decrypt", description="Decrypt some text.", usage="[text]")
async def decrypt_cmd(ctx, *, text):
    await ctx.send(decrypt(text, 5))