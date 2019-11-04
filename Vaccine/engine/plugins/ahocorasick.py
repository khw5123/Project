# -*- coding:utf-8 -*-

FAIL = -1

class aho_corasick:
    def __init__(self):
        self.transitions = {}
        self.outputs = {}
        self.fails = {}

    def make_tree(self, keywords):
        new_state = 0
        for keyword in keywords:
            state = 0
            for j, char in enumerate(keyword):
                res = self.transitions.get((state, char), FAIL)
                if res == FAIL:
                    break
                state = res
            for char in keyword[j:]:
                new_state += 1
                self.transitions[(state, char)] = new_state
                state = new_state
            self.outputs[state] = [keyword]
        queue = []
        for (from_state, char), to_state in self.transitions.items():
            if from_state == 0 and to_state != 0:
                queue.append(to_state)
                self.fails[to_state] = 0
        while queue:
            r = queue.pop(0)
            for (from_state, char), to_state in self.transitions.items():
                if from_state == r:
                    queue.append(to_state)
                    state = self.fails[from_state]
                    while True:
                        res = self.transitions.get((state, char), state and FAIL)
                        if res != FAIL:
                            break
                        state = self.fails[state]
                    failure = self.transitions.get((state, char), state and FAIL)
                    self.fails[to_state] = failure
                    self.outputs.setdefault(to_state, []).extend(self.outputs.get(failure, []))

    def search(self, string):
        state = 0
        results = []
        for i, char in enumerate(string):
            while True:
                res = self.transitions.get((state, char), state and FAIL)
                if res != FAIL:
                    state = res
                    break
                state = self.fails[state]
            for match in self.outputs.get(state, ()):
                pos = i - len(match) + 1
                results.append((pos, match))
        return results
