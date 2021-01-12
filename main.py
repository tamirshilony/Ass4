from PersistenceLayer import _Repository,Logistic,Supplier,Vaccine,Clinic


def main():
    repo = _Repository()
    repo.create_tables()
    with open('config.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        firstLine = lines[0].split(",")
        firstLine = list(map(int, firstLine))
        lines = lines[1:]
        for i in range(0, firstLine[3]):
            nextLogistic = firstLine[0]+firstLine[1]+firstLine[2] + i
            repo.logistics.insert(Logistic(*lines[nextLogistic].split(",")))
        for i in range(0, firstLine[1]):
            nextSupllier = firstLine[0]+i
            repo.suppliers.insert(Supplier(*lines[nextSupllier].split(",")))
        for i in range(0, firstLine[0]):
            nextVaccine = 0 + i
            repo.vaccines.insert(Vaccine(*lines[nextVaccine].split(",")))
        for i in range(0, firstLine[0]):
            nextClinic = firstLine[0]+firstLine[1] + i
            repo.clinics.insert(Clinic(*lines[nextClinic].split(",")))

    with open('orders.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        for line in lines:
            parsedLine = line.split(",")
            repo.sendShipment(*parsedLine) if len(parsedLine) == 2 else repo.receiveShipment(*parsedLine)


if __name__ == '__main__':
    main()


