# -*- coding: UTF-8 -*-
from automata import Automata

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
    res = [
        "{" + ",".join(automata.states) + "}",
        "{" + ",".join(automata.alphabet) + "}",
        "{" + automata.initial + "}",
        "{" + ",".join(automata.final) + "}"
    ]


    delta = []
    for state in automata.states:
        state_text = state
        for (s, a), ns in automata.delta:
            if state == s:
                if a == "λ":
                    a = "&"
                state_text += a + ns
        delta.append(state_text + "#")

    res.append("\n".join(delta))



    text = "\n".join(res)

    file = open(path, "w")
    file.write(text)
    file.close()

    return text



def test__read_automata():
    automata = read_automata('./ej-especif-aut.txt')
    assert set(automata.states) == set(["0","1","2"])
    assert set(automata.alphabet) == set(["a","b"])
    assert automata.initial == "0"
    assert set(automata.final) == set(["1","2"])
    delta = [
        (('0', 'a'), '1'),
        (('0', 'b'), '2'),
        (('0', 'λ'), '0'),
        (('1', 'a'), '1'),
        (('1', 'b'), '0'),
        (('2', 'a'), '2'),
        (('2', 'b'), '2')
    ]
    assert set(automata.delta) == set(delta)

def test__write_automata():
    input_path = './ej-especif-aut.txt'
    output_path = './test_tmp'
    automata = read_automata(input_path)
    output = write_automata(output_path, automata).split("\n")

    input = open(input_path, 'r').read().split("\n")
    for i in range(0, len(input) - 1):
        assert output[i].strip() == input[i].strip()




