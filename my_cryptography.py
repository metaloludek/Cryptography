from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

def encrypt_file(input_path, key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
        cipher_suite = Fernet(key)

    with open(input_path, 'rb') as input_file:
        file_data = input_file.read()
        encrypted_data = cipher_suite.encrypt(file_data)

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename, extension = os.path.splitext(input_path)
    output_path = f"Encrypted{current_time}({extension})"
    with open(output_path, 'wb') as output_file:
        output_file.write(encrypted_data)

    print('File encrypted successfully.')

def decrypt_file(input_path, key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
        cipher_suite = Fernet(key)

    with open(input_path, 'rb') as input_file:
        file_data = input_file.read()
        decrypted_data = cipher_suite.decrypt(file_data)

    filename = os.path.basename(input_path)
    extension_start = filename.rfind('(')
    extension_end = filename.rfind(')')
    if extension_start != -1 and extension_end != -1:
        extension = filename[extension_start + 1:extension_end]
    else:
        extension = ''

    output_filename = filename
    if extension_start != -1:
        output_filename = filename[:extension_start] + filename[extension_end+2:]
    output_path = f"Decrypted_{output_filename}"
    if extension:
        output_path += f".{extension}"
    with open(output_path, 'wb') as output_file:
        output_file.write(decrypted_data)

    print('File decrypted successfully.')


@app.route('/', methods=['GET', 'POST'])
def encrypt_endpoint():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'encrypt':
            input_path = request.form.get('input_path')
            key_path = request.form.get('key_path')

            if not key_path or key_path.isspace():
                key_path = None

            if input_path:
                encrypt_file(input_path, key_path)
                return jsonify({'message': 'File encrypted successfully.'})
            else:
                return jsonify({'message': 'Please provide input file path.'})
        
        elif action == 'decrypt':
            input_path = request.form.get('input_path')
            key_path = request.form.get('key_path')

            if input_path and key_path:
                decrypt_file(input_path, key_path)
                return jsonify({'message': 'File decrypted successfully.'})
            else:
                return jsonify({'message': 'Please provide input file path and key file path.'})
    else:
        return '''
            <h1>File Encryption API</h1>
            <form method="POST" action="/">
                <label for="action">Choose Action:</label>
                <select id="action" name="action">
                    <option value="encrypt">Encrypt</option>
                    <option value="decrypt">Decrypt</option>
                </select><br><br>
                <label for="input_path">Input File Path:</label>
                <input type="text" id="input_path" name="input_path"><br><br>
                <label for="key_path">Key File Path:</label>
                <input type="text" id="key_path" name="key_path"><br><br>
                <input type="submit" value="Submit">
            </form>
        '''

if __name__ == '__main__':
    app.run()
