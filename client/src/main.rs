use incrementalmerkletree::{bridgetree::BridgeTree, Position, Tree};
use orchard::tree::MerkleHashOrchard;
//use zcash_client_backend::data_api::BlockSource;
//use zcash_client_sqlite::{chain, BlockDb};
//use zcash_primitives::consensus::BlockHeight;
use hex;
use std::collections::HashSet;
use std::fs;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn main() -> io::Result<()> {
    let mut targets: HashSet<[u8; 32]> = HashSet::new();
    let cmxs: Vec<String> = fs::read_dir("/home/agi/code/ztrezor/witnesses")
        .unwrap()
        .map(|path| {
            path.unwrap()
                .path()
                .into_os_string()
                .into_string()
                .unwrap()
                .split("/")
                .last()
                .unwrap()
                .to_owned()
                .split(".")
                .collect::<Vec<&str>>()[0]
                .to_owned()
        })
        .filter(|x| x != "anchor")
        .collect();

    println!("Commitments:");
    for cmx in cmxs.iter() {
        println!("    - {}", cmx);
        let data: [u8; 32] = hex::decode(cmx).unwrap().try_into().unwrap();
        targets.insert(data);
    }
    println!("---");

    let file = File::open("/home/agi/cmxs.testnet")?;
    let mut reader = BufReader::new(file);

    let mut tree: BridgeTree<MerkleHashOrchard, 32> = BridgeTree::new(1024);
    let mut positions: Vec<(MerkleHashOrchard, Position)> = vec![];
    let mut i = 0;
    loop {
        let mut cmx = [0u8; 32];
        let ret = reader.read(&mut cmx)?;
        if ret == 0 {
            break;
        }
        let leaf = Option::from(MerkleHashOrchard::from_bytes(&cmx)).expect("invalid cmx in db");
        tree.append(&leaf);
        if targets.contains(&leaf.to_bytes()) {
            let pos = tree.witness().expect("witness");
            positions.push((leaf, pos));
        }
        i += 1;
        if i % 3100 == 0 {
            println!("{:?} %", 100 * i / 31000);
        }
    }

    println!("---");
    println!("{:?} cmxs processed", tree.current_position().unwrap());
    let root = tree.root(0).unwrap();
    println!("anchor: {}", hex::encode(&root.to_bytes()));
    let mut file = File::create("/home/agi/code/ztrezor/witnesses/anchor")?;
    write!(file, "{}", hex::encode(&root.to_bytes()))?;
    println!("---");
    for (leaf, pos) in positions.into_iter() {
        let cmx = hex::encode(leaf.to_bytes());
        let file = File::create(format!("/home/agi/code/ztrezor/witnesses/{}.json", cmx))?;
        let path: Vec<MerkleHashOrchard> = tree.authentication_path(pos, &root).expect("no path");
        let path = path
            .iter()
            .map(|x| hex::encode(&x.to_bytes()))
            .collect::<Vec<String>>();
        let pos = u64::try_from(pos).unwrap();
        let obj: (u64, Vec<String>) = (pos, path);
        serde_json::to_writer_pretty(file, &obj)?;
    }
    Ok(())
}
