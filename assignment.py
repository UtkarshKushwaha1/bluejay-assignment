import pandas as pd
import pandasql as psql

# Read the CSV file into a DataFrame
data = pd.read_csv('data.csv')

# Define the SQL queries
queries = {
    'consecutive_days': '''
        SELECT DISTINCT "Employee Name", "Position ID"
        FROM data
        WHERE "Employee Name" IN (
            SELECT "Employee Name"
            FROM data
            GROUP BY "Employee Name", "Pay Cycle Start Date"
            HAVING COUNT(*) >= 7
        )
    ''',
    'time_between_shifts': '''
        SELECT DISTINCT "Employee Name", "Position ID"
        FROM data
        WHERE "Employee Name" IN (
            SELECT "Employee Name"
            FROM data
            WHERE (strftime('%s', "Time") - strftime('%s', "Time Out")) BETWEEN 3600 AND 36000
            GROUP BY "Employee Name", "Pay Cycle Start Date"
        )
    ''',
    'single_shift_hours': '''
        SELECT "Employee Name", "Position ID"
        FROM data
        GROUP BY "Employee Name", "Position ID", "Pay Cycle Start Date"
        HAVING MAX(strftime('%s', "Time Out") - strftime('%s', "Time")) > 14 * 3600
    '''
}

# Initialize pandasql
pysqldf = lambda q: psql.sqldf(q, globals())

# Run and print the results for each query
for query_name, query_string in queries.items():
    result = pysqldf(query_string)
    print(f"Employees with {query_name}:")
    print(result)
    print("\n")
