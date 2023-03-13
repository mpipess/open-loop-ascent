
const VERT_ANGLE: f64 = std::f64::consts::PI / 2.0;
pub struct Rocket {
    g: f64, //Gravitational acceleration (m/s^2)
    t: f64, //Sim time (s)
    vel_theta: f64, //Angle of velocity vector relative to horizon (radians)
    vert_vel: f64, //Vertical velocity (m/s)
    horiz_vel: f64, //Horizontal velocity (m/s)
    altitude: f64, //Altitude above starting point (m)

    freq: i32, //Sim updates per second (Hz)
    wet_mass: f64, //Mass with propellant (kg)
    dry_mass: f64, //Mass without propellant (kg)
    thrust_sl: f64, //Thrust at 1 atm (N)
    thrust_vac: f64, //Thrust in a vacuum (N)
    burn_time: f64, //Length of burn (s)
    burn_rate: f64, //Rate of propellant consumption (kg/s)
}

//Constructor for Rocket struct
pub fn build_rocket(freq: i32, wet_mass: f64, dry_mass: f64, thrust_sl: f64, thrust_vac: f64, burn_time: f64) -> Rocket {
    Rocket {
        g: -9.8,
        t: 0.0,
        vel_theta: std::f64::consts::PI / 2.0,
        vert_vel: 0.0,
        horiz_vel: 0.0,
        altitude: 0.0,

        freq,
        wet_mass,
        dry_mass,
        thrust_sl,
        thrust_vac,
        burn_time,
        burn_rate: (dry_mass - wet_mass) / burn_time,
    }
}

//Returns atmospheric pressure (atm) at given altitude
fn atm_pres(rkt: &Rocket) -> f64 {
    if rkt.altitude < 44330.0 {
        return (1.0 - (2.25577 / 100000.0) * rkt.altitude).powf(5.25588);
    } else {
        return 0.0;
    }
}

//Returns thrust (N) produced at given pressure
fn thrust(rkt: &Rocket) -> f64 {
    return rkt.thrust_vac + (rkt.thrust_sl - rkt.thrust_vac) * (atm_pres(rkt));
}

//Returns mass (kg) of vehicle at given time
fn mass(rkt: &Rocket) -> f64 {
    let m: f64 = rkt.wet_mass + rkt.burn_rate * rkt.t;
    if m > rkt.dry_mass {
        return m;
    }
    else {
        return rkt.dry_mass;
    }
}

//Returns vertical acceleration (m/s^2)
fn av(rkt: &Rocket) -> f64 {
    return (thrust(rkt) / mass(rkt)) * rkt.vel_theta.sin() + rkt.g;
}

//Returns horizontal acceleration (m/s^2)
fn ah(rkt: &Rocket) -> f64 {
    return (thrust(rkt) / mass(rkt)) * rkt.vel_theta.cos();
}

//Sums vertical acceleration for vertical velocity (m/s)
fn sum_vert_acc(rkt: &mut Rocket) {
    rkt.vert_vel += av(rkt) / rkt.freq as f64;
}

//Sums horizontal acceleration for horizontal velocity (m/s)
fn sum_horiz_acc(rkt: &mut Rocket) {
    rkt.horiz_vel += ah(rkt) / rkt.freq as f64;
}

//Arctans velocity components for new vel_theta (radians)
fn update(rkt: &mut Rocket) {
    sum_vert_acc(rkt);
    sum_horiz_acc(rkt);
    rkt.altitude += rkt.vert_vel / rkt.freq as f64;
    rkt.vel_theta = (rkt.vert_vel / rkt.horiz_vel).atan();
}

//Simulates ascent before and after pitchover
pub fn simulate_ascent(rkt: &mut Rocket, pitch_alt: f64, pitch_angle: f64) {
    let mut hit_ground: bool = false;
    while rkt.altitude < pitch_alt && hit_ground == false {
        update(rkt);
        if rkt.altitude < 0.0 {
        println!("Hit ground at t+ {}", rkt.t);
        hit_ground = true;
        }
        rkt.t += 1.0 / rkt.freq as f64;
    }
    rkt.vel_theta = pitch_angle;
    while rkt.t <= rkt.burn_time && hit_ground == false {
        update(rkt);
        if rkt.altitude < 0.0 {
            println!("Hit ground at t+ {}", rkt.t);
            hit_ground = true;
        }
        rkt.t += 1.0 / rkt.freq as f64;
    }
}

//Returns apogee (m)
pub fn get_apogee(rkt: &Rocket) -> f64 {
    return -1.0 * (rkt.vert_vel * rkt.vert_vel) / (2.0 * rkt.g) + rkt.altitude;
}

//Sets all properties to defaults
fn set_default(rkt: &mut Rocket) {
    rkt.t = 0.0;
    rkt.vel_theta = std::f64::consts::PI / 2.0;
    rkt.vert_vel = 0.0;
    rkt.horiz_vel = 0.0;
    rkt.altitude = 0.0;
}

//Returns pitchover angle (degrees) at input altitude (m) that results in input apogee (m)
pub fn find_pitch_angle(rkt: &mut Rocket, target_ap: f64, pitch_alt: f64) -> f64 {
    println!("Wait a few moments...");
    let mut a: f64 = 0.0;
    let mut b: f64 = std::f64::consts::PI * a / 180.0;
    while get_apogee(rkt) < target_ap && a < 90.0 {
        set_default(rkt);
        simulate_ascent(rkt, pitch_alt, b);
        a += 0.001;
        b = std::f64::consts::PI * a / 180.0;
    }
    println!("Apogee: {}", get_apogee(rkt));
    println!("Cutoff Altitude: {}", rkt.altitude);
    return a;
}

//Optimize with binary search
pub fn find_pitch_angle_binary(rkt: &mut Rocket, target_ap: f64, pitch_alt: f64) -> f64 {
    let mut high: f64 = VERT_ANGLE;
    let mut low: f64 = 0.0;
    let mut a: f64 = 0.0;
    let mut converged: bool = false;
    while !converged {
        set_default(rkt);
        simulate_ascent(rkt, pitch_alt, a);
        if get_apogee(rkt) < target_ap - 0.1 {
            low = a;
            a = (high + low) / 2.0;
        } else if get_apogee(rkt) > target_ap + 0.1 {
            high = a;
            a = (high + low) / 2.0;
        } else {
            converged = true;
        }
    }
    println!("Apogee: {}", get_apogee(rkt));
    println!("Cutoff Altitude: {}", rkt.altitude);
    return a * std::f64::consts::PI / 180.0;
}