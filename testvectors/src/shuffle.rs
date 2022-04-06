use rand::seq::SliceRandom;
use rand::SeedableRng;
use rand_chacha::ChaCha12Rng;

use crate::utils::unhexlify;

pub fn main() {
    println!("=== Shuffle test vectors ===");
    let seed = [43u8; 32];
    println!("seed = {}", unhexlify(&seed));
    let mut rng = ChaCha12Rng::from_seed(seed);
    let mut data: Vec<usize> = (0..20).into_iter().collect();
    println!("expected_states = [");
    for _ in 0..16 {
        println!("\t{:?},", data);
        data.shuffle(&mut rng);
    }
    println!("]");
}
