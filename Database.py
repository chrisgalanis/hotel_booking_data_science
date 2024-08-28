import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS HotelStatistics (
            hotel_name TEXT PRIMARY KEY,
            avg_stay_days REAL,
            avg_actual_stay_days REAL,
            percentage_cancellations REAL
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReservationsPerMonth (
            hotel_name TEXT,
            month TEXT,
            reservations INTEGER,
            PRIMARY KEY (hotel_name, month)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReservationsPerSeason (
            hotel_name TEXT,
            season TEXT,
            reservations INTEGER,
            PRIMARY KEY (hotel_name, season)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReservationsPerRoomType (
            hotel_name TEXT,
            room_type TEXT,
            reservations INTEGER,
            PRIMARY KEY (hotel_name, room_type)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReservationsPerVisitorType (
            hotel_name TEXT,
            visitor_type TEXT,
            reservations INTEGER,
            PRIMARY KEY (hotel_name, visitor_type)
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReservationsPerYear (
            hotel_name TEXT,
            year INTEGER,
            reservations INTEGER,
            PRIMARY KEY (hotel_name, year)
        )''')
        
        self.conn.commit()

    def insert_hotel_statistics(self, hotel_name, avg_stay_days, avg_actual_stay_days, percentage_cancellations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO HotelStatistics (hotel_name, avg_stay_days, avg_actual_stay_days, percentage_cancellations)
        VALUES (?, ?, ?, ?)
        ''', (hotel_name, avg_stay_days, avg_actual_stay_days, percentage_cancellations))
        self.conn.commit()

    def insert_reservations_per_month(self, hotel_name, month, reservations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO ReservationsPerMonth (hotel_name, month, reservations)
        VALUES (?, ?, ?)
        ''', (hotel_name, month, reservations))
        self.conn.commit()

    def insert_reservations_per_season(self, hotel_name, season, reservations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO ReservationsPerSeason (hotel_name, season, reservations)
        VALUES (?, ?, ?)
        ''', (hotel_name, season, reservations))
        self.conn.commit()

    def insert_reservations_per_room_type(self, hotel_name, room_type, reservations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO ReservationsPerRoomType (hotel_name, room_type, reservations)
        VALUES (?, ?, ?)
        ''', (hotel_name, room_type, reservations))
        self.conn.commit()

    def insert_reservations_per_visitor_type(self, hotel_name, visitor_type, reservations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO ReservationsPerVisitorType (hotel_name, visitor_type, reservations)
        VALUES (?, ?, ?)
        ''', (hotel_name, visitor_type, reservations))
        self.conn.commit()

    def insert_reservations_per_year(self, hotel_name, year, reservations):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO ReservationsPerYear (hotel_name, year, reservations)
        VALUES (?, ?, ?)
        ''', (hotel_name, year, reservations))
        self.conn.commit()

    def export_schema(self, output_file='database_schema.sql'):
        with open(output_file, 'w') as f:
            for line in self.conn.iterdump():
                f.write('%s\n' % line)
        print(f"Database schema exported to {output_file}")

    def close(self):
        self.conn.close()