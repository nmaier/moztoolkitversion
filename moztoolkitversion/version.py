# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is toolkitversion.py.
#
# The Initial Developer of the Original Code is
# Nils Maier.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#  Nils Maier <maierman@web.de>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

"""
Mozilla toolkit version parser and comparator

Parsing and comparisons according to:
https://developer.mozilla.org/en/Toolkit_version_format

EBNF Toolkit (kinda):
    version = component, { additional component }, [ ".", "*"];
    additional component = "." , { component };
    component = [ number ] ,  [ "+" | [ string ] , [ number ] , [ string ] ];
    number = [ "-" ], digit , { digit } ;
    digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
    string = ? not number ?

Serialization rules:
    - Any empty component will be "0"
    - Any omitted number will be 0
    - Any omitted string will be ""
    - Number components will be serialized using the normalized numerical
      literal
    - Any trailing "additional component" with a component of "0" will be
      omitted

Comparison rules:
    - Numbers are compared as numbers
    - Strings are compared as strings
    - Non-existing string parts are always greater than existing string parts
      in components, i.e. (None == "" > "a")!
"""

from __future__ import with_statement

import re

__all__ = ["ToolkitVersion", "ToolkitVersionComponent"]

RE_NUMBER = re.compile("-?\d+")
RE_STRING = re.compile("[^\d-]+")

class ToolkitVersionComponent(object):
    def __init__(self, part=None):
        self.numberA = 0
        self.stringB = ""
        self.numberC = 0
        self.stringD = ""
        if part:
            part = str(part)
            nA = RE_NUMBER.match(part)
            if nA:
                part = part[len(nA.group(0)):]
                self.numberA = int(nA.group(0))

            sB = RE_STRING.match(part)
            if sB:
                part = part[len(sB.group(0)):]
                sb = str(sB.group(0))
                if sb.startswith("+"):
                    self.numberA += 1
                    sb = "pre"
                self.stringB = sb

            nC = RE_NUMBER.match(part)
            if nC:
                part = part[len(nC.group(0)):]
                self.numberC = int(nC.group(0))

            self.stringD = part

    def __repr__(self):
        rv = "%d%s" % (self.numberA, self.stringB)
        if self.numberC:
            rv += "%d%s" % (self.numberC, self.stringD)
        return rv
    def to_tuple(self):
        return [self.numberA, self.stringB, self.numberC, self.stringD]

    def __eq__(self, other):
        if not isinstance(other, ToolkitVersionComponent):
            raise ValueError("Must compare components with each other")
        return str(self) == str(other)

    def __ne__(self, other):
        if not isinstance(other, ToolkitVersionComponent):
            raise ValueError("Must compare components with each other")
        return str(self) != str(other)

    def __cmp__(self, other):
        if not isinstance(other, ToolkitVersionComponent):
            raise ValueError("Must compare components with each other")

        if self == other:
            return False

        if self.numberA < other.numberA:
            return -1
        if self.numberA > other.numberA:
            return 1

        if not self.stringB and other.stringB:
            return 1
        if self.stringB and not other.stringB:
            return -1
        if self.stringB < other.stringB:
            return -1
        if self.stringB > other.stringB:
            return 1

        if self.numberC < other.numberC:
            return -1
        if self.numberC > other.numberC:
            return 1

        if not self.stringD and other.stringD:
            return 1
        if self.stringD and not other.stringD:
            return -1
        if self.stringD < other.stringD:
            return -1
        if self.stringD > other.stringD:
            return 1

        return 0

class ToolkitVersion(object):
    def _get_components(self):
        return self._components
    components = property(_get_components)

    _NULL_COMPONENT = ToolkitVersionComponent()

    def __init__(self, version=None):
        self._components = []
        self._parse(str(version or "0"))

    def __repr__(self):
        return ".".join(str(c) for c in self.components)
    def to_tuple(self):
        return [c.to_tuple() for c in self.components]

    def __eq__(self, other):
        if not isinstance(other, ToolkitVersion):
            other = ToolkitVersion(other)
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        if not isinstance(other, ToolkitVersion):
            other = ToolkitVersion(other)

        if self == other:
            return 0

        l = max(len(self.components), len(other.components))
        for i in range(l):
            try:
                a = self.components[i]
            except IndexError:
                a = ToolkitVersionComponent()
            try:
                b = other.components[i]
            except IndexError:
                b = ToolkitVersionComponent()

            rv = cmp(a, b)
            if rv == 0:
                continue
            return rv
        return 0

    def _parse(self, version):
        while version:
            dot = version.find(".")
            if dot >= 0:
                part = version[:dot]
                version = version[dot + 1:]
            else:
                part = version
                version = None
            self._components += ToolkitVersionComponent(part),

        # remove trailing "empty" components
        while len(self._components) > 1:
            c = self._components[-1]
            if c != self._NULL_COMPONENT:
                break
            self._components.pop()
        # Handle trailing * (meaning
        if str(self._components[-1]) == "0*":
            self._components[-1] = ToolkitVersionComponent(1<<31)
