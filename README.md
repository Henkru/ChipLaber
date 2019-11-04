# ChipLaber

This litle script make custom pinout labels for ICs. Resolution: 1 pixel = 0.1 mm

## Usage

```
python chipLaber.py [-h] [-s SIZE] [-o OUTPUT] chip

positional arguments:
  chip                  Chip file

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Font size
  -o OUTPUT, --output OUTPUT
                        Output file
  -hide, --hide         Hide chip name
```

## Examples

### Basic
```
chipLaber.py libs/z80.json
```

### Set font size
```
chipLaber.py -s 15 libs/z80.json
```

### Set outputfile
```
python chipLaber.py -o out/exm.png libs/z80.json
```

## Chipfile
You can easy add your own chips. More exmaples in libs folder.

### Example
```
{
	"name" : "ATtiny45",
	"type" : "DIP8",
	"pins" : [
			"PB5",
			"PB3",
			"PB4",
			"GND",
			"PB0",
			"PB1",
			"PB2",
			"VCC"
	]
}
```

### Result
![Result](https://raw.githubusercontent.com/Henkru/ChipLaber/master/example.png)

## Requirements
 * Python 3 (maybe works on 2.7)
 * [Pillow](http://pillow.readthedocs.org/en/latest/installation.html) 
 * json
 * argparse
