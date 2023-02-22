# py-rcon

This is Python implementation of RCON.

## Requirements

* Python 3

## Installation

```sh
pip install git+https://github.com/ttk1/py-rcon.git
```

## Example

```py
from rcon import Console

console = Console(host='localhost', password='py-rcon')
console.command('say hello')
console.close()
```

console output:

```txt
[04:14:25] [RCON Listener #1/INFO]: Thread RCON Client /127.0.0.1 started
[04:14:25] [Server thread/INFO]: [Rcon] hello
[04:14:25] [RCON Client /127.0.0.1 #4/INFO]: Thread RCON Client /127.0.0.1 shutting down
```

## Shell Mode

```sh
$ rcon-shell
Enter host: localhost
Enter password:
hi!
[localhost:25575] > list
There are 0 of a max of 20 players online:
```

## GUI Mode

Start GUI:

```sh
$ rcon-gui
```

![image](https://user-images.githubusercontent.com/17878271/220715316-d6797f91-b4c2-4907-b28f-8289f3653e02.png)
![image](https://user-images.githubusercontent.com/17878271/220715435-bcfc12af-d5ae-4b6f-8401-f47a6df53278.png)

## Protocol Specification

* https://wiki.vg/RCON
* https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
