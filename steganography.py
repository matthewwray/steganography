from PIL import Image
import argparse

# We have an image, and a message we want to encode into the image.
# To do this, we iterate through each pixel of the image, and then iterate through the R, G, B and A values of each pixel.
# For each RGB value (RGB_val), we set it to: RGB_val = RGB_val - (RGB_val MOD 3)
# Then for each RGB_val we add a corresponding binary bit from the message.
# Finally, once we reach the end of the message, we add 2 to the RGB_val, indicating the message is complete.
# To read the message from the image we simply iterate through each RGB_val and MOD 3 it.
# A value of 0 means a binary bit of 0. A value of 1 means a binary bit of 1. A value of 2 means end of message.

def bits_to_bytes(binary_data):
    # Calculate the number of bits in the binary data
    num_bits = len(binary_data)

    # Ensure that the number of bits is a multiple of 8
    if num_bits % 8 != 0:
        raise ValueError("The number of bits must be a multiple of 8 to convert to bytes.")

    # Convert binary to bytes
    byte_data = int(binary_data, 2).to_bytes(num_bits // 8, byteorder='big')

    return byte_data

def encode_message(im, message):
    pix_val = im.load()
    width, height = im.size

    # Firstly, we check if the message can fit in the message. If not, raise an exception
    if len(message) > width * height * 3:
        raise ValueError("Message is too large for image. Maximum message size (in bits): Image width * image height * 3")


    newImage = Image.new( 'RGBA', (width,height), "black") # We create the new image. Into this we will embed our message
    newPixels = newImage.load()

    # We now iterate over all the rows and columns (in other rows, over all pixels), and then we can iterate through each RGB value.
    # We also keep a tracker for which binary bit we're on, called btracker
    btracker = 0

    for x in range(width): 
        for y in range(height):

            current_rgb = [] # This list will contain our pixel with the message encoded into it.

            for rgb_val in (pix_val[x,y]):
                if btracker >= len(message): # If we've reached the end of the message....
                    current_rgb.append((rgb_val - (rgb_val % 3)) + 2) # ...then add 2...
                else:
                    current_rgb.append((rgb_val - (rgb_val % 3)) + int(message[btracker])) #... else add the message bit and increment our binary tracker.
                    btracker += 1
                
            newPixels[x,y] = tuple(current_rgb) # Convert to tuple and write to image!
    return newImage
    #newImage.save('newimage.png')

def decode_message(im):
    decoded_message = ""

    pix_val = im.load()
    width, height = im.size
    
    # To decode the message from the image, we again must iterate through all rows and columns (pixels), then iterate through that pixel's RGB values,
    # and then get their MOD 3 value, until we get a value that equals 2.
    for x in range(width): 
        for y in range(height):
            for rgb_val in pix_val[x,y][0:3]: # We do the [0:3] indexing part so as to avoid the Alpha channel, which we do not encode our message in. We only want RGB
                current_bit = rgb_val % 3
                if current_bit == 2:
                    return bits_to_bytes(decoded_message)
                else:
                    decoded_message += str(current_bit)
    return bits_to_bytes(decoded_message) # This return statement should only ever be called if the message and the image are exactly the same length, ie there are no 2s in the image

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', help = "Used for encoding. The image to encode the message into.")
parser.add_argument('-m', '--message', help = "Used for encoding. The message to encode into the image.")
parser.add_argument('-d', '--decode', help = "Decode a message from an encoded image.")
parser.add_argument('-o', '--output', help = "Store the output into a file. Without this flag, no ouput will occur at all.")
args = parser.parse_args()

if (args.decode) and (args.image or args.message):
    raise ValueError("Conflicting arguments - cannot both decode and encode")

if (bool(args.image) != bool(args.message)):
    raise ValueError("Invalid arguments - if encoding, you must supply both an image and a message")

if args.decode:
    d_im = Image.open(args.decode, 'r') 
    decode_result = decode_message(d_im)

if (args.image and args.message):
    im = Image.open('picture.jpg', 'r')

    with open(args.message, 'rb') as f:
        message = f.read() # We read the message as bytes. We now need to convert them directly to individual binary bits
        message = ''.join(format(byte, '08b') for byte in message) # This is that aforementioned conversion

    encode_result = encode_message(im, message)

if args.output:
    if (args.image and args.message):
        encode_result.save(args.output)
    elif args.decode:
        with open(args.output, 'wb') as f:
            f.write(decode_result)