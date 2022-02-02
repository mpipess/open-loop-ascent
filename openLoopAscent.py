import math

class Rocket:

    def __init__(self, f, m0, m1, tv, ts, bt):
        self.frequency = 20 #update frequency (Hz)
        self.wetMass = m0 #mass with prop load (kg)
        self.dryMass = m1 #mass without prop load (kg)
        self.burnTime = bt #burn duration (s)
        self.thrustVac = tv #thrust in a vacuum (N)
        self.thrustSL = ts #thrust at 1 atm (N)
        self.burnRate = (m1 - m0) / bt
        self.g = -9.8 #gravitational acceleration (m/s^2)
        self.t = 0 #time (sec)
        self.velTheta = math.pi / 2 #angle of velocity vector from horizontal (radians)
        self.vertVel = 0 #vertical velocity summed from vertical acceleration (m)
        self.horizVel = 0 #horizontal velocity summed from horizontal acceleration (m)
        self.altitude = 0 #altitude summed from self.vertVel (m)

    #Returns atmospheric pressure (Pa) at altitude
    def pressure(self):
        if (self.altitude < 44330):
            return 101325*(1-(2.25577*10**-5)*self.altitude)**5.25588
        else:
            return 0

    #thrust at atmospheric pressure (N)
    def thrust(self):
        return self.thrustVac-(self.thrustVac-self.thrustSL)*(self.pressure()/101325)

    #mass at given time t (kg)
    def mass(self):
        return self.wetMass + self.burnRate * self.t

    #total acceleration prior to gravity loss at given time t (m/s^2)
    def a0(self):
        return self.thrust() / self.mass()

    #vertical component of acceleration including gravity loss at given time t (m/s^2)
    def av(self):
        return self.a0() * math.sin(self.velTheta) + self.g

    #horizontal component of velocity at given time t (m/s^2)
    def ah(self):
        return self.a0() * math.cos(self.velTheta)

    #sum vertical acceleration for velocity at given time t (m/s)
    def sumVertAcc(self):
        self.vertVel += (self.av() / self.frequency)
        return self.vertVel

    #sum horizontal acceleration for velocity at given time t (m/s)
    def sumHorizAcc(self):
        self.horizVel += (self.ah() / self.frequency)

    #arctangent sums for angle of velocity vector from horizontal (degrees)
    def update(self):
        self.sumVertAcc()
        self.sumHorizAcc()
        self.altitude += (self.vertVel / self.frequency)
        self.velTheta = math.atan(self.horizVel / self.vertVel)

    def simulateAscent(self, pitchAlt, pitchAngle):
        #simulates ascent for burn time length
        hitGround = False
        while self.altitude < pitchAlt and hitGround is False:
            self.update()
            if (self.altitude < 0) :
                print("Hit ground at T+ " + str(self.t))
                hitGround = True
            self.t += 1 / self.frequency

        velTheta = (pitchAngle * math.pi) / 18000
        print("Pitchover " + str(self.vertVel))

        while self.t < self.burnTime + 1 and hitGround is False:
            self.update()
            if (self.altitude < 0) :
                print("Hit ground at T+ " + str(self.t))
                hitGround = True
            self.t += 1 / self.frequency

    def getApogee(self):
        return -1 * (self.vertVel ** 2) / (2 * self.g) + self.altitude

demo = Rocket(20, 9665, 3072, 123600, 112900, 150)
demo.simulateAscent(20, 100000)
print("Apogee: " + str(demo.getApogee()))