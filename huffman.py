from collections import Counter
import numpy as np

class Node:
    def __init__(self, symbol, probability, left=None, right=None):
        self.symbol = symbol
        self.probability = probability
        self.left = left
        self.right = right

    # node comparing (sorting nodes based on probabilities)
    def __lt__(self, other):
        return self.probability > other.probability

def huffman_coding(symbols, probabilities):
    nodes = [Node(symbol, prob) for symbol, prob in zip(symbols, probabilities)]

    while len(nodes) > 1: # keep looping until one nodes left where root = 1.0
        nodes.sort() # sort probabilities in ascending order
        left, right = nodes.pop(), nodes.pop() # remove two smallest probabilities infront of the ascending order
        parent = Node(None, left.probability + right.probability, left, right) # sum up the two nodes
        nodes.insert(0, parent) # insert the parent node (sum of two nodes) back into the front of node list (index 0) && shift other probabilities to right

    codes = {}
    curr_node = nodes[0]
    curr_code = ""

    # traverse code from root
    def traverse(node, code):
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = code
            return

        # assign and invert code
        traverse(node.left, code + "1")
        traverse(node.right, code + "0")

    traverse(curr_node, curr_code)
    return codes

def main():

    # 1. Input user name and combine together if got space
    user_input = "".join(input("Enter your name: ").upper().split())

    # 2. Count the frequency of each character symbol
    frequency = Counter(user_input)

    only_num = list(frequency.values())

    total_len = len(user_input)

    character = list(frequency.keys())

    # 3. Count probabilities of each character and arranged in descending order
    probabilities = [frequency[letter]/total_len for letter in character]
    zip_item = list(zip(character, only_num, probabilities))
    zip_item.sort(key=lambda x: x[2], reverse=True) 
    character, only_num, probabilities = zip(*zip_item)

    # 4. Assign codeword
    codeword = huffman_coding(character, probabilities)

    print("-------------------------------------------------------------------------------------")
    print("|                                HUFFMAN CODE TABLE                                 |")
    print("|-----------------------------------------------------------------------------------|")
    print("| Symbol | Character | Frequency | Probability |     Codeword     | Codeword Length |")
    print("| ------ | --------- | --------- | ----------- | ---------------- | --------------- |")

    average_code_length = 0
    entropy = 0

    for i, (character, frequency, probabilities) in enumerate(zip_item):
        symbol = f"S{i}"

        # 5. Code word length
        codeword_length = len(codeword[character])

        # 6. Calculation of average code length   
        average_code_length += probabilities * codeword_length

        # 7. Calculation of Entropy
        entropy += probabilities * np.log2(1/probabilities)

        print(f"|   {symbol}   |     {character}     |     {only_num[i]}     |    {probabilities:.3f}    |      {codeword[character]:^7}     |        {codeword_length}        |")

    print("-------------------------------------------------------------------------------------\n")

    # 8. Calculation of Efficiency
    efficiency = entropy / average_code_length * 100

    print(f"Average Code Length, \u0305L: {average_code_length} bits/symbol")
    print(f"Entropy, H(s): {round(entropy, 4)} bits/symbol")
    print(f"Efficiency, n: {round(efficiency, 4)} %")

if __name__ == "__main__":
    main()