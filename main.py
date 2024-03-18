import pandas as pd

from simple_cli import SimpleCLI
from commands import commands
from util import COLUMN_WIDTH

def main():
    '''Main function.'''
    cli = SimpleCLI()
    cli.add_commands(*commands)
    cli.start()

if __name__ == '__main__':
    main()
