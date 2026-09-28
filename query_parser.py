import sqlparse
import pandas as pd

def parse_sql_query(query_str):
    parsed = sqlparse.parse(query_str)[0]
    query_type = parsed.get_type().upper()
    
    # Extracting Table Names from SQL Tokens
    tokens = [token.value.lower() for token in parsed.tokens if not token.is_whitespace]
    
    target_table = 'unknown'
    if 'users' in tokens:
        target_table = 'users'
    elif 'orders' in tokens:
        target_table = 'orders'
        
    is_write = 1 if query_type in ['UPDATE', 'INSERT', 'DELETE'] else 0
    
    return {
        'query_str': query_str,
        'query_type': query_type,
        'target_table': target_table,
        'is_write': is_write
    }

if __name__ == "__main__":
    q = "UPDATE users SET balance = 500 WHERE id = 1;"
    features = parse_sql_query(q)
    df = pd.DataFrame([features])
    print("--- Extracted Query Features (Data Science) ---")
    print(df.to_string(index=False))