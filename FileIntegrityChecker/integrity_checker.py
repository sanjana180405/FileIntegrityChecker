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
        json.dump(hash_dict, f)

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, 'r') as f:
        return json.load(f)

def check_integrity(directory):
    old_hashes = load_hashes()
    current_hashes = hash_all_files(directory)

    modified = []
    new = []
    deleted = []

    for file, old_hash in old_hashes.items():
        if file not in current_hashes:
            deleted.append(file)
        elif current_hashes[file] != old_hash:
            modified.append(file)

    for file in current_hashes:
        if file not in old_hashes:
            new.append(file)

    return modified, new, deleted

# MAIN
if __name__ == "__main__":
    print("Choose mode (1: Save Hashes, 2: Check Integrity):")
    choice = input("Enter 1 or 2: ")

    directory = 'TestFiles'

    if choice == '1':
        hashes = hash_all_files(directory)
        save_hashes(hashes)
        print("Hashes saved successfully.")
    elif choice == '2':
        modified, new, deleted = check_integrity(directory)
        print("Modified files:", modified)
        print("New files:", new)
        print("Deleted files:", deleted)
    else:
        print("Invalid choice.")
