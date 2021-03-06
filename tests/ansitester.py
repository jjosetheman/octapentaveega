#################################################################################
##                                                                             ##
##   Very simple ANSI-tester Python application for Attiny85 VGA               ##
##                                                                             ##
##                                                                             ##
##   (C) Copyright 2015-2016 Jari Tulilahti                                    ##
##                                                                             ## 
##   All right and deserved.                                                   ## 
##                                                                             ##
##   Licensed under the Apache License, Version 2.0 (the "License")#           ##
##   you may not use this file except in compliance with the License.          ##
##   You may obtain a copy of the License at                                   ##
##                                                                             ##
##       http://www.apache.org/licenses/LICENSE-2.0                            ##
##                                                                             ##
##   Unless required by applicable law or agreed to in writing, software       ##
##   distributed under the License is distributed on an "AS IS" BASIS,         ##
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  ##
##   See the License for the specific language governing permissions and       ##
##   limitations under the License.                                            ##
##                                                                             ##
#################################################################################

import serial
import time
import random
import sys

# Give port name of your UART as first argument. No error checking
# here, sorry.
#
ser = serial.Serial(sys.argv[1], 9600,  timeout = 1)

serwrite = lambda x: ser.write(bytearray(map(ord, x)))
move_to = lambda x, y: serwrite("\x1B[{0};{1}H".format(y, x))
set_color = lambda fg, bg = 0: serwrite("\x1B[3{0};4{1}m".format(fg, bg))

def rndclear(c = 32, fg = 7, bg = 0):
	serwrite("\x1B[3{0};4{1}m".format(fg,bg)) # Set colors
	for loc in random.sample(range(0, 512, 2), 256):
		move_to(int(loc  / 32) * 2, (loc / 2) % 16)
		serwrite(chr(c) + chr(c))
	serwrite("\x1B[H") # Move cursor to 0,0

directions = [
	# Worm travelling North
	{ "x" :  0, "y" : -1, "dirs" : 
		[
			{ "char" : 138, "nextdir" : 0 }, # Straight
			{ "char" : 151, "nextdir" : 1 }, # Left
			{ "char" : 137, "nextdir" : 3 }  # Right
		] 
	},
	# Worm travelling West
	{ "x" : -1, "y" :  0, "dirs" : 
		[
			{ "char" : 133, "nextdir" : 1 }, # Straight
			{ "char" : 137, "nextdir" : 2 }, # Left
			{ "char" : 136, "nextdir" : 0 }  # Right
		]
	},
	# Worm travelling South
	{ "x" :  0, "y" :  1, "dirs" : 
		[
			{ "char" : 138, "nextdir" : 2 }, # Straight
			{ "char" : 136, "nextdir" : 3 }, # Left
			{ "char" : 135, "nextdir" : 1 }  # Right
		] 
	},
	# Worm travelling East
	{ "x" :  1, "y" :  0, "dirs" : 
		[
			{ "char" : 133, "nextdir" : 3 }, # Straight
			{ "char" : 135, "nextdir" : 0 }, # Left
			{ "char" : 151, "nextdir" : 2 }  # Right
		]
	},
]

worms = [
	{ "x" : 16, "y" :  0, "dir" : 2, "color" : 1},
	{ "x" : 12, "y" : 10, "dir" : 2, "color" : 3},
	{ "x" : 31, "y" :  7, "dir" : 1, "color" : 5},
	{ "x" : 22, "y" :  4, "dir" : 3, "color" : 6},
	{ "x" :  0, "y" :  7, "dir" : 3, "color" : 7},
]

serwrite("xx\x08") # dismiss if we're left in ANSI mode...
serwrite("\x1BT") # dismiss possible tricoder
serwrite("\x1B[2J") # Clear screen
serwrite("\x1B[m") # Reset colors
serwrite("\x1B[?7l") # Disable wrap
serwrite("\x1B[0]")

delay = 0.4

