from collections import deque

class BinarySearchTree:
    def __init__(self, root_value=None):
        self.keys = []
        self.root = None
        if root_value is not None:
            self.root = TreeNode(root_value)
            self.keys.append(root_value)

    def __iter__(self):
        if self.root is None:
            return
        nodes = deque([self.root])
        while nodes:
            node = nodes.popleft()
            yield node.value
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)

    def __contains__(self, value):
        return value in self.keys

    def append(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            self.keys.append(value)
        elif value in self.keys:
            return self
        else:
            self._insert_tree_node(self.root, value)

    def _insert_tree_node(self, current_node, value):
        if(value <= current_node.value):
            if(current_node.left):
                self._insert_tree_node(current_node.left, value)
            else:
                current_node.left = TreeNode(value)
                self.keys.append(value)
        elif(value > current_node.value):
            if(current_node.right):
                self._insert_tree_node(current_node.right, value)
            else:
                current_node.right = TreeNode(value)
                self.keys.append(value)
        
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


if __name__ == '__main__':
    tree = BinarySearchTree()
    for v in [8, 3, 10, 1, 6, 4, 14, 13, 7]:
        tree.append(v)

    for v in [8, 12, 13]:
        print(v in tree)

    print(*tree)

    tree = BinarySearchTree()
    for v in [0, 6]:
        print(v in tree)