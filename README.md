## A simple cross-platform file server that syncs files between two directories, or two computers.

Check out the [Contribution Guidelines](https://github.com/c-mcg/File-Server/blob/master/CONTRIBUTING.md) for project structure and code formatting

**Setup:**

* Install [Python 3.6.3+](https://www.python.org/downloads/)

    * Verify install with the command ```python --version```

* Install [Node.js]( https://nodejs.org/en/download/) (8.11.0+)
       
    * Only install Node if you want to build web (if you plan on contributing to the project)
       
    * Verify install with command ```node -v```
       
    * Node is currently required as a web build is not included (This will come with a proper release)

* Run setup.bat (or .sh)

**Running:**

  * Run ```webpack.bat``` or ```webpack.sh```

    * Only required for building web
  * Run ```run_both.bat```or ```run_both.sh```
  * Test by moving files from `test_directories/test_files` to `test_directories/client_dir` or `test_directories/serv_dir`
