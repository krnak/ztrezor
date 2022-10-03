F = GF(2)
Q = PolynomialRing(F, 'y', 80)
y = Q.gens()
R.<x> = PolynomialRing(Q, 'x')
q = x^80 + x^62 + x^51 + x^38 + x^23 + x^13 + 1  # modulus

state = sum(y[i]*x^i for i in range(80))

def next():
    global state
    new_bit = list(state)[-1] if len(list(state)) > 79 else F(0)
    state *= x
    state %= q
    return new_bit

stream = [fnext() for _ in range(80)]
M = Matrix(F, [[row.coefficient(y_i) for y_i in y] for row in stream])
OUT = vector(F, [F(int(x)) for x in "10111101101101011010100101111101010010000001001101001011010110100001111110000011"])
state0 = M \ OUT

state = state0
stream = [fnext() for _ in range(80)]
assert vector(F, stream) == OUT
