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
           """, [Vaccine.id, Vaccine.data, Vaccine.supplier, Vaccine.quantity])

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


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""
               INSERT INTO Suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [Supplier.id, Supplier.name, Supplier.logistic])

    def find(self, Supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Vaccines WHERE id = ?
        """, [Supplier_id])

        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Clinic):
        self._conn.execute("""
               INSERT INTO Clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
           """, [Clinic.id, Clinic.location, Clinic.demand, Clinic.logistic])

    def find(self, Clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Clinics WHERE id = ?
        """, [Clinic_id])

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



# receiveShipment(supplier_name, amount, date)
    # get supplier.id
    # Vaccsines.insert((aoutoincrementId),date,upplier.id,amount)
    # get supplier_logistic_id
    # Logistics.update(supplier_logistic_id, count_sent,amount)

# sendShipment(location,amount)
    # find clinic id by name
    #


