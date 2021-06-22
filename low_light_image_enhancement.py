from __future__ import division
import cv2
import numpy as np
import time

start_time = time.clock()

def find_dark_channel(img):
    dark_channel = np.unravel_index(np.argmin(img), img.shape)[2]
    #print('\n {} | {} | {} | {}'.format(dark_channel,np.unravel_index(np.argmin(img), img.shape), np.argmin(img),img.shape ))
    return dark_channel


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def dehaze(img, light_intensity, windowSize, t0, w):
    size = (img.shape[0], img.shape[1])

    outimg = np.zeros(img.shape, img.dtype)
 
    for y in xrange(size[0]):
        for x in xrange(size[1]):
            x_low = max(x-(windowSize//2), 0)
            y_low = max(y-(windowSize//2), 0)
            x_high = min(x+(windowSize//2), size[1])
            y_high = min(y+(windowSize//2), size[0])

            sliceimg = img[y_low:y_high, x_low:x_high]

            '''Finding Dark Channel'''
            dark_channel = find_dark_channel(sliceimg)

            '''Transmission map value for the current set of pixel values'''
            t = 1.0 - (w * img.item(y, x, dark_channel) / light_intensity)

            '''Blue Channel Value Setting'''
            outimg.itemset((y,x,0), clamp(0, ((img.item(y,x,0) - light_intensity) / max(t, t0) + light_intensity), 255))
            '''Green Channel Value Setting'''
            outimg.itemset((y,x,1), clamp(0, ((img.item(y,x,1) - light_intensity) / max(t, t0) + light_intensity), 255))
            '''Red Channel Value Setting'''
            outimg.itemset((y,x,2), clamp(0, ((img.item(y,x,2) - light_intensity) / max(t, t0) + light_intensity), 255))
    
    return outimg


def main():
    img = cv2.imread('/path/to/image/file.jpg')
    '''Image Inverting'''
    img = ~img
    light_intensity = 255
    '''Defogging Parameter - Between 0 and 1 - 0 means low fog removal thus low surrounding light and 1 means highest possible light condition'''
    w = 0.95
    '''Lower the value better the enhancement, it is meant to avoid dividing by zero'''
    t0 = 0.2
    outimg = dehaze(img, light_intensity, 20, t0, w)
    '''Output Image Inveting Back to get the real image'''
    outimg = ~outimg
    name = '/path/to/save/file.jpg'
    cv2.imwrite(name, outimg)
    print('\nExecution Time = {} seconds'.format(time.clock()-start_time))

if __name__ == "__main__":
    main()
