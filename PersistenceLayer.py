# Data Transfer Objects:
class Vaccine:
    def __init__(self, id, date , supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


# Data Access Objects:
# All of these are meant to be singletons
class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Vaccine):
        self._conn.execute("""
        INSERT INTO Vaccines (id, date , supplier, quantity) VALUES (?, ?, ?, ?)
        """, [Vaccine.id, Vaccine.date, Vaccine.supplier, Vaccine.quantity])

    def find(self, Vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Vaccines WHERE id = ?
            """, [Vaccine_id])
        return Vaccine(*c.fetchone())

    def update(self, Vaccine_id, quantity):
        c = self._conn.cursor()
        c.execute("""
            UPDATE Vaccines SET quantity = ?  WHERE id = ?
            """, [quantity, Vaccine_id])
        if quantity == 0:
            self.delete(Vaccine_id)

    def delete(self, Vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            DELETE FROM Vaccines WHERE id = ?
            """, [Vaccine_id])

    def findOldesVaccines(self):
        c = self._conn.cursor()
        c.execute(""""
        SELECT id FROM Vaccines
        ORDER BY date 
        LIMIT 1
        """)
        return [*c.fetchone()]

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""
        INSERT INTO Suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [Supplier.id, Supplier.name, Supplier.logistic])

    def find(self, attribute, value):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Suppliers WHERE ? = ?
            """, [attribute, value])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Clinic):
        self._conn.execute("""
        INSERT INTO Clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [Clinic.id, Clinic.location, Clinic.demand, Clinic.logistic])

    def find(self, attribute, identify):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Clinics WHERE ? = ?
        """, [attribute, identify])
        return Clinic(*c.fetchone())

    def update(self, Clinic_id, demand):
        c = self._conn.cursor()
        c.execute("""
            UPDATE Clinics SET demand = ? WHERE id = ?
        """, [demand, Clinic_id])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Logistic):
        self._conn.execute("""
        INSERT INTO Logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [Logistic.id, Logistic.name, Logistic.count_sent, Logistic.count_received])

    def find(self, Logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Logistic WHERE id = ?
            """, [Logistic_id])
        return Logistic(*c.fetchone())

    def update(self, Logistic_id, attribute, value):
        c = self._conn.cursor()
        c.execute("""
            UPDATE Logistic SET ? = ?  WHERE id = ?
            """, [attribute, value, Logistic_id])


import sqlite3
import os
class _Repository:

    def __init__(self):
        self.delete_tables = True
        if self.delete_tables:
            isExist = os.path.exists("database.db")
            if isExist:
                os.remove("database.db")
        self._conn = sqlite3.connect("database.db")
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()


        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE vaccines (
            id          INT         PRIMARY KEY,
            date        DATE        NOT NULL,
            supplier    INT         REFERENCES suppliers(id),
            quantity    INT         NOT NULL
            );
            
            CREATE TABLE suppliers (
            id          INT         PRIMARY KEY,
            name        TEXT        NOT NULL,
            logistic    INT         REFERENCES logistics(id)
            );
            
            CREATE TABLE clinics (
            id          INT         PRIMARY KEY,
            location    TEXT        NOT NULL,
            demand      INT         NOT NULL,
            logistic    INT         REFERENCES  logistics(id)
            );
            
            CREATE TABLE Logistics (
            id          INT         PRIMARY KEY,
            name        TEXT        NOT NULL,
            count_sent  INT         NOT NULL,
            count_received  INT     NOT NULL
            );
    """)

    def receiveShipment(self, supplier_name, amount, date):
        # get supplier(DTO)
        supplier = self.suppliers.find("name", supplier_name)
        # insert new vaccsine
        self.vaccines.insert(Vaccine(100, date, supplier.id, amount))
        # get supplier_logistic_id and update logistic
        self.logistics.update(supplier.logistic, supplier.logistic.count_received + amount)

    # sendShipment(location_name,amount)
    def sendShipment(self, location, amount):
        # take from right date
        self.takeOutVaccines(amount)
        # find clinics_id by location
        clinic = self.clinics.find("location", location)
        # Clinic =  Clinics.find(location, location_name)
        self.clinics.update(clinic.id, amount)
        # Clinics.update(Clinic.id,amount)

    # receiveShipment(supplier_name, amount, date)
    # get supplier.id
    # Vaccsines.insert((aoutoincrementId),date,supplier.id,amount)
    # get supplier_logistic_id
    # Logistics.update(supplier_logistic_id, count_sent,amount)

    def takeOutVaccines(self, amount):
        amountLeft = amount
        while amountLeft > 0:
            id = self.vaccines.findOldesVaccines()
            vaccine = self.vaccines.find(id)
            if amountLeft > vaccine.quantity:
                amountLeft -= vaccine.quantity
                self.vaccines.update(id, 0)
            else:
                self.vaccines.update(id, vaccine.quantity-amountLeft)
                amountLeft = 0


