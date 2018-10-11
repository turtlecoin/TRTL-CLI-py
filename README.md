# TRTL CLI py

Command line interface to check TurtleCoin network status and community activity.

### Version
1.4.0

## Usage

### Installation
Clone this repository

```sh
$ git clone https://github.com/turtlecoin/trtl-cli-py.git
```

Install the dependencies

**You need Python 3.6+**

```sh
$ pip install -r requirements.txt
```

### Initializing

```sh
$ py trtl.py
```

TRTL-CLI-py will greet you with a welcome message on startup.

Use `help` or `h` to see a list of possible commands.

```

  Usage:  [options]

  TRTL CLI py

  Options:

        version|v  output the version number
        help|h     output this help message

  Commands:

        market|m       List market data
        supply|s       Lists circulating supply
        network|n      Shows network data
        price|p [qty]  Gives current price information
        ascii|a [pic]  Displays ASCII art
        ascii list|al  Displays a list of ASCII art
        checkpoints|c  Gets latest checkpoint update
        nodes|no        Displays a table of available remote nodes

        license|l      Show license information
        exit|e         Quit the program
``` 

### Contribute

Please do a pull request with any data about trtl that can be useful.

### Thanks

Thanks to @zack796 and @mrrovot off of whose work this is based on.
