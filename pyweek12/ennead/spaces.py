from __future__ import generators
import math
from constants import *

"""
A quick attempt at defining an easy-to-use game-space
"""

class SpaceCordinate():
    #NOTE, these cordinates are relative to the containing space, and
    # are NOT drawspace cordinates. 
    def __init__(self, space, x=0, y=0):
        self.Space = space
        self._x = x
        self._y = y

    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x
    
    def set_y(self, y):
        self._y = y

    def adjust_x(self, dx):
        self._x += x
    
    def adjust_y(self, dy):
        self._y += y
    
    def __repr__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

    def __str__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

    def AdaptCordinateToContainedObject(self, TargetObject):
        space = self.Space
        while not TargetObject in space:
            space = space.parent_space

        if space is None:
            print("Warning: Atempted to adapt cordinate %s for object %s, "+
                  "but they do not share a common space!" %
                  (self, TargetObject))
            return None
        
        ObjectCord = self.Space.GetCordinatesOfContainedObject(TargetObject)

        retval = RefCordinate(self, ObjectCord, TargetObject, negative=True)
        return retval

    def NewCordAtThisPosition(self):
        return SpaceCordinate(self.space, self.get_x(), self.get_y())

class OffsetCordinate(SpaceCordinate):
    def __init__(self, baseCord, x, y):
        SpaceCordinate.__init__(self, baseCord.Space)
        self._baseCord = baseCord
        self.xOffset = x
        self.yOffset = y

    def get_x(self):
        return self._baseCord.get_x() + self.xOffset
    
    def get_y(self):
        return self._baseCord.get_y() + self.yOffset

    def set_x(self, x):
        self._baseCord.set_x(x - self.xOffset)
    
    def set_y(self, y):
        self._baseCord.set_y(y - self.yOffset)

    def adjust_x(self, dx):
        self._baseCord.adjust_x(dx)
    
    def adjust_y(self, dy):
        self._baseCord.adjust_y(dy)
    
    def __repr__(self):
        return "OffsetCordinate(%s, %d, %d)" % (self._baseCord, self.xOffset, self.yOffset)

    def __str__(self):
        return "OffsetCordinate(%s, %d, %d)" % (self._baseCord, self.xOffset, self.yOffset)

        
class RefCordinate(SpaceCordinate):
    def __init__(self, baseCord, offsetCord, space, negative=False):
        SpaceCordinate.__init__(self, space)
        self._baseCord = baseCord
        self._offsetCord = offsetCord
        self._negative = negative

    def get_x(self):
        if not self._negative:
            return self._baseCord.get_x() + self._offsetCord.get_x()
        else:
            return self._baseCord.get_x() - self._offsetCord.get_x()
    
    def get_y(self):
        if not self._negative:
            return self._baseCord.get_y() + self._offsetCord.get_y()
        else:
            return self._baseCord.get_y() - self._offsetCord.get_y()

    def set_x(self, x):
        if not self._negative:
            self._baseCord.set_x(x - self._offsetCord.get_x())
        else:
            self._baseCord.set_x(x + self._offsetCord.get_x())
    
    def set_y(self, y):
        if not self._negative:
            self._baseCord.set_y(y - self._offsetCord.get_y())
        else:
            self._baseCord.set_y(y + self._offsetCord.get_y())

    def adjust_x(self, dx):
        self._baseCord.adjust_x(dx)
    
    def adjust_y(self, dy):
        self._baseCord.adjust_y(dy)
    
    def __repr__(self):
        return "RefCordinate(%s, %s, %s, %d)" % (self._baseCord, self._offsetCord, self.Space, self._negative)

    def __str__(self):
        return "RefCordinate(%s, %s, %s, %d)" % (self._baseCord, self._offsetCord, self.Space, self._negative)

class CordRectangle():
    def __init__(self, bottom_left_cord, width, height):
        self.width = width
        self.height = height
        
        self.BottomLeft = bottom_left_cord
        self.BottomRight = OffsetCordinate(bottom_left_cord, self.width, 0)
        self.TopLeft = OffsetCordinate(bottom_left_cord, 0 , self.height)
        self.TopRight = OffsetCordinate(bottom_left_cord, self.width , self.height)

    def GetCorners(self):
        return [self.BottomLeft, self.BottomRight, self.TopLeft, self.TopRight]


    def __str__(self):
        return ("CordRectangle((%d,%d), (%d,%d), (%d,%d), (%d,%d))" %
                (self.BottomLeft.get_x(), self.BottomLeft.get_y(),
                 self.BottomRight.get_x(), self.BottomRight.get_y(),
                 self.TopLeft.get_x(), self.TopLeft.get_y(),
                 self.TopRight.get_x(), self.TopRight.get_y()))
   
        
