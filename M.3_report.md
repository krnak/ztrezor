# M.3. Summary

We are glad to announce the submission of milestone M.3. This is what we've done:

- Trezor now supports v5 transaction format specified in ZIP-244.
- Interface for `pasta_curves` crate was added.
- Necessary Orchard primitives and schemes were re-implemented to fit the Trezor constrained environment.
- Signing protocol for shielded transaction was designed with these properties:
    - Amount of shielded inputs and outputs per transaction is not limited by the protocol.
    - Signing process and proof computation process can be parallelized.
    - Outputs are reviewed in order they were entered by the user.
    - All randomness required for transaction shielding is derived deterministically, which minimizes communication cost and adds some extra security.
- This signing protocol was implemented as an extension of the current signing protocol for transparent transactions.
- Python module `trezorlib` was extended to support signing shielded transactions and getting viewing keys and shielded addresses.
- Trezor terminal client was extended to support getting viewing keys and shielded addresses.
- Device tests for getting shielded addresses and viewing keys were added.
- Device tests for signing shielded transactions (with test cases accepted by testnet) were added.
- Signing protocol was documented and illustrated [[3][3]].

At the moment, all new code related to shielded transactions is in the form of two pull requests [[1][1]],[[2][2]]. These PRs will be merged after merging some major UI and core Trezor firmware upgrades from the end 2022.

This closes the work on Trezor firmware and starts work on Trezor Suite in M.4.

[1]: https://github.com/trezor/trezor-firmware/pull/2510
[2]: https://github.com/trezor/trezor-firmware/pull/2472
[3]: https://github.com/jarys/ztrezor/blob/main/doc/implementation.md#sign-transaction-flow

# M.3 Detailed

## Why did this take so much time?

- Orchard deployment got delayed by 8 months.
- After several attempts to make `orchard` crate no-std compatible and use it directly, I decided to re-implement it in micropython instead to fit the Trezor constrained environment.
- There didn't exist a fully functional Orchard wallet till October 2022*. Thus I had to develop a lot of support tools to test the app.
- I had to slow down, because I also didn't expect that reaching M.3 was going to take so much time and it started colliding with my personal life.

\* `zcash-cli` wallet was working earlier, but using it would require me to understand and modify its architecture and learn C.

## Lessons learnt

- HWW serves as second factor authorization for a desktop or mobile wallet. Thus it is very inappropriate to develop HWW app before the existence of a desktop/mobile wallet app.
- Due to the design of Sinsemilla commitments, Orchard is not really compatible with hardware wallets. To verify a Sinsemilla commitment, the device must either store a 64kb large precomputed table, or compute inputs of this table, which is computationally demanding. We were able to implement Orchard on Trezor T whose memory and computation power is sufficient. But it will be challenging to implement Orchard in more constrained environments like Trezor 1 and Ledger S. (For comparison, windowed Pederson commitments used in Sapling protocol are lightweight in terms of memory and computation.)
- Since Zcash has very good cryptographic documentation, it was simple to reimplement the Orchard protocol according to HWW needs.
- I could have started with 2-inputs-2-outputs transactions to get a minimum viable product earlier.

## Can I use Trezor for storing my shielded funds now?

No. Wait for a desktop app, which will do the job for you.

Submitting an Orchard shielded transaction requires more than just signing it. It requires blockchain scanning and zero knowledge proof computation.

Using Trezor T as a shielded Zcash storage now would require:
1. Compiling and uploading the Trezor firmware from the branch [[2][2]] on your own.
1. Scanning Zcash blockchain for spendable notes. I do use [modification](https://github.com/jarys/zingolib/tree/trezor) of `zingolib`, which gives me an additional note context (anchor, Merkle tree path, note rseed...).
1. Composing and signing a transaction via Python tools `trezorlib`.
1. Rebuilding the Orchard bundle by [`trezor_orchard`](https://github.com/jarys/trezor_orchard) crate.
1. Computing the authorizing zk-proof. I use [`py-trezor-orchard`](https://github.com/jarys/py-trezor-orchard) module to be able to automate everything from Python.
1. Sending the transaction to the network. I use the `grpcurl` command.

## What's next

Our plan is to extend `zingolib` to support splitted viewing and spending authority. Then we can use it for blockchain scanning. New messages and protocol will be added to Trezor Connect and a new "Zcash shielded account" with an appropriate GUI will be added to Trezor Suite. Finally, we will bind the Rust `orchard` crate to the javascript Trezor Suite via ffi to be able to compute proofs.
