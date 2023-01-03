# Suite requirements

## Solution architecture

There are two component, which we will need to glued to Trezor Suite:
- Rust crate [`zingolib`](https://github.com/zingolabs/zingolib) implements blockchain scanning.
- Rust crate [`trezor_orchard`](https://github.com/jarys/trezor_orchard) implements proof computation and shielding randomness synchronization.

I guess that these crates can be accessed from javascript via some FFI, but I have no experience with this.

Crate `zingolib` also offers a command line interface retrieving json objects. This interface can be run in an interactive (run `zingo-cli` and then enter commands) and non-interactive (run `zingo-cli <command>`) mode.

Interactions between Trezor, Suite, `zingolib` and `trezor_orchard`:

<img src="https://user-images.githubusercontent.com/15908613/210319150-29e9f117-8ac4-44a7-a772-79dae2981ea8.png" alt="" width="450"/>

Transaction shielding on Trezor and proof computation can be parallelized (indicated by light blue in the illustration above). For more details see the [signing flow](https://github.com/jarys/ztrezor/blob/main/doc/implementation.md#sign-transaction-flow).

Current state of these crates:
- `zingolib` is missing watch-only mode. I will implement it.
- `trezor_orchard` finished, but it is missing documentation 

## 1. Trezor Connect requirements

- [ ] add `ZcashGetViewingKey` request (see `trezorlib.zcash.get_viewing_key`)
- [ ] add `ZcashGetAddress` request (see `trezorlib.zcash.get_address`)
- [ ] extend `SignTx` flow according to the `trezorlib.zcash.sign_tx`

estimation: 3 md, this is about translating code written in python into typescript. `yield` used in `trezorlib.zcash.sign_tx` should be translated into some typescript asynchronous equivalent.

## 2. Suite <-> Trezor requirements

- [ ] Suite is able to request and cache Zcash Full Viewing Key via `ZcashGetViewingKey` message
- [ ] Suite is able to request Orchard and unified addresses via `ZcashGetAddress` message
- [ ] Suite is able to run `SignTx` protocol extended by Orchard parameters and shielded inputs and outputs.
- [ ] Suite is able to send a raw transaction into the Zcash network.

estimation:
- 1 md, or for free. I'm not sure how much are Connect and Suite connected.
- 2 md for sending transaction into a network. I use grpcurl command for that. There are many ways, how to send a raw transaction. You will have to choose some.

## 3. Suite <-> `zingolib` requirements

- [ ] Suite is able to create a new watch-only wallet by passing the Full Viewing Key to the `zingo-cli` command or `zingolib` FFI.
- [ ] Suite is able to get spendable notes via `notes` `zingo-cli` command or `zingolib` FFI.
- [ ] _optional: Suite is able to report wallet scanning progress._

estimation: I see three variants
- 5 md for command line based version. This could be slow and unstable.
- 12 md for FFI based version. `zingolib` functions are mostly asynchronous, so it can be hard to develop an appropriate FFI for them.
- 3 md for daemon based version: In ideal case, `zingo-cli` could be run as a daemon, taking command requests end retrieving json objects. Unfortunately, this is not supported afaik. So it would mean 5 md from my side to implement it into `zingolib`.  

## 4. Suite <-> `trezor_orchard` requirements

- [ ] Suite is able to create a `Prover` instance
- [ ] Suite is able to create a `ProvingKey` instance
- [ ] Suite is able to call `prove` method
- [ ] Suite is able to call `prepaire` method
- [ ] Suite is able to call `append_signatures` method
- [ ] Suite is able to call `serialize` method

estimation: 4 md, these methods and functions are not asynchronous.

## 5. Suite GUI requirements

- [ ] there is a new 'Zcash Shielded' account type
- [ ] _optional: there is a new 'Zcash Testnet Shielded' account type_

#### Get Zcash shielded address and viewing keys

- [ ] Shielded addresses are always generated with a fresh index.
- [ ] By default, the user gets a unified address containing an Orchard receiver.
- [ ] User can request a Full Viewing Key.
- [ ] User can request an Incoming Viewing Key.
- [ ] _optional: User can request an orchard+transparent unified address_.

#### Send Zcash shielded transaction

- [ ] Output address field accepts unified addresses and transparent addresses.
- [ ] Suite is able to decode an unified address to get its receivers.
- [ ] If a unified address has an Orchard receiver, then output is shielded.
- [ ] If a unified address has no Orchard receiver, but it has some transparent receiver, then output is transparent.
- [ ] If a unified address has no compatible receiver, the address is rejected with some error message.
- [ ] If a user enters a Sapling address, the address is rejected with the message "Sapling addresses not supported.".
- [ ] If an output is shielded, then it has an additional _memo_ field. Memo is a message for a recipient.
- [ ] Maximum length of memo is 512 bytes of utf8 encoded text. If a user enters a longer memo, he gets an error message.

estimation:
- 1 md for new account type
- 1 md for getting addresses and viewing keys
- 7 md for transaction GUI. A difficulty could be in writing all these validation scripts and unified address decoding script.

## 6. Tests

- [ ] get_address tests
- [ ] get_viewing_key test
- [ ] sign_tx host side input validation tests
- [ ] sign_tx Trezor tests
- [ ] prove tx tests
- [ ] blockchain scanning tests

estimation: 15 md. possible difficulties
- process of writting test includes repairing mistakes
- blockchain scanning is slow due to the need to try to decrypt every utxo in the blockchain -> experimenting takes a time
- proof computation is slow (aprox. 2 mins at stadard laptop) -> experimenting takes time
- Since the environment already consists of 4 entities (Trezor, Suite, zingolib and prover) it could be chalenging to isolate their interactions. This might reqire to replace some of them by some mock components.

## Servers

- [ ] _optional: SL should run Zcash full-node. I recommend using actively maintained pure rust [zebra](https://github.com/ZcashFoundation/zebra) full node._
- [ ] _optional: SL should run a [lightwalletd](https://github.com/zcash/lightwalletd) full node backend._

https://mainnet.lightwalletd.com can be used instead.

## Autoshielding

- [ ] _optional: Shielded account should be preffered. If user receives fund to a transparent address, there should be a simple way (some button or even an automated process) to resend these funds to his shielded account._

## Total estimation

36 md + communication + reserve

## Related links from 2022

adityapk00 leaves zecwallet:
https://forum.zcashcommunity.com/t/future-of-zecwallet/41681

Orchard support for zecwallet:

- not approved grant: https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134
- in progress work: https://github.com/zingolabs/zecwalletlitelib/pull/76

Zingolabs overtake zecwallet
https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134/5
https://github.com/zingolabs/zecwalletlitelib
