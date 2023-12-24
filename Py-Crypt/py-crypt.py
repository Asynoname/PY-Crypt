from cryptography.fernet import Fernet
import os
from pathlib import Path
from colorama import init, Fore, Style
from tqdm import tqdm

init(autoreset=True)

def generate_key():
    key = Fernet.generate_key()
    print(f"{Fore.GREEN}Generated Key:{Style.RESET_ALL} {key.decode('utf-8')}")
    return key

def write_key(key, key_filename="secret.key"):
    with open(key_filename, "wb") as key_file:
        key_file.write(key)

def load_key(key_filename="secret.key"):
    try:
        with open(key_filename, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Key file not found.{Style.RESET_ALL}")
        exit()

def encrypt_folder_to_file(folder_path, key, output_filename="encrypted_data.dat"):
    cipher = Fernet(key)
    encrypted_data_list = []

    file_count = sum(len(files) for _, _, files in os.walk(folder_path))

    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in tqdm(filenames, desc="Encrypting", total=file_count):
            file_path = os.path.join(foldername, filename)
            with open(file_path, "rb") as file:
                plaintext = file.read()
                encrypted_data = cipher.encrypt(plaintext)
                encrypted_data_list.append((file_path, encrypted_data))

    output_filepath = os.path.join(Path.home(), output_filename)

    with open(output_filepath, "wb") as output_file:
        for file_path, encrypted_data in tqdm(encrypted_data_list, desc="Writing to file", total=file_count):
            relative_path = os.path.relpath(file_path, folder_path)
            output_file.write(relative_path.encode('utf-8') + b'\n')
            output_file.write(encrypted_data + b'\n')

def decrypt_file_to_folder(input_filename, key, output_folder_path):
    cipher = Fernet(key)

    try:
        with open(input_filename, "rb") as input_file:
            lines = input_file.readlines()

        decrypted_data_list = []

        for i in tqdm(range(0, len(lines), 2), desc="Decrypting", total=len(lines) // 2):
            relative_path = lines[i].decode('utf-8').strip()
            encrypted_data = lines[i + 1].strip()
            decrypted_data = cipher.decrypt(encrypted_data)
            decrypted_data_list.append((relative_path, decrypted_data))

        for relative_path, decrypted_data in tqdm(decrypted_data_list, desc="Writing to folder", total=len(decrypted_data_list)):
            output_file_path = os.path.join(output_folder_path, relative_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, "wb") as file:
                file.write(decrypted_data)
    except Exception as e:
        print(f"{Fore.RED}Error during decryption:{Style.RESET_ALL} {e}")

def print_banner():
    banner = f"""{Fore.CYAN}
░█▀█░█░█░░░░░█▀▀░█▀▄░█░█░█▀█░▀█▀
░█▀▀░░█░░▄▄▄░█░░░█▀▄░░█░░█▀▀░░█░
░▀░░░░▀░░░░░░▀▀▀░▀░▀░░▀░░▀░░░░▀░
  
{Fore.YELLOW}Made by AsyNoName{Style.RESET_ALL}"""
    print(banner)

def main():
    print_banner()
    action = input(f"{Fore.YELLOW}Enter 'e' for encrypt or 'd' for decrypt:{Style.RESET_ALL} ").lower()
    key_filename = "secret.key"

    if os.path.exists(key_filename):
        key = load_key(key_filename)
    else:
        key = generate_key()
        write_key(key, key_filename)

    if action == 'e':
        folder_path = input(f"{Fore.YELLOW}Enter the folder path to encrypt:{Style.RESET_ALL} ")
        folder_path = os.path.normpath(folder_path)  # Normalize path separators
        encrypt_folder_to_file(folder_path, key)
    elif action == 'd':
        input_filename = input(f"{Fore.YELLOW}Enter the encrypted file path to decrypt:{Style.RESET_ALL} ")
        input_filename = os.path.normpath(input_filename)  # Normalize path separators

        if not os.path.isfile(input_filename):
            print(f"{Fore.RED}Error: The provided path is not a file. Please provide a valid file path.{Style.RESET_ALL}")
            return

        output_folder_path = input(f"{Fore.YELLOW}Enter the folder path to store decrypted files:{Style.RESET_ALL} ")
        output_folder_path = os.path.normpath(output_folder_path)  # Normalize path separators
        decrypt_file_to_folder(input_filename, key, output_folder_path)
    else:
        print(f"{Fore.RED}Invalid action. Please enter 'e' for encrypt or 'd' for decrypt.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
