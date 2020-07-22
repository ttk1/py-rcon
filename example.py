#!/bin/env python

from rcon import Console

console = Console(host='localhost', password='py-rcon')
console.command('say hello')
console.close()

'''
[04:14:25] [RCON Listener #1/INFO]: Thread RCON Client /127.0.0.1 started
[04:14:25] [Server thread/INFO]: [Rcon] hello
[04:14:25] [RCON Client /127.0.0.1 #4/INFO]: Thread RCON Client /127.0.0.1 shutting down
'''
