'''
simple_cli.py

Contains functionality which facilitates command line functionality. Written wholly by Rich Padayachy
'''

from argparse import ArgumentParser, Namespace
import sys
from typing import Any, Callable




class Command:
    def __init__(
            self,
            name: str,
            func: Callable[[Namespace], str | int | None],
            desc: str,
            arg_names: list[tuple[list[str], dict[str, Any]]],
        ) -> None:
        self.name = name
        self.func = func
        self.desc = desc
        self._setup_parser(*arg_names)

    def _setup_parser(self, *arg_names: tuple[list[str], dict[str, Any]]):
        arg_parser = ArgumentParser(
            prog = self.name,
            description = self.desc,
        )
        for arg in arg_names:
            arg_parser.add_argument(*arg[0], **arg[1])
        self.arg_parser = arg_parser

    def __call__(self, params: list[str]):
        args = self.arg_parser.parse_args(params)
        self.func(args)



class CommandList:
    def __init__(self) -> None:
        self.commands: list[Command] = []

    def add_command(
            self,
            cmd_name: str,
            cmd_func: Callable[[Namespace], str | int | None],
            cmd_desc: str,
            params: list[tuple[list[str], dict[str, Any]]],
        ):
        command = Command(cmd_name, cmd_func, cmd_desc, params)
        self.commands.append(command)

    def get_command(self, name: str):
        c = list(filter(lambda x: x.name == name, self.commands))
        if len(c) == 0:
            return None
        return c[0]


class SimpleCLI:
    '''
    Provides a simple CLI interface to which
    commands can be added.
    '''
    def __init__(self, add_builtins: bool = True):
        self.command_list = CommandList()
        self.add_command = self.command_list.add_command
        if add_builtins:
            self.add_command('exit', lambda _: sys.exit(0), 'Exit the CLI.', [])

    def run_command(self, command_text: str):
        command_name, *command_args = command_text.split(' ')
        command = self.command_list.get_command(command_name)
        if command is not None:
            output = command(command_args)
            print(output)
        else:
            print(f'No command named: "{command_name}".')
    def _run_cli(self):
        while True:
            line = input('Test: >> ')
            self.run_command(line)

    def start(self):
        try:
            self._run_cli()
        except KeyboardInterrupt:
            print('^C detected, exiting gracefully...')
            sys.exit(0)
