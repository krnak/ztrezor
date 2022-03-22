# 4.2.2022

### ZIP-244

ZIP-244 was modified to be more friendly to HWWs

### orchard

zcash/orchard crate was extended to support HWWs

### pyorchard

I made a python wrapper for orchard crate to access its functionalities directly from python.

### reddsa

reddsa is the signature scheme for zcash shielded transactions

reddsa crate was extended to support HWWs

### trezor-firmware

was extended to support

- v5 transaction format
- orchard shielded inputs and outputs

in more details

- review shielded output on display
- new tx signing workflow
- Orchard commitments verification
- synchronization of some randomness generators
- ZIP-244 tx identifier and sighash implementation
- reddsa implementation

further I

- refactored code
- reimplemented OrchardKeychain






