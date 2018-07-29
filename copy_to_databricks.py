import sys
from urllib.request import urlopen
import datetime
import time
from subprocess import call
import argparse

#START HERE
parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
parser.add_argument('--file', help='file name to copy, if not specified, all files under source will be copied')
parser.add_argument('--source', help='source local directory to copy from')
parser.add_argument('--destination', help='destination dbfs directory to copy into')
parser.add_argument('--help', help='help')


call(["databricks", "fs ls --help"], shell = True)

