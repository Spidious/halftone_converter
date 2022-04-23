from PIL import Image, ImageDraw
import PIL
import os

########################### IMAGE SETTINGS ###########################

#set the input image (if not in same folder set file path)
INPUT_FILE = "example.jpg"
CLEAR_TXT = True        #delete the text files generated at completion

SIZE = 40               #Number of pixels per max size circle diameter
CYAN_ANGLE = 22.5       #Angle of the Cyan grid
MAGENTA_ANGLE = 52.5    #Angle of the Magenta grid
YELLOW_ANGLE = 7.5      #Angle of the Yellow grid
KEY_ANGLE = 82.5        #Angle of the Key grid (basically black)

########################### writeTXT ######################################


def writeTXT(image, file, angle, subset, width, height):            #code the text files
    big = PIL.Image.new(mode="CMYK", size=(width*2, height*2))      #new bigger image
    Image.Image.paste(big, image, (int(width/2), int(height/2)))    #paste into bigger image
    big = big.rotate(-angle, expand = 0)                            #rotate to cyan position

    bigWidth, bigHeight = big.size                                  #Get Image Size
    img = big.resize((int(bigWidth/SIZE), int(bigHeight/SIZE)))     #Resize Image to 1/size the original image

    valRange = 255/((SIZE/2)+1)                        #Take the value range (divide 255 by the circle radius +2, idk why plus 2 it just works)
    IMAGE = Image.Image.split(img)                     #split the image 

    pix = IMAGE[subset].load()                         #allow each pixel to be addressable
    smallWidth, smallHeight = IMAGE[subset].size
    
    for y in range(smallHeight):                    #iterate through Y (height)
        for x in range(smallWidth):                 #iterate through x (width)
            case = 0                                #case to represent size of circle radius in unit of number of pixels
            for i in range(int(SIZE/2)+2):          #loop through min to max circle size
                if(int(pix[x,y]) < (valRange*i)):   #if pixel color value is less than range times I
                    case = i-1                      #set case to one less than i
                    break                           #stop, or everything sets to the same value
            if(case < 10):                          #if it is one character, add a zero in front (makes decoding easier)
                file.write("0")                     #add the zero in front
            file.write(str(case))       #write the case value (case represents the radius in pixels (ie: case = 3 means 3 pixel radius))
            file.write(" ")             #add space
        file.write('\n')                #add new line at end of width
    return IMAGE[subset]                            #End function

########################## makeDot #########################################

def makeDot(file, angle, width, height):            #put dots on image
    dots = PIL.Image.new(mode="RGB", size=(width*2, height*2), color = (255,255,255))   #create the image for dots

    ycor = 0            # grid cell y cor
    dotsDraw = ImageDraw.Draw(dots)     #creates drawable image
    for y in range(int((height*2)/SIZE)):
        xcor = 0        # grid cell for x cor (needs to reset after every width loop)
        for x in range(int((width*2)/SIZE)):
            rad = int(file.read(2))     #read the radius character from the text file
            toss = file.read(1)         #unused variable to remove the spacees
            #Size        Top left x-cord           Top right y-cord           Bottom left x-cord        Bottom left y-cord
            size = [(((int(SIZE/2)-rad)+xcor), ((int(SIZE/2)-rad)+ycor)), (((int(SIZE/2)+rad)+xcor), ((int(SIZE/2)+rad)+ycor))]
            xcor+=SIZE                  #iterate xcor by SIZE
            if(rad == 0):
                continue                #skip drawing an ellipse if radius is 0
            dotsDraw.ellipse(size, fill = 'black', outline = None)  #Draw a black ellipse with no outline
        toss = file.read(1)     #read the '\n'
        ycor+=SIZE              #iterate ycor by SIZE
    #return image to normal height width as dots
    dots = dots.rotate(angle, expand = 0)
    dots = dots.crop((width/2, height/2, (width/2)+width, (height/2)+height))

    return dots

####################### MAIN ########################################

#   Create image object and get width and height
im = Image.open(INPUT_FILE)
cmyk_image = im.convert('CMYK')
width,height = im.size

#create text file directory
path = 'color codes'
if(not os.path.exists(path)):
    os.mkdir(path)

#   Write to text files for each color (image is not currently split)
file = open('/color codes/cyan code.txt', 'w+')
c = writeTXT(im, file, CYAN_ANGLE, 0, width, height)   #write the CYAN text file
file.close()

file = open('/color codes/magenta code.txt', 'w+')
m = writeTXT(im, file, MAGENTA_ANGLE, 1, width, height)    #write the MAGENTA text file
file.close()

file = open('/color codes/yellow code.txt', 'w+')
y = writeTXT(im, file, YELLOW_ANGLE, 2, width, height)    #write the YELLOW text file
file.close()

file = open('/color codes/key code.txt', 'w+')
k = writeTXT(im, file, KEY_ANGLE, 3, width, height)    #write the KEY text file
file.close()

######## Convert to dots (dot images are rgb not cmyk)########
file = open('/color codes/cyan code.txt', 'r')
c_dot = makeDot(file, CYAN_ANGLE, width, height)
file.close()

file = open('/color codes/magenta code.txt', 'r')
m_dot = makeDot(file, MAGENTA_ANGLE, width, height)
file.close()

file = open('/color codes/yellow code.txt', 'r')
y_dot = makeDot(file, YELLOW_ANGLE, width, height)
file.close()

file = open('/color codes/key code.txt', 'r')
k_dot = makeDot(file, KEY_ANGLE, width, height)
file.close()

#   convert each image to CMYK
c_dot = c_dot.convert('CMYK')
m_dot = m_dot.convert('CMYK')
y_dot = y_dot.convert('CMYK')
k_dot = k_dot.convert('CMYK')

#   Split the images
CYAN = Image.Image.split(c_dot)
MAGENTA = Image.Image.split(m_dot)
YELLOW = Image.Image.split(y_dot)
BLACK = Image.Image.split(k_dot)

#   Merge each color into one image
IMAGE = Image.merge('CMYK', (CYAN[0], MAGENTA[1], YELLOW[2], BLACK[3]))
IMAGE.save("halftone.jpg")

#   Check to remove text files or to keep them
if(CLEAR_TXT):
    os.remove("/color codes/cyan code.txt")
    os.remove("/color codes/magenta code.txt")
    os.remove("/color codes/yellow code.txt")
    os.remove("/color codes/key code.txt")

#   Completion confirmation
print("Done!")