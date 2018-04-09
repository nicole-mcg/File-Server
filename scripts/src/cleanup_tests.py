import os, shutil

def removetests():
    bin_count = 0
    for dirpath, dirnames, files in os.walk('.'):
        if '__test__' in dirnames:
            try:
                shutil.rmtree(dirpath + "/__test__/bin")
                bin_count += 1
            except FileNotFoundError:
                pass
    print("Removed " + str(bin_count) + " test bin folders.")

if __name__ == "__main__":
    os.chdir("../src/file_server")
    removetests()
