import os, sys, platform, subprocess

def is_node_installed():
    try:
        subprocess.check_output("node --version")
        return True
    except:
        return False

def install_node():
    is_64 = sys.maxsize > 2**32

    if platform.system() == "Windows":
        import requests

        url = "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x86.msi"
        if is_64:
            url = "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x64.msi"

        print("Downloading Node.js {}-bit installer to node_setup.msi".format(64 if is_64 else 32))
        file_stream = requests.get(url, stream=True)
        file_stream.raise_for_status()
        with open('node_setup.msi', 'wb') as setup_file:
            for chunk in file_stream.iter_content(1024):
                setup_file.write(chunk)

        print("Installing Node.js")
        os.system("msiexec.exe /i node_setup.msi /QN")
        os.remove("node_setup.msi")

        my_env = os.environ

        node_path = "{}/nodejs".format(os.environ["ProgramFiles"])
        if os.path.isfile("{}/node.exe".format(node_path)):
            my_env = os.environ.copy()
            my_env["PATH"] = "{};{}".format(node_path, my_env["PATH"])
        
        subprocess.Popen(["python", "./scripts/src/setup.py".format(os.getcwd()), "skip_to_end"], cwd=os.getcwd(), env=my_env)

        sys.exit(0)

if __name__ == "__main__":

    skip_to_end = len(sys.argv) > 1 and sys.argv[1] == "skip_to_end"

    if not skip_to_end:
        print("Installing pip requirements")
        os.system("python -m pip install --no-cache -r requirements.txt")

        if not is_node_installed():
            install_node()

    else:
        if not is_node_installed():
            print("Node was not installed successfully")

    print("Installing node modules")
    os.chdir("web")
    os.system("npm install package.json")
    os.chdir("..")

    print("Creating test files")
    os.chdir("scripts")
    os.system("create_test_files")

    print("Clearing test directories")
    os.system("clear_test_dirs")