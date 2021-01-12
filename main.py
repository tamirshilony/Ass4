from PersistenceLayer import _Repository



def main():
    repo = _Repository()
    with open('config.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        firstLine = lines[0].split(",")
        for i in range (1,int(firstLine[3])):
            nextLogistic = int(firstLine[0])+int(firstLine[1])+int(firstLine[2])
            repo.Logistic.insert(*lines[nextLogistic].split(","))
        for i in range (1,int(firstLine[1])):
            nextSupllier = int(firstLine[0])
            repo.suppliers.insert(*lines[nextSupllier].split(","))
        # first_line = inputfile.readline().split(",")
        # first_line[-1] = first_line[-1].strip()
        # num_of_entries = 0
        # for i in range (0,len(first_line)):
        #     num_of_entries += int(first_line[i])
        # entries = list(num_of_entries)
        print(*lines[nextLogistic].split(","))
        # i = 0
        # for line in inputfile:
        #     entries[i] = line


# def parseLine(type)

if __name__ == '__main__':
    main()


