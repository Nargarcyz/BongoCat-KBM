# from KBMListeners import startListening, mousePosition, keyPressed
import pygame, sys
import pyautogui
import math
import numpy as np
import pynput

mousePosition = (0,0)
keyPressed = None

def on_press(key):
    global keyPressed
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        keyPressed = key
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format(key))
    global keyPressed
    keyPressed = None
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False

def on_move(x, y):
    # print('Pointer moved to {0}'.format((x, y)))
    global mousePosition
    mousePosition = (x,y)

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))


def startListening():
    # ...or, in a non-blocking fashion:
    
    KBlistener = pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    KBlistener.start()

    # Mlistener = pynput.mouse.Listener(
    #     on_move=on_move,
    #     # on_click=on_click)
    #     )
    # Mlistener.start()





class RectMap():
    def __init__(self,p1,p2,width,height):
        self.origin = (0,0)
        self.p1 = p1
        self.p2 = p2
        self.width = width
        self.height = height
    def display(self):
        # pygame.draw.line(screen, (0,255,0) , (self.originX, self.originY), (self.x1, self.y1), 4)
        # print(str(self.p1) + " to " + str(self.p1[0] + self.width))
        pygame.draw.line(screen, (0,255,0), self.p1 , (self.p1[0] + self.width, self.p1[1] ),4)
        pygame.draw.line(screen, (0,255,0), self.p2 , (self.p2[0] + self.width, self.p2[1] ),4)
        pygame.draw.line(screen, (0,255,0), self.p2 , self.p1,4)
        pygame.draw.line(screen, (0,255,0), (self.p2[0] + self.width, self.p2[1] ) , (self.p1[0] + self.width, self.p1[1] ),4)

class RectMapV2():

    def calculatePoints(self):
        inclinationMat = np.array( [[math.cos(self.inclination * math.pi/180) , -math.sin(self.inclination * math.pi/180) ],
                                    [0 , 0 ]])
        rotationMat = np.array( [[math.cos(self.rotation * math.pi/180) , -math.sin(self.rotation * math.pi/180) ],
                                 [math.sin(self.rotation * math.pi/180) , math.cos(self.rotation * math.pi/180) ]])
        
        (x1,y1) = np.dot(inclinationMat,(0,-self.height)).astype(int) + np.array((0,self.height))
        (x2,y2) = np.dot(rotationMat,(0,0)).astype(int)# + self.origin
        self.xOffset = x1-x2
        (x3,y3) = np.array((x1,y1)) + np.array((self.width,0))
        (x4,y4) = np.array((x2,y2)) + np.array((self.width,0))


        (x1,y1) = np.dot(rotationMat,np.array((x1,y1))).astype(int)# + self.origin
        (x3,y3) = np.dot(rotationMat,(x3,y3)).astype(int)
        (x4,y4) = np.dot(rotationMat,(x4,y4)).astype(int)

        self.p1 = (x1,y1) + self.origin
        self.p2 = (x2,y2) + self.origin
        self.p3 = (x3,y3) + self.origin
        self.p4 = (x4,y4) + self.origin

    def __init__(self,origin, rotation, inclination, width, height):
        self.origin = origin
        self.rotation = rotation
        self.inclination = inclination
        self.width = width
        self.height = height
        self.calculatePoints()


    def display(self):
        # pygame.draw.line(screen, (0,255,0), self.p1, self.p3, 4)
        # pygame.draw.line(screen, (0,255,0), self.p2, self.p4, 4)
        # pygame.draw.line(screen, (0,255,0), self.p1, self.p2, 4)
        # pygame.draw.line(screen, (0,255,0), self.p3, self.p4, 4)

        # pygame.draw.circle(screen,(255,0,0), self.p1, 8)
        # pygame.draw.circle(screen,(0,255,0), self.p2, 8)
        # pygame.draw.circle(screen,(0,0,255), self.p3, 8)
        # pygame.draw.circle(screen,(0,255,255), self.p4, 8)
        pygame.draw.polygon(screen, (0,0,0), [self.p1,self.p3,self.p4,self.p2])
        # pygame.draw.circle(screen,(0,0,0), self.origin, 8)

    def setRotation(self,angle):
        self.rotation = angle
        self.calculatePoints()
    def getRotation(self):
        return self.rotation

    def setInclination(self,angle):
        self.inclination = angle
        self.calculatePoints()
    def getInclination(self):
        return self.inclination


