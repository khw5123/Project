import sys
sys.setrecursionlimit(10**6)

class Node(object):
    def __init__(self, data, value):
        self.data = data
        self.value = value
        self.left = self.right = None

class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert_value(self.root, data)
        return self.root is not None

    def _insert_value(self, node, data):
        if node is None:
            node = Node(data, data[2])
        else:
            if data[0] <= node.data[0]:
                node.left = self._insert_value(node.left, data)
            else:
                node.right = self._insert_value(node.right, data)
        return node

    def pre_order_traversal(self, answer):
        def _pre_order_traversal(root):
            if root is None:
                pass
            else:
                answer[-1].append(root.value)
                _pre_order_traversal(root.left)
                _pre_order_traversal(root.right)
        _pre_order_traversal(self.root)

    def post_order_traversal(self, answer):
        def _post_order_traversal(root):
            if root is None:
                pass
            else:
                _post_order_traversal(root.left)
                _post_order_traversal(root.right)
                answer[-1].append(root.value)
        _post_order_traversal(self.root)

def solution(nodeinfo):
    answer = [[]]
    for i in range(len(nodeinfo)):
        nodeinfo[i].append(i+1)
    nodeinfo.sort(key=lambda x:(-x[1], x[0]))
    bst = BinarySearchTree()
    for node in nodeinfo:
        bst.insert(node)
    bst.pre_order_traversal(answer)
    answer.append([])
    bst.post_order_traversal(answer)
    return answer