import os, sys, platform, subprocess, json, webbrowser, time

NODE_NAME = "Node.js"
JAVA_NAME = "Java"

INSTALL_INFO = {
    JAVA_NAME: {
        "commands_to_check": [
            ["java", "-version"], 
            ["java", "--version"],
        ],
        "expected_path": "",
        "urls": {
            "Windows": {
                "32": "http://download2098.mediafire.com/f8114fw87tjg/yg8gamtuvqbj583/jre-8u171-windows-i586.exe",
                "64": "http://download876.mediafire.com/5dcubdcdefxg/auxybmuydx9bnbt/jre-8u171-windows-x64.exe"
            }
        }
    },
    NODE_NAME: {
        "commands_to_check": [
            ["node", "--version"]
        ],
        "expected_path": "",
        "urls": {
            "Windows": {
                "32": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x86.msi",
                "64": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x64.msi"
            }
        }
    }
}

INSTALLER_URLS = {
    JAVA_NAME: {
        "Windows": {
            "32": "http://download2098.mediafire.com/f8114fw87tjg/yg8gamtuvqbj583/jre-8u171-windows-i586.exe",
            "64": "http://download876.mediafire.com/5dcubdcdefxg/auxybmuydx9bnbt/jre-8u171-windows-x64.exe"
        }
    },
    NODE_NAME: {
        "Windows": {
            "32": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x86.msi",
            "64": "https://nodejs.org/dist/v8.11.1/node-v8.11.1-x64.msi"
        }
    }
}

EXPECTED_PATHS = {
    JAVA_NAME: "",
    NODE_NAME: ""
}

is_64 = sys.maxsize > 2**32
curr_os = platform.system()

if curr_os == "Windows":
    INSTALL_INFO[JAVA_NAME]["expected_path"] = "{}\\Common Files\\Oracle\\Java\\javapath".format(os.environ["ProgramFiles(X86)"])
    INSTALL_INFO[NODE_NAME]["expected_path"] = "{}\\nodejs".format(os.environ["ProgramFiles"])

attempted_installs = []
for key in INSTALL_INFO.keys():
    if key in sys.argv:
        print("Adding {} to attempted_installs".format(key))
        attempted_installs.append(key)

def add_conf_if_needed(conf, default=False):
    if not conf in setup_conf:
        setup_conf[conf] = False

file = open("./conf/setup-conf.json", "r")
setup_conf = file.read()
file.close()

setup_conf = json.loads(setup_conf)

add_conf_if_needed("install-java", True)
add_conf_if_needed("install-node", True)

def add_path(program_name, addToSystem=False):
    path = INSTALL_INFO[program_name]["expected_path"]

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

    rerun(program_name, env)
    sys.exit(0)

def rerun(arg, env=os.environ):
    print("Rerunning with args: {}".format(["python", "./scripts/src/setup.py", arg, *attempted_installs]))
    subprocess.Popen(["python", "./scripts/src/setup.py", arg, *attempted_installs], cwd=os.getcwd(), env=env)

def download_and_install(program_name, install_file_name, install_cmd):

    if program_name in attempted_installs:
        return

    url = INSTALL_INFO[program_name]["urls"]["Windows"]["64" if is_64 else "32"]

    if curr_os == "Windows":
        import requests

        if not os.path.exists("temp"):
            os.makedirs("temp")

        print("Downloading {} {}-bit installer to temp/{}".format(program_name, 64 if is_64 else 32, install_file_name))
        file_stream = requests.get(url, stream=True)
        file_stream.raise_for_status()
        with open("./temp/{}".format(install_file_name), 'wb') as setup_file:
            for chunk in file_stream.iter_content(1024):
                setup_file.write(chunk)

        print("Installing {}".format(program_name))
        return_code = os.system(install_cmd)
        if return_code == 0:
            print("{} installed successfully".format(program_name))
        else:
            print("Error installing {}. Return code: {}".format(program_name, return_code))

        os.system("powershell -Command \"Remove-Item temp -Force -Recurse\"")

        add_path(program_name)

def check_program_path_exists(program_name):
    for cmd in INSTALL_INFO[program_name]["commands_to_check"]:
        try:
            if subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
                return True
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            pass
    return False

def verify_program_install(program_name, install_file_name, install_cmd):

    if not check_program_path_exists(program_name):

        # Add program to system path if command doesn't exist but path does
        if os.path.isdir(INSTALL_INFO[program_name]["expected_path"]):
            print("Adding Java to system path")
            add_path(program_name, True)

        if not check_program_path_exists(program_name):
            #print("Please download and install Java from the website")
            #print("Java is currently not available for automatic download due to licensing (External hosting coming soon)")
            #time.sleep(2)
            #webbrowser.open("https://java.com/en/download/", new=2)
            download_and_install(program_name, install_file_name, install_cmd)
    
if __name__ == "__main__":

    try:
        import requests
    except ModuleNotFoundError:
        os.system("python -m pip install --no-cache requests")

    if setup_conf["install-java"]:
        verify_program_install(JAVA_NAME, "java_setup.exe", "\".\\temp\\java_setup.exe\" /s")

    if setup_conf["install-node"]:
        verify_program_install(NODE_NAME, "node_setup.msi", "msiexec.exe /i \"temp\\node_setup.msi\" /QN")

    print("Installing pip requirements")
    os.system("python -m pip install --no-cache -r requirements.txt")

    if check_program_path_exists(NODE_NAME):
        print("Installing node modules")
        os.chdir("web")
        os.system("npm install package.json")
        os.chdir("..")

    print("Creating test files")
    os.chdir("scripts")
    os.system("create_test_files")

    print("Clearing test directories")
    os.system("clear_test_dirs")