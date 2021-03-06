## termagic: use cursor gestures to execute commands

![Showcase GIF](showcase.gif)

### Installation

```
git clone git@github.com:void4/termagic.git
cd termagic
pip install -r requirements.txt
```

Optionally, for img2txt visualization: `sudo apt install caca-utils`

### Usage

`python magic.py`

```
usage: magic.py [-h] [--loop] [--exec] [--draw] [--save SAVE] [--daemon]

Execute commands by tracing shapes with your cursor

optional arguments:
  -h, --help   show this help message and exit
  --loop       loop indefinitely, draw an x to exit
  --exec       execute commands immediately
  --draw       draw the recognized shape as ascii image
  --save SAVE  save a custom shape and command
  --daemon     run this app in the background
```

To save a new pattern, supply its name to the `--save` parameter: `python magic.py --save mypatternname`

If you want to import some of the functionality in your own programs, have a look at `external.py`
