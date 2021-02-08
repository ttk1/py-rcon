py-rcon
=======

This is Python implementation of RCON.

Installation
------------

.. code-block:: bash

  pip install git+https://github.com/ttk1/py-rcon.git

Example
-------

.. code-block:: python

  from rcon import Console

  console = Console(host='localhost', password='py-rcon')
  console.command('say hello')
  console.close()

console output:

.. code-block:: text

  [04:14:25] [RCON Listener #1/INFO]: Thread RCON Client /127.0.0.1 started
  [04:14:25] [Server thread/INFO]: [Rcon] hello
  [04:14:25] [RCON Client /127.0.0.1 #4/INFO]: Thread RCON Client /127.0.0.1 shutting down

RCON Shell
----------

.. code-block:: bash

  $ python -m rcon
  Enter host: localhost
  Enter password:
  hi!
  [localhost:25575] > list
  There are 0 of a max of 20 players online:

Protocol Specification
----------------------

* https://wiki.vg/RCON
* https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
