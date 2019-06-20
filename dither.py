from PIL import Image
from math import sqrt

def getClosestColor(c, colors):
    """ Returns closest color in 'colors' to target 'c'. All colors are represented
        as RGB tuples.\n
        Method runs in O(N) time, where 'N' is the size of 'colors'. \n

        PARAMETERS:\n
        \tc : Target color to be approximated, formatted as an RGB tuple\n
        \tcolors : a list containing all valid color options, each formatted as an RGB tuple\n

        RETURNS:\n
        \tnearest: the closest avaliable RGB tuple to 'c' contained within 'colors'
    """
    nearest = (0, 0, 0)# always overridden in first iteration of for loop
    minDiff = 1000     # initialised to be greater than all possible differences
    for col in colors:
        diff = sqrt((col[0]-c[0])**2 + (col[1]-c[1])**2 + (col[2]-c[2])**2)
        if(diff < minDiff):
            minDiff = diff
            nearest = col
    return nearest

def clamp(x): return max(0, min(255, x))

def applyErr(tup, err, factor):
    r = clamp(int(tup[0] + err[0]*factor))
    g = clamp(int(tup[1] + err[1]*factor))
    b = clamp(int(tup[2] + err[2]*factor))
    return r, g, b

def ditherImage(target, colors = None, colorstops = None, saveOutput = True, outputType = "", showFinal = True):
    #attempt to open target image
    try:
        im = Image.open(target)
        mode, size = im.mode, im.size
        width, height = size[0], size[1]
        pix = list(im.getdata())
        im.close()
    except:
        print("Oh noes! An I/O error! :O")
        return

    COLORS = [(0,0,0), (255,192,203), (250,250,250)]

    #lambda expression to flatten x,y location
    index = lambda x, y: x + y * width
    #Floyd-Steinberg dithering. https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
    for y in range(int(height)):
        for x in range(int(width)):
            old = pix[index(x, y)]
            new = getClosestColor(old, COLORS)
            pix[index(x,y)] = new
            #calculates difference in r/g/b channels
            err = (old[0]-new[0], old[1]-new[1], old[2]-new[2])

            if (x != width-1):
                pix[index(x+1,y)] = applyErr(pix[index(x+1,y)], err, 7/16)
            if (y != height-1):
                pix[index(x,y+1)] = applyErr(pix[index(x,y+1)], err, 5/16)
                if (x > 0):
                    pix[index(x-1,y+1)] = applyErr(pix[index(x-1,y+1)], err, 3/16)
                if (x != width-1):
                    pix[index(x+1,y+1)] = applyErr(pix[index(x+1,y+1)], err, 1/16)

    newIm = Image.new(mode, size)
    newIm.putdata(pix)

    #save new image
    if saveOutput:
        tokens = target.split('.', maxsplit=1)
        type = tokens[1] if outputType == "" or outputType is None else outputType
        outname = "%s (dithered).%s" % (tokens[0], type)
        try:
            newIm.save(outname)
        except:
            print("error: file '%s' could not be saved" % outname)
            return
        print("output saved '%s'\n" % outname)
    #display image
    if showFinal : newIm.show()

ditherImage("sadpug.jpeg", outputType="png")
ditherImage("sadpug.jpeg")
