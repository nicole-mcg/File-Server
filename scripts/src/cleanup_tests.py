import os, shutil

def removetests():
    test_count = 0
    bin_count = 0
    for dirpath, dirnames, files in os.walk('.'):
        if '__test__' in dirnames:
            test_count = test_count + 1
            try:
                shutil.rmtree(dirpath + "/__test__/bin")
                bin_count = bin_count + 1
            except FileNotFoundError:
                print("This __test__ folder doesn't contain any bin folder")
    print("Found a total of " + str(test_count) + " __test__ folders.")
    print("Found " + str(bin_count) + " bin folders within them.")

if __name__ == "__main__":
    os.chdir("..")
    os.chdir("..")
    os.chdir("./src/file_server")
    removetests()
