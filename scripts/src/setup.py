import os, sys, platform, subprocess

EXPECTED_NODE_PATH = "{}\\nodejs".format(os.environ["ProgramFiles"])

def rerun(arg, env=os.environ):
    subprocess.Popen(["python", "./scripts/src/setup.py", arg], cwd=os.getcwd(), env=env)

def is_node_installed():
    return os.system("node --version") == 0

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
        
        rerun("skip_to_end")
        sys.exit(0)

if __name__ == "__main__":

    skip_to_end = len(sys.argv) > 1 and sys.argv[1] == "skip_to_end"

    if not is_node_installed() and os.path.isdir(EXPECTED_NODE_PATH):
        print("Adding node to system path")
        process = subprocess.Popen(["powershell", "-Command", "[Environment]::SetEnvironmentVariable(\"Path\", $env:Path + \";{};\", [EnvironmentVariableTarget]::Machine)".format(EXPECTED_NODE_PATH)])
        process.wait()

        env = os.environ.copy()
        env.update({"PATH": "{};{};".format(EXPECTED_NODE_PATH, os.environ["PATH"])})
        rerun(sys.argv[1] if len(sys.argv) > 1 else "", env)
        sys.exit(0)

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