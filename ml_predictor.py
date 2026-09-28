from sklearn.ensemble import RandomForestClassifier
import numpy as np

class NeuroLockML:
    def __init__(self):
        # n_estimators=5 and max_depth=3 for instant CPU loading without freezing
        self.model = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
        self._train_dummy_model()

    def _train_dummy_model(self):
        # Feature Format: [Q1_IsWrite, Q2_IsWrite, IsSameTable]
        X_train = np.array([
            [1, 1, 1],  # Both Write, Same Table -> HAZARD (1)
            [1, 0, 1],  # Read + Write, Same Table -> HAZARD (1)
            [0, 0, 1],  # Both Read, Same Table -> SAFE (0)
            [1, 1, 0],  # Both Write, Different Tables -> SAFE (0)
            [0, 1, 0]   # Read + Write, Different Tables -> SAFE (0)
        ])
        y_train = np.array([1, 1, 0, 0, 0])
        self.model.fit(X_train, y_train)

    def predict_hazard(self, q1_feat, q2_feat):
        t1 = q1_feat.get('target_table') or q1_feat.get('table')
        t2 = q2_feat.get('target_table') or q2_feat.get('table')
        
        same_table = 1 if (t1 == t2 and t1 is not None) else 0
        w1 = 1 if q1_feat.get('is_write') else 0
        w2 = 1 if q2_feat.get('is_write') else 0

        input_vector = np.array([[w1, w2, same_table]])
        
        prediction = self.model.predict(input_vector)[0]
        prob = float(self.model.predict_proba(input_vector)[0][1])
        
        return prob, int(prediction)

# Pre-instantiate single engine
_ml_engine = NeuroLockML()

def predict_hazard(q1_feat, q2_feat):
    return _ml_engine.predict_hazard(q1_feat, q2_feat)