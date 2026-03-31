import string
import secrets
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- Password Generator ----------------
def generate_password(base_word="", length=12):
    substitutions = {'a': '@', 's': '$', 'o': '0', 'i': '1', 'e': '3'}
    base_word = base_word.strip()
    transformed = "".join(substitutions.get(c.lower(), c) for c in base_word)
    
    password = list(transformed.capitalize())
    
    characters = string.ascii_letters + string.digits + string.punctuation
    
    while len(password) < length:
        password.append(secrets.choice(characters))
    
    extra_part = password[len(transformed):]
    secrets.SystemRandom().shuffle(extra_part)
    final_password = password[:len(transformed)] + extra_part
    return ''.join(final_password)

# ---------------- KeePass Integration ----------------
def save_to_keepass(kdbx_file, kdbx_password, entry_title, username, password):
    try:
        from pykeepass import PyKeePass
    except ImportError:
        return False, "pykeepass não está instalado. Corre: pip install pykeepass"

    try:
        kp = PyKeePass(kdbx_file, password=kdbx_password)
    except FileNotFoundError:
        return False, f"Ficheiro KeePass '{kdbx_file}' não encontrado."
    except Exception as e:
        return False, f"Erro ao abrir KeePass: {e}"

    existing_entry = kp.find_entries(title=entry_title, username=username, first=True)
    
    if existing_entry:
        existing_entry.password = password
        msg = f"Entrada existente encontrada. Password atualizada para: {entry_title}"
    else:
        kp.add_entry(kp.root_group, entry_title, username, password)
        msg = f"Nova entrada criada no KeePass: {entry_title}"
    
    kp.save()
    return True, msg

# ---------------- API Routes ----------------
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    base_word = data.get('base', '')
    try:
        length = int(data.get('length', 12))
        if length < 4 or length > 64:
            return jsonify({'error': 'Tamanho deve ser entre 4 e 64'}), 400
    except ValueError:
        return jsonify({'error': 'Tamanho inválido'}), 400

    password = generate_password(base_word, length)
    return jsonify({'password': password})

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    
    required = ['password', 'title', 'username', 'kdbx_file', 'kdbx_password']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo obrigatório em falta: {field}'}), 400

    success, msg = save_to_keepass(
        data['kdbx_file'],
        data['kdbx_password'],
        data['title'],
        data['username'],
        data['password']
    )
    
    if success:
        return jsonify({'message': msg})
    else:
        return jsonify({'error': msg}), 500

@app.route('/generate-and-save', methods=['POST'])
def generate_and_save():
    data = request.get_json()
    
    base_word = data.get('base', '')
    try:
        length = int(data.get('length', 12))
    except ValueError:
        return jsonify({'error': 'Tamanho inválido'}), 400

    password = generate_password(base_word, length)

    required = ['title', 'username', 'kdbx_file', 'kdbx_password']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400

    success, msg = save_to_keepass(
        data['kdbx_file'],
        data['kdbx_password'],
        data['title'],
        data['username'],
        password
    )

    if success:
        return jsonify({'password': password, 'message': msg})
    else:
        return jsonify({'error': msg}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
