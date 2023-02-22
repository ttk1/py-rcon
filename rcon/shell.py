try:
    import readline
except ModuleNotFoundError:
    pass

import traceback

from rcon.console import Console
from rcon.util import remove_formatting_codes


class Shell():
    def __init__(self, host, password, port):
        self._host = host
        self._password = password
        self._port = port
        self._console = Console(host, password, port)

    def start(self):
        print('hi!')
        while True:
            try:
                command = input(f'[{self._host}:{self._port}] > ')
                res_body = self._console.command(command).body
                print(remove_formatting_codes(res_body))
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                self._console.close()
                break
            except:
                self._console.close()
                traceback.format_exc()
                break
        print('bye!')
