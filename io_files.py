# -*- coding: UTF-8 -*-
from automata import Automata, TRAP_STATE


def norm_trap_state(state):
    if state == TRAP_STATE:
        return "T"
    return state

# TODO: read/write grammar

def read_automata(path):
    f = open(path, 'r')
    text = f.readlines()

    states = text[0].strip().strip('{}').split(",")
    alphabet = text[1].strip().strip('{}').split(",")
    initial = text[2].strip().strip('{}')
    final = text[3].strip().strip('{}').split(",")

    delta = []
    for line in text[4:]:
        line = line.replace("#", "").strip()
        s = line[0]
        for i in range(1, len(line), 2):
            [a, ns] = line[i: i+2]
            if a == '&':
                a = 'λ'
            delta.append( ((s, a), ns) )

    automata = Automata(
        alphabet = alphabet,
        states = states,
        delta = delta,
        initial = initial,
        final = final
    )

    return automata

def write_automata(path, automata):
    pretty_states = list(automata.states)
    i = pretty_states.index(TRAP_STATE)
    pretty_states[i] = "T"
    res = [
        "{" + ",".join(pretty_states) + "}",
        "{" + ",".join(automata.alphabet) + "}",
        "{" + automata.initial + "}",
        "{" + ",".join(automata.final) + "}"
    ]


    delta = []
    for state in sorted(automata.delta.keys()):
        state_text = norm_trap_state(state)
        delta_value = automata.delta[state]
        for char in sorted(delta_value.keys()):
            next_states = delta_value[char]
            if char == "λ": char = "&"
            for ns in next_states:
                state_text += char + norm_trap_state(ns)
        delta.append(state_text + "#")


    res.append("\n".join(delta))
    text = "\n".join(res)

    file = open(path, "w")
    file.write(text)
    file.close()

    return text



def test__read_automata():
    delta = [
        (('0', 'a'), '1'),
        (('0', 'b'), '2'),
        (('0', 'λ'), '0'),
        (('1', 'a'), '1'),
        (('1', 'b'), '0'),
        (('2', 'a'), '2'),
        (('2', 'b'), '2')
    ]

    expected_automata = Automata(
        alphabet = ["a","b"],
        states = ["0","1","2"],
        delta = delta,
        initial = "0",
        final = ["1","2"]
    )
    actual_automata = read_automata('./ej-especif-aut.txt')

    assert set(actual_automata.states) == set(expected_automata.states)
    assert set(actual_automata.alphabet) == set(expected_automata.alphabet)
    assert actual_automata.initial == expected_automata.initial
    assert set(actual_automata.final) == set(expected_automata.final)
    assert set(actual_automata.delta) == set(expected_automata.delta)

def test__write_automata():
    output_path = './test_tmp'
    delta = [
        (('0', 'a'), '1'),
        (('0', 'b'), '2'),
        (('0', 'λ'), '0'),
        (('1', 'a'), '1'),
        (('1', 'b'), '0'),
        (('2', 'a'), '2'),
        (('2', 'b'), '2')
    ]

    m = Automata(
        alphabet = ["a","b"],
        states = ["0","1","2"],
        delta = delta,
        initial = "0",
        final = ["1","2"]
    )



    output = write_automata(output_path, m).split("\n")

    assert output[0].strip().strip('{}') == "0,1,2,T"
    assert output[1].strip().strip('{}') == "a,b"
    assert output[2].strip().strip('{}') == "0"
    assert output[3].strip().strip('{}') == "1,2"
    # Delta
    assert output[4].strip() == "0a1b2&0#"
    assert output[5].strip() == "1a1b0#"
    assert output[6].strip() == "2a2b2#"
    assert output[7].strip() == "TaTbT#"




