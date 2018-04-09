# Contents

  * ### Project Structure
    * Whole Project
    * Front End
    * Back End
  * ### Coding Conventions
    * Whole Project
    * Front End
    * Back End

# Project Structure

### Whole Project
  * Developer scripts: `scripts/src/`
    * These scripts make it quicker and easier to do repetative things while working on the project
    * These scripts are designed to be run together in another command (without pausing) to create useful commands (E.g `setup.bat`)
  * Test directories: `test/`
    * These are created with the `create_test_dirs` script
    * There should be three folders `client_dir`, `serv_dir` and `test_files`
      * `client_dir` and `serv_dir` are the folders to be watched when running with `run_server`, `run_client` or `run_both`
      * The `test_files` folder is populated by the `create_test_files` script. The files created by this script are free to be modified at any times if you require more/fewer/small/bigger files

### Front End (ReactJS and Less) 
  * Pages: `web/src/page/`
  * Widgets: `web/src/widgets/`
    * Each widget folder contains two files `index.jsx` and `index.less`
    * `index.jsx` is the JavaScript structure for the widget, `index.less` is the styling
  * Less functions and variables (Use these!): `web/src/less/`
    * Functions ensure styling shows properly on all compatible browsers
    * Most functions are setup to be run without parameters. E.g `.user-select();` would make text non-selectable and `.border-radius();` will give a standard border-radius for the site

### Back End (Python)
  * ...
  
# Coding Conventions

### Whole project
  * Indent 4 spaces
  * Space out blocks of code and group lines with similar functionality
  * Attempt to write a short comment on each block of code
  * A good example of this can be found at `src/file_server/file/__test__/test_snapshot.py`
  
### Front End (ReactJS)
  * ...

### Back End (Python)
  * Variables, functions, and methods should be named with underscores between words. E.g `example_var`
  * Classes should be named with upper camel case. E.g `ExampleClass`

