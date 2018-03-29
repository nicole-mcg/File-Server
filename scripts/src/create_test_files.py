import os

if __name__ == "__main__":
    os.chdir("..")
    
    file_contents = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"

    file_path = "./test/"

    os.makedirs(os.path.dirname(file_path + "serv_dir/"), exist_ok=True)
    os.makedirs(os.path.dirname(file_path + "client_dir/"), exist_ok=True)

    file_path +=  "test_files/"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    for i in range(0, 50):
        file = open(file_path + str(i),'wb')
        file.write(str.encode(file_contents * 100000))
        file.close()