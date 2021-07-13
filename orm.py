# relation

import sqlite3
con = sqlite3.connect('chinook.db')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


con.row_factory = dict_factory
cur = con.cursor()

sql_query = '''
SELECT * FROM customers;
'''
cur.execute(sql_query)

customers = cur.fetchall()

con.close()

# for customer in customers:
#     print(customer['CustomerId'], customer['FirstName'], customer['LastName'])


# 辞書型からオブジェクトに変換する。作業しやすいから。 object
class Customer:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

# c1 = Customer('Yoshio', 'Yabusaki')
# c2 = Customer('Lev', 'Tolstoy')
#
# print(c1.get_full_name())
# print(c2.get_full_name())


# mapping
customer_objects = []
for c in customers:
    customer_objects.append(
        Customer(c['FirstName'], c['LastName'])
    )

# データを使いたいように使う  usage
for cust in customer_objects:
    print(cust.get_full_name())