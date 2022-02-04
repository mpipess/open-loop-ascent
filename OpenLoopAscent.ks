
//Sim parameters and data
set g to 9.8. //gravitational acceleration (m/s^2)
set t to 0. //time (sec)
set velTheta to 90. //angle of velocity vector from horizontal (degrees)
set vertVelocity to 0. //vertical velocity summed from vertical acceleration (m)
set horizVelocity to 0. //horizontal velocity summed from horizontal acceleration (m)
set myAltitude to 0. //altitude summed from vertVelocity (m)
set frequency to 20. //number of measurements per second (Hz)

//Rocket data
set wetMass to 9665. //mass with fuel load (kg)
set dryMass to 3072. //mass without fuel load (kg)
set burnTime to 142. //burn duration (sec)
set vacThrust to 123600. //thrust produced in a vacuum (N)
set slThrust to 112900. //thrust produced at 1 atm (N)
set burnRate to (dryMass - wetMass) / burnTime. //fuel burn rate (kg/s)
set pitchAlt to 20. //Altitude of pitchover (m)
set pitchAngle to 89.989. //Angle of pitchover (degrees)

//Returns atmospheric pressure (Pa) at altitude
declare function pressure {
    if (myAltitude < 44330) {
        return 101325 * (1 - (2.25577 * 10^(-5)) * myAltitude)^5.25588.
    }
    else {
        return 0.
    }
}

//Returns thrust (N) at pressure
declare function thrust {
    return vacThrust - (vacThrust - slThrust) * (pressure() / 101325).
}

//Returns mass (kg) at time t
declare function myMass {
    return wetMass + burnRate * t.
}

//Returns vertical acceleration (m/s^2)
declare function av {
    return thrust() / myMass() * sin(velTheta) - g.
}

//Returns horizontal acceleration (m/s^2)
declare function ah {
    return thrust() / myMass() * cos(velTheta).
}

//sum vertical acceleration for velocity (m/s)
declare function sumVertAcc {
    set vertVelocity to vertVelocity + (av() / frequency).
}

//sum horizontal acceleration for velocity (m/s)
declare function sumHorizAcc {
    set horizVelocity to horizVelocity + (ah() / frequency).
}

//arctangent sums for angle of velocity vector from horizontal (degrees)
declare function update {
    sumVertAcc().
    sumHorizAcc().
    set myAltitude to myAltitude + (vertVelocity / frequency).
    set velTheta to arctan(vertVelocity / horizVelocity).
}

//Flight Section
clearscreen.
set attitude to 90.
lock steering to heading(90, attitude).
lock throttle to 1.0.
set count to 5.
until (count = 0) {
    print count + "...".
    set count to count - 1.
    wait 1.
}
stage.
print("Ignition").
wait 3.
stage.
print("Liftoff").

set liftoffTime to Time:seconds.
lock currentTime to Time:seconds - liftoffTime.
//simulates ascent for burn time length
until (myAltitude > pitchAlt) {
    update().
    print("Pitch: " + velTheta) at (0, 9).
    print("T+ " + t) at (0, 10).
    set attitude to velTheta.
    set t to t + (1 / frequency).
    wait until currentTime > t.
}

set velTheta to pitchAngle.
print("Pitchover " + vertVelocity).

until (t > burnTime) {
    update().
    print("Pitch: " + velTheta) at (0, 9).
    print("T+ " + t) at (0, 10).
    set attitude to velTheta.
    set t to t + (1 / frequency).
    wait until currentTime > t.
}

//calculate altitude at burnout -- sum vertical acceleration (m)
print("Altitude at cutoff: " + myAltitude).
print("% variation: " + (altitude - myAltitude) / myAltitude * 100).

//apogee calculator
//alt to apogee: vf=0, a=g, vi=sumVertAcc vf^2=vi^2+2ady dy=-vi^2/2a
//total alt of apogee: dy+altitude
set myApogee to (vertVelocity^2) / (2 * g) + myAltitude.
print("Apogee altitude: " + myApogee).
print("% variation: " + (Orbit:apoapsis - myApogee) / myApogee * 100).