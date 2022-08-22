use incrementalmerkletree::{bridgetree::BridgeTree, Tree};
use orchard::{note::ExtractedNoteCommitment, tree::MerkleHashOrchard};
use std::env;
use subtle::CtOption;
//use zcash_client_backend::data_api::BlockSource;
//use zcash_client_sqlite::{chain, BlockDb};
//use zcash_primitives::consensus::BlockHeight;
use hex;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn main() -> io::Result<()> {
    //let mut target = String::new();
    //println!("target cmx:");
    //std::io::stdin().read_line(&mut target).unwrap();
    //let target_bytes: [u8; 32] = hex::decode(target).unwrap().try_into().unwrap();
    //let target = MerkleHashOrchard::from_bytes(&target_bytes).unwrap();
    let args: Vec<String> = env::args().collect();
    println!("Commitments:");
    let mut targets: Vec<MerkleHashOrchard> = vec![];
    for arg in args[1..].iter() {
        println!("{}", arg);
        let data: [u8; 32] = hex::decode(arg).unwrap().try_into().unwrap();
        targets.push(MerkleHashOrchard::from_bytes(&data).unwrap())
    }
    println!("---");

    let file = File::open("/home/agi/cmxs.testnet")?;
    let mut reader = BufReader::new(file);

    let mut tree: BridgeTree<MerkleHashOrchard, 32> = BridgeTree::new(1024);
    let mut positions = vec![];
    let mut i = 0;
    loop {
        let mut cmx = [0u8; 32];
        let ret = reader.read(&mut cmx)?;
        if ret == 0 {
            break;
        }
        let leaf = Option::from(MerkleHashOrchard::from_bytes(&cmx)).expect("invalid cmx in db");
        tree.append(&leaf);
        if targets.contains(&leaf) {
            let pos = tree.witness().expect("witness");
            positions.push((leaf, pos));
        }
        i += 1;
        if i % 3050 == 0 {
            println!("{:?} %", 100 * i / 30500)
        }
    }
    println!("---");
    println!("{:?} cmxs processed", tree.current_position());
    let root = tree.root(0).unwrap();
    println!("anchor: {},", hex::encode(&root.to_bytes()));
    println!("---");
    for (leaf, pos) in positions.into_iter() {
        println!("{:?}", leaf);
        println!("{:?}", pos);
        let path: Vec<MerkleHashOrchard> = tree.authentication_path(pos, &root).expect("no path");
        println!("[");
        for x in path.iter() {
            println!("\t\"{}\",", hex::encode(&x.to_bytes()));
        }
        println!("]");
        println!("---");
    }

    Ok(())
}
