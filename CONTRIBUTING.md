# Contents
  * ### Project Structure
    * **Whole Project**
    * **Front End**
    * **Back End**
  * ### Coding Conventions
    * **Whole Project**
    * **Front End**
    * **Back End**

# Project Structure
  * ### Whole Project
    * **Developer scripts**: `scripts/src/`
      * These scripts make it quicker and easier to do repetative things while working on the project
      * These scripts are designed to be run together in another command (without pausing) to create useful commands (E.g `setup.bat`)
    * **Test directories**: `test_directories/`
      * These are created with the `create_test_dirs` script
      * There should be three folders `client_dir`, `serv_dir` and `test_files`
        * `client_dir` and `serv_dir` are the folders to be watched when running with `run_server`, `run_client` or `run_both`
        * The `test_files` folder is populated by the `create_test_files` script. The files created by this script are free to be modified at any times if you require more/fewer/small/bigger files
  * ### Front End (ReactJS and Less) `web/src/`
    * **Pages**: `web/src/page/`
      * **Tests**: `web/src/page/test/*.test.jsx` Where `*` is the name of file being tested
    * **Widgets**: `web/src/widgets/`
      * **Tests**: `web/src/widgets/*/index.test.jsx`
      * Each widget folder contains two files `index.jsx` and `index.less` which contain the structure and styling respectively, for the widget
      * Widgets should contain definitions for `defaultProps` and `propTypes`, marking required props in `propTypes`
    * **Less functions and variables (Use these!)**: `web/src/less/`
      * **Variables**
        * **Text**
          * **Text colours** (white and black): `@font-color-dark`, `@font-color-light`
          * **Font Sizes**: `@font-size-small`, `@font-size-medium`, `@font-size-large`, `@font-size-huge`
        * **Spacing** - Try to use these for `padding` and `margin`
          * `@space-small`, `@space-medium`, `@space-large`, `@space-huge`
        * **Colours** 
          * **Primary colours** (blue): `@color-primary`, `@color-primary-dark`, `@color-primary-light`
          * **Neutral colours** (white and beige): `@color-neutral0`, `@color-neutral1`
      * **Functions**
        * Functions ensure styling shows properly on all compatible browsers
        * Most functions are setup to be run without parameters. E.g `.user-select();` would make text non-selectable and `.border-radius();` will give a standard border-radius for the site
        
  * ### Back End (Python) `src/`
    * **Program Entry**: `file_server/__init__.py`
    * **FileServer**: `file_server/server.py` This is the class for a file server. It also handles web server functions
    * **FileClient**: `file_server/client.py` This is the class for a file client.
    * **FileHub**: `file_server/hub/file_hub.py` The parent class for FileServer and FileClient, handles file watch operations
      * **Packets**: `file_server/hub/packets` These are packet handlers for data sent between the client and server    
    * **Web Server**: `file_server/web/`
      * **Endpoints**: `file_server/web/endpoints/` These are endpoint handler for the web server. They provide an easy protocol for data requests to the web server
    * **Account Functions**: `file_server/account/`
      * **Account**: `file_server/account/account.py` Class used to hold data for an account, can be used by client or server
      * **AccountManager**: `file_server/account/account_manager.py` Used to create, load and validate accounts. Only used by the server!
    * **File Operations**: `file_server/file/`
      * **FileSocket**: `file_server/file/file_socket.py` This class provides a high level interface for common protocols in the FileServer. This class should be used over the raw sockets whenever possible
      * **FileSnapshot, DirectorySnapshot**: `file_server/file/file_snapshot.py` These classes are used to cache a directory's metadata. It also provides conversion of the file tree to JSON
      * **FileEventHandler**: `file_server/file/event_handler.py` This class is used to handle events given by the file watch
    * **Utility Functions**: `file_server/util/` All classes and functions can be imported from package (except test utils). E.g `from file_server.util import ByteBuffer`
      * **File Utilities**: `file_server/util/file_util.py` Provides common functions for manipulating files
      * **Network Utilites**: `file_server/util/network_util.py` Contains common network functions. Functions should be imported from package
      * **Test Utilities**: `file_server/util/test_util.py` Provides functions commonly used in tests. Cannot be imported from module to avoid parsing this file unless it's a test
    * **Tests**: Should be `./__tests__/test_*.py` where `.` is the directory of the Python file being tested and `*` is the name of the file
# Coding Conventions
  * ### Whole project
    * Indent 4 spaces
    * Space out blocks of code and group lines with similar functionality
    * Attempt to write a short comment on each block of code
  * ### Front End (ReactJS)
    * Variables, functions, and methods should be named with camel case. E.g `exampleVar`
    * Classes should be named with upper camel case. E.g `ExampleClass`
  * ### Back End (Python)
    * **Variables**: should be named with underscores between words. E.g `example_var`
    * **Classes**
      * should be named with upper camel case. E.g `ExampleClass`
      * Comments should be in the following format:
        ```
          # Short description of what class handles or represents
          # Any additional information for the class (such a usage and/or warnings)
          class ExampleClass():
              def __init__(self):
                  pass
        ```
    * **Functions, and Methods**
      * should be named with underscores between words. E.g `example_function`
      * Comments should be in the following format:
        ```
          # Short description of what the method does
          # Any additional information (Such as warnings for improper usage)
          # first_parameter: a description of the first paremeter. Any warnings or additional information
          # Returns "A short description of what is returned and how it can be used"
          def example_method(self, first_parameter):
              return False
        ```
