import sqlite3

class _Repository:


    def __init__(self):
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
        name        TEXT        NOT NULL        DEFAULT 'notDef',
        logistic    INT         REFERENCES logistics(id)
        );
        
        CREATE TABLE clinics (
        id          INT         PRIMARY KEY,
        location    TEXT        NOT NULL,
        demand      INT         NOT NULL,
        logistic    INT         REFERENCES  logistics(id)
        );
        
        CREATE TABLE logistics (
        id          INT         PRIMARY KEY,
        name        TEXT        NOT NULL        DEFAULT 'notDef',
        count_sent  INT         NOT NULL        DEFAULT -1,
        count_recieved  INT     NOT NULL        EFAULT -1
        );
    """)


