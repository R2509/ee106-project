from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Callable




class Command:
    def __init__(
            self,
            name: str,
            func: Callable[[Namespace], None],
            desc: str,
            arg_names: list[str],
        ) -> None:
        self.name = name
        self.func = func
        self.desc = desc
        self._setup_parser(*arg_names)

    def _setup_parser(self, *arg_names: str):
        arg_parser = ArgumentParser(
            prog = self.name,
            description = self.desc,
        )
        for arg in arg_names:
            arg_parser.add_argument(arg)
        self.arg_parser = arg_parser

    def __call__(self, params: str):
        args = self.arg_parser.parse_args(params)
        self.func(args)



class CommandList:
    def __init__(self) -> None:
        self.commands: list[Command] = []

    def add_command(
            self,
            cmd_name: str,
            cmd_func: Callable[..., None],
            cmd_desc: str,
            arg_names: list[str],
        ):
        command = Command(cmd_name, cmd_func, cmd_desc, arg_names)
        self.commands.append(command)

    def get_command(self, name: str):
        c = list(filter(lambda x: x.name == name, self.commands))
        if len(c) == 0:
            return None
        return c[0]



class SimpleCLI:
    def __init__(self):
        self.command_list = CommandList()
        self.add_command = self.command_list.add_command

    def run_command(self, command_text: str):
        command_name, *command_args = command_text.split(' ')
        command = self.command_list.get_command(command_name)
        if command is not None:
            command(''.join(command_args))
        else:
            print(f'No command named: "{command_name}".')


cli = SimpleCLI()
def sus(args: Namespace):
    print(args.text)
cli.add_command('test', sus, 'Soe random test', ['text'])

while True:
    line = input('Test: >> ')
    cli.run_command(line)