def mapMouse(rectangle, mousePosition):
    # xdf = (rectangle.p1[0]-rectangle.p2[0])
    # print("1:" + str(xdf))
    # xdf = math.dist(rectangle.p1,rectangle.p2)
    # print("2:" + str(xdf))
    # print(mousePosition[1]/screenSize[1])
    mpX = (mousePosition[0] *  rectangle.width / screenSize[0]) + (mousePosition[1]/screenSize[1] * rectangle.xOffset ) #* math.copysign(1,xdf)
    mpY = mousePosition[1] *  rectangle.height / screenSize[1] 
    # mpX = mpX + rectangle.origin[0]
    # mpY = mpY + rectangle.origin[1]
    mousePos = np.array((mpX,mpY))
    rotationMat = np.array( [[math.cos(rectangle.rotation * math.pi/180) , -math.sin(rectangle.rotation * math.pi/180) ],
                                 [math.sin(rectangle.rotation * math.pi/180) , math.cos(rectangle.rotation * math.pi/180) ]])
    mousePos = np.ceil(np.dot(rotationMat,mousePos)).astype(int)
    mousePos = mousePos + rectangle.origin
    return mousePos

def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    # pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

windowSize = (width,height) = (750,750)
pygame.init()
screenSize = (pygame.display.Info().current_w,pygame.display.Info().current_h)
# print(screenSize)
pygame.font.init()
screen = pygame.display.set_mode(windowSize)


bongoCat = pygame.image.load("bongo.png")
bongoCat = pygame.transform.scale(bongoCat,windowSize)

table = pygame.image.load("table.png")
table = pygame.transform.scale(table,windowSize)

bongoLArm = pygame.image.load("arm.png")
bongoLArmRect = bongoLArm.get_rect()

bongoRArmUp = pygame.image.load("pawUp.png")
bongoRArmUpRect = bongoRArmUp.get_rect()
bongoRArmUpRect.center = (bongoRArmUpRect.width/2,bongoRArmUpRect.height/2)

bongoRArmDown = pygame.image.load("pawDown.png")

mouse = pygame.image.load("mouse.png")
mouseRect = mouse.get_rect()

keyboard = pygame.image.load("keyboard.png")

# print(bongoCat)

# mapRectangle = RectMap( (50,0) , (0,50) ,100,50)
mapRectangle = RectMapV2( np.array((234,500)), -167 ,-20, 100,100)
# mapRectangle = RectMapV2( np.array((234,500)), 0 ,20, 100,100)

sign = lambda a: (a>0) - (a<0)

startListening()

angle = 0
while True:
    # print(str(mousePosition) + " " + str(keyPressed))
    mousePosition = pyautogui.position()
    
    # print(pyautogui.position())

    # mapRectangle.setRotation(mapRectangle.getRotation()+0.1)
    # mapRectangle.setInclination(mapRectangle.getInclination()+1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4): sys.exit()

    screen.fill((255,255,255))

    
    mappedMouse = mapMouse(mapRectangle,mousePosition)

    
    # mouseRect.move(mappedMouse[0],mappedMouse[1])
    mouseRect.center = mappedMouse

    # pygame.draw.circle(screen,(255,0,0),mappedMouseCoords, 10)
    pygame.draw.circle(screen,(255,0,0),mappedMouse, 10)
    mapRectangle.display()


    armPos = np.array((359,348))
    # armPos += np.array((-100,0))
    # bongoLArm = pygame.transform.rotate(bongoLArm, math.atan2(mappedMouse[1]-armPos[1]  , mappedMouse[0]-armPos[0] ))
    
    # bArm = pygame.transform.rotate(bArm,90)
    # bArm = pygame.transform.rotate(bongoLArm,math.atan2(armPos[1]-mappedMouse[1]  , armPos[0]-mappedMouse[0] ) * 180 / math.pi)
    # bArmRect = bongoLArm.get_rect()
    # bArmRect.center = armPos

    
    # angle += 1
    angle = math.atan2(armPos[1]-mappedMouse[1]  , armPos[0]-mappedMouse[0] ) * 180 / math.pi
    
    # angle=90
    
    screen.blit(table,(0,0))
    screen.blit(mouse,mouseRect)
    blitRotate(screen, bongoLArm, mappedMouse, (0,50), -angle)
    screen.blit(bongoCat,(0,0))

    
    screen.blit(keyboard,(375,429))

    if keyPressed == None:
        screen.blit(bongoRArmUp,np.array((513-bongoRArmUpRect.width/2,370-bongoRArmUpRect.height/2)).astype(int))
    else:
        p = (478,417)
        screen.blit(bongoRArmDown,p)
        # pygame.draw.circle(screen,(255,0,0), p, 8)




    
    
    # screen.blit(bongoLArm,mappedMouse)
    pygame.display.flip()
    pygame.display.update()
    