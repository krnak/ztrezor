#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_variables)]
use rand_chacha::ChaCha12Rng;

use rand::prelude::SliceRandom;
use rand::SeedableRng;

mod shuffle;
mod transaction;
pub mod utils;
pub mod write_v5_bundle;
fn main() {
    //shuffle::main();
    transaction::main();
}

fn find_identity_gen() {
    for i in 0..256 {
        let seed = [i as u8; 32];
        let mut rng = ChaCha12Rng::from_seed(seed);

        let mut data1 = vec![0, 1];
        data1.shuffle(&mut rng);

        let mut data2 = vec![0, 1];
        data2.shuffle(&mut rng);

        if data1 == vec![0, 1] && data2 == vec![0, 1] {
            println!("{:?}", i);
            break;
        }
    }
}
