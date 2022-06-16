# Suite requirements

## Features

**address generation:** User can generate three types of Zcash addresses:
transparent, pure orchard-shielded and unified (transparent + orchard-shielded). Unified address is default.

**memos:** User can attach a memo (512 bytes message for a recipient) to every shielded output.

**autoshieding:** User can send all his transparent funds to his shielded address by clicking a button.

## Technical requirements

**lightwalletd:** SL must run a [lightwalletd](https://github.com/zcash/lightwalletd) full node backend.

**librustzcash:** Suite app must be able to use functionalitis from [librustzcash](https://github.com/zcash/librustzcash) library.

**database:** Suite scans blockchain for incoming transaction and stores them in a database. One shielded UTXO is about 1kb.

## Related

adityapk00 leaves zecwallet:
https://forum.zcashcommunity.com/t/future-of-zecwallet/41681

Orchard support for zecwallet:

- not approved grant: https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134
- in progress work: https://github.com/zingolabs/zecwalletlitelib/pull/76

Zingolabs overtake zecwallet
https://forum.zcashcommunity.com/t/zecwallet-and-orchard/42134/5
https://github.com/zingolabs/zecwalletlitelib
