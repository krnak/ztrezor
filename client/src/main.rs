use incrementalmerkletree::{bridgetree::BridgeTree, Tree};
use orchard::tree::MerkleHashOrchard;
use subtle::CtOption;
//use zcash_client_backend::data_api::BlockSource;
//use zcash_client_sqlite::{chain, BlockDb};
//use zcash_primitives::consensus::BlockHeight;
use hex;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn main() -> io::Result<()> {
    let file = File::open("/home/agi/code/ztrezor/block_db/orchard_cmxs.txt")?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        println!("{:?}", hex::decode(line?).unwrap());
    }

    let raw_leafs: Vec<[u8; 32]> = vec![];
    let leafs: Vec<MerkleHashOrchard> = raw_leafs
        .iter()
        .map(|leaf| MerkleHashOrchard::from_bytes(leaf).unwrap())
        .collect();

    // build merkle paths
    let mut tree: BridgeTree<MerkleHashOrchard, 32> = BridgeTree::new(1024);

    //authentication_path
    for leaf in leafs.iter() {
        tree.append(leaf);
    }
    let anchor = tree.root(0).unwrap();
    println!("{:?}", anchor);

    Ok(())
}
