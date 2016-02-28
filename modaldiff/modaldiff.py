#encoding: utf-8

__version__ = "0.1"

import argparse

def cmd_main(args):
    '''
    Modal Diff is a tool to compare text files in a modal way. What this means is
    that you use some pseudo-xml-Markup in your text files to choose - for specific
    parts of the file - specific ways to compare 2 or more versions.
    '''

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reffile', metavar='REF', type=str,
                        help='file defining the reference state')
    parser.add_argument('newfile', metavar='NEW', type=str,
                        help='file defining the new state to be compared against the reference state')

    args = parser.parse_args(args)
    

def main():
    import sys
    cmd_main(sys.argv[1:])
