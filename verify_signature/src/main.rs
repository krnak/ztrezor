use hex;
use reddsa::{
    orchard::{Binding, SpendAuth},
    SigType, Signature, VerificationKey,
};

use pasta_curves::group::GroupEncoding;
use pasta_curves::{Ep, Fq};

fn main() {
    /*
    let value_commit_base = Ep::from_bytes(
        &hex::decode("6743f93a6ebda72a8c7c5a2b7fa304fe32b29b4f706aa8f7420f3d8e7a59702f")
            .unwrap()
            .try_into()
            .unwrap(),
    )
    .unwrap();

    let sighash: [u8; 32] =
        hex::decode("1d36d6511d144f5b3731784fc3f9edf8e29a82c8eccb3ce1bcec62b8f2f7cb14")
            .unwrap()
            .try_into()
            .unwrap();

    let cv1 = Ep::from_bytes(
        &hex::decode("5b164013e1282804a76ad7e7eb3a6763dcba9058e1b537eeb429dd1ba179b424")
            .unwrap()
            .try_into()
            .unwrap(),
    )
    .unwrap();
    let cv2 = Ep::from_bytes(
        &hex::decode("715258ad3ae479bd21091df909c4ad4f449f9f2b845dfdf85d43dc5708b90289")
            .unwrap()
            .try_into()
            .unwrap(),
    )
    .unwrap();
    let cv_net = value_commit_base * Fq::from(99980000);

    let bvk = (cv1 + cv2 - cv_net).to_bytes();
    verify::<Binding>(
        bvk,
        hex::decode("04f790f5a3d2bd53df269268d9803db613ea8af20f5093e43757741e4d56e30d5c1437f3b8f0566e186b40860a3dca20c5fecf8700bd666f9c106f1687c76e01")
            .unwrap().try_into().unwrap(),
        &sighash,
    );

    verify::<SpendAuth>(
        hex::decode("677bcabda1e50ca44734521feb2a2c97a6150cd8fbe8ec99a5b28dbc3b305fa9")
            .unwrap().try_into().unwrap(),
        hex::decode("1be34305730cd2ae9686ce2906d07f41b96ad446ce1f048b7cfcba67031418b5600bfd3a38600b925f1fefb9be2f6c91989d73b36d29d0f66a9f7a0b06294508")
            .unwrap().try_into().unwrap(),
        &sighash,
    );

    verify::<SpendAuth>(
        hex::decode("0b0eff64a6813694020cdc17f0b4cf0168513746f2c69c47d378dd3b53df6c9e")
            .unwrap().try_into().unwrap(),
        hex::decode("fcbbf054c198f28b1a72383693ff51c3f9b2090431982af35b3fa6c539924939d2fbf4e40f5486ae30afa7a2aad0a648fbe8f8f82f876b4df555fbfa46af6211")
            .unwrap().try_into().unwrap(),
        &sighash,
    );*/

    verify::<SpendAuth>(
        [
            7, 134, 96, 79, 198, 100, 78, 92, 203, 159, 197, 57, 108, 181, 100, 134, 52, 252, 23,
            241, 125, 40, 145, 252, 96, 19, 1, 94, 170, 126, 12, 5,
        ],
        [
            153, 182, 38, 143, 242, 100, 74, 235, 221, 130, 99, 102, 220, 156, 47, 97, 188, 166,
            60, 254, 181, 54, 223, 45, 121, 221, 234, 14, 33, 145, 242, 132, 121, 168, 237, 26,
            174, 32, 92, 22, 76, 75, 205, 175, 193, 159, 214, 35, 33, 136, 174, 193, 105, 29, 21,
            162, 246, 35, 138, 128, 143, 115, 151, 35,
        ],
        &[
            127, 150, 19, 68, 47, 211, 164, 137, 3, 63, 120, 143, 236, 185, 25, 104, 108, 67, 234,
            179, 32, 46, 92, 153, 239, 235, 250, 27, 173, 254, 122, 226,
        ],
    );
}

fn verify<S: SigType>(vk: [u8; 32], sig: [u8; 64], msg: &[u8]) {
    let vk: VerificationKey<S> = vk.try_into().unwrap();
    let sig = Signature::try_from(sig).unwrap();
    println!("{:?}", vk.verify(msg, &sig));
}
