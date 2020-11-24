py-rcon
=======

This is Python implementation of RCON.

Installation
------------

.. code-block:: bash

  git clone https://github.com/ttk1/py-rcon.git
  cd py-rcon
  pip install .

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

Protocol Specification
----------------------

* https://wiki.vg/RCON
* https://developer.valvesoftware.com/wiki/Source_RCON_Protocol
