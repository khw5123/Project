class Node(object):
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.pass_count = 0
        self.children = {}

class Trie(object):
    def __init__(self):
        self.head = Node(None)

    def insert(self, string):
        curr_node = self.head
        for char in string:
            curr_node.pass_count += 1
            if char not in curr_node.children:
                curr_node.children[char] = Node(char)
            curr_node = curr_node.children[char]
        curr_node.pass_count += 1
        curr_node.data = string

    def search(self, string):
        curr_node = self.head
        for char in string:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return False
        if curr_node.pass_count == 1:
            return True
        else:
            return False

def solution(words):
    answer = 0
    trie = Trie()
    for word in words:
        trie.insert(word)
    for word in words:
        tmp = True
        for i in range(1, len(word)+1):
            if trie.search(word[:i]):
                answer += i
                tmp = False
                break
        if tmp:
            answer += len(word)
    return answer