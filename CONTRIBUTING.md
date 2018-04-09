

# Coding Conventions

## Whole project
  * Indent 4 spaces
  * Space out blocks of code and group lines with similar functionality
  * Attempt to write a short comment on each block of code
  * A good example of this can be found at `src/file_server/file/__test__/test_snapshot.py`

## Back End (Python)
  * Variables, functions, and methods should be named with underscores between words. E.g `example_var`
  * Classes should be named with upper camel case. E.g `ExampleClass`

# Project Structure

## Front End (ReactJS and Less)
  * Less functions and variables (Use these!): `web/src/less/`
    * Functions ensure styling shows properly on all compatible browsers
    * Most functions are setup to be run without parameters. E.g `.user-select();` would make text non-selectable and `.border-radius();` will give a standard border-radius for the site 
  * Pages: `web/src/page/`
  * Widgets: `web/src/widgets/`
    * Each widget folder contains two files `index.jsx` and `index.less`
    * `index.jsx` is the JavaScript structure for the widget, `index.less` is the styling

## Back End (Python)
  * ...
