import modaldiff
from pytest import mark

testdata = [ ("testdta/all_variants_01/reference.txt", "testdta/all_variants_01/input.txt", None) ]

@mark.parametrize("a,b,expected", testdata)
def test_complete_tool(a, b, expected):
    modaldiff.cmd_main([a, b])
