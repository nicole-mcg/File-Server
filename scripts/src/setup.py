import os, sys, platform, subprocess, json, webbrowser, time

JAVA_INSTALLER_URLS = {
    "Windows": {
        "32": "http://download2098.mediafire.com/f8114fw87tjg/yg8gamtuvqbj583/jre-8u171-windows-i586.exe",
        "64": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x64.msi"
    }
}

NODE_INSTALLER_URLS = {
    "Windows": {
        "32": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x86.msi",
        "64": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x64.msi"
    }
}

is_64 = sys.maxsize > 2**32
curr_os = platform.system()


EXPECTED_JAVA_PATH = ""
EXPECTED_NODE_PATH = ""

if curr_os == "Windows":
    EXPECTED_NODE_PATH = "{}\\nodejs".format(os.environ["ProgramFiles"])
    EXPECTED_JAVA_PATH = "{}\\Common Files\\Oracle\\Java\\javapath".format(os.environ["ProgramFiles(X86)"])


def add_conf_if_needed(conf, default=False):
    if not conf in setup_conf:
        setup_conf[conf] = False

file = open("./conf/setup-conf.json", "r")
setup_conf = file.read()
file.close()

setup_conf = json.loads(setup_conf)

add_conf_if_needed("install-java", True)
add_conf_if_needed("install-node", True)



def add_path(path, addToSystem=False):

    if addToSystem:
        if curr_os == "Windows":
            process = subprocess.Popen(["powershell", "-Command", "[Environment]::SetEnvironmentVariable(\"Path\", $env:Path + \";{};\", [EnvironmentVariableTarget]::Machine)".format(path)])
            process.wait()
        elif curr_os == "Linux":
            pass
        elif curr_os == "MAC_STRING":
            pass

    env = os.environ.copy()
    env.update({"PATH": "{};{};".format(path, os.environ["PATH"])})

    rerun(sys.argv[1] if len(sys.argv) > 1 else "", env)
    sys.exit(0)

def rerun(arg, env=os.environ):
    subprocess.Popen(["python", "./scripts/src/setup.py", arg], cwd=os.getcwd(), env=env)

def download_and_install(program_name, urls, install_file_name, install_cmd, rerun_args):

    url = urls["Windows"]["64" if is_64 else "32"]

    if curr_os == "Windows":
        import requests

        print("Downloading {} {}-bit installer to {}".format(program_name, 64 if is_64 else 32, install_file_name))
        file_stream = requests.get(url, stream=True)
        file_stream.raise_for_status()
        with open(install_file_name, 'wb') as setup_file:
            for chunk in file_stream.iter_content(1024):
                setup_file.write(chunk)

        print("Installing {}".format(program_name))
        os.system(install_cmd)
        os.remove(install_file_name)

        add_path(EXPECTED_NODE_PATH)
        
        rerun(rerun_args)
        sys.exit(0)

def node_path_exists():
    return os.system("node --version") == 0

def java_path_exists():
    return os.system("java -version") == 0 or os.system("java --version") == 0
    
if __name__ == "__main__":

    if setup_conf["install-java"] and not java_path_exists():

        # Add Node to system path if command doesn't exist but path does
        if not java_path_exists() and os.path.isdir(EXPECTED_JAVA_PATH):
            print("Adding Java to system path")
            add_path(EXPECTED_JAVA_PATH, True)

        if not java_path_exists():
            print("Please download and install Java from the website")
            print("Java is currently not available for automatic download due to licensing (External hosting coming soon)")
            time.sleep(2)
            webbrowser.open("https://java.com/en/download/", new=2)
            #download_and_install("Java", NODE_INSTALLER_URLS, "node_setup.msi", "msiexec.exe /i node_setup.msi /QN", "node_was_installed")

    if setup_conf["install-node"] and not node_path_exists():
        node_was_installed = len(sys.argv) > 1 and sys.argv[1] == "node_was_installed"

        # Add Node to system path if command doesn't exist but path does
        if os.path.isdir(EXPECTED_NODE_PATH):
            print("Adding Node.js to system path")
            add_path(EXPECTED_NODE_PATH, True)

        if not node_path_exists():
            download_and_install("Node.js", NODE_INSTALLER_URLS, "node_setup.msi", "msiexec.exe /i node_setup.msi /QN", "node_was_installed")

    print("Installing pip requirements")
    os.system("python -m pip install --no-cache -r requirements.txt")

    if node_path_exists():
        print("Installing node modules")
        os.chdir("web")
        os.system("npm install package.json")
        os.chdir("..")

    print("Creating test files")
    os.chdir("scripts")
    os.system("create_test_files")

    print("Clearing test directories")
    os.system("clear_test_dirs")