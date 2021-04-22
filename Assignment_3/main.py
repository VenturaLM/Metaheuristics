import sys


def importFromTXTFile(file_name, lines):
    file = open(file_name, "r")
    for i in file:
        currentPlace = i[:-1]
        currentPlace = currentPlace.replace(" ", "")
        currentPlace = currentPlace.split(":")
        lines.append(currentPlace)


def moveToDictionary(dictionary, lines):
    # Adds to the dictionary each pair "Event" - "Time".
    # Example: [['A0', 'B10', 'C21']]
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            for k in range(len(lines[i][j])):
                # If the character is a letter, it is a event.
                if lines[i][j][k].isalpha():
                    dictionary['Event'].append(lines[i][j][k])
                else:
                    # The rest of the characters of the list[i][j][k] is a number.
                    dictionary['Time'].append(lines[i][j][1:])
                    break


def main():
    if len(sys.argv) == 2:
        dictionary = {'Event': [], 'Time': []}
        lines = []

        importFromTXTFile(sys.argv[1], lines)
        moveToDictionary(dictionary, lines)
        print(dictionary)


if __name__ == "__main__":
    main()
