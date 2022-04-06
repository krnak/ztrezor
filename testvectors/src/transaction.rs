use crate::{utils::unhexlify, write_v5_bundle::write_v5_bundle};
use bech32::{self, ToBase32, Variant};
use f4jumble;
use incrementalmerkletree::{bridgetree::BridgeTree, Frontier, Position, Tree};
use orchard::{
    builder::Builder,
    bundle::{commitments::hash_bundle_txid_data, Bundle, Flags},
    keys::{FullViewingKey, OutgoingViewingKey, SpendingKey},
    note::{Note, Nullifier},
    tree::{MerkleHashOrchard, MerklePath},
    value::NoteValue,
    Address,
};
use rand::SeedableRng;
use rand_chacha::ChaCha12Rng;

fn encode_orchard_address(address: &Address) -> String {
    let hrp = "utest";
    let mut buffer = [0u8; 1 + 1 + 43 + 16];
    buffer[0] = 0x03; // typecode
    buffer[1] = 43; // length
    buffer[2..45].copy_from_slice(&address.to_raw_address_bytes());
    buffer[45..50].copy_from_slice(hrp.as_bytes());
    f4jumble::f4jumble_mut(&mut buffer).unwrap();
    bech32::encode(hrp, buffer.to_base32(), Variant::Bech32m).expect("hrp is invalid")
}

#[allow(unreachable_code)]
pub fn main() {
    println!("=== shielding synchronization ===");
    let key_seed: [u8; 64] = [
        // slip-0014 seed
        199, 108, 74, 196, 244, 228, 160, 13, 107, 39, 77, 92, 57, 199, 0, 187, 74, 125, 220, 4,
        251, 198, 247, 142, 133, 202, 117, 0, 123, 91, 73, 95, 116, 169, 4, 62, 235, 119, 189, 213,
        58, 166, 252, 58, 14, 49, 70, 34, 112, 49, 111, 160, 75, 140, 25, 17, 76, 135, 152, 112,
        108, 208, 42, 200,
    ];
    let sk = SpendingKey::from_zip32_seed(&key_seed, 1, 0).unwrap();
    let fvk: FullViewingKey = (&sk).into();
    let ifvk = fvk.derive_internal();
    let ovk: OutgoingViewingKey = (&fvk).into();
    let iovk: OutgoingViewingKey = (&ifvk).into();
    let iaddress = ifvk.address_at(0u32);
    let address_1 = fvk.address_at(0u32);
    //let address_2 = fvk.address_at(1u32);

    let mut rng = ChaCha12Rng::from_seed([0u8; 32]);

    let spends: Vec<(FullViewingKey, Note)> = vec![(
        fvk.clone(),
        Note::new(
            address_1,
            NoteValue::from_raw(5000),
            Nullifier::from_bytes(&[0u8; 32]).unwrap(),
            &mut rng,
        ),
    )];
    let outputs: Vec<(
        Option<OutgoingViewingKey>,
        Address,
        NoteValue,
        Option<[u8; 512]>,
    )> = vec![(
        Some(ovk.clone()),
        address_1,
        NoteValue::from_raw(5000),
        None,
    )];

    // build merkle paths
    let mut tree: BridgeTree<MerkleHashOrchard, 32> = BridgeTree::new(1024);
    let leafs: Vec<MerkleHashOrchard> = spends
        .iter()
        .map(|(_, note)| MerkleHashOrchard::from_cmx(&note.commitment().into()))
        .collect();
    //authentication_path
    for leaf in leafs.iter() {
        tree.append(leaf);
        tree.witness();
    }
    let anchor = tree.root();
    let paths: Vec<MerklePath> = leafs
        .into_iter()
        .enumerate()
        .map(|(i, leaf)| {
            let pos = Position::from(i);
            let path = tree.authentication_path(pos, &leaf).unwrap();
            (pos, path).into()
        })
        .collect();

    let mut builder: Builder = Builder::new(Flags::from_parts(true, true), anchor.into());
    for ((fvk, note), path) in spends.iter().zip(paths.into_iter()) {
        builder.add_spend(fvk.clone(), note.clone(), path).unwrap();
    }

    for (ovk, address, value, memo) in outputs.iter() {
        builder
            .add_recipient(ovk.clone(), address.clone(), value.clone(), memo.clone())
            .unwrap();
    }
    let seed = [5u8; 32];
    let mut rng = ChaCha12Rng::from_seed(seed.clone());

    let bundle: Bundle<_, i64> = builder.build_online(&mut rng).unwrap();

    let txid = hash_bundle_txid_data(&bundle);
    let mut serialized: Vec<u8> = vec![];
    write_v5_bundle(Some(&bundle), &mut serialized).unwrap();

    println!("tx = SignTx(");
    println!("\tinputs_count = 0,");
    println!("\toutputs_count = 0,");
    println!("\tcoin_name = \"Zcash Testnet\",");
    println!("\tversion = 5,");
    println!("\tversion_group_id = 0x26A7270A,");
    println!("\tbranch_id = 0x37519621,"); // TODO: update this
    println!("\texpiry = 0,");
    println!("\torchard = ZcashOrchardData(");
    println!("\t\toutputs_count = {:?},", spends.len());
    println!("\t\tinputs_count = {:?},", outputs.len());
    println!("\t\tanchor = {},", unhexlify(&anchor.to_bytes()[..]));
    println!("\t\tenable_spends = True,");
    println!("\t\tenable_outputs = True,");
    println!("\t\taccount = 0,");
    println!("\t),");
    println!(")");

    println!("key_seed = {}", unhexlify(&key_seed[..]));
    println!("shielding_seed = {}", unhexlify(&seed[..]));
    println!("inputs = [");
    for (fvk, note) in spends.iter() {
        println!("\tZcashOrchardInput(");
        println!("\t\tnote = {},", unhexlify(&note.to_bytes()[..]));
        println!("\t\tamount = {:?},", note.value().inner());
        println!("\t\tinternal = False,");
        println!("\t),");
    }
    println!("]");

    println!("outputs = [");
    for (ovk, address, value, memo) in outputs.iter() {
        println!("\tZcashOrchardOutput(");
        println!("\t\tamount = {:?},", value.inner());
        println!("\t\taddress = {:?}", encode_orchard_address(address));
        if let &Some(m) = memo {
            println!("memo = {}", unhexlify(&m[..]));
        }
        println!("\t),");
    }
    println!("]");

    println!("serialized = {}", unhexlify(&serialized));
    println!("digest = {}", unhexlify(txid.as_bytes()));
}
