"""
Description:
 Generates a CSV report containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""

import os
import sqlite3
import pandas as pd
from create_relationships import db_path

def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)

def get_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        query = """
        SELECT person1.name, person2.name, start_date
        FROM relationships
        JOIN people AS person1 ON relationships.person1_id = person1.id
        JOIN people AS person2 ON relationships.person2_id = person2.id
        WHERE type = 'spouse';
        """
        cur.execute(query)
        results = cur.fetchall()
    return results

def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file.

    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    df = pd.DataFrame(married_couples, columns=['Person 1', 'Person 2', 'Start Date'])
    df.to_csv(csv_path, index=False)
    print(f"Saved married couples to '{csv_path}'")

if __name__ == '__main__':
    main()
