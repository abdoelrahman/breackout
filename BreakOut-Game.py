from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import time


WINDOW_WIDTH = 555 
WINDOW_HEIGHT = 600 
deltaX = 1
deltaY = 1
time_interval = 1 # try  1000 msec
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()  # turn all of pygame on.
boopSound = pygame.mixer.Sound('sounds/boop.wav')
bloopSound = pygame.mixer.Sound('sounds/bloop.wav')
explosionSound = pygame.mixer.Sound('sounds/explosion.wav')
solidSound = pygame.mixer.Sound('sounds/solid (1).wav')
class RECTA:
    def __init__(self, left, bottom, right , top):
            self.left = left
            self.bottom = bottom
            self.right = right
            self.top = top
    
ball = RECTA(100, 100, 110, 110) # initial position of the ball
wall = RECTA(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
player = RECTA(10,0,60,10) # initial position of the bat
imaginaryAttacker = RECTA(0, 0, 0, 0)
# Initialize The  Attacker
attackers = [imaginaryAttacker]
horizentalSpace = 5
verticalSpace = 5
attackerLeft = 0
attackerWidth = 50
attackerheight = 15
attackerBtm =  WINDOW_HEIGHT - 45
attackerNum = 30
def initAttackers() : 
    global attackers 
    global horizentalSpace 
    global verticalSpace  
    global attackerLeft 
    global attackerWidth  
    global attackerheight  
    global attackerBtm 
    global attackerNum

    for i in range(attackerNum) : 
            if attackers[i].right  + horizentalSpace >= WINDOW_WIDTH : 
                attackerLeft = 0 
                attackerBtm -= 20
            attackers.append(RECTA(attackerLeft + horizentalSpace, attackerBtm, attackerLeft + horizentalSpace+ attackerWidth , attackerBtm + attackerheight ))
            attackerLeft += 55

initAttackers()

# Moveing the Attackers Down 
def moveDown() :
    # global attackers
    global attackers 
    global horizentalSpace 
    global verticalSpace  
    global attackerLeft 
    global attackerWidth  
    global attackerheight  
    global attackerBtm
    global attackerNum
    attackers = [imaginaryAttacker]
    for i in range(attackerNum) : 
        if attackers[i].right  + horizentalSpace >= WINDOW_WIDTH : 
            attackerLeft = 0 
            attackerBtm -= 20
        attackers.append(RECTA(attackerLeft + horizentalSpace, attackerBtm , attackerLeft + horizentalSpace+ attackerWidth , attackerBtm + attackerheight+2 ))
        attackerLeft += 55

# Initialization
def init():
	glClearColor (0.0, 0.0, 0.0, 0.0)
  
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity ()
	glOrtho(0, WINDOW_WIDTH, 0 , WINDOW_HEIGHT , 0 , 1) # l,r,b,t,n,f


	glMatrixMode (GL_MODELVIEW)
	
def DrawRectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS) 
    glVertex(rect.left,rect.bottom,0)      #Left - Bottom 
    glVertex(rect.right,rect.bottom,0) 
    glVertex(rect.right,rect.top,0) 
    glVertex(rect.left,rect.top,0) 
    glEnd() 

def drawText(string, x, y):
    glLineWidth(3)
    glColor(1,0,0)  # Yellow Color
    glLoadIdentity() 
    # remove the previous transformations
    # glScale(0.13,0.13,1)  # Try this line
    glTranslate(x,y,0)  # try comment this line
    glScale(0.13,0.13,1)
    string = string.encode() # conversion from Unicode string to byte string
    for c in string: # render character by character starting from the origin
        glutStrokeCharacter(GLUT_STROKE_ROMAN , c )

p_player = 0

def Test_Ball_Wall(ball, wall):  # Collision Detection between Ball and Wall
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM
    global deltaY
    global deltaX
    global dies



    #print(ball.right)
    if ball.right >= wall.right: 
        deltaX = -deltaX
        boopSound.play()
    if ball.left <= wall.left: 
        deltaX = -deltaX
        boopSound.play()
    if ball.top >= wall.top: 
        deltaY = -deltaY
        boopSound.play()
    if ball.bottom <= wall.bottom: 
            deltaY = -deltaY
            boopSound.play()
            if dies <= 8:
                dies = dies +1
            # deltaY = 0
            # deltaX = 0
            # drawText("GAME OVER ", (WINDOW_WIDTH // 2) -40, WINDOW_HEIGHT // 2)
    #Otherwise returns None

def Test_Ball_Player(ball, player):  # Collision Detection between Ball and Bat
    global deltaY
    global p_player
    A = ball.left>=player.left
    D = ball.left<=player.right
    B = ball.right<=player.right
    C = ball.right>=player.left
    
    if ball.bottom <= player.top and ((A and D) or (B and C)) and deltaY == -1:
        deltaY= - deltaY
        p_player = 0
        solidSound.play()
   
