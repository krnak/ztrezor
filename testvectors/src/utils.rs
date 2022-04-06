use hex;
pub fn unhexlify(data: &[u8]) -> String {
    format!("unhexlify({:?})", hex::encode(data))
}
