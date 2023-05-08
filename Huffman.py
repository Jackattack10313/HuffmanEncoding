import heapq


class Node:
    value = None
    left = None
    right = None

    def __init__(self, value):
        self.value = value

    def isLeaf(self):
        return self.left is None and self.right is None

    def getValue(self):
        return self.value

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def hasLeft(self):
        return self.left is not None

    def hasRight(self):
        return self.right is not None

    # Only will be adding trees to left or right of new node
    def insertLeft(self, left):
        self.left = left

    def insertRight(self, right):
        self.right = right

    def __lt__(self, other):
        return self.value[1] < other.value[1]


def get_codes_helper(curr_node, code):
    if curr_node.isLeaf():
        code_dict[curr_node.getValue()[0]] = code
    else:
        if curr_node.hasLeft():
            get_codes_helper(curr_node.getLeft(), code + "0")
        if curr_node.hasRight():
            get_codes_helper(curr_node.getRight(), code + "1")


def load_file():
    valid = False
    global filename
    while not valid:
        try:
            filename = input("Enter the name of .txt file (without extension): ")
            read = open(filename + ".txt")
            valid = True
        except:
            print("Invalid filename!")

    global file_string
    file_string = read.read()
    for i in file_string:
        if i not in frequency_dict:
            frequency_dict[i] = 1
        else:
            frequency_dict[i] += 1
    for i in frequency_dict:
        working_nodes.append(Node((i, frequency_dict[i])))


def encode():
    while len(working_nodes) > 1:
        left = heapq.heappop(working_nodes)
        right = heapq.heappop(working_nodes)
        new_node = Node(("-", (left.getValue()[1] + right.getValue()[1])))
        new_node.insertLeft(left)
        new_node.insertRight(right)
        heapq.heappush(working_nodes, new_node)

    node = heapq.heappop(working_nodes)
    get_codes_helper(node, "")
    for i in file_string:
        global huffman_encoded_string
        huffman_encoded_string += code_dict[i]


def get_binary():
    return bin(int.from_bytes(file_string.encode(), 'big'))[2:]


def decode():
    decoded_str = ""
    temp_str = ""
    i = 0
    while i < len(huffman_encoded_string):
        while temp_str not in reverse_code_dict:
            temp_str += huffman_encoded_string[i]
            i += 1
        decoded_str += reverse_code_dict[temp_str]
        temp_str = ""
    return decoded_str


def generateFiles():
    write = open(filename + "_binary.txt", "w")
    write.write(binary_string)
    write = open(filename + "_Huffman_encoded.txt", "w")
    write.write(huffman_encoded_string)
    write = open(filename + "_Huffman_decoded.txt", "w")
    write.write(huffman_decoded_string)


def compare():
    print("Huffman encoding binary file length: " + str(len(huffman_encoded_string)))
    print("Regular ASCII binary file length: " + str(len(binary_string)))


def main():
    global binary_string
    global huffman_decoded_string
    global reverse_code_dict
    load_file()
    heapq.heapify(working_nodes)
    encode()
    reverse_code_dict = {}
    for item in code_dict.items():
        reverse_code_dict[item[1]] = item[0]
    huffman_decoded_string = decode()
    binary_string = get_binary()
    generateFiles()
    compare()


filename = ""
binary_string = ""
file_string = ""
huffman_encoded_string = ""
huffman_decoded_string = ""
frequency_dict = {}
working_nodes = []
code_dict = {}
reverse_code_dict = {}
if __name__ == "__main__":
    main()
