//Mathematical constants
var radToDeg = 180 / Math.PI; //constant to convert radians to degrees
var degToRad = Math.PI / 180; //constant to convert degrees to radians
var g = 9.8; //gravitational acceleration (m/s^2)

//Rocket data
var wetMass = 9714; //mass with fuel load (kg)
var dryMass = 3122; //mass without fuel load (kg)
var burnTime = 142; //burn duration (sec)
var thrust = 113000; //thrust (N)
var burnRate = (wetMass - dryMass) / burnTime; //fuel burn rate (kg/s)

//Sim parameters and data
var t = 0; //time (sec)
var velTheta = 90; //angle of velocity vector from horizontal (degrees)
var vertSigma = 0; //vertical velocity summed from vertical acceleration (m)
var horizSigma = 0; //horizontal velocity summed from horizontal acceleration (m)
var altSigma = 0; //altitude summed from vertSigma (m)
var frequency = 1; //number of measurements per second (Hz)

//mass at given time t
function mass(t) {
    return wetMass - burnRate * t;
}

//total acceleration prior to gravity loss at given time t
function a0(t) {
    return thrust / mass(t);
}

//vertical component of acceleration including gravity loss at given time t
function av(t) {
    return (a0(t) * (Math.sin(velTheta * degToRad))) - g;
}

//horizontal component of velocity at given time t
function ah(t) {
    return (a0(t) * (Math.cos(velTheta * degToRad)));
}

//sum vertical acceleration for velocity at given time t
function sumVertAcc(t) {
    vertSigma += (av(t) / frequency);
    return vertSigma;
}

//sum horizontal acceleration for velocity at given time t
function sumHorizAcc(t) {
    horizSigma += (ah(t) / frequency);
    return horizSigma;
}

//arctangent sums for angle of velocity vector from horizontal
function velTheta1(t) {
    return Math.atan(sumVertAcc(t) / sumHorizAcc(t)) * radToDeg;
}

var simOutput = "";
//simulates ascent for burn time length
while (t < 11) {
    velTheta = velTheta1(t);
    console.log(velTheta);
    altSigma += (vertSigma / frequency);
    t += 1 / frequency;

    simOutput += velTheta.toString() + ", "
}
velTheta = 89.9;
console.log("Pitchover " + vertSigma);
while (t < 143) {
    velTheta = velTheta1(t);
    console.log(velTheta);
    altSigma += (vertSigma / frequency);
    t += 1 / frequency;

    simOutput += velTheta.toString() + ", "
}

//calculate altitude at burnout -- sum vertical acceleration
console.log("Altitude at cutoff: " + altSigma)

//apogee calculator
//alt to apogee: vf=0, a=g, vi=sumVertAcc; vf^2=vi^2+2ady; dy=-vi^2/2a
//total alt of apogee: dy+altitude
console.log("Vertical speed at cutoff: " + vertSigma);
console.log("Alt to apogee: " + (vertSigma**2)/(2*g));
console.log("Apogee altitude: " + ((vertSigma**2)/(2*g) + altSigma));

const fs = require ("fs");
fs.writeFile("simOutput.txt", simOutput, (err) => {
    if (err) throw err;
});