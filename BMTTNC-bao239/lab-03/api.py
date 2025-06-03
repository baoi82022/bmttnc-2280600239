from flask import Flask, request, jsonify
from cipher.rsa import RSACipher

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data.get('message')
    key_type = data.get('key_type')

    if not message or key_type not in ['public', 'private']:
        return jsonify({'error': 'Missing or invalid input'}), 400

    private_key, public_key = rsa_cipher.load_keys()
    key = public_key if key_type == 'public' else private_key

    encrypted_bytes = rsa_cipher.encrypt(message, key)
    encrypted_hex = encrypted_bytes.hex()

    return jsonify({'encrypted_message': encrypted_hex})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data.get('ciphertext')
    key_type = data.get('key_type')

    if not ciphertext_hex or key_type not in ['public', 'private']:
        return jsonify({'error': 'Missing or invalid input'}), 400

    private_key, public_key = rsa_cipher.load_keys()
    key = public_key if key_type == 'public' else private_key

    try:
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        return jsonify({'error': 'Invalid hex format'}), 400

    decrypted_message = rsa_cipher.decrypt(ciphertext_bytes, key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Missing message'}), 400

    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(message, private_key)
    signature_hex = signature.hex()

    return jsonify({'signature': signature_hex})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')

    if not message or not signature_hex:
        return jsonify({'error': 'Missing message or signature'}), 400

    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'Invalid hex format for signature'}), 400

    public_key, _ = rsa_cipher.load_keys()
    is_verified = rsa_cipher.verify(message, signature, public_key)

    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
