import pymysql

host = "127.0.0.1"
user = "root"
password = "Jyoti@123"
database = "identification"

connection = pymysql.connect(
    host=host, user=user, password=password, database=database,
)

cursor = connection.cursor()

table_names = [
    "identification_1",
    "identification_2",
    "identification_3",
    "identification_4",
    "identification_5",
    "identification_6",
    "identification_7",
    "identification_8",
    "identification_9",
    "identification_10",
]

power_values = []

for i in range(10):
    power_value = float(input(f"Enter power value {i+1}: "))
    power_values.append(power_value)
    
    table_number = int(input(f"Enter the table number (1-10) for power value {power_value}: "))
    
    if 1 <= table_number <= 10:
        table_name = table_names[table_number - 1] 
        match_found = False

        query = f"SELECT radius FROM {table_name} WHERE power_min <= %s AND %s <= power_max"
        cursor.execute(query, (power_value, power_value))
        result = cursor.fetchone()

        if result:
            radius = result[0]
            print(f"Power: {power_value}, Radius: {radius}")
            match_found = True
            
            insert_query = "INSERT INTO matched_result (power_value, radius) VALUES (%s, %s)"
            cursor.execute(insert_query, (power_value, radius))
            connection.commit()

        if not match_found:
            print(f"No matching power range found for power {power_value}")
    else:
        print("Invalid table number. Please enter a number between 1 and 10.")

cursor.close()
connection.close()
