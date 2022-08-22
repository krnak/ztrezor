# Implementation

## Security model

<img src="interactions.png" alt="Trezor - Host - User - full node interactions" width="600"/>  

Our communication scheme consists of four players: an user, a hardware wallet (HWW), a host (typically a PC or a cell phone) and Zcash fullnode (a server maintaining a full blockchain copy).

Threat model for host<->fullnode communication is well-described in [Zcash doc](https://zcash.readthedocs.io/en/latest/rtd_pages/wallet_threat_model.html). In this section we focus only to the communication between the host, the user and the HWW.

Our security goals differs according to following two scenarios:  

1. If the **Host is honest**, then all Zcash privacy features are preserved.
2. Even if the **Host is malicious**, he cannot create a valid transaction with undesired effects. However, he can violate all Zcash privacy features.

Knowledge of full viewing key is necessary for proof computation. Since FVK must be revealed to the host, there is no chance to preserve privacy against the host. Malicious can view details of all incoming and out-coming transactions.

TODO: gapped model

## Comparison with the Ledger

- We implement Orchard shielded protocol, while Ledger implemented the Sapling shielded protocol.
- We have no control over the proof randomness. (Ledger maybe wont too after the NU5.)
- We don't have to worry about memory optimizations so much.

## Efficiency and memory analysis

#### Field and Pallas
Orchard uses arithmetics in 255-bit finite fiald Fp. Crate `pasta_curves` contains very efficient `no_std`-compatible implementation of Fp and of Pallas elliptic curve. Crate uses standard speed-up techniques like Montgomery reductions and projective coordinates.

Squaring in Fp is optimized by large pre-computed tables. Crate also contains a (`no_std` compatible) table-less squaring implemented via Tonelli–Shanks' square-root algorithm[[1](https://eprint.iacr.org/2012/685.pdf)] for `p mod 16 = 1`. Squaring is necessary for hashing to the curve.

Hashing to the Pallas is realized by simplified version of SWU algoritm. Since `a = 0` for Pallas, algoritm first hashes a messages to the different curve and the maps the point to the Pallas by curve isogeny.

Tonelli-Shanks: 822 multiplications
Hashing requires: TODO
Isogeny computation requires: TODO

#### ZIP-32
#### Address generation
#### Shielding


## Shortened shielding flow

![shielding data flow](shielding_flow.png)


## Delayed shielding

Since Action shielding is slow, we delay the shielding as follows:

Phase 1: Host streams shielded inputs and outputs. User confirms outputs on the screen. Trezor sets a MAC for each message and let the host to store it.

Phase 2: Host restreams all shielded inputs and outputs including a coresponding MACs. Trezor checks a MAC for every message and it sequentially computes a digest of shielded data.

This increases the complexity of the communication protocol, but on the other side it does not let a user to wait between confirmations of individual shielded outputs.

## Authorization proof

Transaction is authorized by zero-knowledge proof. We delegate computation of this proof to the host. We considered several models of interaction between HWW and the prover algorithm.

### Nullifiers

```
note := (addr, v, rho, rseed)
psi := PRF(rseed, rho) mod p
cm  := Extract $ Sinsemilla $ (addr, v, rho, psi)
nf  := Extract $ [Poseidon(nk,rho) + psi mod p]G + cm
```

```
note := (addr(my), v(bindingSig), rho', rseed')
psi := PRF(rseed, rho) mod p (only equality)
cm  := Extract $ Sinsemilla $ (addr, v, rho, psi)

inputs: nk -> addr, rho, psi , v
nf  := Extract $ [Poseidon(nk(my),rho) + psi mod p]G + (Extract $ Sinsemilla $ (addr(my) || v || rho || psi))
```

- cm can be always manipulated
- all cms manipulable throught artificial anchor
- valid nullifier is only one


#### Randomness by synchronized PRGNs

+ easy and efficient
- **hard to stabilize**

#### Randomness by deterministic PRGNs

- hard to code
- not mergable
+ parallelization signing and proving
+ in fact don't have to be fully random


#### Randomness by Trezor

- need for Poseidon hash function
- serialization of all data
- unable to parallelize signing and proving

#### Randomness by Client

- hard to analyze
- non-verifiable randomness
+ no need for Poseidon
+ mergable
+ parallelizable


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
<<<<<<< HEAD
=======

## Zcash codebase analysis

Zcash repositores relevant to this project are generally written in Rust.
#### Orchard
- [librustzcash]()
  - [zcash_note_encryption]()
  - [f4jumble]()
- [orchard]()
- [reddsa]()
- [pasta_curves]()
- [halo2_gadgets]()
- [halo2_proofs]()
- [incrementalmerkletree]()

#### Cryptography
- [ff]()
- [group]()
- [fpe]()
- [subtle]()

#### Wallet
- [zcashd]() / [zebrad]()
- [lightwalletd]()
- [zingolib]()

## `trezorlib` implementation

[lightwalletd](https://github.com/zcash/lightwalletd) (coded in Go lang) can be used for communication with a full node.

[halo2](https://github.com/zcash/halo2) crate (coded in Rust) will be used for proof computation.
>>>>>>> 8c63eb92866e28917ddbf19cf00a73b8d3414246
