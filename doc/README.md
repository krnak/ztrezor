:warning: This document is work in progress. :warning:

# Trezor support for Zcash shielded transaction  

## Introduction  

The goal of this document is to explain how Zcash Orchard shielded transactions are implemented in Trezor.

## Notation

I use `inline code font` for names of types and variables. I write `type[n]` for an array of type `type` and length `n`. I write only `type[]`, if the length of the array is obvious from the context.

I ilustrate some schemes with pseudocode, where `:=` denotes a definition, `||` denotes concatenation and `[x]G` denotes multiplication of point `G` by scalar `x`.

## Structure of this document

This document has two sections:

[Zcash overview]("zcash_overview.md") section gives basic overview of Zcash technology and it explains related terms. It has sections:

[Implementation]("implementation.md") section describes implementation of shielded transaction into trezor.
