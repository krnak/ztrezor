# Implementation

## Security model

<img src="interactions.png" alt="Trezor - Host - User - full node interactions" width="600"/>  

Our communication scheme consists of four players. User, Trezor, a Host (typically a PC or a cell phone) and Zcash fullnode (a server maintaining a full blockchain copy).  

Our security goals differs according to following two scenarios:  

1. If the **Host is honest**, then all Zcash privacy features are preserved.
2. Even if the **Host is malicious**, he cannot spend Zcash funds from the Trezor. However, he can violate Zcash privacy features.  

Zcash privacy guarantees are for example:

- **Shielded address unlinkability:** Two shielded addresses with the same spending authority cannot be linked (without knowledge of Incoming Viewing Key).  

- **Transaction graph shielding:** As in Bitcoin, every shielded input corresponds to some shielded output. However this correspondence is unrecognizable (without knowledge of Incoming Viewing Key for a particular tuple).

- **Amount privacy:** Given a shielded input (resp. output), nobody can compute how many ZECs were spent (resp. sent).

## Comparison with the Ledger

- We implement Orchard shielded protocol, while Ledger implemented the Sapling shielded protocol.
- We have no control over the proof randomness. (Ledger maybe wont too after the NU5.)
- We don't have to worry about memory optimizations so much.

## Data flow

![shielding data flow](shielding_flow.png)


## Delayed shielding

Since Action shielding is slow, we delay the shielding as follows:

Phase 1: Host streams shielded inputs and outputs. User confirms outputs on the screen. Trezor sets a MAC for each message and let the host to store it.

Phase 2: Host restreams all shielded inputs and outputs including a coresponding MACs. Trezor checks a MAC for every message and it sequentially computes a digest of shielded data.

This method will increase the complexity of the communication protocol, but ont he other side it will not let user to wait between confirmations of individual shielded outputs.

## `trezor-firmware` implementation

Zcash libraries are now available in Rust. I would like to use them directly as dependencies. It will be necessary to make them `![no_std]` compatible.

| library | no_std | alloc |
| -       | -      | -     |
| [f4jumble](https://github.com/zcash/librustzcash/components/f4jumble) | :heavy_check_mark: | :heavy_check_mark: |
| [zcash_note_encryption](https://github.com/zcash/librustzcash/components/f4jumble) | :heavy_check_mark: | :heavy_check_mark: |
| [orchard](https://github.com/zcash/orchard) | in process | :heavy_check_mark: |
| [pasta_curves](https://github.com/zcash/pasta_curves) | :heavy_check_mark: | :heavy_check_mark: |
| [reddsa](https://github.com/str4d/redjubjub) | :heavy_check_mark: | :heavy_check_mark: |
| [fpe](https://github.com/str4d/fpe) | in progress | :heavy_check_mark: |
| poseidon | almost | almost |

## `trezorlib` implementation

[lightwalletd](https://github.com/zcash/lightwalletd) (coded in Go lang) can be used for communication with a full node.

[halo2](https://github.com/zcash/halo2) crate (coded in Rust) will be used for proof computation.
