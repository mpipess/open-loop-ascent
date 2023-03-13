use rust_ascent;
fn main() {
    let mut rock1 = rust_ascent::build_rocket(20, 2965000, 3072.0, 112900.0, 123600.0, 142.0);
    println!("{}", rust_ascent::find_pitch_angle_binary(&mut rock1, 100000.0, 20.0));
}
