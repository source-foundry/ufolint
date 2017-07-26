#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

try:
    import xml.etree.cElementTree as ETree           # python 2
    from xml.etree.cElementTree import ParseError
except ImportError:
    import xml.etree.ElementTree as ETree            # python 3
    from xml.etree.ElementTree import ParseError

from ufolint.data.tstobj import Result


class AbstractPlistValidator(object):
    def __init__(self, ufopath, ufoversion):
        self.ufopath = ufopath
        self.ufoversion = ufoversion
        self.result_list = []

    def run_validations(self):
        raise NotImplementedError

    def _add_resultobj_to_result_list(self, resultobj):
        self.result_list.append(resultobj)

    def _get_resultobj(self, filepath):
            return Result(filepath)


class MetainfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(MetainfoPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "metainfo.plist"

    def run_validations(self):
        pass


class FontinfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(FontinfoPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "fontinfo.plist"

    def run_validations(self):
        pass


class GroupsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(GroupsPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "groups.plist"

    def run_validations(self):
        pass


class KerningPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(KerningPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "kerning.plist"

    def run_validations(self):
        pass


class LibPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(LibPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "lib.plist"

    def run_validations(self):
        pass


class ContentsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(ContentsPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "glyphs" + os.path.sep + "contents.plist"  # test multiple glyphs directories in v3+

    def run_validations(self):
        pass


class LayerContentsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(LayerContentsPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "layercontents.plist"

    def run_validations(self):
        pass


class LayerinfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion):
        super(LayerinfoPlistValidator, self).__init__(ufopath, ufoversion)
        self.filepath = self.ufopath + os.path.sep + "glyphs" + os.path.sep + "layerinfo.plist"

    def run_validations(self):
        pass