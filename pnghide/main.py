import argparse
import sys
from cryptography.fernet import Fernet




PNG_SIGNATURE = [137, 80, 78, 71, 13, 10, 26, 10]
PNG_SIGNATURE_SIZE = 8

KEY = "kLxNqw6tMz_8sP4rTTN6HtK1Hm9LCtsBkacIqfXbDxI="




def read_uint8(file, num_bytes):
    uint8_values = []
    for _ in range(num_bytes):
        byte = file.read(1)
        if not byte:
            return None  # End of file reached
        uint8_values.append(int.from_bytes(byte, byteorder='big'))
    return uint8_values



def read_bytes(file, num_bytes, data_type):
    byte_data = read_uint8(file, num_bytes)
    if byte_data is None:
        return None  # End of file reached

    if data_type == 'uint8':
        return byte_data
    elif data_type == 'uint32':
        return int.from_bytes(byte_data, byteorder='big')
    else:
        raise ValueError(f"Unsupported data type: {data_type}")



def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data



def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def inject_chunk(file, data, chunk_type):
    chunk_length = len(data)

    chunk_type_bytes = bytes(chunk_type, 'ascii')

    file.write(chunk_length.to_bytes(4, byteorder='big'))

    file.write(chunk_type_bytes)

    file.write(data)

    crc32 = 0xDEADBEEF
    file.write(crc32.to_bytes(4, byteorder='big'))

    print(f"Injected chunk type: {chunk_type}, size: {chunk_length}")





def get_custom_chunk_data(file, chunk_length, decryption_key):
    # Read data from the custom chunk
    encrypted_data = file.read(chunk_length)

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, decryption_key)

    return decrypted_data



def extract_png_image(data, output_file):
    with open(output_file, 'wb') as f:
        f.write(data)
    print(f"PNG image extracted to: {output_file}")



def extract_text_data(data, output_file):
    with open(output_file, 'w') as f:
        f.write(data.decode('utf-8'))
    print(f"Text data extracted to: {output_file}")



def seek_to_next_chunk(file, chunk_length):
    try:
        file.seek(chunk_length + 4, 1)  # 4 bytes for CRC
        return True
    except OSError:
        return False  # Unable to seek




def PNG_reader(file_path, output_path):
    try:
        with open(file_path, 'rb') as file:
            # Verify PNG file signature
            signature = read_bytes(file, PNG_SIGNATURE_SIZE, 'uint8')
            # print(f"Signature: {signature}")
            if signature != PNG_SIGNATURE:
                print("Error: Signature does not match PNG signature.", file=sys.stderr)
                return

            # Chunk layout
            while True:
                # Chunk length
                chunk_length = read_bytes(file, 4, 'uint32')
                if chunk_length is None:
                    break  # End of file reached

                # Chunk Type
                chunk_type_bytes = read_bytes(file, 4, 'uint8')
                chunk_type = bytes(chunk_type_bytes).decode('ascii')

                # Chunk Data
                if chunk_type in ["IPNG", "TPNG"]:
                    custom_data = get_custom_chunk_data(file, chunk_length, KEY)
                    if chunk_type == "IPNG":
                        extract_png_image(custom_data, f'{output_path}.png')
                    elif chunk_type == "TPNG":
                        extract_text_data(custom_data, f'{output_path}.txt')
                    break  # No need to continue after custom chunk


                # print(f"Chunk length: {chunk_length}")
                # print(f"Chunk type: {chunk_type}")
                # print("--------------------------")


                # Seek to the next chunk
                if not seek_to_next_chunk(file, chunk_length):
                    print("Error: Unable to seek to the start of the next chunk.", file=sys.stderr)
                    return

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.", file=sys.stderr)






def embed(input_path, output_path, embed_path):
    try:
        with open(input_path, 'r+b') as infile, open(output_path, 'wb') as outfile:
            
            with open(embed_path, "rb") as embed_file:
                data = embed_file.read()

            # Copy input file to output file
            outfile.write(infile.read())

            
            encrypted_data = encrypt_data(data, KEY)
            # Inject an encrypted custom chunk containing the PNG image
            if embed_path.endswith(".png"):
                inject_chunk(outfile, encrypted_data, "IPNG")
            else:
                inject_chunk(outfile, encrypted_data, "TPNG")

                
    except FileNotFoundError:
        print(f"Error: The file {input_path} was not found.\n", file=sys.stderr)
        sys.exit(1)



def extract(input_path, output_path):
    PNG_reader(input_path, output_path)




def main():
    parser = argparse.ArgumentParser(description="Embed or extract data from a PNG file.")
    parser.add_argument('operation', type=str, choices=['embed', 'extract'], help="Choose 'embed' or 'extract'")
    parser.add_argument('--input', type=str, required=True, help="Path to the input PNG file")
    parser.add_argument('--output', type=str, required=True, help="Path to the output PNG file")

    args, extra_args = parser.parse_known_args()

    if args.operation == 'embed':
        embed_parser = argparse.ArgumentParser(description="Embed data into the PNG file.")
        embed_parser.add_argument('--file', type=str, required=True, help="Path to the image or text file to embed")
        embed_args = embed_parser.parse_args(extra_args)

        embed(args.input, args.output, embed_args.file)

    elif args.operation == 'extract':
        extract(args.input, args.output)



if __name__ == "__main__":
    main()