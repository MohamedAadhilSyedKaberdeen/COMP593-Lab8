"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.

Usage:
 python create_relationships.py
"""

import os
import sqlite3
from random import randint, choice
from faker import Faker

# Determine the path of the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'social_network.db')

def main():
    create_relationships_table()
    populate_relationships_table()
    verify_data()  # Add this to check if data was inserted

def create_relationships_table():
    """Creates the relationships table in the DB"""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        create_relationships_table_query = """
        CREATE TABLE IF NOT EXISTS relationships
        (
            id INTEGER PRIMARY KEY, 
            person1_id INTEGER NOT NULL,
            person2_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            start_date DATE NOT NULL,
            FOREIGN KEY (person1_id) REFERENCES people (id),
            FOREIGN KEY (person2_id) REFERENCES people (id)
        );
        """
        cur.execute(create_relationships_table_query)
        con.commit()
        print("Created 'relationships' table.")

def populate_relationships_table():
    """Adds 100 random relationships to the DB"""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        add_relationship_query = """
        INSERT INTO relationships
        (
            person1_id,
            person2_id,
            type,
            start_date
        )
        VALUES (?, ?, ?, ?);
        """
        fake = Faker()
        
        for _ in range(100):
            person1_id = randint(1, 200)
            person2_id = randint(1, 200)
            while person2_id == person1_id:
                person2_id = randint(1, 200)
            relationship_type = choice(['friend', 'spouse', 'partner', 'relative'])
            start_date = fake.date_between(start_date='-50y', end_date='today').strftime('%Y-%m-%d')
            new_relationship = (person1_id, person2_id, relationship_type, start_date)
            cur.execute(add_relationship_query, new_relationship)
        
        con.commit()
        print("Inserted 100 random relationships.")

def verify_data():
    """Verifies that data was inserted into the 'relationships' table"""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM relationships")
        count = cur.fetchone()[0]
        print(f"Total records in 'relationships' table: {count}")

if __name__ == '__main__':
    main()
