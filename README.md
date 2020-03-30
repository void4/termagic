## termagic: use cursor gestures to execute commands

![Showcase GIF](showcase.gif)

### Installation

```
git clone git@github.com:void4/termagic.git
pip install -r requirements.txt
```

Optionally, for img2txt visualization: `sudo apt install caca-utils`

### Usage

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
