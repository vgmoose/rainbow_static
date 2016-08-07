#!/usr/bin/python
import json, sys, os, struct

# template code here borrowed from splite
# https://github.com/vgmoose/Splite/blob/master/splite.py
print ".--=============--=============--."
print "|         Rainbow Static         |"
print ".--=============--=============--."

yeswords = ["yes", "y", "ya", "ok", "okay"]

# try to install the pyton image library
# if it isn't already installed
try:
    from PIL import Image
except:
    ans = raw_input("The Python Image Library is required to continue. Install it now? ")
    if ans.lower() in yeswords:
        try:
            os.system("sudo easy_install pip")
            os.system("sudo pip install Pillow")
        except:
            print("Install failed. Make sure you have a working gcc compiler")
            print("I was trying to run: \"sudo easy_install pip\" and then \"pip install Pillow\"")
            exit()
	
# the .prev file contains the last run to make 
# repeated use easier
prev = []
try:
	f = open(".prev", "r")
	for line in f:
		prev.append(line)
	f.close()
except:
	pass

cur = open(".prev", "w")
cur_line = 0

def to_rgb(argb):
	return "".join(map(chr, argb)).encode('hex')

# this method will get input and display
# the previous input as a recommended default
# or the second parameter if no .prev file value exists
def sp_input(msg, default=""):
	global cur_line
    
	default = str(default)
	
	out = "| " + msg
	old = ""
	try:
		old += prev[cur_line].rstrip("\n")
	except:
		old = default
		
	if old != "":
		out += " [" + old + "]"
	
	out += ": "
	resp = raw_input(out)
	
	if resp == "":
		resp = old
		
	cur_line += 1
	cur.write(resp+"\n")
	
	return resp

try:
	sheet = sys.argv[1]
	print("| Using " + sheet)
except:
	sheet = raw_input("| Path to generator file: ")
	
width  = int(sp_input(" Width of video (px)", 1920))
height = int(sp_input("Height of video (px)", 1080))

depth = int(sp_input("Color depth (x in 2^x total colors)", 24))

#im = Image.open(sheet)
#pix = im.convert('RGBA')

print ".--------------------------------"
print "| I'm going to take " + sheet
print "| and turn it into a %dx%d video" % (width, height)
print "| with %d different colors (%d-bit)" % (2**depth, depth)
print ".--------------------------------"
ans = raw_input("| Is this correct? ")

if not ans.lower() in yeswords:
	print("| I'm sorry to hear that :(")
	print ".--------------------------------"
	exit()
	
atlas_name = sp_input("Enter output filename", "rainbow.mov")
print ".--------------------------------"

# pixels per frame
ppf = width*height

# try to open the target file
print("| Opening " + sheet);

# total bytes to process (size of file)
total_bytes = os.path.getsize(sheet)

fp = None
try:
	fp = open(sheet, "rb")
except:
	print("Couldn't open " + sheet)
	exit()
	
cur_byte = 0
cur_frame = 0

# make a target directory
try:
	os.mkdir(atlas_name)
except:
	pass

print ("| Converting to rainbow static...")

while cur_byte < total_bytes:
	# create an image for this frame
	frame = Image.new("RGB", (width, height))
	putpixel = frame.im.putpixel
	
	for y in range(height):
		for x in range(width):
			# cur val for 24-bit color is the next three bytes
			streak = [ord(z) for z in fp.read(3)]
			
			# overflow when at least three pixels aren't available
			streak += [0x00]*(3-len(streak))
			
			# set the pixel in this frame
			putpixel((x, y), tuple(streak))
			
			# we processed 3 bytes
			cur_byte += 3
			
	cur_frame += 1
	
	# write the image to a file
	frame.save(atlas_name+os.sep+"frame%06d.png" % cur_frame)
	
fp.close()

print ".--=============--=============--."
print "|           All Done!!           |"
print ".--=============--=============--."