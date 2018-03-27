import os, shutil

def clear_dir(file_path):
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

if __name__ == "__main__":
    
    directory = "./test/"
    clear_dir(directory + "serv_dir/")
    clear_dir(directory + "client_dir/")