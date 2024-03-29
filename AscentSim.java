public class AscentSim {

   public static void main(String[] args) {
      
      Rocket rox = new Rocket(20, 9665, 3072, 112900, 123600, 142);
      System.out.println(rox.findPitchAngleBinary(100000, 20));
      //Rocket rs112 = new Rocket(20, 5272, 1133, 88400, 98500, 95);
      //System.out.println("Pitchover Angle: " + rs112.findPitchAngle(150000, 20));
      
   }
   
}

class Rocket {

   private double g = -9.8; //Gravitational acceleration (m/s^2)
   private double t = 0.0; //Sim time (s)
   private double velTheta = Math.PI / 2; //Angle of velocity vector relative to horizon (radians)
   private double vertVel = 0; //Vertical velocity (m/s)
   private double horizVel = 0; //Horizontal velocity (m/s)
   private double altitude = 0; //Altitude above starting point (m)
   private int freq; //Sim updates per second (Hz)
   
   private int wetMass; //Mass with propellant (kg)
   private int dryMass; //Mass without propellant (kg)
   private int thrustSL; //Thrust at 1 atm (N)
   private int thrustVac; //Thrust in a vacuum (N)
   private int burnTime; //Length of burn (s)
   private double burnRate; //Rate of propellant consumption (kg/s)
   
   public Rocket(int f, int m0, int m1, int ts, int tv, int bt) {
      freq = f;
      wetMass = m0;
      dryMass = m1;
      thrustSL = ts;
      thrustVac = tv;
      burnTime = bt;
      burnRate = (double) (m1 - m0) / bt;
   }
   
   //Returns atmospheric pressure (atm) at given altitude
   private double atmPres() {
      if (altitude < 44330)
         return Math.pow(1 - (2.25577 / 100000) * altitude, 5.25588);
      else
         return 0.0;
   }
   
   //Returns thrust (N) produced at given pressure
   private double thrust() {
      return thrustVac + (thrustSL - thrustVac) * (atmPres());
   }
   
   //Returns mass (kg) of vehicle at given time
   private double mass() {
      double m = wetMass + burnRate * t;
      if (m > dryMass) {
         return m;
      }
      else {
         return dryMass;
      }
   }
   
   //Returns vertical acceleration (m/s^2)
   private double av() {
      return (thrust() / mass()) * Math.sin(velTheta) + g;
   }
   
   //Returns horizontal acceleration (m/s^2)
   private double ah() {
      return (thrust() / mass()) * Math.cos(velTheta);
   }
   
   //Sums vertical acceleration for vertical velocity (m/s)
   private void sumVertAcc() {
      vertVel += av() / freq;
   }
   
   //Sums horizontal acceleration for horizontal velocity (m/s)
   private void sumHorizAcc() {
      horizVel += ah() / freq;
   }
   
   //Arctans velocity components for new velTheta (radians)
   private void update() {
      sumVertAcc();
      sumHorizAcc();
      altitude += vertVel / freq;
      velTheta = Math.atan(vertVel / horizVel);
   }
   
   //Simulates ascent before and after pitchover
   public void simulateAscent(int pitchAlt, double pitchAngle) {
      boolean didHitGround = false;
      while (altitude < pitchAlt && didHitGround == false) {
         update();
         if (altitude < 0) {
            //System.out.println("Hit ground at t+ " + t);
            didHitGround = true;
         }
         t += (double) 1 / freq;
      }
      velTheta = pitchAngle;
      while (t <= burnTime && didHitGround == false) {
         update();
         if (altitude < 0) {
            //System.out.println("Hit ground at t+ " + t);
            didHitGround = true;
         }
         t += (double) 1 / freq;
      }
   }
   
   //Returns apogee (m)
   public double getApogee() {
      return -1 * (vertVel * vertVel) / (2 * g) + altitude;
   }
   
   //Sets all properties to defaults
   private void setToDefault() {
      t = 0.0;
      velTheta = Math.PI / 2;
      vertVel = 0;
      horizVel = 0;
      altitude = 0;
   }
   
   //Returns pitchover angle (degrees) at input altitude (m) that results in input apogee (m)
   public double findPitchAngle(int targetAp, int pitchAlt) {
      System.out.println("Wait a few moments...");
      double a = 0.0;
      double b = Math.PI * a / 180;
      while (this.getApogee() < targetAp && a < 90) {
         setToDefault();
         this.simulateAscent(pitchAlt, b);
         a += 0.001;
         b = Math.PI * a / 180;
      }
      System.out.println("Apogee: " + this.getApogee());
      System.out.println("Cutoff Altitude: " + altitude);
      return (double) Math.round(a * 1000) / 1000;
   }

   //Returns pitchover angle (degrees) at input altitude (m) that results in input apogee (m)
   public double findPitchAngleBinary(int targetAp, int pitchAlt) {
      double high = Math.PI / 2.0;
      double low = 0.0;
      double a = 0.0;
      boolean converged = false;
      while (!converged) {
         setToDefault();
         this.simulateAscent(pitchAlt, a);
         if (this.getApogee() < targetAp - 0.1) {
            low = a;
            a = (high + low) / 2.0;
        } else if (this.getApogee() > targetAp + 0.1) {
            high = a;
            a = (high + low) / 2.0;
        } else {
            converged = true;
        }
      }
      System.out.println("Apogee: " + this.getApogee());
      System.out.println("Cutoff Altitude: " + altitude);
      return 90 - a * Math.PI / 180.0;
   }
   
}