"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0

    # Attribute _last: to make sure the bullets are being fired in occordance to 
    #           the BULLET_RATE
    # Invariant: _last is an int >=0

    # Attribute _previousShip: The information of the previous ship so when the game is reset 
    #            after a collsion it remebers the infomation about the ship
    # Invariant: _previousShip is a Ship object

    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self,jsonfile):
        """
        Initializes the wave.

        Note that this is a proper initializer, because
        wave is NOT a subclass of GameApp (we only
        want one Window).  However, it needs to know the
        width and height of the window, so we pass them
        as arguments.

        Parameter jsonfile: a json file containing info about the games level
        Precondition: jsonfile is a .json file
        """
        self._data = jsonfile 
        p = ((self._data["ship"])['position'])
        an = ((self._data["ship"])['angle'])
        a = SHIP_RADIUS*2
        self._ship = Ship(x=p[0],y=p[1],width=a,height=a,source=SHIP_IMAGE,angle=an)
        self._asteroids  = []
        self._create_ASTEROIDS()
        self._bullets = []
        self._last = 0
        self._lives = SHIP_LIVES
        self._previousShip = self._ship
        

    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update( self, input):
        """
        Animates a single frame in the game.

    
        Parameter input: the user input, used to control the ship and change state
        Precondition: input is an instance of GInput
        """
        
        self._gbullet =  []
        self._gastroid = []
        shipisNone = False
        self._ship = self._previousShip 
        if self._ship != None and self._lives>0:
            self._moveShip(input)
            self._fireBullets(input)
            
            self._checkshipwrapping()
            for asteroid in range(len(self._asteroids)):
                self._asteroids[asteroid].setlocation()
                jd= False
                for bullet in range(len(self._bullets)):
                    if self._asteroids[asteroid].checkForCollide(self._bullets[bullet]) == True:
                        jd = True
                        self._splitUpAstBull(asteroid, bullet)
                        self._gbullet.append(bullet)
                        self._gastroid.append(asteroid)
                       

                if (jd == False and (self._asteroids[asteroid].checkForCollide(self._ship) == True)):
                    self._splitUpAstShip(asteroid, self._ship)
                    self._gastroid.append(asteroid)
                    shipisNone =  True

                self._checkasteroidwrapping(self._asteroids[asteroid])
            self._checkGarbage(shipisNone)
            
                
        
            


    
    

        


    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        """
        Draws the game objects to the view.
        
        Parameter view: the game view, used in drawing 
        Precondition: view is an instance of GView
        
        """
        if self._ship != None:
            self._ship.draw(view)
            for asteroids in self._asteroids:
                asteroids.draw(view)
            for bullets in self._bullets:
                bullets.draw(view)
        

        

    # RESET METHOD FOR CREATING A NEW LIFE
    def _checkGarbage(self,shipisNone):
        """
        Does a garbage check and deletes any astroid/bullets that were involved in a
        collison. Also check if the boolean 'shipisNone' is equal to True in which
        it saves a copy of the ship deletes a life and makes the ship None

        Parameter shipisNone: a boolean 
        Precondition: shipisNone is a boolean

        """

        self._garabage() 
        if shipisNone == True:
            self._previousShip = self._ship
            self._lives = self._lives - 1
            self._ship = None
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _moveShip(self, input):
        """
        Moves the ship based off three different inputs
        Those inputs are left right and up

        Parameter input: the user input, used to control the ship and change state
        Precondition: input is an instance of GInput

        """
        newangle = self._ship.getAngle() 
        if input.is_key_down('left'):
            newangle += SHIP_TURN_RATE 
            
            Ship.turn(self,newangle)

        if input.is_key_down('right'):
            newangle-= SHIP_TURN_RATE 
            Ship.turn(self,newangle)

        if input.is_key_down('up'):
            self._change_velocity() 
            self._ship.setlocation()


    def _fireBullets(self,input):
        """
        Method to fire bullets based off imput given
        
        Parameter input: the user input, used to control the ship and change state
        Precondition: input is an instance of GInput

        """
        if input.is_key_down('spacebar'):
            self._checkToFireBullets()
            
        for bullets in self._bullets:
            bullets.move()
            self._deleteBullets()




    def _getImpulse(self):
        """
        Returns: the ships new impulse based off of the facing angle

        """
        face = self._ship.getFacing()
        return face* SHIP_IMPULSE


    def _change_velocity (self):
        """
        Moves the ship based off the inpulse
        
        """
        impulse = self._getImpulse()
        velocity = self._ship.getVel()
        newvel= velocity.__add__(impulse)
        if newvel.length() <= SHIP_MAX_SPEED:
            self._ship.setVel(newvel)
        else:
            newvel = (newvel.normalize())*SHIP_MAX_SPEED
            self._ship.setVel(newvel)
    def _checkshipwrapping(self):
        """
        A series of if statements to make sure the ship wraps around the screen

        """
        if self._ship.x < -DEAD_ZONE :
            self._ship.x = self._ship.x + (GAME_WIDTH+2*DEAD_ZONE)
        if self._ship.x > GAME_WIDTH+DEAD_ZONE :
            self._ship.x = self._ship.x - (GAME_WIDTH+2*DEAD_ZONE)
        if self._ship.y < -DEAD_ZONE :
            self._ship.y = self._ship.y + GAME_HEIGHT+2*DEAD_ZONE
        if self._ship.y > GAME_HEIGHT+DEAD_ZONE :
            self._ship.y = self._ship.y - GAME_HEIGHT+2*DEAD_ZONE
    def _checkasteroidwrapping(self, asteriod):
        """
        A series of if statements to make sure the 'asteriod' wraps around the screen
        
        Parameter asteriod: the asteriod to which keep on screen
        Precondition: asteriod is an object of the asteriod class in models.py
        """
        if asteriod.x < -DEAD_ZONE:
            asteriod.x = asteriod.x + GAME_WIDTH+2*DEAD_ZONE
        if asteriod.x > GAME_WIDTH+DEAD_ZONE:
            asteriod.x = asteriod.x - GAME_WIDTH+2*DEAD_ZONE
        if asteriod.y < -DEAD_ZONE:
            asteriod.y = asteriod.y + GAME_HEIGHT+2*DEAD_ZONE
        if asteriod.y > GAME_HEIGHT+DEAD_ZONE:
            asteriod.y = asteriod.y - GAME_HEIGHT+2*DEAD_ZONE

    def _create_ASTEROIDS(self):
        """
        A method that reads the _data looking for information on the asteriods
        when it finds the asteriods in the dictionary it creates an asteriod 
        object for each asteroid in the _data 

        """
        shortendlist = (self._data["asteroids"])
        for asteroids in shortendlist:
            if asteroids['size'] == 'small':
                size = SMALL_IMAGE 
                rad = SMALL_RADIUS
            elif asteroids['size'] == 'medium':
                size = MEDIUM_IMAGE
                rad = MEDIUM_RADIUS
            else:
                size = LARGE_IMAGE
                rad = LARGE_RADIUS
            direction = asteroids['direction']
            position = asteroids['position']
            newobj = [Asteroid(position[0], position[1],size,rad*2,rad*2,direction )]
            self._asteroids += newobj
    

    def _createBullet(self):
        """
        Method that gets infomation from self._ship and creates a bullet object off it.
        It then adds the new bullet object to the _bullets list

        """
        tip = self._ship.getFacing().__mul__(SHIP_RADIUS) 
        x = self._ship.x +tip.x
        y = self._ship.y +tip.y
        area = BULLET_RADIUS*3
        bullVel= self._ship.getFacing().__mul__(BULLET_SPEED)
        bullet = Bullet(x= x+1 ,y=y+1 ,width = area, height = area , color = BULLET_COLOR, velocity= bullVel )
        self._bullets = self._bullets + [bullet]



    def _checkToFireBullets(self):
        """
        Method to make sure the bullets are being fired in occordance to 
        the BULLET_RATE and calls the _createBullet() method.

        """
        self._last += 10
        if self._last >= BULLET_RATE:
            self._last = 0
            self._createBullet()
    def _deleteBullets(self):
        """
        Method that deletes bullets that leave the screen

        """
        i = 0
        while i < len(self._bullets):
            if self._bullets[i].getLeftArea():
                del self._bullets[i]
            else:
                i += 1
    def _garabage(self):
        """
        Method that traverses through both the _gbullet and _gasteroid lists
        deleting those objects from their respective lists
        
        """
        for bull in self._gbullet:
            del self._bullets[bull]
            
        for asd in self._gastroid:
            del self._asteroids[asd]   
            

    def getShip(self):
        """
        Returns: current ship object
        
        """
        return self._ship

    def getLives(self):
        """
        Returns: current _lives
        
        """
        return self._lives

    def getTotalAst(self):
        """
        Returns: The total asteroids in the _asteroids list
        
        """
        return len(self._asteroids)

    def _splitUpAstBull(self, asteroid, bullet):
        """
        Method that splits up the Asteroid into three smaller asteroids if 
        the asteriod bing hit was a Large or Medium asteroid 
        
        Parameter asteriod: the index of the hit asteroid
        Precondition asteriod: asteriod is an int

        Parameter bullet: the index of the bullet that hit the asteroid
        Precondition bullet: bullet is an int
    
        """
        ast = self._asteroids[asteroid]
        bull = self._bullets[bullet]
        x = ast.x
        y = ast.y
        collvec = (bull.getVel()).normalize()
        rv1 = collvec.rotation((2*math.pi)/3)
        rv2 = collvec.rotation((-2*math.pi)/3)
        
        if ast.getSize()== LARGE_ASTEROID:
            rad = MEDIUM_RADIUS
            newobj = [Asteroid(x+(rad*collvec.x), y+(rad*collvec.y),'asteroid2.png',rad*2,rad*2,[collvec.x,collvec.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv1.x), y+(rad*rv1.y),'asteroid2.png',rad*2,rad*2,[rv1.x,rv1.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv2.x), y+(rad*rv2.y),'asteroid2.png',rad*2,rad*2,[rv2.x,rv2.y] )]
            self._asteroids += newobj
        if ast.getSize()== MEDIUM_ASTEROID:
            rad = SMALL_RADIUS
            newobj = [Asteroid(x+(rad*collvec.x), y+(rad*collvec.y),'asteroid3.png',rad*2,rad*2,[collvec.x,collvec.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv1.x), y+(rad*rv1.y),'asteroid3.png',rad*2,rad*2,[rv1.x,rv1.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv2.x), y+(rad*rv2.y),'asteroid3.png',rad*2,rad*2,[rv2.x,rv2.y] )]
            self._asteroids += newobj
    
    def _splitUpAstShip(self, asteroid, ship):
        """
        Method that splits up the Asteroid into three smaller asteroids if 
        the asteriod bing hit was a Large or Medium asteroid 
        
        Parameter asteriod: the index of the hit asteroid
        Precondition asteriod: asteriod is an int

        Parameter ship: the current wave._ship object
        Precondition ship: is a Ship object
        
        
        """
        ast = self._asteroids[asteroid]
        
        x = ast.x
        y = ast.y
        if (ship.getVel().x == 0.0 and ship.getVel().y == 0.0):
            collvec = (ship.getFacing()).normalize()
        else:
            collvec = (ship.getVel()).normalize()
        rv1 = collvec.rotation((2*math.pi)/3)
        rv2 = collvec.rotation((-2*math.pi)/3)
        
        if ast.getSize()== LARGE_ASTEROID:
            rad = MEDIUM_RADIUS
            newobj = [Asteroid(x+(rad*collvec.x), y+(rad*collvec.y),'asteroid2.png',rad*2,rad*2,[collvec.x,collvec.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv1.x), y+(rad*rv1.y),'asteroid2.png',rad*2,rad*2,[rv1.x,rv1.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv2.x), y+(rad*rv2.y),'asteroid2.png',rad*2,rad*2,[rv2.x,rv2.y] )]
            self._asteroids += newobj
        if ast.getSize()== MEDIUM_ASTEROID:
            rad = SMALL_RADIUS
            newobj = [Asteroid(x+(rad*collvec.x), y+(rad*collvec.y),'asteroid3.png',rad*2,rad*2,[collvec.x,collvec.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv1.x), y+(rad*rv1.y),'asteroid3.png',rad*2,rad*2,[rv1.x,rv1.y] )]
            self._asteroids += newobj
            newobj = [Asteroid(x+(rad*rv2.x), y+(rad*rv2.y),'asteroid3.png',rad*2,rad*2,[rv2.x,rv2.y] )]
            self._asteroids += newobj

            