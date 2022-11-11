# Implementation

## Security model

<img src="interactions.png" alt="Trezor - Host - User - full node interactions" width="600"/>  

Our communication scheme consists of four players: an user, a hardware wallet (HWW), a host (typically a PC or a cell phone) and Zcash fullnode (a server maintaining a full blockchain copy).

Threat model for communication between host and fullnode is described in [Zcash doc](https://zcash.readthedocs.io/en/latest/rtd_pages/wallet_threat_model.html). In this section we focus only to the communication between the host, the user and the HWW.

Our security goals differs according to following two scenarios:  

1. If the **Host is honest**, then all Zcash privacy features are preserved.
2. Even if the **Host is malicious**, he cannot create a valid transaction with undesired effects. However, he can violate all Zcash privacy features.

Every shielded transaction is authorized by a zero knowledge proof. Since compution of this proof is computationally demanding, this task must be delaged to the host. To do so, Full Viewing Key (FVK), which guarantees full access to the user's transaction history, must be revealed to the host. There no way how HWW can prevent a malicious host from sharing FVK with an attacker.

(Even if a mallicious host were locked into some sandbox without access to any side-channel, it can send FVK to an attacker by secretly encoding it into a transaction itself by manipulating proof randomness. Attacker then gains FVK by scanning every transaction in the blockchain.)

## Comparison with the Ledger

- We implement Orchard shielded protocol, while Ledger implemented the Sapling shielded protocol.
- We have no control over the proof randomness. (Ledger maybe wont too after the NU5.)
- We don't have to worry about memory optimizations so much.

## Efficiency and memory analysis

#### Field and Pallas
Orchard uses arithmetics in 255-bit finite fiald Fp. Crate `pasta_curves` contains very efficient `no_std`-compatible implementation of Fp and of Pallas elliptic curve. Crate uses standard speed-up techniques like Montgomery reductions and projective coordinates.

Squaring in Fp is optimized by large pre-computed tables. Crate also contains a (`no_std` compatible) table-less squaring implemented via Tonelli–Shanks' square-root algorithm[[1](https://eprint.iacr.org/2012/685.pdf)] for `p mod 16 = 1`. Squaring is necessary for hashing to the curve and unpacking compressed curve points.

Hashing to the Pallas is realized by simplified version of SWU algoritm. Since linear term of Pallas equation is zero, algoritm first hashes a messages to a isogenic curve (isoPallas) and then maps the result to the Pallas.

#### Algorithms efficiency
```python
fiel_mul = ?
blake = ?

curve_add = 14 * field_mul
curve_double = 7 * field_mul
curve_mul = 254 * curve_double + 254 * curve_add = 5334 * field_mul
isogeny = 33 * field_mul

field_sqrt = 822 * field_mul
hash_to_field = 3 * blake
map_to_curve = 19 * field_mul + 2 * field_sqrt = 1663 * field_mul
hash_to_curve = hash_to_field + 2 * map_to_curve + isogeny + curve_add = 3 * BLAKE + 3373 * field_mul

sinsemilla_block = hash_to_curve + 2 * curve_add
commit_ivk = 51 * sinsemilla_block + curve_mul + curve_add
commit_note = 109 * sinsemilla_block + curve_mul + curve_add
reddsa_sign = 2 * blake + field_mul + 2 * curve_mul
```

#### ZIP-32
#### Address generation
#### Shielding


## Shortened shielding flow

![shielding data flow](shielding_flow.png)

## Transaction signing flow

In this section I will describe how a shielded transaction is signed. This process can be separated into three phases.

1. confirm transaction
2. shield transaction and compute its sighash
3. retrieve signatures

In the first phase, transaction details are requested by Trezor. All transaction inputs and outputs (both transparent and shielded) are requested by Trezor one by one. Trezor requires user to confirm transaction outputs and fee. At the same time it incrementally updates digest of all received data to authentize them in phase 2.

Transaction sighash is computed in the second phase. From now, let call different parts of the transaction _bundles_. For sighash of the transparent bundle, hash components
- `prevouts_digest`,
- `amounts_digest`,
- `scriptpubkeys_digest`,
- `sequence_digest` and
- `outputs_digest`
were already computed in the first phase. On contrary, Orchard bundle sighash components
- `commitments_digest`,
- `memos_digest` and
- `notes_digest`
must be computed now. This requires following steps:
1. Trezor derives a _bundle shielding seed_, from which all the randomness necessary for bundle shielding is derived. Trezor send this seed to the Host.
2. Since result of Orchard bundle shielding is completely determined by the set of Orchard inputs and outputs, anchor, flags and _bundle shielding seed_, the Host can replicate all following steps (3-8) to get the Orchard bundle. While Trezor is computing the bundle shielding to get its sighash, Host can compute a bundle authorizing proof in parallel.
3. Trezor makes the set of shielded inputs equal in size to the set of shielded outputs by padding the smaller one with dummy notes.
4. Trezor shuffles shielded inputs and output and zip them into Actions.
5. Trezor precomputes the Full Viewing Key for the account from which is being spent.
6. Trezor start incremental computation of the Orchard bundle sighash. For each action:
7.1. Trezor request the action input (if it is not dummy).
7.2. Trezor request the action output (if it is not dummy).
7.3. Trezor derives _action shielding seed_ from the _bundle shielding seed_ and Action index.
7.4. Trezor shields the Action and updates sighasher state by action components. This computation includes:
- derivation of all necessary randomness computed from the _action shielding seed_
- derivation of the dummy input or output
- computation of input note nullifier
- randomization of spend validating key
- computation of output note commitmnet
- computation of the value commitment
- encryption of the note plaintext
- encryption of the outgoing note plaintext
8. Trezor finishes the computation of Orchard bundle sighash by hashing all its components with _anchor_, _value balance_ and _flags_.

There two reasons, why components of Orchard bundle are not computed already in the first phase.
1. Since Orchard bundle shielding is computationally demanding, this would cause (approx. 12s) delays between confirmations of individual shielded outputs.
2. We want to let the user to confirm transaction outputs in the same order he entered them on the Host and then compute sighash on shuffled outputs.


## Randomness derivation

The _bundle shielding seed_ is derived as follows:
```python
ss_slip21 = self.keychain.derive_slip21(
    [b"Zcash Orchard", b"bundle_shielding_seed"],
).key()
bundle_shielding_seed = blake2b(
    b"TrezorShieldSeed",
    outlen=32,
    header_digest ||
        transparent_digest ||
        message_accumulator_state ||
        orchard_anchor ||
        ss_slip21,
)
```
For each action
```python
action_shielding_seed = blake2b(
    b"ActionShieldSeed",
    outlen=32,
    bundle_shielding_seed || i.to_bytes(4, "little"),
)
```
Blinding factors for Action shielding are derived as follows:
```python
random(dst, outlen) = blake2b(b"ActionExpandSeed", outlen,  action_shielding_seed + dst)
alpha = to_scalar(random(b"alpha", 64))
rcv = to_scalar(random(b"rcv", 64))

dummy_address = (
    random(b"dummy_d", 11),
    to_scalar(random(b"dummy_ivk", 64))
)
ock = random(b"dummy_ock", 32)
op = random(b"dummy_op", 64)
rseed_old = random(b"dummy_rseed_old", 32)
rseed_new = random(b"rseed_new", 32)
dummy_sk = random(b"dummy_sk", 32)
rho = to_base(random(b"dummy_rho"))
spend_auth_T = random(b"spend_auth_T", 32)
```

Permutation derivation is is little bit more complicated. We use personalized blake2b in counter mode to generate a stream of randomness. This stream is chunkized into block of 4 bytes and interpreted as a sequence of little-endinan unsigned integers. These integers are used to sample uniformly random integers necessary for Fisher-Yates algorithm.

```python
personal = b"Inps_Permutation"  # for inputs permutation
         | b"Outs_Permutation"  # for outputs permutation

block(i) = blake2b(personal, outlen=64, bundle_shielding_seed || i.to_bytes(4, "little"))
byte_stream = block(0) || block(1) || block(2) + ...
u32(i) = int.from_bytes(byte_stream[4*i : 4*(i+1)], "little")
u32_stream = [u32(0), u32(1), u32(2), ... ]

MAX = 0xFFFF_FFFF

sample_uniform(n, gen) = do
    while True:
        wide = next(gen) * n
        high = wide >> 32
        low = wide & MAX
        if low <= MAX - n or low <= MAX - (MAX - n) % n:
            return high

shuffle(x) = do
    gen = u32_stream
    for i in range(len(x) - 1, 0, -1):
        j = sample_uniform(i + 1, gen)
        x[i], x[j] = x[j], x[i]
```

## Authorization proof

Transaction is authorized by zero-knowledge proof. We delegate computation of this proof to the host. We considered several models of interaction between HWW and the prover algorithm.

#### Randomness by Host

All randomness is computed by the Host. Trezor just verifies effect of the transaction.

- harder to analyze
- non-verifiable randomness

+ no need for Poseidon
+ parallelizable

#### Randomness derived from a seed

- harder to code
+ easy and efficient
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
