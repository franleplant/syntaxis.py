# -*- coding: UTF-8 -*-

#TODO: change the nams of the machine tuple to fit the theoretical def
class Automata:
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
        next_states = []
        for rule, ns in self.delta:
            if rule == (current_state, char):
                next_states.append(ns)

        return next_states

    def pprint(self):
        print("Automata")
        print("--------")
        print("States   {}".format(self.states))
        print("Alphabet {}".format(self.alphabet))
        print("Initial  {}".format(self.initial))
        print("Final    {}".format(self.final))
        print("Delta")
        for rule in self.delta:
            print(rule)




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


