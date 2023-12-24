import os
import zipfile
from PIL import Image
from tqdm import tqdm

def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, quality=quality)

def zip_folder(folder_path, zip_path, compression_level=9):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
        file_list = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)

        # Use tqdm to track the compression progress
        for file_path in tqdm(file_list, desc="Compressing", unit="file"):
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                compressed_image_path = os.path.join(os.path.dirname(file_path), f"compressed_{os.path.basename(file_path)}")
                compress_image(file_path, compressed_image_path)
                arc_name = os.path.relpath(compressed_image_path, folder_path)
                zipf.write(compressed_image_path, arcname=arc_name)
                os.remove(compressed_image_path)
            else:
                arc_name = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arc_name)

if __name__ == "__main__":
    folder_to_compress = input("Enter the path to the folder to compress: ")
    compression_level = int(input("Enter the compression level (0 to 9, where 9 is maximum compression): "))

    if not os.path.exists(folder_to_compress):
        print("Error: The specified folder does not exist.")
    else:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_zip_path = os.path.join(desktop_path, 'compressed_folder.zip')

        zip_folder(folder_to_compress, output_zip_path, compression_level)
        print(f"Folder '{folder_to_compress}' compressed successfully to '{output_zip_path}' with compression level {compression_level}.")
