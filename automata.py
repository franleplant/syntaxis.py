# -*- coding: UTF-8 -*-

TRAP_STATE = "trap_state"
def to_delta_map(delta, states, alphabet, trap_state = TRAP_STATE):
    delta_inner = { s: { a: set([TRAP_STATE]) for a in alphabet} for s in states }
    for (s, c), ns in delta:
        # Only put delta transitions if they are present
        if c == "λ":
            delta_inner.get(s)[c] = set([])
        next_states = delta_inner[s][c]

        if TRAP_STATE in next_states:
            next_states.remove(TRAP_STATE)

        next_states.add(ns)
        delta_inner[s][c] = next_states

    return delta_inner



class Automata:
    def __init__(self, alphabet, states, delta, initial, final, trap_state = TRAP_STATE):
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

        states.append(trap_state)

        self.alphabet = alphabet
        self.states   = states
        self.delta    = to_delta_map(delta, states, alphabet, trap_state)
        self.initial  = initial
        self.final    = final

        self.state    = self.initial

    def next(self, char):
        if not char in self.alphabet:
            return False

        next_states = self.get_next_states(self.state, char)
        if len(next_states) > 1:
            print("None deterministic automata!!!")
        elif len(next_states) == 0:
            print("Not transitions available for this symboles")

        self.state = next_states[0]

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

    def get_next_states(self, current_state, char):
        default = {}
        ret = self.delta.get(current_state, default).get(char, default)
        return list(ret)

    def pprint(self):
        print("Automata")
        print("--------")
        print("States   {}".format(self.states))
        print("Alphabet {}".format(self.alphabet))
        print("Initial  {}".format(self.initial))
        print("Final    {}".format(self.final))
        print("Delta")
        for key, value in self.delta.items():
            print(key, value)




def test_automata():
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

    automata = Automata(
            alphabet = alphabet,
            states = states,
            delta = delta,
            initial = initial,
            final = final
            )

    assert automata.check_string("ababa") == True
    assert automata.check_string("ababc") == False
    assert automata.check_string("aab") == False


