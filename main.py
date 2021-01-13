import sys

from PersistenceLayer import _Repository,Logistic,Supplier,Vaccine,Clinic
import atexit

def main():
    repo = _Repository()
    atexit.register(repo._close)
    repo.create_tables()

    with open(sys.argv[1]) as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        firstLine = lines[0].split(",")
        firstLine = list(map(int, firstLine))
        lines = lines[1:]
        # Logistics
        for i in range(0, firstLine[3]):
            nextLogistic = firstLine[0]+firstLine[1]+firstLine[2] + i
            repo.logistics.insert(Logistic(*lines[nextLogistic].split(",")))
        # Suppliers
        for i in range(0, firstLine[1]):
            nextSupllier = firstLine[0]+i
            repo.suppliers.insert(Supplier(*lines[nextSupllier].split(",")))
        # Vaccine
        for i in range(0, firstLine[0]):
            nextVaccine = 0 + i
            repo.vaccines.insert(Vaccine(*lines[nextVaccine].split(",")))
        # Clinic
        for i in range(0, firstLine[2]):
            nextClinic = firstLine[0]+firstLine[1] + i
            repo.clinics.insert(Clinic(*lines[nextClinic].split(",")))

    outputfile = open(sys.argv[3], "w")

    with open(sys.argv[2]) as inputfile:
        lines = [line.rstrip('\n') for line in inputfile]
        for line in lines:
            parsedLine = line.split(",")
            if len(parsedLine) == 2:
                repo.sendShipment(*parsedLine)
            else:
                repo.receiveShipment(*parsedLine)
            logToFile(repo,outputfile)
            if line != lines[-1]:
                outputfile.write("\n")

    outputfile.close()


def logToFile(repo,outputfile):
        outputfile.write(str(*repo.vaccines.getQuantities()) +","
                         +str(*repo.clinics.getTotalDemand())+","
                         +str(*repo.logistics.getTotalRecieved())+","
                         +str(*repo.logistics.getTotalSent()))


if __name__ == '__main__':
    main()


