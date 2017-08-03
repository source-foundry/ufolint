#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Version Number
# ------------------------------------------------------------------------------
major_version = "0"
minor_version = "2"
patch_version = "0"

# ------------------------------------------------------------------------------
# Help String
# ------------------------------------------------------------------------------

HELP = """====================================================
ufolint
Copyright 2017 Christopher Simpkins
MIT License
Source: https://github.com/source-foundry/ufolint
====================================================

ufolint is a UFO source file linter.

Usage:

  $ ufolint [UFO path 1] ([UFO path2] [UFO path ...])
  
The application returns exit status code 0 if all tests are successful and exit status code 1 if any failures are detected.

"""

# ------------------------------------------------------------------------------
# Version String
# ------------------------------------------------------------------------------

VERSION = "ufolint v" + major_version + "." + minor_version + "." + patch_version


# ------------------------------------------------------------------------------
# Usage String
# ------------------------------------------------------------------------------
USAGE = "ufolint [UFO path 1] ([UFO path2] [UFO path ...])"
