# M.3. Summary

We are glad to announce the submission of milestone M.3. This is what we've done:

- Trezor now supports v5 transaction format specified in ZIP-244.
- Interface for pasta_curves crate was added.
- Necessary Orchard primitives and schemes were re-implemented to fit the Trezor constrained environment.
- Signing protocol for shielded transaction was designed with theses properties:
- - Amount of shielded inputs and outputs per transaction is not limited by the protocol.
- - Signing process and proof computation process can be parallelized.
- - Outputs are reviewed in order they were entered by the user.
- - All randomness required for transaction shielding is derived deterministically, which minimizes communication cost and adds some extra security.
- The new signing protocol was implemented as an extension of the current signing protocol for transparent transactions.
- Python module `trezorlib` was extended to support signing shielded transactions and getting viewing keys and shielded addresses.
- Trezor terminal client was extended to support getting viewing keys and shielded addresses. 
- Device tests for getting shielded addresses and viewing keys were added.
- Device tests for signing shielded transactions (with test cases accepted by testnet) were added.
- Signing protocol was documented and illustrated.

At the moment, all new code related to shielded transactions is in the form of two pull requests [1][1],[2][2]. These PRs will be merged after merging some major UI and core Trezor firmware upgrades from the end 2022.

This closes the work on Trezor firmware and starts work on Trezor Suite in M.4.

[1]: https://github.com/trezor/trezor-firmware/pull/2510
[2]: https://github.com/trezor/trezor-firmware/pull/2472

# M.3 Detailed

TODO
