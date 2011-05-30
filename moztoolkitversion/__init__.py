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

from version import ToolkitVersion, ToolkitVersionComponent

__version__ = "1.0b1"
__all__ = ["ToolkitVersion", "ToolkitVersionComponent"]
