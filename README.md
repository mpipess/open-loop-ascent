# open-loop-ascent

  This simulator is meant to aid in finding the correct angle to which to pitch over during a rocket's first stage ascent.
  The user inputs rocket data, then runs the sim with parameters of pitchover altitude (representing clearance of pad structures) and a target apogee, from which the program can brute-force a pitchover angle through repeated simulation.
  The simulation steps time forward at a user-set interval, getting acceleration from mass and thrust, velocity from summation of accelerations, pitch attitude from the ratio of vertical and horizontal velocities, and altitude from summation of vertical velocity.
  Apogee calculation is via basic kinematics.
  I may add further functionality (ex. drag calcs) as I learn those.
