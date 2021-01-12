from PersistenceLayer import _Repository



def main():
    repo = _Repository()
    with open('config.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        firstLine = lines[0].split(",")
        firstLine = list(map(int, firstLine))
        lines = lines[1:]
        for i in range (0,firstLine[3]-1):
            nextLogistic = firstLine[0]+firstLine[1]+firstLine[2] + i
            repo.Logistic.insert(*lines[nextLogistic].split(","))
        for i in range (0,firstLine[1]-1):
            nextSupllier = firstLine[0]+i
            repo.suppliers.insert(*lines[nextSupllier].split(","))
        for i in range (0,firstLine[0]-1):
            nextVaccine = 0 + i
            repo.vaccines.insert(*lines[nextVaccine].split(","))
        for i in range(0, firstLine[0] - 1):
            nextClinic = firstLine[0]+firstLine[1] + i
            repo.vaccines.insert(*lines[nextClinic].split(","))

    with open('orders.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        for line in lines:
            parsedLine = line.split(",")
            repo.sendShipment(*parsedLine) if len(parsedLine) == 2 else repo.reciveShipment()

if __name__ == '__main__':
    main()


