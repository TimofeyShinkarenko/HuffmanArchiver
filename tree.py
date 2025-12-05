from queue import PriorityQueue

from node import Node


class FrequencyTree:
    def __init__(self, freq_dict: dict):
        self.node_queue = self.make_node_queue_from_dict(freq_dict)
        self.root = None
        self.codes = {}

    @staticmethod
    def make_node_queue_from_dict(freq_dict) -> PriorityQueue:
        priority_queue = PriorityQueue()
        for symbol, count in freq_dict.items():
            node = Node(symbol, count)
            priority_queue.put((count, node))

        return priority_queue

    def make_tree(self):
        while self.node_queue.qsize() > 1:
            weight1, node1 = self.node_queue.get()
            weight2, node2 = self.node_queue.get()

            merged_weight = weight1 + weight2
            merged_node = Node(None, merged_weight)

            merged_node.left = node1
            merged_node.right = node2

            self.node_queue.put((merged_weight, merged_node))

        if not self.node_queue.empty():
            _, self.root = self.node_queue.get()

    def generate_codes(self):
        self.generate_codes_helper(self.root, "")
        return self.codes

    def generate_codes_helper(self, node, current_code):
        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = current_code
            return

        self.generate_codes_helper(node.left, current_code + "0")
        self.generate_codes_helper(node.right, current_code + "1")
