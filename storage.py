import pickle
import os

from config import STORAGE_DIR


def exists(key):
    path = os.path.join(STORAGE_DIR, key)
    return os.path.isfile(path)

def save(key, value):
    path = os.path.join(STORAGE_DIR, key)

    with open(path, 'wb') as output_file:
        pickle.dump(value, output_file)

def load(key):
    if not exists(key):
        return

    path = os.path.join(STORAGE_DIR, key)

    with open(path, 'rb') as input_file:
        value = pickle.load(input_file)

    return value
