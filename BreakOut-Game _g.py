from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import time

WINDOW_WIDTH = 555 
WINDOW_HEIGHT = 600 
deltaX = 1
deltaY = 1
time_interval = 1 
attempts = 5
mouse_x=0
score = 0
# Sound 
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
attackerBtm =  WINDOW_HEIGHT - 70
attackerNum = 40
def initAttackers() : 
    global attackers 
    global horizentalSpace 
    global verticalSpace  
    global attackerLeft 
    global attackerWidth  
    global attackerheight  
    global attackerBtm 
    global attackerNum
    for i in  range(attackerNum) : 
        if i < 30 :
            if attackers[i].right  + horizentalSpace >= WINDOW_WIDTH : 
                attackerLeft = 0 
                attackerBtm -= 20
            attackers.append(RECTA(attackerLeft + horizentalSpace, attackerBtm, attackerLeft + horizentalSpace+ attackerWidth , attackerBtm + attackerheight ))
            attackerLeft += 55
        else : 
            if attackers[i].right  + horizentalSpace >= WINDOW_WIDTH : 
                attackerLeft = 0 
                attackerBtm -= 20
            attackers.append(RECTA(attackerLeft + horizentalSpace, attackerBtm-50, attackerLeft + horizentalSpace+ attackerWidth , attackerBtm -50 + attackerheight ))
            attackerLeft += 55 
initAttackers()

def moveDown(v) :  
    for attacker in attackers : 
        attacker.top -= 30
        attacker.bottom -= 30
    ball.top -= 30
    ball.bottom -= 30
    glutTimerFunc(10000,moveDown,1)

def init():
	glClearColor (.1,.1,.1, 0.0)
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

def drawText(string, x, y, xColor, yColor, zColor):
    glLineWidth(1)
    glColor(xColor,yColor,zColor)  # Yellow Color
    glLoadIdentity() 
    # remove the previous transformations
    # glScale(0.13,0.13,1)  # Try this line
    glTranslate(x,y,0)  # try comment this line
    glScale(0.13,0.13,1)
    string = string.encode() # conversion from Unicode string to byte string
    for c in string: # render character by character starting from the origin
        glutStrokeCharacter(GLUT_STROKE_ROMAN , c ) 		

def Test_Ball_Wall(ball, wall):  # Collision Detection between Ball and Wall
    global deltaY
    global deltaX
    global attempts
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
        attempts -= 1
        ball.left = 100 
        ball.bottom = 100
        ball.top = 110
        ball.right = 110
        deltaY = 1
        deltaX = 1

def Test_Ball_Player(ball, player):  # Collision Detection between Ball and Bat
    global deltaY
    A = ball.left>=player.left
    D = ball.left<=player.right
    B = ball.right<=player.right
    C = ball.right>=player.left
    if ball.bottom <= player.top and ((A and D) or (B and C)) and deltaY == -1:
        deltaY= - deltaY
        solidSound.play()
   
def Test_Ball_Attacker(ball, attackersQuads): # Collision Detection between Ball and Attackers
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
        #     explosionSound.play()
        # if ( J and K and L ) :
        #     attackers.remove(i)
        #     deltaY = - deltaX
        #     score += 1
        #     explosionSound.play()

def Test_Bat_Attacker(bat, attackers) :  # Collision Detection between Ball and Attackers
    for i in attackers : 
        if bat.top >= i.bottom : 
            attackers.remove(i)
 
def keyboard(key, x, y):
    if key == b"q": 
        sys.exit(0)
    if key == b"c": 
        Retry()

def Retry() : 
    global attempts
    global attackerNum
    global deltaY
    global deltaX
    global score
    global attackerBtm
    global  attackerLeft
    attackerLeft = 0
    attackerBtm =  WINDOW_HEIGHT - 70
    initAttackers()
    attempts = 8
    score = 0
    ball.left = 100
    ball.right = 110
    deltaX = 1
    deltaY = 1

def MouseMotion(x, y): # returns the mouse coordinates in "pixel"
	global mouse_x
	mouse_x=x
	#print("mouse_x= ",x, "pixels")
	#print("mouse_y= ",y, "pixels")

def Timer(v): 
	Display() 
	glutTimerFunc(time_interval,Timer,1)

def Display() : 
    global attackers
    global score
    global deltaY 
    global deltaX

    glClear(GL_COLOR_BUFFER_BIT)
    # render The Attacker 
    x = .4
    y = 0
    z = .2
    for attacker in attackers :
        glColor(y, x, z) 
        DrawRectangle(attacker)
        x += .001
        y += .01
        z += .001

    # Render The Ball
    ball.left = ball.left + deltaX   # updating ball's coordinates
    ball.right = ball.right + deltaX 
    ball.top = ball.top + deltaY
    ball.bottom = ball.bottom + deltaY

    glColor(1,1,1)  
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

    # collision between The Ball & The Player
    Test_Ball_Player(ball,player)

    # detecte The Collesion Btween player & Attackers
    Test_Bat_Attacker(player, attackers)
    # ________________________________________________________________________________#
    string = "score : " + str(score)
    drawText(string, 10, 560, 1, 1, 0)
    
    string2 = 'Your Attempts : ' + str(attempts)
    drawText(string2, WINDOW_WIDTH -170, 560, 0.8, 0.4, .4)

    # Vectory
    if len(attackers) == 0 and attempts > 0 : 
        deltaY = 0
        deltaX = 0
        attackers = [imaginaryAttacker]
        ball.left = 0
        ball.right = 0
        drawText("Vectory ", (WINDOW_WIDTH // 2) -40, WINDOW_HEIGHT // 2, 0, 1, 0)
        drawText("Press C to Retry ", (WINDOW_WIDTH // 2) -80, (WINDOW_HEIGHT // 2) -80, .8, .8, .8)

    # Game Over
    if attempts == 0 :
        deltaY = 0
        deltaX = 0
        attackers = [imaginaryAttacker]
        ball.left = 0
        ball.right = 0
        drawText("GAME OVER ", (WINDOW_WIDTH // 2) -40, WINDOW_HEIGHT // 2, 1, 0, 0)
        drawText("Press C to Retry ", (WINDOW_WIDTH // 2) -60, (WINDOW_HEIGHT // 2)- 80, .8, .8, .8)


    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode ( GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize (WINDOW_WIDTH, WINDOW_HEIGHT) # mouse coordinates inbetween [WINDOW_WIDTH=800,WINDOW_HEIGHT=500]
    #glutInitWindowSize (1100, 600) # try and notice the bat; mouse coordinates inbetween [1100,600] (where 1100 pixels = 800 in openGL)
    glutInitWindowPosition (150, 50)
    glutCreateWindow (b"breackout");
    glutDisplayFunc(Display)
    glutTimerFunc(time_interval,Timer,1)
    glutTimerFunc(10000,moveDown,1)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(MouseMotion)
    init( )   
    glutMainLoop()

main()