use orchard::keys::*;
use rand::prelude::*;
use rand::SeedableRng;
use rand_chacha::ChaCha20Rng;
use zcash_address::{
    unified::{self, *},
    Network,
};

fn main() {
    let seed: [u8; 64] = [
        199, 108, 74, 196, 244, 228, 160, 13, 107, 39, 77, 92, 57, 199, 0, 187, 74, 125, 220, 4,
        251, 198, 247, 142, 133, 202, 117, 0, 123, 91, 73, 95, 116, 169, 4, 62, 235, 119, 189, 213,
        58, 166, 252, 58, 14, 49, 70, 34, 112, 49, 111, 160, 75, 140, 25, 17, 76, 135, 152, 112,
        108, 208, 42, 200,
    ];
    let mut rng = ChaCha20Rng::seed_from_u64(0);
    println!("@pytest.mark.skip_t1");
    println!("def test_get_viewing_key(client: Client):");
    println!("     # Testnet");
    test_get_viewing_key(
        &seed[..],
        1,
        Network::Test,
        "Zcash Testnet".to_owned(),
        &mut rng,
    );
    println!("     # Mainnet");
    test_get_viewing_key(&seed[..], 133, Network::Main, "Zcash".to_owned(), &mut rng);

    println!("");
    println!("@pytest.mark.skip_t1");
    println!("def test_get_address(client: Client):");
    println!("     # Testnet");
    test_get_address(
        &seed[..],
        1,
        Network::Test,
        "Zcash Testnet".to_owned(),
        &mut rng,
    );
    println!("     # Mainnet");
    test_get_address(&seed[..], 133, Network::Main, "Zcash".to_owned(), &mut rng);
}

fn test_get_viewing_key(
    seed: &[u8],
    coin: u32,
    network: Network,
    coin_name: String,
    rng: &mut impl Rng,
) {
    for _ in 0..3 {
        let account = rng.gen_range(0..100);
        let sk = SpendingKey::from_zip32_seed(&seed, coin, account).unwrap();
        let fvk: FullViewingKey = (&sk).into();
        let ufvk =
            unified::Ufvk::try_from_items(vec![unified::Fvk::Orchard(fvk.to_bytes())]).unwrap();
        println!(
            "    z_address_n = parse_path(\"m/32h/{}h/{}h\")",
            coin, account
        );
        println!(
            "    fvk = zcash.get_viewing_key(client, z_address_n, \"{}\", full=True)",
            coin_name
        );
        println!("    assert fvk == \"{}\"", ufvk.encode(&network));
        let ivk: IncomingViewingKey = fvk.to_ivk(Scope::External);
        let uivk =
            unified::Uivk::try_from_items(vec![unified::Ivk::Orchard(ivk.to_bytes())]).unwrap();
        println!(
            "    ivk = zcash.get_viewing_key(client, z_address_n, \"{}\", full=False)",
            coin_name
        );
        println!("    assert ivk == \"{}\"", uivk.encode(&network));
        /*for j in [0u64, 42] {
            let address = fvk.address_at(j, Scope::External);
            let uaddr = unified::Address::try_from_items(vec![unified::Receiver::Orchard(
                address.to_raw_address_bytes(),
            )])
            .unwrap();
            println!("address = zcash.get_address(client, z_address_n=z_address_n, coin_name=\"{}\", diversifier_index={})", coin_name, j);
            println!("assert address == \"{}\"", uaddr.encode(&network));
        }*/
        println!("");
    }
}

fn test_get_address(
    seed: &[u8],
    coin: u32,
    network: Network,
    coin_name: String,
    rng: &mut impl Rng,
) {
    for _ in 0..3 {
        let account = rng.gen_range(0..100);
        let sk = SpendingKey::from_zip32_seed(&seed, coin, account).unwrap();
        let fvk: FullViewingKey = (&sk).into();
        let di: u64 = rng.gen_range(0..1000);
        let address = fvk.address_at(di, Scope::External);
        let uaddr = unified::Address::try_from_items(vec![unified::Receiver::Orchard(
            address.to_raw_address_bytes(),
        )])
        .unwrap();
        println!("    address = zcash.get_address(client, z_address_n=parse_path(\"m/32h/{}h/{}h\"), coin_name=\"{}\", diversifier_index={})", coin, account, coin_name, di);
        println!("    assert address == \"{}\"", uaddr.encode(&network));
        println!("");
    }
}