for zz in range(200):
	text = random.choice([
		'512 bytes RAM\n',
		'This is Attiny85 VGA\n',
		'8 bits rules!\n',
		'Jartza made this\n',
	])
	space = 16 - (len(text) / 2)
	spacing = "                "[0:random.randint(1, int(space * 2))]
	serwrite(spacing)
	serwrite(text)
	if delay > 0:
		time.sleep(delay)
	if zz % 14 == 0:
		delay -= 0.1

rndclear(150, 7, 4)
rndclear()

# Draw color bars
x = 0
d = 1
c = 0
for zz in range(560):
	set_color(int(c), int(c - 0.5))
	move_to(x, 15)
	serwrite("\x96\x96\x96\x96\x96\x96\x96\x96\n")
	x += d
	c += .25
	if int(c) == 8:
		c = 1
	if x in [0, 24]:
		d = -d

rndclear()

# Draw some worms in the screen
for z in range(200):
	for worm in worms:
		move = directions[worm["dir"]]
		worm["x"] = (worm["x"] + move["x"]) % 32
		worm["y"] = (worm["y"] + move["y"]) % 16
		turn = random.choice([1, 2, 0, 0, 0])
		move_to(worm["x"], worm["y"])
		set_color(worm["color"])
		serwrite(chr(move["dirs"][turn]["char"]))
		worm["dir"] = move["dirs"][turn]["nextdir"]

rndclear(160)
rndclear(32)

# Colors go-around
for i in [150, 149, 146, 149, 150, 160]:
	a = chr(i)
	x = random.randint(3, 16)
	y = random.randint(3, 10)
	serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
	move_to(x,y)
	serwrite("OctaPentaVeega")

	for i in range(32):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(i, 0)
		serwrite(a)

	for i in range(0,16):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(31, i)
		serwrite(a)

	for i in range(31,-1,-1):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(i, 15)
		serwrite(a)

	for i in range(15,-1,-1):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(0, i)
		serwrite(a)

	move_to(x,y)
	serwrite("              ")

rndclear(160)

# Random color characters
for zz in range(20):
	for i in range(65,91):
		move_to(random.randint(0, 31), random.randint(0, 15))
		(f, b) = random.sample(range(8), 2)
		set_color(f, b)
		serwrite(chr(i))

rndclear()
# Show color map
scrolltext = "Attiny85 VGA, displaying 32x16 characters on screen " \
	"with 6x10 pixel font. Single Attiny85 for Black & White output, " \
	"Three Attiny85s for 8 color output. " \
	"Industry standard VGA 640x480 @ 60Hz.     "

move_to(0, 2);
serwrite("    (C) 2015-2016 // Jartza\n")
serwrite("\n")
serwrite("    Attiny85 running @ 20MHz\n")

move_to(0, 6)
serwrite("        Supported colors:\n")

move_to(0, 7)
set_color(0, 7)
serwrite("  bg :   0  1  2  3  4  5  6  7 \n")

for x in range(8):
	move_to(2, x + 8)
	set_color(7, 0)
	serwrite("fg {0}".format(x))
	move_to(8, x + 8)
	for i in range(8):
		set_color(x, i)	
		serwrite("xY")
		serwrite("\x1B[m ")	

# Disable wrap and move cursor to 31, 0
serwrite("\x1B[?7l")
move_to(31, 0)
set_color(7, 0)

ser.flush()

# Scroll text
for i in range(len(scrolltext)):
	serwrite("\x1B[[" + scrolltext[i % len(scrolltext)])
	ser.flush()
	time.sleep(0.08)

for i in range(32):
	serwrite("\x1B[[")
	ser.flush()
	time.sleep(0.1)

move_to(0,0)
serwrite("         OctaPentaVeega\n")

ser.flush()
time.sleep(3)

for i in range(32):
	serwrite("\x1BD")
	ser.flush()
	time.sleep(0.05)

serwrite("\x1B[16]") # Graphics mode
serwrite("\x1B[2J") # Clear screen
serwrite("\x1B[m") # Reset colors
serwrite("\x1B[?7l") # disable wrap
serwrite("\x1BG") # Tricoder mode

