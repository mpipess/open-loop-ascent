#This simulator is meant to aid in finding the correct angle to which to pitch over
#during a rocket's first stage ascent.
#The user inputs rocket data, then runs the sim with parameters of pitchover altitude
#(representing clearance of pad structures) and a target apogee, from which the program
#can brute-force a pitchover angle through repeated simulation.
#The simulation steps time forward at a user-set erval, getting acceleration from
#mass and thrust, velocity from summation of accelerations, pitch attitude from the ratio
#of vertical and horizontal velocities, and altitude from summation of vertical velocity.
#Apogee calculation is via basic kinematics.

import math

class Rocket:

    def __init__(self, freq, wetMass, dryMass, thrustSL, thrustVac, burnTime):
        self.freq = freq #Sim updates per second (Hz)
        self.wetMass = wetMass #Mass with propellant (kg)
        self.dryMass = dryMass #Mass without propellant (kg)
        self.thrustSL = thrustSL #Thrust at 1 atm (N)
        self.thrustVac = thrustVac #Thrust in a vacuum (N)
        self.burnTime = burnTime #Length of burn (s)
        self.burnRate = (dryMass - wetMass) / burnTime #Rate of propellant consumption (kg/s)
        self.g = -9.8 #Gravitational acceleration (m/s^2)
        self.t = 0.0 #Sim time (s)
        self.velTheta = math.pi / 2 #Angle of velocity vector relative to horizon (radians)
        self.vertVel = 0 #Vertical velocity (m/s)
        self.horizVel = 0 #Horizontal velocity (m/s)
        self.altitude = 0 #Altitude above starting position (m)


    #Returns atmospheric pressure (Pa) at given altitude
    def atmPres(self):
        if (self.altitude < 44330):
            return 101325 * (1 - (2.25577 / 100000) * self.altitude)**5.25588
        else:
            return 0

    #Returns thrust (N) produced at given pressure
    def thrust(self):
        return self.thrustVac + (self.thrustSL - self.thrustVac) * (self.atmPres() / 101325)

    #Returns mass (kg) of vehicle at given time
    def mass(self):
        m = self.wetMass + self.burnRate * self.t
        if (m > self.dryMass):
            return self.wetMass + self.burnRate * self.t
        else:
            return self.dryMass

    #Returns vertical acceleration (m/s^2)
    def av(self):
        return (self.thrust() / self.mass()) * math.sin(self.velTheta) + self.g

    #Returns horizontal acceleration (m/s^2)
    def ah(self):
        return (self.thrust() / self.mass()) * math.cos(self.velTheta)

    #Sums vertical acceleration for vertical velocity (m/s)
    def sumVertAcc(self): 
        self.vertVel += self.av() / self.freq

    #Sums horizontal acceleration for horizontal velocity (m/s)
    def sumHorizAcc(self):
        self.horizVel += self.ah() / self.freq

    #Arctans velocity components for new velTheta (radians)
    def update(self):
        self.sumVertAcc()
        self.sumHorizAcc()
        self.altitude += self.vertVel / self.freq
        self.velTheta = math.atan(self.vertVel / self.horizVel)

    #Simulates ascent before and after pitchover
    def simulateAscent(self, pitchAlt, pitchAngle):
        while (self.altitude < pitchAlt):
            self.update()
            if (self.altitude < 0):
                #print("Hit ground at t+ " + str(self.t))
                break
            self.t += 1 / self.freq
        self.velTheta = pitchAngle
        while (self.t <= self.burnTime):
            self.update()
            if (self.altitude < 0):
                #print("Hit ground at t+ " + str(self.t))
                break
            self.t += 1 / self.freq

    #Returns apogee (m)
    def getApogee(self):
        return -1 * (self.vertVel**2) / (2 * self.g) + self.altitude

    #Sets all properties to defaults
    def setToDefault(self):
        self.t = 0.0
        self.velTheta = math.pi / 2
        self.vertVel = 0
        self.horizVel = 0
        self.altitude = 0

    #Returns pitchover angle (degrees) at input altitude (m) that results in input apogee (m)
    def findPitchAngle(self, targetAp, pitchAlt):
        print("Wait several eternities...")
        a = 0
        b = math.pi * a / 180
        while (self.getApogee() < targetAp and a < 90):
            self.setToDefault()
            self.simulateAscent(pitchAlt, b)
            a += 0.001
            b = math.pi * a / 180
        print("Apogee: " + str(self.getApogee()))
        print("Cutoff Altitude: " + str(self.altitude))
        return round(a, 3)

rox = Rocket(20, 9665, 3072, 112900, 123600, 142)
print(rox.findPitchAngle(100000, 20))
rs112 = Rocket(20, 5272, 1133, 88400, 98500, 95)
#print(rs112.findPitchAngle(150000, 20))