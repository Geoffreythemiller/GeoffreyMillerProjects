"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLeftArea(self):
        """
        Returns the boolean _left area
        
        """
        return self._leftarea
    def getVel(self):
        """
        Returns the vector for velocity
        
        """

        return self._velocity
    def setVel(self,vel):
        """
        Sets Velocity to vel 
        Parameter vel: the new vector to replace the old velocity vector
        Precondition vel: vel is a vector
        """
        self._velocity = vel
    def isBullet(self):
        """
        Return True always to identify that this object is a bullet
        """

        return True
    def isShip(self):
        """
        Return False always to identify that this object is not a ship 
        """

        return False

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, x, y, width, height, color, velocity):
        super().__init__( x=x, y=y, width=width, height=height, fillcolor =color)
        self._velocity = velocity
        self._leftarea = False

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        """
        Moves the Bullet and checks if it left the area

        """
        self.x = self.getVel().x + (self.x)
        self.y = self.getVel().y + (self.y)
        if self.x < -DEAD_ZONE:
            self._leftarea = True
        if self.x > GAME_WIDTH+DEAD_ZONE:
            self._leftarea = True
        if self.y < -DEAD_ZONE:
           self._leftarea = True
        if self.y > GAME_HEIGHT+DEAD_ZONE:
           self._leftarea = True

class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAngle(self):
        """
        Returns: the objects angle
        
        """
        return self.angle
    def setAngle(self,newangle):
        """
        sets the new angle
        Perameter: newangle is the ajusted angle
        Precondition: newangle is a float 
        """
        self.angle = newangle
    def setFace(self,newangle):
        """
        Sets the _facing with the newangle, uses a getter to get the angle instead of the parameter
        Perameter: newangle is the ajusted angle
        Precondition: newangle is a float 
        """
        self._facing = introcs.Vector2(x= math.cos(degToRad(self.getAngle())), y= math.sin(degToRad(self.getAngle())))
    def getFacing(self):
        """
        Returns: _facing 
        
        """
        return self._facing
    def getVel(self):
        """
        Returns the vector for velocity
        
        """

        return self._velocity
    def setVel(self,vel):
        """
        Sets Velocity to vel 
        Parameter vel: the new vector to replace the old velocity vector
        Precondition vel: vel is a vector
        """
        self._velocity = vel
    def isBullet(self):
        """
        Return False always to identify that this object is not a bullet
        """

        return False
    def isShip(self):
        """
        Return True always to identify that this object is  a ship 
        """

        return True
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, width, height, source, angle):
        super().__init__( x=x, y=y, width=width, height=height, source=source, angle = angle)
        self._velocity =  introcs.Vector2(x=0, y=0)
        self._facing =  introcs.Vector2(x= math.cos(degToRad(angle)), y= math.sin(degToRad(angle)))
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    #Turn METHOD
    def turn(self,newangle):
        """
        Turns the ship based off the new angle
        
        Perameter: newangle is the ajusted angle
        Precondition: newangle is a float 
        """
        self._ship.setAngle(newangle)
        self._ship.setFace(newangle)
    def setlocation(self):
        """
        Changes the position of the ship by adding the velocity to both the x and y
        
        """
        self.x = self.getVel().x + (self.x)
        self.y = self.getVel().y + (self.y)
class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVel(self):
        """
        Returns the vector for velocity
        
        """

        return self._velocity

    def setVel(self,vel):
        """
        Sets Velocity to vel 
        Parameter vel: the new vector to replace the old velocity vector
        Precondition vel: vel is a vector
        """
        self._velocity = vel

    def getSize(self):
        """
        Returns the size as the const for the image location
        """
        return self._size
    
    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, x,y, size, width, height,direction):
        super().__init__( x=x, y=y, source = size, width=width, height=height,)
        
        if size == SMALL_IMAGE:
            self._size = SMALL_IMAGE
            self._speed = SMALL_SPEED
        elif size == MEDIUM_IMAGE:
            self._size = MEDIUM_ASTEROID
            self._speed = MEDIUM_SPEED
        elif size == LARGE_IMAGE:
            self._size = LARGE_ASTEROID
            self._speed = LARGE_SPEED
        if direction != [0,0]:
            direction = introcs.Vector2(x=direction[0], y=direction[1])
            uvdirection= direction.normalize()
            self._velocity =  uvdirection.__mul__(self._speed)
        else:
            self._velocity = 0
        
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def setlocation(self):
        """
        Changes the position of the asteroid by adding the velocity to both the x and y
        
        """
        self.x = self.getVel().x + (self.x)
        self.y = self.getVel().y + (self.y)

    def checkForCollide(self, other):
        firstpoint = introcs.Point2(self.x,self.y)
        secondpoint = introcs.Point2(other.x,other.y)
        distance = firstpoint.distance(secondpoint)
        if (distance < (self.width/2+other.width/2)) and (other.isShip()==True):
            return True
        if (distance < (self.width/2+other.width/2)) and (other.isBullet()==True):
            return True
            
        
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
