# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


try:
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels = 21

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
            pixel_order=ORDER)
except:
    pass


class LedSTRIP(object):

    def right(self, wait):
        for i in range(num_pixels-2):
            #pixels.fill((255,50,0))
            pixels[i] = [255,255,255]
            pixels[i+1] = [255,255,255]
            pixels[i+2] = [255,255,255]
            pixels.show()
            time.sleep(wait)
        pixels.fill((0,0,0)
        pixels.show()

    def left(self, wait):
        for i in range(num_pixels-2):
            j = num_pixels-1-i
            #pixels.fill((255,50,0))
            pixels[j] = [255,255,255]
            pixels[j-1] = [255,255,255]
            pixels[j-2] = [255,255,255]
            pixels.show()
            time.sleep(wait)
        pixels.fill((0,0,0)
        pixels.show()

