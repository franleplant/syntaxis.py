
# -*- coding: UTF-8 -*-

class Fsa:
    def __init__(self, alphabet, states, delta, initial, final):
        # Final should be a subset of States
        for f in final:
            if not f in states:
                raise BaseException("final should be subset of states set")

        # Initial should be a state
        if not initial in states:
            raise BaseException("initial should belong to the states set")

        # All components in delta should belong to their own sets
        for (s, c), ns in delta:
            if not s in states:
                raise BaseException("states in delta should belong to states set")
            if c != "λ" and not c in alphabet:
                raise BaseException("char in delta should belong to alphabet set")
            if not ns in states:
                raise BaseException("states in delta should belong to states set")

        self.alphabet = alphabet
        self.states   = states
        self.delta    = delta
        self.initial  = initial
        self.final    = final

        self.state    = self.initial

    def next(self, char):
        if not char in self.alphabet:
            return False

        next_state = self.state

        for rule, ns in self.delta:
            if rule == (self.state, char):
                next_state = ns

        self.state = next_state

        return True


    def end(self):
        res = False

        if self.state in self.final:
            res = True

        self.state = self.initial

        return res

    def check_string(self, string):
        for char in string:
            if not self.next(char):
                return False
        return self.end()




def test_fsa():
    delta = [
        (("q0", "a"), "q1"),
        (("q0", "b"), "q0"),
        (("q1", "a"), "q0"),
        (("q1", "b"), "q1")
    ]
    states   = ["q0", "q1"]
    final    = ["q1"]
    alphabet = ["a", "b"]
    initial  = "q0"

    fsa = Fsa(
            alphabet = alphabet,
            states = states,
            delta = delta,
            initial = initial,
            final = final
            )

    assert fsa.check_string("ababa") == True
    assert fsa.check_string("ababc") == False
    assert fsa.check_string("aab") == False


def lambda_closure(Q, m):
    L = set(Q)
    marked = set([])
    while L != marked:
        for t in (L - marked):
            marked.add(t)
            for rule, ns in m.delta:
                if rule == (t, "λ"):
                    L.add(ns)

    return list(L)

def test_lambda_closure():
    delta = [
        (("q0", "a"), "q1"),
        (("q0", "b"), "q0"),
        (("q1", "λ"), "q2")
    ]
    states   = ["q0", "q1", "q2"]
    final    = ["q1"]
    alphabet = ["a", "b"]
    initial  = "q0"

    fsa = Fsa(
            alphabet = alphabet,
            states = states,
            delta = delta,
            initial = initial,
            final = final
            )

    L = lambda_closure(["q1"], fsa)
    assert L == ["q1", "q2"]



def mover(T, a, m):
    L = set([])
    for t in T:
        for rule, ns in m.delta:
            if rule == (t, a):
                L.add(ns)

    return lambda_closure(L, m)




def test_mover():
    delta = [
        (("q0", "a"), "q1"),
        (("q0", "b"), "q0"),
        (("q1", "λ"), "q2")
    ]
    states   = ["q0", "q1", "q2"]
    final    = ["q1"]
    alphabet = ["a", "b"]
    initial  = "q0"

    fsa = Fsa(
            alphabet = alphabet,
            states = states,
            delta = delta,
            initial = initial,
            final = final
            )

    L = mover(["q0"], "a", fsa)
    assert L == ["q1", "q2"]



def stateset_name(states):
    return "".join(sorted(states))

def test_stateset_name():
    res = stateset_name(["q2", "q1"])
    assert res == "q1q2"

