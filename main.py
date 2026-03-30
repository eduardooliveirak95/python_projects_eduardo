import string
import secrets
import argparse
from pykeepass import PyKeePass

# ---------------- Password Generator ----------------
def generate_password(base_word="", length=12):
    substitutions = {'a': '@', 's': '$', 'o': '0', 'i': '1', 'e': '3'}
    base_word = base_word.strip()
    transformed = "".join(substitutions.get(c.lower(), c) for c in base_word)
    
    # Capitaliza a primeira letra
    password = list(transformed.capitalize())
    
    # Caracteres extras
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Completa até ao tamanho desejado
    while len(password) < length:
        password.append(secrets.choice(characters))
    
    # Baralha apenas a parte extra
    extra_part = password[len(transformed):]
    secrets.SystemRandom().shuffle(extra_part)
    final_password = password[:len(transformed)] + extra_part
    return ''.join(final_password)

# ---------------- KeePass Integration ----------------
def save_to_keepass(kdbx_file, kdbx_password, entry_title, username, password):
    try:
        kp = PyKeePass(kdbx_file, password=kdbx_password)
    except FileNotFoundError:
        print(f"[!] KeePass file '{kdbx_file}' not found.")
        return
    except Exception as e:
        print(f"[!] Error opening KeePass: {e}")
        return

    # Procura entrada existente pelo título e username
    existing_entry = kp.find_entries(title=entry_title, username=username, first=True)
    
    if existing_entry:
        existing_entry.password = password
        print(f"[✔] Existing entry found. Password updated for: {entry_title}")
    else:
        kp.add_entry(kp.root_group, entry_title, username, password)
        print(f"[✔] New entry created in KeePass: {entry_title}")

    kp.save()

# ---------------- CLI / Prompts ----------------
def main():
    parser = argparse.ArgumentParser(description="🔐 Password Generator + KeePass CLI")
    
    parser.add_argument("--length", type=int, help="Tamanho da password")
    parser.add_argument("--base", type=str, help="Palavra base")
    parser.add_argument("--title", type=str, help="Título da entrada (site/app)")
    parser.add_argument("--user", type=str, help="Username/Login")
    parser.add_argument("--kdbx", type=str, help="Ficheiro KeePass (.kdbx)")
    parser.add_argument("--kdbx-pass", type=str, help="Password do ficheiro KeePass")
    
    args = parser.parse_args()

    # Prompts se não houver argumentos
    if args.length is None:
        args.length = int(input("Tamanho da password (default 12): ") or 12)
    if args.base is None:
        args.base = input("Palavra base (opcional): ")
    if args.title is None:
        args.title = input("Título da entrada (site/app): ")
    if args.user is None:
        args.user = input("Username/Login: ")
    if args.kdbx is None:
        args.kdbx = input("Ficheiro KeePass (.kdbx): ")
    if args.kdbx_pass is None:
        args.kdbx_pass = input("Password do ficheiro KeePass: ")

    try:
        password = generate_password(args.base, args.length)
        print(f"\nGenerated password: {password}\n")
        save_to_keepass(args.kdbx, args.kdbx_pass, args.title, args.user, password)
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()