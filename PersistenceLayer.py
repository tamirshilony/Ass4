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
        INSERT INTO vaccines (id, date , supplier, quantity) VALUES (?, ?, ?, ?)
        """, [Vaccine.id, Vaccine.date, Vaccine.supplier, Vaccine.quantity])

    def find(self, Vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
            """, [Vaccine_id])
        return Vaccine(*c.fetchone())

    def update(self, Vaccine_id, quantity):
        c = self._conn.cursor()
        c.execute("""
            UPDATE vaccines SET quantity = ?  WHERE id = ?
            """, [quantity, Vaccine_id])
        if quantity == 0:
            self.delete(Vaccine_id)

    def delete(self, Vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            DELETE FROM vaccines WHERE id = ?
            """, [Vaccine_id])

    def findOldesVaccines(self):
        c = self._conn.cursor()
        c.execute("""
        SELECT id FROM vaccines
        ORDER BY date 
        LIMIT 1
        """)
        return [*c.fetchone()]

    def findLastVaccinesId(self):
        c = self._conn.cursor()
        c.execute("""
        SELECT id FROM vaccines
        ORDER BY date DESC
        LIMIT 1
        """)
        return [*c.fetchone()]
    
    def getQuantities(self):
        c = self._conn.cursor()
        c.execute("""
        SELECT SUM (quantity)
        FROM vaccines
        """)
        return [*c.fetchone()]

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""
        INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
        """, [Supplier.id, Supplier.name, Supplier.logistic])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM suppliers WHERE id = ?
            """, [id])
        return Supplier(*c.fetchone())

    def findByName(self, name):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM suppliers WHERE name = ?
            """, [name])
        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Clinic):
        self._conn.execute("""
        INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [Clinic.id, Clinic.location, Clinic.demand, Clinic.logistic])


    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE id = ?
        """, [id])
        return Clinic(*c.fetchone())

    def findByLocation(self, location):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE location = ?
        """, [location])
        return Clinic(*c.fetchone())

    def update(self, Clinic_id, demand):
        c = self._conn.cursor()
        c.execute("""
            UPDATE clinics SET demand = ? WHERE id = ?
        """, [demand, Clinic_id])

    def toPRINT(self, id_clinic):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE id = ?
        """, [id_clinic])
        return c.fetchone()
    
    def getTotalDemand(self):
        c = self._conn.cursor()
        c.execute("""
                SELECT SUM (demand)
                FROM clinics
                """)
        return [*c.fetchone()]
        




class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Logistic):
        self._conn.execute("""
        INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [Logistic.id, Logistic.name, Logistic.count_sent, Logistic.count_received])

    def find(self, Logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ?
            """, [Logistic_id])
        return Logistic(*c.fetchone())

    def updateSent(self, Logistic_id, value):
        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_sent = ?  WHERE id = ?
            """, [value, Logistic_id])

    def updateRecieve(self, Logistic_id, value):
        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_received = ?  WHERE id = ?
            """, [value, Logistic_id])

    def getTotalRecieved(self):
        c = self._conn.cursor()
        c.execute("""
                SELECT SUM (count_received)
                FROM logistics
                """)
        return [*c.fetchone()]
    
    def getTotalSent(self):
        c = self._conn.cursor()
        c.execute("""
                SELECT SUM (count_sent)
                FROM logistics
                """)
        return [*c.fetchone()]


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
            logistic    INTEGER         REFERENCES logistics(id)
            );
            
            CREATE TABLE clinics (
            id          INT         PRIMARY KEY,
            location    TEXT        NOT NULL,
            demand      INT         NOT NULL,
            logistic    INTEGER         REFERENCES  logistics(id)
            );
            
            CREATE TABLE logistics (
            id          INT         PRIMARY KEY,
            name        TEXT        NOT NULL,
            count_sent  INT         NOT NULL,
            count_received  INT     NOT NULL
            );
    """)

    def receiveShipment(self, supplier_name, amount, date):
        # get supplier(DTO)
        supplier = self.suppliers.findByName(supplier_name)
        # find next id
        next_id = self.vaccines.findLastVaccinesId()
        # insert new vaccine
        self.vaccines.insert(Vaccine(int(*next_id)+1, date, supplier.id, amount))
        # get supplier_logistic_id and update logistic
        logistic = self.logistics.find(supplier.logistic)
        self.logistics.updateRecieve(logistic.id, logistic.count_received + int(amount))

    # sendShipment(location_name,amount)
    def sendShipment(self, location, amount):
        # take amount vaccine from distribution center and update
        self.takeOutVaccines(amount)
        # get the clinic(DTO)
        clinic = self.clinics.findByLocation(location)
        # update clinic demand
        self.clinics.update(clinic.id, clinic.demand - int(amount))
        clc = (self.clinics.find(clinic.id))
        # get clinic_logistic
        logistic = self.logistics.find(clinic.logistic)
        # update logistic count_sent
        self.logistics.updateSent(logistic.id, logistic.count_sent+int(amount))


    def takeOutVaccines(self, amount):
        amountLeft = int(amount)
        while amountLeft > 0:
            id = self.vaccines.findOldesVaccines()
            vaccine = self.vaccines.find(*id)
            if amountLeft > vaccine.quantity:
                amountLeft -= vaccine.quantity
                self.vaccines.update(*id, 0)
            else:
                self.vaccines.update(*id, vaccine.quantity-amountLeft)
                amountLeft = 0








