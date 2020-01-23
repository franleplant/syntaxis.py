# -*- coding: UTF-8 -*-

from automata import Automata, TRAP_STATE

def beautify_automata(m):
    new_states = range(len(m.states))
    new_initial = m.states.index(m.initial)
    new_final = [ m.states.index(f) for f in m.final]
    new_trap_state = m.states.index(TRAP_STATE)

    new_delta = []
    for s in m.states:
        delta_value = m.delta.get(s)
        for a, nss in delta_value.items():
            for ns in nss:
                new_delta.append( ((m.states.index(s), a), m.states.index(ns)) )



    return Automata(
        alphabet = m.alphabet,
        states = new_states,
        delta = new_delta,
        initial = new_initial,
        final = new_final,
        trap_state = new_trap_state
    )



# TODO:
# - automata -> min automata

#TODO: beautify code
def remove_inaccesible_states(m):
    """ remove all inaccesible states from automata m
    """

    states = m.states
    n = range(len(states))
    T = [[0 for j in n] for i in n]

    # Relationship Matrix
    for i in n:
        for j in n:
            qi = states[i]
            qj = states[j]
            iRj = 0

            for a in m.alphabet:
                if qj in m.get_next_states(qi, a):
                    iRj = 1
            T[i][j] = iRj


    # Calculate Warshal on the relation matrix
    for k in n:
        for i in n:
            for j in n:
                T[i][j] = T[i][j] or ( T[i][k] and T[k][j] )


    # Get reachable states
    initial_state_index = states.index(m.initial)
    new_states = []
    # this row shows which states are reachable from the initial state (def of accesibility)
    reachable_states = T[initial_state_index]
    for j in range(len(reachable_states)):
        is_qj_reachable = reachable_states[j]
        if is_qj_reachable == 1:
            new_states.append(states[j])



    #remove transitions from inaccesible states
    new_delta = list(filter(lambda rule: (rule[0][0] in new_states), m.delta))

    return Automata(
        alphabet = m.alphabet,
        states = list(set(new_states)),
        delta = new_delta,
        initial = m.initial,
        final = m.final
    )

def test_remove_inaccesible_states():
    delta = [
        (("q0", "a"), "q1"),
        (("q0", "b"), "q0"),
        (("q1", "a"), "q0"),
        (("q1", "b"), "q2"),
        (("inaccesible", "b"), "inaccesible")
    ]
    states   = ["q0", "q1", "q2", "inaccesible"]
    final    = ["q1"]
    alphabet = ["a", "b"]
    initial  = "q0"

    m = Automata(
        alphabet = alphabet,
        states = states,
        delta = delta,
        initial = initial,
        final = final
    )

    m = remove_inaccesible_states(m)

    assert set(m.states) == set(['q0', 'q1', 'q2', 'trap_state'])
    #TODO: fix
    #assert m.delta == [(('q0', 'a'), 'q1'), (('q0', 'b'), 'q0'), (('q1', 'a'), 'q0'), (('q1', 'b'), 'q2')]



def test_beautify_automata():
    delta = [
        (("q0", "a"), "q1"),
        (("q0", "b"), "q0"),
        (("q1", "a"), "q0"),
        (("q1", "b"), "q2"),
        (("inaccesible", "b"), "inaccesible")
    ]
    states   = ["q0", "q1", "q2", "inaccesible"]
    final    = ["q1"]
    alphabet = ["a", "b"]
    initial  = "q0"

    m = Automata(
        alphabet = alphabet,
        states = states,
        delta = delta,
        initial = initial,
        final = final
    )


    # TEST! TODO
    m1 = beautify_automata(m)
    print("UUUUUUU")
    m1.pprint()


