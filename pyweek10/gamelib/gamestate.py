import math
from pyglet.window import key


TWOPI = 2*math.pi


##Ship Movement Characteristics
MAX_AMPLITUDE = .9
MIN_AMPLITUDE = .1
MAX_AMPLITUDE_VELOCITY = 0.2
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
            self._t = (self._t + delta_t) % (TWOPI/self._AngularFrequency)
        
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
        
        I know I don't need all these intermediate variables, but for readbility and 
        ease of development I'll leave them this way for now.  
                
        NOTE: Since we check that the current position is farther from 0 than the new
        amplitude we can avoid those nasty situations where ArcSin does not exist.
            
        """
        currentPos = self.GetPosition()
        
        newAmp = self._Amplitude + deltaAmp
        if ((currentPos) > newAmp):
            print("DEBUG: Attempted to reduce amplitude below current ship position!")
            return
        
        if (newAmp > MAX_AMPLITUDE) or (newAmp < MIN_AMPLITUDE):
            return
        
        print( "DEBUG: NewAmplitude: %f" % newAmp)               
        newPhase = math.asin(currentPos/newAmp)
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
            return

        newPhase = (oldFreq * oldt + oldPhase) % TWOPI
        newt = 0.0
        
        print( "DEBUG NewVelocity: %f * pi" % (newFreq/math.pi))
        
        self._AngularFrequency, self._Phase, self._t = newFreq, newPhase, newt

    
    def AdjustPhase(self, deltaPhase):
        """
        Adjust the phase of the ships waveform. By definition this operation SHOULD alter the ships position.
        
        I actually dont know if we will need this
        """
        self._Phase += deltaPhase % TWOPI
            
    def GetPosition(self):
        return self._Amplitude * math.sin(self._Omega * self._t + self._Phase)
