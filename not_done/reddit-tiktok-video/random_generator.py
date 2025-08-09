#generate unique uuid and then hash it with sha512
import uuid
import hashlib
import os
import time
import random

def generate_unique_uuid():
    # Generate a random UUID
    unique_id = uuid.uuid4()

    # Hash the UUID using SHA-512
    sha512_hash = hashlib.sha512(str(unique_id).encode()).hexdigest()
    #cut it to 20 characters
    sha512_hash = sha512_hash[:20]

    return sha512_hash

# geenrate random password that has lower and capital letters , numbers and symbols and is maximum 20 chars
def generate_random_password(length=20):
    characters = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789'
        '!@#$%?'
    )
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

print(generate_random_password())


#Omqsx9GPQ3KV2DtNc!XD