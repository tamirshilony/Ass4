from PersistenceLayer import _Repository,Logistic,Supplier,Vaccine,Clinic


def main():
    repo = _Repository()
    repo.create_tables()

    total_inventory = 0
    total_demand = 0
    total_received = 0
    total_sent = 0

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
            total_inventory += int(lines[nextVaccine].split(",")[3])
            print(total_inventory)
        for i in range(0, firstLine[2]):
            nextClinic = firstLine[0]+firstLine[1] + i
            repo.clinics.insert(Clinic(*lines[nextClinic].split(",")))
            total_demand += int(lines[nextClinic].split(",")[2])
            print(total_demand)

    with open('orders.txt') as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        for line in lines:
            parsedLine = line.split(",")
            if len(parsedLine) == 2:
                repo.sendShipment(*parsedLine)
                total_inventory -= int(parsedLine[1])
                total_sent += int(parsedLine[1])
            else:
                repo.receiveShipment(*parsedLine)
                total_inventory += int(parsedLine[1])
                total_received += int(parsedLine[1])
            logToFile(total_inventory,total_demand,total_received,total_sent)

def logToFile(a,b,c,d):
    with open('output.txt', 'a') as outputfile:
        outputfile.write(str(a)+","+str(b)+","+str(c)+","+str(d))


if __name__ == '__main__':
    main()


