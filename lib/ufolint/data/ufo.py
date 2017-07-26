#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path


class Ufo(object):
    def __init__(self, ufopath, glyphsdir_list):
        self.ufopath = ufopath
        self.glyphsdir_list = glyphsdir_list
        self.plist_list = None
        self.directory_list = None
        self.mandatory_root_basefilepaths = None
        self.mandatory_glyphsdir_basefilepaths = None

    def _make_root_plist_path(self, basefilename):
        if basefilename == "metainfo.plist":
            return os.path.join(self.ufopath, basefilename)
        elif basefilename == "fontinfo.plist":
            return os.path.join(self.ufopath, basefilename)
        elif basefilename == "groups.plist":
            return os.path.join(self.ufopath, basefilename)
        elif basefilename == "kerning.plist":
            return os.path.join(self.ufopath, basefilename)
        elif basefilename == "lib.plist":
            return os.path.join(self.ufopath, basefilename)
        elif basefilename == "layercontents.plist":
            return os.path.join(self.ufopath, basefilename)

    def _make_glyphsdir_plist_path(self, glyphsdirname, basefilename):
        if basefilename == "contents.plist":
            return os.path.join(self.ufopath, glyphsdirname, basefilename)
        elif basefilename == "layerinfo.plist":
            return os.path.join(self.ufopath, glyphsdirname, basefilename)

    def get_root_plist_filepath(self, basefilename):
        return self._make_root_plist_path(basefilename)

    def get_glyphsdir_plist_filepath_list(self, basefilename, glyphsdir_list):
        path_list = []
        for glyphsdir in glyphsdir_list:
            glyphsdir_basename = glyphsdir[1]
            path_list.append(self._make_glyphsdir_plist_path(glyphsdir_basename, basefilename))
        return path_list

    def get_mandatory_filepaths_list(self):
        """
        Creates a list of relative filepaths to mandatory files in UFOv2
        :return: list of filepath strings
        """
        mandatory_filepath_list = []
        for mandatory_root_basefile in self.mandatory_root_basefilepaths:
            mandatory_filepath_list.append(self.get_root_plist_filepath(mandatory_root_basefile))
        for mandatory_glyphs_basefile in self.mandatory_glyphsdir_basefilepaths:
            mandatory_filepath_list.append(self.get_root_plist_filepath(mandatory_glyphs_basefile))
        return mandatory_filepath_list


class Ufo2(Ufo):
    def __init__(self, ufopath, glyphsdir_list):
        super(Ufo, self).__init__()
        self.ufopath = ufopath
        self.glyphsdir_list = glyphsdir_list
        self.mandatory_root_basefilepaths = ['metainfo.plist']
        self.mandatory_glyphsdir_basefilepaths = ['contents.plist']


class Ufo3(Ufo):
    def __init__(self, ufopath, glyphsdir_list):
        super(Ufo, self).__init__()
        self.ufopath = ufopath
        self.glyphsdir_list = glyphsdir_list
        self.mandatory_root_basefilepaths = [
            'metainfo.plist',
            'layercontents.plist'
        ]
        self.mandatory_glyphsdir_basefilepaths = ['contents.plist']

