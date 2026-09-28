import threading
import time
import sqlite3

class LockManager:
    def __init__(self, db_path='neurolock_db.sqlite'):
        self.db_path = db_path
        # Dynamic Mutex Lock for each table
        self.table_locks = {
            'users': threading.Lock(),
            'orders': threading.Lock(),
            'products': threading.Lock()
        }

    def acquire_table_lock(self, table_name, thread_id):
        if table_name in self.table_locks:
            print(f"⌛ [Thread-{thread_id}] Attempting to acquire Mutex Lock on Table: '{table_name}'...")
            start_time = time.time()
            self.table_locks[table_name].acquire()
            wait_time = round(time.time() - start_time, 2)
            print(f"🔒 [Thread-{thread_id}] LOCKED Table: '{table_name}' (Wait Time: {wait_time}s)")
        else:
            print(f"⚠️ [Thread-{thread_id}] Table '{table_name}' lock untracked, proceeding directly.")

    def release_table_lock(self, table_name, thread_id):
        if table_name in self.table_locks and self.table_locks[table_name].locked():
            self.table_locks[table_name].release()
            print(f"🔓 [Thread-{thread_id}] RELEASED Mutex Lock on Table: '{table_name}'")

    def execute_sql_query(self, sql_query, thread_id):
        """ Executes the actual SQL query on the SQLite DB file """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
            print(f"⚡ [Thread-{thread_id}] DB EXECUTION SUCCESSFUL: {sql_query}")
            conn.close()
        except Exception as e:
            print(f"❌ [Thread-{thread_id}] DB EXECUTION ERROR: {e}")