# steganography
A basic command-line image steganopgrahy utility written in Python.
This program can be used to hide information (text, audio, images, etc) in an image, and can extract information that has been hidden within images.

## How it works
We have an image, and a message we want to encode into the image.
To do this, we iterate through each pixel of the image, and then iterate through the R, G and B values of each pixel.

For each RGB value (RGB_val), we set it to: RGB_val = RGB_val - (RGB_val MOD 3)

Then for each RGB_val we add a corresponding binary bit from the message.

Finally, once we reach the end of the message, we add 2 to the RGB_val, indicating the message is complete.

To read the message from the image we simply iterate through each RGB_val and MOD 3 it.
A value of 0 means a binary bit of 0. A value of 1 means a binary bit of 1. A value of 2 means end of message.
