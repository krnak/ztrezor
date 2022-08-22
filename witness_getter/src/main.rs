use futures::executor::block_on;
use std::sync::Arc;

use http;
use tokio::sync::RwLock;
use zcash_primitives::consensus::BlockHeight;
use zingoconfig::{Network, ZingoConfig};
use zingolib::blaze::block_witness_data::BlockAndWitnessData;
use zingolib::blaze::sync_status::SyncStatus;

fn main() {
    let sync_status = Arc::new(RwLock::new(SyncStatus::default()));
    let config = ZingoConfig::create_unconnected(
        Network::Mainnet,
        Some("/home/agi/ztrezor/witness_getter/cache".into()),
    );
    let client = BlockAndWitnessData::new(&config, sync_status);
    //let uri = http::Uri::from_static("https://testnet.lightwalletd.com");
    let uri = ZingoConfig::get_server_or_default(None);
    let height = BlockHeight::from_u32(2_000_465);
    let transaction_num = 1;
    let action_num = 1;
    let call = client.get_orchard_note_witness(uri, height, transaction_num, action_num);
    let witness = block_on(call).expect("failed");
    println!("Hello, world! {:?}", witness.position());
}
