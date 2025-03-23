import os


def ifFolderExists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
