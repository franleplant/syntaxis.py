def print_res(res):
    if res:
        print("accepted")
    else:
        print("rejected")

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
            if not c in alphabet:
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

        for rule, ns in delta:
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

def test_fsa():
    assert fsa.check_string("ababa") == True
    assert fsa.check_string("ababc") == False
    assert fsa.check_string("aab") == False
