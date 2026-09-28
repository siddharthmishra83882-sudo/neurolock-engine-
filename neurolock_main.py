import threading
import time
from db_lock_manager import LockManager
from query_parser import parse_sql_query
from ml_predictor import NeuroLockML

lock_mgr = LockManager()
ml_engine = NeuroLockML()

def execute_query_task(query_feat, thread_id, delay=0):
    if delay > 0:
        print(f"⏸️ [NeuroLock Scheduler] Delaying Thread-{thread_id} by {delay}s to prevent Lock Collision...")
        time.sleep(delay)
        
    target_table = query_feat['target_table']
    
    # OS Thread Mutex Lock
    lock_mgr.acquire_table_lock(target_table, thread_id)
    
    # Actual SQLite Database Execution
    lock_mgr.execute_sql_query(query_feat['query_str'], thread_id)
    time.sleep(0.5) # Simulating execution hold time
    
    lock_mgr.release_table_lock(target_table, thread_id)

def run_neurolock_pipeline(sql_q1, sql_q2):
    print("\n================ NEUROLOCK REAL DB PIPELINE ================")
    print(f"Incoming Query 1: {sql_q1}")
    print(f"Incoming Query 2: {sql_q2}\n")
    
    q1_feat = parse_sql_query(sql_q1)
    q2_feat = parse_sql_query(sql_q2)
    
    # ML Prediction using saved Random Forest Model
    hazard = ml_engine.predict_hazard(q1_feat, q2_feat)
    
    if hazard == 1:
        print("🚨 [ML ALERT] High Lock Hazard Detected! Scheduling Query 2 sequentially.\n")
        t1 = threading.Thread(target=execute_query_task, args=(q1_feat, 1, 0))
        t2 = threading.Thread(target=execute_query_task, args=(q2_feat, 2, 1.0))
    else:
        print("✅ [ML ALERT] Low Collision Risk. Executing parallel threads.\n")
        t1 = threading.Thread(target=execute_query_task, args=(q1_feat, 1, 0))
        t2 = threading.Thread(target=execute_query_task, args=(q2_feat, 2, 0))
        
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("============================================================\n")

if __name__ == "__main__":
    # Test Real DB Queries
    q_write1 = "UPDATE users SET balance = balance + 100 WHERE id = 1;"
    q_write2 = "UPDATE users SET status = 'active' WHERE id = 1;"
    run_neurolock_pipeline(q_write1, q_write2)