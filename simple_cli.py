'''
Allows the creation and usage of a basic Command-Line Interface.
'''

import sys

from argparse import ArgumentParser, Namespace
import traceback
from typing import Any, Callable

from util import TEXT_GREY, TEXT_RESET, logger


class _Command:
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



class _CommandList:
    def __init__(self) -> None:
        self.commands: list[_Command] = []

    def add_command(
            self,
            cmd_name: str,
            cmd_func: Callable[[Namespace], str | int | None],
            cmd_desc: str,
            params: list[tuple[list[str], dict[str, Any]]],
        ):
        '''
        Add a command to the CLI.
        '''
        command = _Command(cmd_name, cmd_func, cmd_desc, params)
        self.commands.append(command)
    def add_commands(
            self,
            *cmds: tuple[
                str,
                Callable[[Namespace], str | int | None],
                str,
                list[tuple[list[str], dict[str, Any]]],
            ],
        ):
        '''
        Add multiple commands to the CLI. Commands are passed as in
        `SimpleCLI.add_command()`, with each command being a tuple.
        '''
        for cmd in cmds:
            self.add_command(*cmd)

    def get_command(self, name: str):
        c = list(filter(lambda x: x.name == name, self.commands))
        if len(c) == 0:
            return None
        return c[0]

    def list_commands(self):
        return [command.name for command in self.commands]

class SimpleCLI:
    '''
    Provides a simple CLI interface to which
    commands can be added.
    '''
    def __init__(self, include_default_commands: bool = True):
        self.command_list = _CommandList()
        self.add_command = self.command_list.add_command
        self.add_commands = self.command_list.add_commands

        if include_default_commands:
            self._add_default_commands()

    def _add_default_commands(self):
        def cmd_exit(ns: Namespace):
            sys.exit(ns.code)
        def cmd_clear(ns: Namespace):
            logger.clear_terminal()

        def cmd_help(ns: Namespace):
            cmdlist_str = ' '.join(self.command_list.list_commands())
            return f'Available commands:\n\t{TEXT_GREY}{cmdlist_str}{TEXT_RESET}'

        self.add_command('exit', cmd_exit, 'Exit the CLI.', [
            (['-c', '--code'], {
                'action': 'store',
                'default': '0',
                'type': int,
            }),
        ])
        
        self.add_command('clear', cmd_clear, 'Clear the terminal.', [])
        self.add_command('help', cmd_help, 'List available commands.', [])

    def _split_command_text(self, command_text: str):
        '''
        Ensures that all double-quoted string arguments in the input text are
        kept intact.
        '''
        initial_split = command_text.split()

        out = []
        acc = ''
        for item in initial_split:
            append = False

            if not '"' in item:
                append = True
            if len(acc) > 0 and '"' in item:
                append = True
            if item[0] == '"' and len(item) > 1 and item[-1] == '"':
                append = True

            if len(acc) > 0:
                acc += f' {item}'
            else:
                acc = item
            if append:
                out.append(acc.strip('"'))
                acc = ''

        return out

    def run_command(self, command_text: str):
        command_name, *command_args = self._split_command_text(command_text)

        if command_name == '':
            return

        command = self.command_list.get_command(command_name)

        if command is not None:
            output = command(command_args)
            logger.log(f'{output}\n')
        else:
            logger.log(f'No command named: "{command_name}".\n\r')
    def _run_cli(self):
        while True:
            # Get a line of input.
            line = input('Python: > ')
            # Split by any semicolons (in case the
            # user wants to run multiple commands).
            commands = line.split(';')
            # Run each command in turn.
            for command in commands:
                # Dont't try to run empty command strings!
                if len(command) > 0:
                    self.run_command(command)

    def start(self):
        try:
            self._run_cli()
        except KeyboardInterrupt:
            print('^C detected, exiting gracefully...')
            sys.exit(0)
