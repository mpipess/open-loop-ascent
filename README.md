# open-loop-ascent
Made to work with Kerbal Space Program and its kOS mod.

This simulator is meant to aid in finding the correct angle to which to pitch over during a rocket's first stage ascent.

The user inputs rocket data, then runs the sim with parameters of pitchover altitude (representing clearance of pad structures) and a target apogee, from which the program can brute-force a pitchover angle through repeated simulation.

The simulation steps time forward at a user-set interval, getting acceleration from mass and thrust, velocity from summation of accelerations, pitch attitude from the ratio of vertical and horizontal velocities, and altitude from summation of vertical velocity.

Apogee calculation is via basic kinematics.

I may add further functionality (ex. drag calcs) as I learn the physics.

Instructions:
1. Instantiate your rocket as a Rocket object with the correct parameters.
2. Run the findPitchAngle method with your target apogee (meters) and pitchover altitude (meters).
3. Transfer the pitchover angle (final number output) (degrees) to the Kerboscript file.
4. Copy the Kerboscript file to the correct place in your KSP installation -- likely Ships/script.
