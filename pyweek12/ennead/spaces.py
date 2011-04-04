from __future__ import generators
import math

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
    
    def __repr__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

    def __str__(self):
        return "SpaceCordinate(%s, %d, %d)" % (self.Space, self._x, self._y)

class RefCordinate():
    def __init__(self, baseCord, offsetCord, space):
        self.Space = space
        self._baseCord = baseCord
        self._offsetCord = offsetCord

    def get_x(self):
        return self._baseCord.get_x() + self._offsetCord.get_x()
    
    def get_y(self):
        return self._baseCord.get_y() + self._offsetCord.get_y()

    def set_x(self, x):
        self._baseCord.set_x(x - self._offsetCord.get_x())
    
    def set_y(self, y):
        self._baseCord.set_y(y - self._offsetCord.get_y())
    
    def __repr__(self):
        return "RefCordinate(%s, %s, %s)" % (self._baseCord, self._offsetCord, self.Space)

    def __str__(self):
        return "RefCordinate(%s, %s, %s)" % (self._baseCord, self._offsetCord, self.Space)

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

    def Draw(self, xy_pos):
        pass

    def on_mouse_event(self, Event_Type, x, y, dx, dy, buttons, modifiers):
        print "Mouse event at %d %d (reported by %s)" % (x,y, self.GameObjectType)

    def __iter__(self):
        yield self

    def __contains__ (self, GameObject):
        return False
    
    def GetCordinatesInParentSpace(self):
        if self.parent_space is not None:
            return self.parent_space.GetCordinatesOfContainedObject(self)
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
                return RefCordinate(BaseCord, OffsetCord, self)

    def Update(self, delta_t):
        for GameObj in self.ContentObjects.keys():
            GameObj.Update(delta_t)

    def on_mouse_event(self, Event_Type, x, y, dx, dy, buttons, modifiers):
        print "Mouse event at %d,%d (reported by %s)" % (x,y, self.GameObjectType)
        for GameObj, Cord in self.ContentObjects.items():
            Obj_x_low = Cord.get_x()
            Obj_x_high = GameObj.width + Obj_x_low
            
            Obj_y_low = Cord.get_y()
            Obj_y_high = GameObj.height + Obj_y_low
            
            if (( Obj_x_low < x < Obj_x_high ) and
                ( Obj_y_low < y < Obj_y_high)):
                GameObj.on_mouse_event(
                    Event_Type,
                    x - Obj_x_low,
                    y - Obj_y_low,
                    dx, dy,
                    buttons,
                    modifiers)
            

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
