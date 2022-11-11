from hashlib import blake2b


def gen(ti, to, oi, oo, ss):
    rng = BundleShieldingRng(ss)
    actions_count = 0 if len(oi) + len(oo) == 0 else max(2, len(oi), len(oo))

    for i in range(len(ti)):
        yield f"request_input({i}),"

    for i in range(len(oi)):
        yield f"request_orchard_input({i}),"

    for i, txo in enumerate(to):
        yield f"request_output({i}),"
        if txo.address is not None:
            yield "ButtonRequest(code=B.ConfirmOutput),"

    for i, txo in enumerate(oo):
        yield f"request_orchard_output({i}),"
        if txo.address is not None:
            yield "ButtonRequest(code=B.ConfirmOutput)"

    if len(oi) > 8:  # dust inputs
        pass  #TODO

    yield "ButtonRequest(code=B.SignTx),"
    if actions_count > 0:
        yield "request_no_op(),  # shielding seed"

    oi_indices = pad(list(range(len(oi))), actions_count)
    oo_indices = pad(list(range(len(oo))), actions_count)
    rng.shuffle_inputs(oi_indices)
    rng.shuffle_outputs(oo_indices)

    for i, (j, k) in enumerate(zip(oi_indices, oo_indices)):
        if j is not None:
            yield f"request_orchard_input({j}),"
        if k is not None:
            yield f"request_orchard_output({k}),"

    returns = ""
    for i in range(len(ti)):
        yield f"request_input({i}),{returns}"
        returns = f"  # t-signature {i}"

    for i in range(len(to)):
        yield f"request_output({i}),{returns}"
        returns = ""

    for i, j in enumerate(oi_indices):
        if j is not None:
            if returns:
                yield f"request_no_op(),{returns}"
            returns = f"  # returns o-signature of o-input {j} in action {i}"

    yield f"request_finished(),{returns}"


def pad(x, l):
    return x + (l - len(x)) * [None]


def chunks(x, l):
    assert len(x) % l == 0
    for i in range(len(x) // l):
        yield x[l * i: l * (i + 1)]


class BundleShieldingRng:
    def __init__(self, seed: bytes) -> None:
        self.seed = seed

    def shuffle_inputs(self, inputs: list[int | None]) -> None:
        rng = self._blake2b_ctr_mode_rng(personal=b"Inps_Permutation")
        _shuffle(inputs, rng)

    def shuffle_outputs(self, outputs: list[int | None]) -> None:
        rng = self._blake2b_ctr_mode_rng(personal=b"Outs_Permutation")
        _shuffle(outputs, rng)

    def _blake2b_ctr_mode_rng(self, personal: bytes):
        i = 0
        while True:
            h = blake2b(person=personal, digest_size=64)
            h.update(self.seed)
            h.update(i.to_bytes(4, "little"))
            digest = h.digest()
            for chunk in chunks(digest, 4):
                yield int.from_bytes(chunk, "little")
            i += 1


MAX = 0xFFFF_FFFF


def _sample_uniform(n, rng):
    """Samples unifomly an element of `range(n)`."""
    while True:
        wide = next(rng) * n
        high = wide >> 32
        low = wide & MAX
        if low <= MAX - n or low <= MAX - (MAX - n) % n:
            return high


def _shuffle(x, rng) -> None:
    # Fisher-Yates shuffle
    for i in range(len(x) - 1, 0, -1):
        j = _sample_uniform(i + 1, rng)
        x[i], x[j] = x[j], x[i]
