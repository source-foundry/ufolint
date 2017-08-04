# ufolint

[![Build Status](https://travis-ci.org/source-foundry/ufolint.svg?branch=master)](https://travis-ci.org/source-foundry/ufolint) [![Build status](https://ci.appveyor.com/api/projects/status/lsuj8p7myp6mdo2e/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/ufolint/branch/master) [![codecov](https://codecov.io/gh/source-foundry/ufolint/branch/master/graph/badge.svg)](https://codecov.io/gh/source-foundry/ufolint)


ufolint is a source file linter for typeface development in [Unified Font Object](http://unifiedfontobject.org/) (UFO) source code.  It was designed for continuous integration testing of UFO source contributions to typeface projects. 

<p align="center">
  <img src="https://raw.githubusercontent.com/source-foundry/ufolint/images/images/ufolint_example.gif"/>
</p>


The application performs a UFO version specific static analysis of the source text files against the [UFO v2 and v3 specifications](http://unifiedfontobject.org/) for issues that include:

  - supported UFO version
  - mandatory files and directories
  - mandatory file path naming conventions
  - source defined file path and directory path consistency across source files
  - valid XML file format
  - *.plist file property list value checks
  - *.plist file property list value type checks
  - fontinfo.plist OpenType property naming conventions
  - fontinfo.plist OpenType property data validations
  - *.glif file format version testing
  - *.glif file outline, attribute, anchor, guideline, image, note validations
  - images follow UFO v3+ png specification
  - source files import into ufoLib library with ufoLib public methods

These tests are performed through a combination of public methods in the [ufoLib library](https://github.com/unified-font-object/ufoLib) (released by the authors of the UFO specification) and additional tests that are implemented in the ufolint application.  ufolint catches exceptions raised in the ufoLib public read methods for all *.plist file types and all ufoLib validations performed on *.glif files.  These are returned to users with informative error messages that indicate the filepath(s) of concern and exit status code 1.


## Install and Upgrade

Use the command:

```
$ pip install ufolint
```

Upgrade to a new version of the application with the command:

```
$ pip install --upgrade ufolint
```


## Usage

The process is fully automated.  Simply point ufolint to one or more UFO source directories and it takes care of the rest.  ufolint exits with status code 0 if all tests pass and exits with status code 1 if any tests fail.

```
$ ufolint [UFO source path] ([UFO path 2] [UFO path3]...)
```

##### Example

```
$ ufolint Awesome-Regular.ufo Awesome-Bold.ufo
```

For critical failures that prevent the completion of further testing, ufolint exits immediately and other tests are aborted.  In all other circumstances, failures are collected across the entire analysis and displayed at the completion of all tests.  

ufolint provides verbose, useful error messages that include the file(s) of concern, the error type, and in many cases, the problematic line in the file.


## Acknowledgments

Built with the fantastic [ufoLib library](https://github.com/unified-font-object/ufoLib) where the lion's share of validation work has been performed!


## License

[MIT License](https://github.com/source-foundry/ufolint/blob/master/docs/LICENSE)
