from sklearn.ensemble import RandomForestClassifier
import numpy as np

class NeuroLockML:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self._train_dummy_model()

    def _train_dummy_model(self):
        # Feature Format: [Q1_IsWrite, Q2_IsWrite, IsSameTable]
        # Target: 1 = High Lock Hazard (Collision), 0 = Safe
        X_train = np.array([
            [1, 1, 1],  # Both Write, Same Table -> HAZARD (1)
            [1, 0, 1],  # One Write, One Read, Same Table -> HAZARD (1)
            [0, 0, 1],  # Both Read, Same Table -> SAFE (0)
            [1, 1, 0],  # Both Write, Different Tables -> SAFE (0)
            [0, 1, 0]   # Read & Write, Different Tables -> SAFE (0)
        ])
        y_train = np.array([1, 1, 0, 0, 0])
        self.model.fit(X_train, y_train)

    def predict_hazard(self, q1_feat, q2_feat):
        same_table = 1 if q1_feat['target_table'] == q2_feat['target_table'] else 0
        input_vector = [[q1_feat['is_write'], q2_feat['is_write'], same_table]]
        
        prediction = self.model.predict(input_vector)[0]
        return prediction  # Returns 1 for Collision Risk, 0 for Safe

if __name__ == "__main__":
    ml = NeuroLockML()
    # Test Prediction
    print("--- ML Hazard Prediction Test ---")
    q1 = {'is_write': 1, 'target_table': 'users'}
    q2 = {'is_write': 1, 'target_table': 'users'}
    
    hazard = ml.predict_hazard(q1, q2)
    print("Prediction Result:", "⚠️ HIGH LOCK COLLISION HAZARD!" if hazard == 1 else "✅ SAFE TO RUN PARALLEL")