score = 0

def Test_Ball_Attacker(ball, attackersQuads):
    global score
    global deltaY
    global deltaX
    global attackers 
    for i in attackersQuads: 
        # from Btm of the attacker 
        A = ball.top == i.bottom
        B = ball.right >= i.left
        C = ball.left <= i.right
        # from Top of the attacker
        D = ball.bottom == i.top
        E = ball.right >= i.left
        F = ball.left <= i.right
        # fom Right
        G = ball.left == i.right 
        H = ball.bottom <= i.top 
        I = ball.top >= i.bottom
        # from Left
        J = ball.right == i.left
        K = ball.bottom <= i.top
        L = ball.top >= i.bottom
        
        if ( D and E and F ) : 
            attackers.remove(i)
            deltaY = - deltaY
            score += 1
            explosionSound.play()
        if ( A and B and C ) : 
            attackers.remove(i)
            deltaY = - deltaY
            score += 1
            explosionSound.play()
        # if ( G and H and I ) : 
        #     attackers.remove(i)
        #     deltaY = - deltaX
        #     score += 1
        # if ( J and K and L ) : 
        #     attackers.remove(i)
        #     deltaY = - deltaX
        #     score += 1

# Key Board Messages 
def keyboard(key, x, y):
    global deltaY
    global deltaX
    global dies

    if key == b"q":
            sys.exit(0)
    if key == b"a":
        deltaY = 1
        deltaX = 1
        dies = 0



mouse_x=0
def MouseMotion(x, y): # returns the mouse coordinates in "pixel"
	global mouse_x
	mouse_x=x
	#print("mouse_x= ",x, "pixels")
	#print("mouse_y= ",y, "pixels")

def Timer(v): 
	Display() 
	glutTimerFunc(time_interval,Timer,1)


dies = 0
g_timer=0
def Display() : 
    global attackers
    global score
    global deltaY 
    global deltaX
    global p_player
    global dies
    global g_timer
    glClear(GL_COLOR_BUFFER_BIT)
    glColor(1, 0, 1)
    # string = "dies: " + str(dies)
    # drawText(string, 10, 440)
    # glColor(.3, .3, 1)
    glClear(GL_COLOR_BUFFER_BIT )

     # render The Attacker 
    for attacker in attackers :
        DrawRectangle(attacker)

    string = "die : " + str(dies)
    drawText(string, 10, 440)
    string = "score : " + str(score)
    drawText(string, 10, 400)
    # Render The Ball
    ball.left = ball.left + deltaX   # updating ball's coordinates
    ball.right = ball.right + deltaX 
    ball.top = ball.top + deltaY
    ball.bottom = ball.bottom + deltaY

    glColor(1,p_player,p_player)  # White color
    DrawRectangle(ball)

      # Render The Bat 
    player.left=mouse_x-30  # remember that "mouse_x" is a global variable 
    player.right=mouse_x+30
    DrawRectangle(player)
# _______________________________________________________________________________#
    # detecte The Collesion Btween Ball & Attackers
    Test_Ball_Attacker(ball, attackers)

     # Detection between The Ball & The Wall
    Test_Ball_Wall(ball,wall)
    
    # Detection between The Ball & The Player
    Test_Ball_Player(ball,player)
    
    # Win The Game

    if len(attackers) == 1 :
        deltaY = 0
        deltaX = 0
        glColor(0, 1, 0)
        drawText("YOu WIN  ", (WINDOW_WIDTH // 2) -40, WINDOW_HEIGHT // 2)
    if dies >= 8:
        deltaY = 0
        deltaX = 0
        glColor(0, 1, 0)
        drawText("game over  ", (WINDOW_WIDTH // 2) - 40, WINDOW_HEIGHT // 2)













    if p_player < 1:
        p_player += .01
    glutSwapBuffers()

def main():
   glutInit()
   glutInitDisplayMode ( GLUT_DOUBLE | GLUT_RGB)
   glutInitWindowSize (WINDOW_WIDTH, WINDOW_HEIGHT) # mouse coordinates inbetween [WINDOW_WIDTH=800,WINDOW_HEIGHT=500]
   #glutInitWindowSize (1100, 600) # try and notice the bat; mouse coordinates inbetween [1100,600] (where 1100 pixels = 800 in openGL)
   glutInitWindowPosition (150, 50)
   glutCreateWindow (b"Simple Ball Bat OpenGL game");
   glutDisplayFunc(Display)
   glutTimerFunc(time_interval,Timer,1)
   glutKeyboardFunc(keyboard)
   glutPassiveMotionFunc(MouseMotion)
   init( )   
   glutMainLoop()

main()