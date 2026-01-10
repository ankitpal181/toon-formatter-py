
import pytest
from toon_parse.utils import is_code

def test_is_code_shell_commands():
    assert is_code("npm install foo")
    assert is_code("pip install bar")
    assert is_code("git commit -m 'msg'")
    assert is_code("$ echo hello")
    assert is_code("# This is a comment")

def test_is_code_programming_snippets():
    assert is_code("def foo():\n    return 1")
    assert is_code("const x = {\n  a: 1\n};")
    assert is_code("import os\nprint(os.getcwd())")
    assert is_code("class MyClass:\n    pass")

def test_is_code_false_positives():
    assert not is_code("Just a normal sentence.")
    assert not is_code("hello world")
    assert not is_code("1. Item one\n2. Item two") # Simple list
    assert not is_code('{\n "key": "value"\n}') # JSON
    assert not is_code('<root>\n  <child>val</child>\n</root>') # XML
    assert not is_code("")
    assert not is_code(None)

def test_is_code_short_strings():
    # Logic requires len >= 5
    assert not is_code("foo")
    assert not is_code("a=1") 

def test_is_code_shebang():
    assert is_code("#!/bin/bash\necho hi")
