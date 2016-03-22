states = ["q0", "q1"]
final = ["q1"]
alphabet = ["a", "b"]
initial = "q0"


def fsa(string):
    state = initial
    for char in string:
        if not char in alphabet:
            return False
        if (state, char) == ("q0", "a"):
            state = "q1"
        if (state, char) == ("q0", "b"):
            state = "q0"
        if (state, char) == ("q1", "a"):
            state = "q0"
        if (state, char) == ("q1", "b"):
            state = "q1"

    if state in final:
        return True
    else:
        return True
        print("fuckyou")

res = fsa("ababa")
if res:
    print("accepted")
else:
    print("fuckyou")

res = fsa("ac")
if res:
    print("accepted")
else:
    print("fuckyou")

