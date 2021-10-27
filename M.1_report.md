# M.1. Summary

We are glad to announce the submission of milestone M.1. During past two months we

- analyzed design and memory and computational requirements of all Zcash primitives
- explored transaction shielding and authorization data flows
- added basic structure of zcash app into trezor-firmware monolith
- enabled alloc feature on Trezor to facilitate orchard crate import
- added no_std+alloc support for all necessary Orchard crates

This effort results in direct import of orchard crate into Trezor, including all necessary primitives and schemes like key generator, action commitment or transaction signing.

So far, we import all necessary primitives from fully tested crates, so writing our own unit tests would be superfluous.

Finally we are excited to announce that we are nowhere far from submission of M.2.

# M.1 Detailed

### no_std+alloc support

| crate | no_std+alloc |
| -       | -            |
| [f4jumble](https://github.com/zcash/librustzcash/tree/master/components/f4jumble) | ✔️ [PR](https://github.com/zcash/librustzcash/pull/446) |
| [zcash_note_encryption](https://github.com/zcash/librustzcash/tree/master/components/zcash_note_encryption) | ✔️ [PR](https://github.com/zcash/librustzcash/pull/450) |
| [orchard](https://github.com/zcash/orchard) | ✔️ [branch](https://github.com/jarys/orchard/tree/no-std-alloc), [issue](https://github.com/zcash/orchard/issues/211) |
| [pasta_curves](https://github.com/zcash/pasta_curves) | ✔️ [PR](https://github.com/zcash/pasta_curves/pull/21) |
| [reddsa](https://github.com/str4d/redjubjub) | ✔️ [branch](https://github.com/jarys/redjubjub/tree/no-std-alloc) |
| [fpe](https://github.com/str4d/fpe) | ✔️ [PR](https://github.com/str4d/fpe/pull/21) |
| poseidon | ✔️ in orchard |
| [bech32m](https://github.com/rust-bitcoin/rust-bech32) | ✔️ |

### Sinsemilla

Sinsemilla's design is based on a 64kB precomputed table. For future memory optimizations, we made a benchmark of the 'table-less' version of Sinsemilla. Hashing speed is approx. 100 bits/second, resulting in 11s per 1 Action commitment.

### Trezor firmware

Trezor firmware was extended by

- zcash python module
- zcash Rust module
- trezorctl zcash commands
- zcash diagnostic protobuf messages

See [comparison](https://github.com/trezor/trezor-firmware/compare/master...jarys:zcash).

Also we implemented the `alloc` feature using [`static-alloc`](https://crates.io/crates/static-alloc) crate and 8kB static array. Unfortunately this requires the `alloc_error_handler` feature, which is currently unstable \[[issue](https://github.com/rust-lang/rust/issues/66740)\]. Avoiding unstable Rust is subject of future enhancements.

### Documentation

I described signing protocol, security model, action shielding dataflow and other project related stuff in (work in progress) [project documentation](https://github.com/jarys/ztrezor/blob/main/doc/README.md). 
