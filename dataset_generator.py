import pandas as pd
import random
import sqlparse

# Sample Tables & SQL Templates
TABLES = ['users', 'orders', 'products', 'audit_logs', 'payments']
WRITE_OPS = ['UPDATE', 'INSERT', 'DELETE']
READ_OPS = ['SELECT']

def generate_random_query():
    table = random.choice(TABLES)
    is_write = random.choice([True, False])
    
    if is_write:
        op = random.choice(WRITE_OPS)
        if op == 'UPDATE':
            sql = f"UPDATE {table} SET status = 'updated' WHERE id = {random.randint(1, 100)};"
        elif op == 'INSERT':
            sql = f"INSERT INTO {table} VALUES ({random.randint(1, 100)}, 'data');"
        else:
            sql = f"DELETE FROM {table} WHERE id = {random.randint(1, 100)};"
    else:
        sql = f"SELECT * FROM {table} WHERE id = {random.randint(1, 100)};"
        
    return sql, table, 1 if is_write else 0

def generate_query_pair_dataset(num_samples=500):
    dataset = []
    
    for i in range(num_samples):
        q1_sql, q1_table, q1_is_write = generate_random_query()
        q2_sql, q2_table, q2_is_write = generate_random_query()
        
        # Logic for Ground Truth Label (Collision Hazard)
        # Rule: Same Table + At least one WRITE operation = Lock Contention Risk (1)
        same_table = 1 if q1_table == q2_table else 0
        at_least_one_write = 1 if (q1_is_write == 1 or q2_is_write == 1) else 0
        both_write = 1 if (q1_is_write == 1 and q2_is_write == 1) else 0
        
        # Lock Hazard Label
        if same_table and at_least_one_write:
            hazard_label = 1
        else:
            hazard_label = 0
            
        dataset.append({
            'q1_sql': q1_sql,
            'q2_sql': q2_sql,
            'q1_table': q1_table,
            'q2_table': q2_table,
            'q1_is_write': q1_is_write,
            'q2_is_write': q2_is_write,
            'same_table': same_table,
            'at_least_one_write': at_least_one_write,
            'both_write': both_write,
            'hazard_label': hazard_label
        })
        
    df = pd.DataFrame(dataset)
    df.to_csv('sql_hazard_dataset.csv', index=False)
    print(f"✅ Successful! Generated {num_samples} Query Pair Records in 'sql_hazard_dataset.csv'.")
    print("\n--- Dataset Sample Preview ---")
    print(df[['q1_is_write', 'q2_is_write', 'same_table', 'hazard_label']].head())

if __name__ == "__main__":
    generate_query_pair_dataset(500)