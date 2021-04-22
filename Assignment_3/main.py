import sys
import numpy as np
import pandas as pd


def importFromTXTFile(file_name, lines):
    file = open(file_name, "r")
    for i in file:
        currentPlace = i[:-1]
        currentPlace = currentPlace.replace(" ", "")
        currentPlace = currentPlace.split(":")
        lines.append(currentPlace)


def moveToRecords(records, lines):
    # Adds to the dictionary each pair "Event" - "Time".
    # Example: [['A0', 'B10', 'C21']]
    for i in range(len(lines)):
        e = []
        t = []
        for j in range(len(lines[i])):
            for k in range(len(lines[i][j])):

                # If the character is a letter, it is a event.
                if lines[i][j][k].isalpha():
                    e.append(lines[i][j][k])
                else:
                    # The rest of the characters of the list[i][j][k] is a number.
                    t.append(lines[i][j][1:])
                    break
        records['Event'].append(e)
        records['Time'].append(t)


def createDataFrame():
    # Creates the dataframe.
    df = pd.DataFrame(records, columns=['Event', 'Time'])
    # Change the context from "DataFrame" to "Numpy structure".
    numpy_array = df.to_numpy()


def main():
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []

        importFromTXTFile(sys.argv[1], lines)
        moveToRecords(records, lines)
        print(records)


if __name__ == "__main__":
    main()
