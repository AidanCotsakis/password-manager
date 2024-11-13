
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
from PIL import Image
import numpy as np

READ_PATH = "image.png"
WRITE_PATH = "image.png"
ORIGINAL_PATH = "image.png"

def encrypt(password: str, plaintext: str) -> bytes:
	# Convert the password to bytes
	password_bytes = password.encode('utf-8')
	
	# Generate a random salt
	salt = os.urandom(16)
	
	# Derive a key using PBKDF2HMAC
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	key = kdf.derive(password_bytes)
	
	# Encrypt the plaintext using AES GCM
	aesgcm = AESGCM(key)
	nonce = os.urandom(12)  # 96-bit nonce
	ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
	
	# Combine salt, nonce, and ciphertext for storage
	encrypted_data = salt + nonce + ciphertext
	
	return encrypted_data

def decrypt(password: str, encrypted_data: bytes) -> str:
	# Extract salt, nonce, and ciphertext
	salt = encrypted_data[:16]
	nonce = encrypted_data[16:28]
	ciphertext = encrypted_data[28:]
	
	# Derive the key using the same method as encryption
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	key = kdf.derive(password.encode('utf-8'))
	
	# Decrypt the ciphertext using AES GCM
	aesgcm = AESGCM(key)
	plaintext = aesgcm.decrypt(nonce, ciphertext, None)
	
	return plaintext.decode('utf-8')

def bytesToBinaryString(data: bytes) -> str:
	binaryStr = ""
	for byte in data:
		binaryStr += bin(byte)[2:].zfill(8)

	return binaryStr

def binaryStringToBytes(binaryStr: str) -> bytes:
	byteArray = bytearray()
	
	for i in range(0, len(binaryStr), 8):
		byte = binaryStr[i:i+8]
		byteArray.append(int(byte, 2))
	
	return bytes(byteArray)

def writeImage(image_path, binary_string, output_image_path, length_bits=64):
	binary_length = len(binary_string)
	length_binary = format(binary_length, f'0{length_bits}b')

	full_binary_string = length_binary + binary_string

	image = Image.open(image_path)
	image_array = np.array(image)
	flat_image_array = image_array.flatten()

	binary_array = np.array([int(bit) for bit in full_binary_string])

	if len(binary_array) > len(flat_image_array[:len(binary_array)]):
		raise ValueError("Binary string is too long to fit in the image")

	flat_image_array[:len(binary_array)] = (flat_image_array[:len(binary_array)] & ~1) | binary_array
	image_array = flat_image_array.reshape(image_array.shape)
	
	edited_image = Image.fromarray(image_array)
	edited_image.save(output_image_path)

def readImage(image_path, length_bits=64):
	image = Image.open(image_path)
	image_array = np.array(image)
	flat_image_array = image_array.flatten()

	length_binary = ''.join(map(str, flat_image_array[:length_bits] & 1))
	binary_length = int(length_binary, 2)

	extracted_bits = flat_image_array[length_bits:length_bits + binary_length] & 1
	binary_string = ''.join(map(str, extracted_bits))
	
	return binary_string

def write(password: str, plaintext: str):
	encryptedData = encrypt(password, plaintext)
	binary = bytesToBinaryString(encryptedData)
	writeImage(ORIGINAL_PATH, binary, WRITE_PATH)

def read(password: str):
	binary = readImage(READ_PATH)
	encryptedData = binaryStringToBytes(binary)
	plaintext = decrypt(password, encryptedData)

	return plaintext
