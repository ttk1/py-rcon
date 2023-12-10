# py-rcon

This is a Python implementation of RCON mainly for Minecraft.

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

Server console output:

```txt
[04:14:25] [RCON Listener #1/INFO]: Thread RCON Client /127.0.0.1 started
[04:14:25] [Server thread/INFO]: [Rcon] hello
[04:14:25] [RCON Client /127.0.0.1 #4/INFO]: Thread RCON Client /127.0.0.1 shutting down
```

## Asynchronous IO Support (Experimental Feature)

This can be used when asynchronous IO is needed, such as Discord bot.

Below is an example using [discord.py](https://github.com/Rapptz/discord.py):

```py
import discord
from rcon.async_support import Console

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
console = Console(host='localhost', password='rcon')


@tree.command()
async def mc_list(interaction: discord.Interaction):
    if not console.is_open():
        await console.open()
    await interaction.response.defer()
    res = await console.command('list')
    await interaction.followup.send(res.body)

client.run('TOKEN')
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
