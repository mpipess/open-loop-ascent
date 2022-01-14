import math

#Sim parameters and data
g = 9.8 #gravitational acceleration (m/s^2)
t = 0 #time (sec)
velTheta = math.pi / 2 #angle of velocity vector from horizontal (radians)
vertVelocity = 0 #vertical velocity summed from vertical acceleration (m)
horizVelocity = 0 #horizontal velocity summed from horizontal acceleration (m)
altitude = 0 #altitude summed from vertVelocity (m)
frequency = 5 #number of measurements per second (Hz)

#Rocket data
wetMass = 9714 #mass with fuel load (kg)
dryMass = 3122 #mass without fuel load (kg)
burnTime = 142 #burn duration (sec)
vacThrust = 123600 #thrust produced in a vacuum (N)
slThrust = 112900 #thrust produced at sea level (N)
burnRate = (dryMass - wetMass) / burnTime #fuel burn rate (kg/s)

#atmospheric pressure at altitude (Pa)
def pressure():
    if (altitude < 44330):
        return 101325*(1-(2.25577*10**-5)*altitude)**5.25588
    else:
        return 0

#thrust at atmospheric pressure (N)
def thrust():
    return vacThrust-(vacThrust-slThrust)*(pressure()/101325)

#mass at given time t (kg)
def mass():
    return wetMass + burnRate * t

#total acceleration prior to gravity loss at given time t (m/s^2)
def a0():
    return thrust() / mass()

#vertical component of acceleration including gravity loss at given time t (m/s^2)
def av():
    return a0() * math.sin(velTheta) - g

#horizontal component of velocity at given time t (m/s^2)
def ah():
    return a0() * math.cos(velTheta)

#sum vertical acceleration for velocity at given time t (m/s)
def sumVertAcc():
    global vertVelocity
    vertVelocity += (av() / frequency)
    return vertVelocity

#sum horizontal acceleration for velocity at given time t (m/s)
def sumHorizAcc():
    global horizVelocity
    horizVelocity += (ah() / frequency)
    return horizVelocity

#arctangent sums for angle of velocity vector from horizontal (degrees)
def velTheta1():
    return math.atan(sumVertAcc() / sumHorizAcc())

simOutput = ""
#simulates ascent for burn time length
while t < 9:
    velTheta = velTheta1()
    print(velTheta * (180/math.pi))
    altitude += (vertVelocity / frequency)
    t += 1 / frequency
    
    simOutput += str(velTheta * (180/math.pi)) + ", "

velTheta = (8985 * math.pi)/18000
print("Pitchover " + str(vertVelocity))

while t < burnTime + 1:
    velTheta = velTheta1()
    print(velTheta * (180/math.pi))
    altitude += (vertVelocity / frequency)
    t += 1 / frequency
    
    simOutput += str(velTheta * (180/math.pi)) + ", "

#calculate altitude at burnout -- sum vertical acceleration (m)
print("Altitude at cutoff: " + str(altitude))

#apogee calculator
#alt to apogee: vf=0, a=g, vi=sumVertAcc vf^2=vi^2+2ady dy=-vi^2/2a
#total alt of apogee: dy+altitude
print("Vertical speed at cutoff: " + str(vertVelocity))
print("Total speed at cutoff: " + str(vertVelocity/math.sin(velTheta)))
print("Alt to apogee: " + str((vertVelocity**2)/(2*g)))
print("Apogee altitude: " + str(((vertVelocity**2)/(2*g) + altitude)))

print(simOutput)