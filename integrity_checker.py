import hashlib
import os
import json

HASH_FILE = 'hashes.json'

def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def hash_all_files(directory):
    hash_dict = {}
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            hash_dict[filepath] = get_file_hash(filepath)
    return hash_dict

def save_hashes(hash_dict):
    with open(HASH_FILE, 'w') as f:
        json.dump(hash_dict, f, indent=4)

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, 'r') as f:
        return json.load(f)

def check_integrity(current_hashes, original_hashes):
    modified = []
    new = []
    deleted = []

    for path, hash_val in current_hashes.items():
        if path not in original_hashes:
            new.append(path)
        elif original_hashes[path] != hash_val:
            modified.append(path)

    for path in original_hashes:
        if path not in current_hashes:
            deleted.append(path)

    return modified, new, deleted

if __name__ == '__main__':
    directory = input("Enter directory to scan: ")
    mode = input("Choose mode (1: Save Hashes, 2: Check Integrity): ")

    if mode == '1':
        hashes = hash_all_files(directory)
        save_hashes(hashes)
        print("Hashes saved successfully.")
    elif mode == '2':
        current_hashes = hash_all_files(directory)
        original_hashes = load_hashes()
        modified, new, deleted = check_integrity(current_hashes, original_hashes)

        print("\n--- File Integrity Report ---")
        print("Modified Files:", modified)
        print("New Files:", new)
        print("Deleted Files:", deleted)
    else:
        print("Invalid option.")
