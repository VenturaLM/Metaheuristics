profits = list()

encoding = input(
    "Select type of encoding:\n1. Binary encoding. [Default]\n2. Integer encoding.\n> ")
text_name = input("\nSelect text file:\n> ")

file_name = ""

if encoding == "2":
    file_name = "./integer_encoding_data/" + text_name + ".txt"
else:
    file_name = "./binary_encoding_data/" + text_name + ".txt"

with open(file_name) as fin:
    for line in fin:
        profits.append(line.strip())

profits.sort()

with open(file_name, 'w') as fout:
    for profit in profits:
        fout.write(profit + '\n')
