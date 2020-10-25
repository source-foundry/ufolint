## Changelog

### v1.0.2

- add cPython 3.9 testing
- add CodeQL static source testing
- update fonttools dependency to v4.16.1

### v1.0.1

- refactor to achieve line lengths < 90
- convert to GitHub Actions CI testing service
- upgrade appdirs dependency to v1.4.4
- upgrade fonttools dependency to v4.14.0
- upgrade pytz dependency to v2020.1
- upgrade six dependency to 1.15.0

### v1.0.0

- v1 release
- broadened pinning of Python dependency versions
- updated build dependencies to current release versions
- test against pinned dependency versions in tox CI testing

### v0.4.1

- package wheel for Python 3 only

### v0.4.0

- converted from `ufoLib` to `fontTools.ufoLib` dependency
- add requirement for `fontTools` library v4.0.0 (first Python 3.6+ only release)
- dropped support for Python 2.7
- dropped support for Python 3 versions < 3.6
- setup.py overhaul with new Python 3.6+ Python interpreter requirement
- add fontTools [ufo] extras dependencies to requirements.txt
- switched Py2 `basestring` type to `str` type in `ufolint.validators.typevalidators` module
- removed Py2 `plistlib.readPlist` in `ufolint.controllers.runner` module
- removed Py2 `xml.etree.CElementTree` in `ufolint.validators.plistvalidators`
- removed Py2 `xml.etree.CElementTree` in `ufolint.validators.xmlvalidators`
- PEP8 Python source formatting changes
- add Makefile
- remove unnecessary shell scripts (functionality replaced by Makefile)
- update MANIFEST.in file paths
- changed Python interpreter version in tox.ini configuration file

### v0.3.5

- improved error messages on \*.glif file test failures
- added CONTRIBUTORS.md documentation
- modified copyright in license and in-application help to "Source Foundry Authors"

### v0.3.4

- force install of ufoLib dependency at version >= 2.2.0. This is release where optional validation support introduced and code in this project was modified to support the changes in ufoLib

### v0.3.3

- updated ufoLib dependency to v2.3.2

### v0.3.2

- updated ufoLib dependency to v2.3.1

### v0.3.1

- added license to Python wheels
- source formatting changes
- plistvalidators module: eliminated unnecessary assignment
- runner module: eliminated unnecessary import
- xmlvalidators module: eliminated unnecessary import

### v0.3.0

- updated ufoLib dependency to v2.2.1
- modified ufoLib.UFOReader instantiation in order to continue to support validation on UFO file reads after the ufoLib dependency changes
- modified ufoLib.glifLib.GlyphSet instantiation in order to continue to support validation on UFO file reads after the ufoLib dependency changes
- added Python 3.7 interpreter testing in CI testing settings files
- eliminated Python 3.4 interpreter testing in CI testing settings files

### v0.2.2

- updated ufoLib dependency to v2.1.1 (PR #6)
- updated release.sh shell script
- modified Appveyor CI testing settings

### v0.2.1

- added explicit ufolint labeling to test header and test success/fail strings to improve clarity of test that is being executed during multi-application CI testing

### v0.2.0

- initial release version
