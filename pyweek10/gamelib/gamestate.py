import math
from pyglet.window import key
from constants import *

TWOPI = (2*math.pi)


##Ship Movement Characteristics

# The maximum amplitude of the ship's path, 1 being the top of the screen
MAX_AMPLITUDE = 1
# the minimum amplitude of the ships path, 0 being perfectly horizontal
MIN_AMPLITUDE = 0
# how far the ship can move per tick
MAX_AMPLITUDE_VELOCITY = 0.1
# calculates the amp movement of the ship
AMPLITUDE_ACCEL_FUNC = lambda t, accel: min(MAX_AMPLITUDE_VELOCITY * t + accel, MAX_AMPLITUDE_VELOCITY)

MAX_FREQUENCY = 3*math.pi
MIN_FREQUENCY = .5*math.pi
MAX_FREQUENCY_VELOCITY = .5*math.pi
FREQUENCY_ACCEL_FUNC = lambda t, accel: min(MAX_FREQUENCY_VELOCITY * t + accel, MAX_FREQUENCY_VELOCITY)

def SinusoidToCartesian(A, omega, t , phi):
    """
        A = Amplitude
        omega = angular frequency, (1/omega gives period)
        phi = phase
    """
    y = A * math.sin(omega * t + phi)
    x = A * math.cos(omega * t + phi)
    return (x,y)

class Entity:
    def __init__(self, parent_level, entity_flag = ENTITY_STATIC):
        self.parent_level = parent_level
        
        self._WindowHeight = None
        self._WindowWidth = None        
        
        self.SetWindowHeight(self.parent_level.get_height())
        self.SetWindowWidth(self.parent_level.get_width())
        
        self.parent_level.register_entity(self, entity_flag)
        
    def __del__(self):
        self.parent_level.remove_entity(self)
        
    def SetWindowHeight(self, window_height):
        assert(window_height != 0)
        self._WindowHeight = window_height

    def SetWindowWidth(self, window_width):
        assert(window_width != 0)
        self._WindowWidth = window_width
        
    def draw(self):
        pass

class Actor(Entity):
    def __init__(self, parent_level, entity_flag = ENTITY_ACTOR):
        Entity.__init__(self, parent_level, entity_flag)
        
    def draw(self):
        Entity.draw(self)
        
    def Tick(self, delta_t):
        pass
    
class Reactor(Entity):
    def __init__(self, parent_level, entity_flag = ENTITY_REACTOR):
        Entity.__init__(self, parent_level, entity_flag)
        
    def draw(self):
        Entity.draw(self)
    
    def Tick(self, delta_t, KeyState):
        pass

