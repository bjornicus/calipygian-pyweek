from __future__ import generators
import math

"""
A quick attempt at defining an easy-to-use game-space
(after having issues last year with this, I figured we can start here.
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
    
    def __repr__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

    def __str__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

class RefCordinate():
    #NOTE, these cordinates are relative to the containing space, and
    # are NOT drawspace cordinates. 
    def __init__(self, baseCord, offsetCord, space):
        self.Space = space
        self._baseCord = baseCord
        self._offsetCord = offsetCord

    def get_x(self):
        return baseCord.get_x() + offsetCord.get_x()
    
    def get_y(self):
        return baseCord.get_x() + offsetCord.get_x()

    def set_x(self, x):
        baseCord.set_x(x - offsetCord.get_x())
    
    def set_y(self, y):
        baseCord.set_y(y - offsetCord.get_y())
    
    def __repr__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

    def __str__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

class GameObject(object):
    '''
    Ay element of the game
    '''
    GameObjectType = None

    def __init__(self):
        self.parent_space = None

    def Update(self, delta_t):
        pass

    def Draw(self, xy_pos):
        pass

    def __iter__(self):
        yield self

    def __contains__ (self, GameObject):
        return False
    
    def GetCordinatesInParentSpace(self):
        if self.parent_space is not None:
            return self.parent_space.GetCordinatesOfObject(self)
        else:
            return SpaceCordinate(None)

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
        for GameObj in self.ContentObjects.keys():
            if TargetObject is GameObj:
                return self.ContentObjects[TargetObject];
            if TargetObject in GameObj:
                SubSpace = GameObj
                OffsetCord = self.ContentObjects[SubSpace];
                BaseCord = SubSpace.GetCordinatesOfContainedObject(TargetObject)
                return RefCordinate(BaseCord, OffsetCord)

    def Update(self, delta_t):
        for GameObj in self.ContentObjects.keys():
            GameObj.Update(delta_t)

    def __iter__(self):
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