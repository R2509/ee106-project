'''
simple_cli.py

Contains functionality which facilitates command line functionality. Written wholly by Rich Padayachy
'''

from argparse import ArgumentParser, Namespace
import sys
from typing import Any, Callable

from finalised.util import logger




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
        result = self.func(args)

        if result is None:
            return ''
        return str(result)



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
        filtered_cmd_list = list(filter(lambda x: x.name == name, self.commands))
        if len(filtered_cmd_list) == 0:
            return None
        assert len(filtered_cmd_list) == 1,\
            'More than one command was found with the same name.'
        return filtered_cmd_list[0]

    def list_commands(self):
        return [command.name for command in self.commands]


class SimpleCLI:
    '''
    Provides a simple CLI interface to which
    commands can be added.
    '''
    def __init__(self, include_default_commands: bool = True):
        self.command_list = CommandList()
        self.add_command = self.command_list.add_command

        if include_default_commands:
            self._add_default_commands()

    def _add_default_commands(self):
        def cmd_exit(ns: Namespace):
            sys.exit(ns.code)

        self.add_command('exit', cmd_exit, 'Exit the CLI.', [
            (['code'], {
                'action': 'store',
                'type': int,
                'default': 0,
            }),
        ])

    def run_command(self, command_text: str):
        command_name, *command_args = command_text.split(' ')

        if command_name == '':
            return

        command = self.command_list.get_command(command_name)

        if command is not None:
            output = command(command_args)
            logger.log(output)
        else:
            logger.log(f'No command named: "{command_name}".')
    def _run_cli(self):
        while True:
            line = input('Project: >> ')
            self.run_command(line)

    def start(self):
        try:
            self._run_cli()
        except KeyboardInterrupt:
            print('^C detected. Exiting gracefully...')
            sys.exit(0)