class Oscillator:
    def __init__(self):

        self._Amplitude = .5
        self._Omega = math.pi
        self._Phase = 0.0
        self._t = 0.0

        self.AmplitudeVelocity = 0
        self.FrequencyVelocity = 0

    def Tick(self, delta_t, KeyState):
        """
        Simulate the passage of time on the ships sinusodial position.

        We mod t by 2pi/omega to keep it small. Anytime we
        would adjust the angularFrequency we end up zeroing t anyway.

        One more step along the inevitable march of time
        One more step closer to the heat-death of the universe
        """
        if(not KeyState[key.SPACE]):
            self._t = (self._t + delta_t) % (TWOPI/self._Omega)

        if KeyState[key.UP] and not KeyState[key.DOWN]:
            self.AmplitudeVelocity = AMPLITUDE_ACCEL_FUNC(delta_t, self.AmplitudeVelocity)
            self.AdjustAmplitude(self.AmplitudeVelocity)
        elif KeyState[key.DOWN] and not KeyState[key.UP]:
            self.AmplitudeVelocity = -AMPLITUDE_ACCEL_FUNC(delta_t, abs(self.AmplitudeVelocity))
            self.AdjustAmplitude(self.AmplitudeVelocity)
        else:
            self.AmplitudeVelocity = 0


        if KeyState[key.RIGHT] and not KeyState[key.LEFT]:
            self.FrequencyVelocity = FREQUENCY_ACCEL_FUNC(delta_t, self.FrequencyVelocity)
            self.AdjustAngularFrequency(self.FrequencyVelocity)
        elif KeyState[key.LEFT] and not KeyState[key.RIGHT]:
            self.FrequencyVelocity = -FREQUENCY_ACCEL_FUNC(delta_t, abs(self.FrequencyVelocity))
            self.AdjustAngularFrequency(self.FrequencyVelocity)
        else:
            self.FrequencyVelocity = 0


    def AdjustAmplitude(self, deltaAmp):
        """
        Adjust the Amplitude of the ships waveform while maintaining its current position.

        Unfortunately this is a nasty operation. We need to compute a new Phase/Time such
        that the ships new position within the waveform with the higher amplitude matches
        its current position. This means inverse trig (arcSin in particular).

        The formula is pretty strait forward though:

        given: Theta = Omega * t + Phi

        A1 * Sin(Theta1) = A2 * Sin(Theta2)

        becomes

        Theta2 = ArcSin((A1 * Sin(Theta1))/A2)

        Of course, we have a problem here, there are actually TWO solutions to this equation
        one for the ascending edge, and one for the falling edge (there is only one solution
        at the peaks and valleys of course).

        Once we have Theta2, we can set time to 0 and calculate a new phase offset, modding
        the phase by TWOPI to keep it small.

        I know I don't need all these intermediate variables, but for readability and
        ease of development I'll leave them this way for now.

        NOTE: Since we check that the current position is farther from 0 than the new
        amplitude we can avoid those nasty situations where ArcSin does not exist.

        """

        currentPos = self.GetPosition()
        oldTheta = (self._Omega * self._t + self._Phase) % (2 * math.pi)

        newAmp = self._Amplitude + deltaAmp
        if (abs(currentPos) > newAmp):
            if(currentPos > 0):
                currentPos = newAmp
            else:
                currentPos = -newAmp

        if (newAmp > MAX_AMPLITUDE) or (newAmp < MIN_AMPLITUDE):
            self.AmplitudeVelocity = 0
            return

        # lim (x -> inf) asin(x) = 0
        if (newAmp != 0):
            newPhase = math.asin(currentPos/newAmp)
        else:
            newPhase = 0

        # asin returns values between -pi/2 and pi/2, we use values between 0 and 2*pi
        if (newPhase < 0):
            newPhase += (2*math.pi)

        # asin has multiple solutions everywhere that isn't a peak or a trough
        # by default, asin always returns the solution between -pi/2 and pi/2
        # (quadrants 0 and 3), to maintain continuity we want to use the solutions
        # from pi/2 to 3pi/2 (quadrants 1 and 2) if that was where the original
        # position was located
        if ( (math.pi/2) < oldTheta <= (math.pi) ):
            #Adjust the new phase to be in quadrant 1
            newPhase = math.pi - newPhase
        elif ( (math.pi) < oldTheta <= ((math.pi*3)/2) ):
            #Adjust the new phase to be in quadrant 2
            newPhase = math.pi + (2*math.pi - newPhase)

        newt = 0.0

        self._Amplitude, self._Phase, self._t = newAmp, newPhase, newt


    def AdjustAngularFrequency(self, deltaFreq):
        """
        Adjust the angular frequency of the ships waveform while maintaining its current position.

        While adjusting the Angular Frequency we need to adjust the Time t) and phase such
        that:

        Omega1 * t1 = Phi1 = Omega2 * t2 = Phi2

        To make this easy, we just reset time to 0 and calculate the new phase offset.

        t2 = 0
        Phi2 = Omega1 * t1 = Phi1

        Finally, we mod Phi2 by TWOPI to keep it small.

        I know I don't need all these intermediate variables, but for readbility and
        ease of development I'll leave them this way for now.
        """
        oldFreq, oldPhase, oldt = self._Omega, self._Phase, self._t

        newFreq = oldFreq + deltaFreq

        if (newFreq > MAX_FREQUENCY) or (newFreq < MIN_FREQUENCY):
            self.FrequencyVelocity = 0
            return

        newPhase = (oldFreq * oldt + oldPhase) % TWOPI
        newt = 0.0

        self._Omega, self._Phase, self._t = newFreq, newPhase, newt


    def AdjustPhase(self, deltaPhase):
        """
        Adjust the phase of the ships waveform. By definition this operation SHOULD alter the ships position.

        I actually don't know if we will need this
        """
        self._Phase += deltaPhase % TWOPI

    def GetPosition(self):
        return self.GetFuturePosition(0)

    def GetFuturePosition(self, t_future):
        return self._Amplitude * math.sin(self.GetFutureTheta(t_future))

    def GetTheta(self):
        return self.GetFutureTheta(0)

    def GetFutureTheta(self, t_future):
        return ((self._Omega * (self._t + t_future)) + self._Phase)
    
    def GetAngle(self):
        return self.GetFutureAngle(0)

    def GetFutureAngle(self, t_future):
        return self._Amplitude * math.cos(self.GetFutureTheta(t_future)) * 90.0

    def GetPredictiveCoordinate(self, t_future):
        return (t_future, self.GetFuturePosition(t_future), self.GetFutureAngle(t_future))

    def GetPredictivePath(self, t_start, t_stop, t_step):

        assert(t_start < t_stop)
        assert(t_step > 0)
        path = []
        t_cursor = t_start

        while(t_cursor < t_stop):
            path.append(self.GetPredictiveCoordinate(t_cursor))
            t_cursor += t_step
        return path