image=[
#red
[
"......    ...     ..   ..      .. .  ....   ....    ...     ....",
".......    ...    ..         ... ..   ....  ....    ...    .... ",
"   .....    ..    ..    .      . .  . .   . ...    ...    ....  ",
"     ....   ...   ..    .      . ..  ..   .....    ...    ...   ",
"...   ....   ..   ...   .  ..    .............    ...    ...    ",
".....  ....  ...   ..   ......   ..... .......   ....   ...     ",
"......  ...   ..   ..   ......   .   .     ...   ...    ...   . ",
"      .  ...  ..   ..   .....          .   ..    ...   ...  ....",
"       .  ...  ..  ..   ......  ..  .  .   ..   ...   ...  ..   ",
"          ...  ..  ..   .....          .  ...   ...   ..   .    ",
"           ...  .   ..  .......        .  ..   ...   ..         ",
".......     ..  ..  ..  ... .   .     ......   ...   ..  .      ",
"........    ... ..  ......      .     ....... ...   ..  .       ",
".........    ..  ..........    ..     ...........   .. .  ......",
" .. ......   ....................    ............. ..  .  ......",
"             ....................   . ...............   ....    ",
"             ........  ...........    ............... .  .      ",
"             .........................................          ",
"             .........................................          ",
"............  .....      .............        ...............   ",
".............  ...   ..     ........    ....   .................",
"...........    .. .........   .....  .  ....... ..... ....      ",
"               . .................. .  ......... ....           ",
"               ................. ... .  ......... ...   .       ",
"           ..   .................................. .......      ",
".............. .....      ...........       ...... ...... ......",
"..................  .    . .........       . ............ ......",
".......... ....     .    .   .......  .   ..    ......... ..... ",
"          ..... ...         .......         ...... .. ...       ",
"          ... ........    ............................ ...      ",
"           ............................................ ..      ",
"           .....................................................",
"................................................................",
".......... ..............................................       ",
"            ............................................        ",
"            ... ..................................... ..        ",
"            . ................. ........................        ",
"...............................  .................. .... ...  . ",
"............... ............   ..   .............. . .. .....   ",
"             .   ............... .................              ",
"                 ............... .................              ",
"                 .................................              ",
"                 ..................................             ",
"..............    ...........   ...........................   . ",
"............       ..........    ................ ..........    ",
"                   .......... . ................                ",
"                    .......................... .                ",
"                   ............    ........... .                ",
"                    ............  ............ .                ",
"                     ...........  ...........  ............  .  ",
" ..........           .........   ........... ..............  . ",
"  ..  ....             ............................             ",
"                        ......................                  ",
"                       .  ......   ...........                  ",
"                       ....         ..........                  ",
"                       .......................                  ",
".................      ......      . .........  ......... ...   ",
"      .............    .....           .......  ..... . .. ..   ",
"                     . .....  .    ..  .......  .               ",
"                     . .....        .  ..........               ",
"...................... .....        .  ............. ...   .    ",
" ..................  . .....           ...................      ",
"                     .  ....        .  ..........               ",
"                     .  ....        .. ...... ...               "
],
#green
[
"......     ..     .     .      .      ...      .      .      .  ",
" ......    ...    .                   .               .     .   ",
"    ....    ..    .     .                     .      .     .    ",
"      ...   ..    ..    .                   .       ..    ..    ",
"       ...   ..    .    .               . ....    ...    ..     ",
" ..     ..    .    ..   .  ..              . .    ..     ..     ",
"        ...   ..   ..   .. ..              .     ...    ..      ",
"         ...   .   ..   ..  .                    ...   ...      ",
"          ..   .    .    . ..                   ...    .        ",
"           ..  ..   .    . .                    ..    ..        ",
"           ..   .   .    .. .                   ..    .         ",
"  . ..      ..  .   ..                ..  ..   ..    ..         ",
" ......     ..   .  ..  .             .......  ..    .          ",
"  .......    ..  . .......            ...........   .      ..  .",
"       .     .............     ..     ...........   .       .   ",
"             ........                     ........ ..    ..     ",
"              ......     .    ...      .   . .......            ",
"              ......     ..  .......................            ",
"             ........   .................... .........          ",
"..     ....     ...        ...........        .... ... .        ",
"          ..    ..           .......           ...  . ......  . ",
"               .   . ...      ....       ......  .. . .         ",
"               . .........  .   ..      .......  ....           ",
"                 .... ..... ..   ...      ......  ..    .       ",
"           ..   ..... ... .  .. ..     .. .....    .... ..      ",
"    .  .. ....  ....      .. .....          ....   ...    .     ",
" ......... ... ...           .... .           ....  . ... ..... ",
" ........  ....     .    .   ......        .     .  .....       ",
"           .. . ...          ...  .          ....  .. ...       ",
"           .  ........    . ....  ....   ............  ..       ",
"           .  .......      ....... ...    ............          ",
"           . ...........   ... ...      . ............ ......   ",
".......... .............   ... ....  .    ...........   ....... ",
"           .. ........... ....... ..     ..............         ",
"            ... ......... ...... .... . .......... ..  .        ",
"            ... .................................  .. ..        ",
"            . . ..............  ................. . . ..        ",
"    ....... ... .......... ..      ..............   ...         ",
"........... ..  ..........          .............  . .          ",
"                 ..........  ..  .......... .... .              ",
"                 .........  ...  ......... ..... .              ",
"                 ......... ............... ....                 ",
"                  ............ .......... ....                  ",
"    ......        ..........      ....... .... ..               ",
"      ....         .........      ....... ...  ..               ",
"                    ....  .      .....   ...   .                ",
"                    ... .....    ....... ..    .                ",
"                    ..........     ........                     ",
"                     .......         ... .  .                   ",
"                      .......       ....  ...  ....     ..      ",
"   .                   .......     .....  ..  ...      ..       ",
"                       ........   ...... ..  .                  ",
"                        .... ..    .... ..  ..                  ",
"                          ..         .........                  ",
"                                      .. .....                  ",
"                         .  .      .....  ....                  ",
" ..............        . ..           . ..  .                   ",
"                       ....             .. ..   ..              ",
"                        ...         .  .... ..                  ",
"                         ..         .   .   .                   ",
" ................  ..  ....         .   .  .. ...               ",
"                         ..            .. ...  ... ...          ",
"                         ..         .  ..  ..  ..               ",
"                         ..         .. ..   .  .                "
],
#blue
[
"                          .                                     ",
"                          .                                     ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                 .                 .            ",
"                                 .                              ",
"                                 .                              ",
"                                                                ",
"                                                                ",
"                                                 .              ",
"         .                                       .              ",
"                              .    .            ..      ..      ",
"                              .......         .       .         ",
"                              ....             .                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                           ....                 ",
"                                           ..                   ",
"                                      ......                    ",
"                                      .....                     ",
"                                       ...                      ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                             .     .  .                         ",
"                              ..   ....                         ",
"                                   ...                          ",
"                               .  .....                         ",
"                            ..    .....                         ",
"                                  .....                         ",
"                                  .....                         "
]
]

nums = [ "  ", " .", ". ", ".." ]

for row in range(16):
	for char in range(32):
		red = 0
		green = 0
		blue = 0
		for index in range (row * 4, row * 4 + 4):
			red <<= 2
			green <<= 2
			blue <<= 2
			red |= nums.index(image[0][index][(char * 2):(char * 2) + 2][:2])
			green |= nums.index(image[1][index][(char * 2):(char * 2) + 2][:2])
			blue |= nums.index(image[2][index][(char * 2):(char * 2) + 2][:2])
		if red in [8,10,13,27,127]:
			serwrite(chr(27) + chr(red))
		else:
			serwrite(chr(red))
		if green in [8,10,13,27,127]:
			serwrite(chr(27) + chr(green))
		else:
			serwrite(chr(green))
		if blue in [8,10,13,27,127]:
			serwrite(chr(27) + chr(blue))
		else:
			serwrite(chr(blue))
	if row < 15:
		serwrite(chr(13))

ser.flush()
time.sleep(5)

serwrite("\x1BT") # Disable Tricoder
serwrite("\x1B[0;0m") # Reset colors
rndclear(0)
serwrite("\x1B[0]") # Disable graphics mode

ser.flush()
ser.close()
