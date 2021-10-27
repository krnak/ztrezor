# M.1. Summary

We are glad to announce submission of milestone M.1. During past two months we

- analyzed design and memory and computational requirements of all Zcash primitives
- explored transaction shielding and authorization data flows
- added basic structure of zcash app into trezor-firmware monolith
- enabled alloc features on Trezor to facilitate orchard crate import
- added no_std+alloc support for all necessary Orchard crates

So far, we import all necessary primitives from fully tested crates, so writing our own unit test would be superfluous.

Finally we are exited to announce that we are nowhere far from submission of M.2.

# M.1 Detailed

## Primitives table

| library | no_std+alloc |
| -       | -            |
| [f4jumble](https://github.com/zcash/librustzcash/components/f4jumble) | ✔️ [PR](https://github.com/zcash/librustzcash/pull/446) |
| [zcash_note_encryption](https://github.com/zcash/librustzcash/components/zcash_note_encryption) | ✔️ [PR](https://github.com/zcash/librustzcash/pull/450) |
| [orchard](https://github.com/zcash/orchard) | ✔️ [branch](https://github.com/jarys/orchard/tree/no-std-alloc), [issue](https://github.com/zcash/orchard/issues/211) |
| [pasta_curves](https://github.com/zcash/pasta_curves) | ✔️ [PR](https://github.com/zcash/pasta_curves/pull/21) |
| [reddsa](https://github.com/str4d/redjubjub) | ✔️ [branch](https://github.com/jarys/redjubjub/tree/no-std-alloc) |
| [fpe](https://github.com/str4d/fpe) | ✔️ [PR](https://github.com/str4d/fpe/pull/21) | 
| poseidon | ✔️ in orchard |

## Sinsemilla

Sinsemilla design is based 64kB precomputed table. For future memory optimizations, we made a bechmark of 'table-less' version of Sinsemilla. Hashing speed is approx. 100bits/second, resulting in 11s per 1 Action commitment.

## trezor-firmaware

Trezor firmware were extended by

- zcash python module
- zcash Rust module
- trezorctl zcash commands
- zcash diagnostic protobuf messages

See (comparison)[https://github.com/trezor/trezor-firmware/compare/master...jarys:zcash].

