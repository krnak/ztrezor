# Suite requirements

## Solution architecture

There are two component, which we will need to glued to Trezor Suite:
- Rust crate [`zingolib`](https://github.com/zingolabs/zingolib) implements blockchain scanning.
- Rust crate [`trezor_orchard`](https://github.com/jarys/trezor_orchard) implements proof generation.

I guess that they can accessed from javascript via some FFI, but I have no experince with this.

Crate `zingolib` also offers a command line interface retrieving json objects. This interface can be run in an interactive (run `zingo-cli` and then enter commands) and non-interactive (run `zingo-cli <command>`) mode.

![image](https://user-images.githubusercontent.com/15908613/210319150-29e9f117-8ac4-44a7-a772-79dae2981ea8.png)

## Get Zcash address UI

- [ ] Addresses are always generated with fresh index
- [ ] By default, user gets an unified address containing a transparent address and an Orchard shielded address
- [ ] User can get a pure transparent address.
- [ ] User can get a pure Orchard shielded address.


## Send ZEC UI

- [ ] Address field accepts unified address.
- [ ] Suite is able to decode an unified address to get its receivers.
- [ ] If a unified address has Orchard receiver, then output is shielded.
- [ ] If a unified address has not Orchard receiver, but it has some transparent receiver, then output is transparent.
- [ ] If a unified address has no compatible receiver, address is rejected with some error message.
- [ ] If user enters Sapling address, address is rejected with message "Sapling addresses not supported.".
- [ ] If an output shielded, then it has an additional _memo_ field. Memo is a message for a recipient. Maximum length of memo is 512 bytes of utf8 encoded text.

## Servers

- [ ] SL should run Zcash full-node. I recommend using actively maintained pure rust [zebra](https://github.com/ZcashFoundation/zebra) full node. 
- [ ] SL should run a [lightwalletd](https://github.com/zcash/lightwalletd) full node backend.

## Rust functionalities

There will be a special Rust crate (`trezor_orchard`), which will enable a client to finish transaction authorization.

- [ ] Suite must be able to use functionalities of `trezor_orchard` crate.
- [ ] Unified address decoding can be imported from `librustzcash`.

## Storage

- [ ] Suite must be able to store all detected incoming shielded UTXOs. This requires circa 1kb per zUTXO.

## Autoshielding

TODO

## Related

adityapk00 leaves zecwallet:
https://forum.zcashcommunity.com/t/future-of-zecwallet/41681

Orchard support for zecwallet:

- not approved grant: https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134
- in progress work: https://github.com/zingolabs/zecwalletlitelib/pull/76

Zingolabs overtake zecwallet
https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134/5
https://github.com/zingolabs/zecwalletlitelib
