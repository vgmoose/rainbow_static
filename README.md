# rainbow_static
Generate rainbow static given based on inputted files

## Usage
Rainbow static takes a file as input, and then generates frames based off
```
python rainbow.py [path to file]
```

## Todo
Currently, only the frames of the video are exported as PNG files. These will need to be stitched together with ffmpeg:
```
ffmpeg -r 30 -f image2 -s 100x100 -i frame%06d.png -vcodec libx264 -crf 0  output.mp4
```

Importing is also not possible at this time, and the color depth field is currently not supported (always exports images with 24-bit palettes)