class GameObject(object):
    '''
    Any element of the game
    '''
    GameObjectType = None

    def __init__(self):
        self.parent_space = None
        self.width = 0
        self.height = 0

    def Update(self, delta_t):
        pass

    def Draw (self, xy_pos):
        pass

    def Draw_Platform(self, xy_pos):
        pass

    def Draw_Puzzle(self, xy_pos):
        pass

    def on_mouse_event(self, Event_Type, Chord, buttons, modifiers, gesture):
        pass

    def __iter__(self):
        yield self

    def __contains__ (self, GameObject):
        return False
    
    def GetCordinatesInParentSpace(self):
        if self.parent_space is not None:
            return self.parent_space.GetCordinatesOfContainedObject(self)
        else:
            return SpaceCordinate(self)

    def GetBoundingRectangle(self):
        if self.parent_space is None:
            return CordRectangle(SpaceCordinate(self), self.width, self.height)
        
        BaseCord = self.parent_space.GetCordinatesOfContainedObject(self)
        return CordRectangle(BaseCord, self.width, self.height)

    def CheckForIntersection(self, CordRect):
        BottomLeft = CordRect.BottomLeft.AdaptCordinateToContainedObject(self)
        BottomRight = CordRect.BottomRight.AdaptCordinateToContainedObject(self)
        TopLeft = CordRect.TopLeft.AdaptCordinateToContainedObject(self)
        TopRight = CordRect.TopRight.AdaptCordinateToContainedObject(self)

        #test to see if one of the rectangle corners is inside of this objects bounds
        cords = [BottomLeft, BottomRight, TopLeft, TopRight]
        for cord in cords:
            if (( 0 <= cord.get_x() < self.width ) and
                ( 0 <= cord.get_y() < self.height)):
                return True

        #test to see if one of this objects corners is inside of the rectangle
        cords = self.GetBoundingRectangle().GetCorners()
        for cord in cords:
            if (( BottomLeft.get_x() <= cord.get_x() < BottomRight.get_x() ) and
                ( BottomLeft.get_y() <= cord.get_y() < TopLeft.get_y())):
                return True

        return False            
            
    def TestCordIsWithinObject(self, Cord):
        if Cord is None:
            return False

        AdaptedCord = Cord.AdaptCordinateToContainedObject(self)

        """print ("Testing (%d, %d) against (%d, %d)" %
               ( AdaptedCord.get_x(), AdaptedCord.get_y(),
                self.width, self.height))"""
        if (( 0 <= AdaptedCord.get_x() < self.width ) and
            ( 0 <= AdaptedCord.get_y() < self.height)):
            return True
        else:
            return False

    def GetObjectsInRectangle(self, rect):
        if not self.CheckForIntersection(rect):
            return []
        return [self]

class CordinateSpace(GameObject):
    GameObjectType = "CordinateSpace"
    
    def __init__(self):
        GameObject.__init__(self)
        self.ContentObjects = {} #dictionary of objects and cordinates

    def AddObject(self, GameObject, x=0, y=0):
        self.ContentObjects[GameObject] = SpaceCordinate(self, x, y)
        GameObject.parent_space = self

    def RemoveObject(self, TargetObject):
        TargetObject.parent_space = none
        del self.ContentObjects[TargetObject]

    def GetCordinatesOfContainedObject(self, TargetObject):
        if TargetObject is self:
            return SpaceCordinate(self)
        for GameObj in self.ContentObjects.keys():
            if TargetObject is GameObj:
                return self.ContentObjects[TargetObject];
            if TargetObject in GameObj:
                SubSpace = GameObj
                OffsetCord = self.ContentObjects[SubSpace];
                BaseCord = SubSpace.GetCordinatesOfContainedObject(TargetObject)
                return RefCordinate(BaseCord, OffsetCord, self)
        print( "Attempted to get cordinates of object %s from space %s, " +
               "which does not house that object" %
               (TargetObject, self))
        return None #This should blow up, letting us know when something has gone wrong            

    def GetObjectsInRectangle(self, rect):
        
        if not self.CheckForIntersection(rect):
            return []
        objects = []
        for GameObj in self.ContentObjects.keys():
            if GameObj.CheckForIntersection(rect):
                 objects.extend(GameObj.GetObjectsInRectangle(rect))
        return objects

    def Update(self, delta_t):
        for GameObj in self.ContentObjects.keys():
            GameObj.Update(delta_t)

    def on_mouse_event(self, Event_Type, Cord, buttons, modifiers, gesture):
        for GameObj in self.ContentObjects.keys():          
            if (GameObj.TestCordIsWithinObject(Cord)):
                GameObj.on_mouse_event(
                    Event_Type,
                    Cord,
                    buttons,
                    modifiers,
                    gesture)
            

    def __iter__(self):
        yield self
        for GameObj in self.ContentObjects.keys():
            for SubGameObj in GameObj:
                if SubGameObj is not None:
                    yield SubGameObj


    def __contains__ (self, TargetObject):
        if TargetObject is self:
            return True
        if TargetObject in self.ContentObjects.keys():
            return True
        for SubSpace in self.ContentObjects.keys():
            if TargetObject in SubSpace:
                return True
        return False
