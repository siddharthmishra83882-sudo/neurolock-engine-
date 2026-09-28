import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load Generated Synthetic Dataset
print("📊 Loading dataset from 'sql_hazard_dataset.csv'...")
df = pd.read_csv('sql_hazard_dataset.csv')

# 2. Separate Features (X) and Target Label (y)
X = df[['q1_is_write', 'q2_is_write', 'same_table']]
y = df['hazard_label']

# 3. Train-Test Split (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Random Forest Model
print("🧠 Training Random Forest Classifier for Lock Contention Hazard Prediction...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n=================== MODEL PERFORMANCE ===================")
print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))
print("=========================================================")

# 6. Save Trained Model Weights
model_filename = 'neurolock_model.joblib'
joblib.dump(model, model_filename)
print(f"💾 Trained model saved successfully as '{model_filename}'!")