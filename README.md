# Password Manager with PgUI and Encryption

A comprehensive password management application built with a custom Pygame-based GUI, **PgUI**, and enhanced with robust encryption and steganography features. This project integrates secure password handling, random generation, and hidden image storage capabilities.

## Features

- **Custom PgUI Interface**: Interactive GUI built from scratch with Pygame for managing stored passwords seamlessly.
- **AES-GCM Encryption**: Implements industry-standard AES-GCM for encrypting passwords, ensuring secure storage and retrieval.
- **Image Steganography**: Stores encrypted data within images to add an extra layer of security.
- **Random Password Generator**: Generates strong, random passwords with a single click for enhanced security.
- **Clipboard Integration**: Allows users to copy sensitive information quickly without manual entry.

## Setup

### Prerequisites

- **Python 3.8+**
- Required Libraries: Install dependencies with:

  ```bash
  pip install pygame cryptography pillow numpy
  ```

### **File Structure**
- **main.py**: Initializes the GUI and manages user interaction and password storage.
- **encryption.py**: Handles password encryption, decryption, and storage within images.
- **PgUI**: Custom-built module for handling the Pygame-based GUI.

## **Usage**
1. **Run the Application**: Start the main script with:

    ```bash
    python main.py
    ```

2. **Select image to store data:** Add an image to the directory and name it `image.png`.

3. **Set master password:** Run `encryption.py` to set the image up with a master password.

4. **Load Encrypted Data**: Run `main.py` and enter the correct password and press `Enter` to view stored data.

5. **Create a New Password**: Click the '+' button, fill in fields, and save.

6. **Random Passwords**: Click the randomize button to generate a secure password instantly.

7. **Copy to Clipboard**: Click the copy icon next to a field to quickly copy information.

## **Security Details**
- **AES-GCM with PBKDF2-HMAC**: The application derives encryption keys using PBKDF2-HMAC with SHA256, and securely encrypts passwords.
- **Steganography in Images**: Data is stored by encoding binary data into image pixels, providing secure, hidden storage.