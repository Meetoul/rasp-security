import pickle
import os

STORAGE_PATH = 'storage'

def exists(key):
    path = os.path.join(STORAGE_PATH, key)
    return os.path.isfile(path)

def save(key, value):
    path = os.path.join(STORAGE_PATH, key)

    with open(path, 'wb') as output_file:
        pickle.dump(value, output_file)

def load(key):
    if not exists(key):
        return

    path = os.path.join(STORAGE_PATH, key)

    with open(path, 'rb') as input_file:
        value = pickle.load(input_file)

    return value
