from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "normal_operation.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "isolation_forest.joblib"


# Features used by the anomaly detector
FEATURES = [
    "voltage",
    "current",
    "frequency",
    "power_factor",
    "active_power",
    "reactive_power",
]


def train_model():
    # Load normal-operation data
    data = pd.read_csv(DATA_PATH)

    # Select ML features
    X = data[FEATURES]

    # Create Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )

    # Train only on normal-operation data
    model.fit(X)

    # Save trained model
    joblib.dump(model, MODEL_PATH)

    print(f"Training samples: {len(X)}")
    print(f"Features used: {len(FEATURES)}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
    