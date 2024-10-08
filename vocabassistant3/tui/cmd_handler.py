
from typing import Callable, Dict, Tuple


class CmdHandler:
    def __init__(self, prompt:str, cmds: Dict[str, Tuple[str, Callable]]) -> None:
        self.quit=False
        self.prompt=prompt
        self.cmds=cmds
        self.cmds["help"]=("Show available commands", self.show_help)
        self.cmds["q"]=("Quit", self.do_quit)

    def main_loop(self):
        while not self.quit:
            cmd=input(self.prompt)
            if cmd in self.cmds:
                try:
                    self.cmds[cmd][1]()
                except ExitException as e:
                    self.quit=True
                    return
                except Exception as e:
                    print("Error: "+str(e))
            else:
                print("Command unknown. Type help to see all commands.")
    def show_help(self):
        for cmd, (descp, func) in self.cmds.items():
            print(f"{cmd}: {descp}")
    def do_quit(self):
        self.quit=True

class ExitException(Exception):
    pass
