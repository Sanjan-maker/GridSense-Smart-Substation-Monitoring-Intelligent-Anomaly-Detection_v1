from pathlib import Path

import joblib
import pandas as pd

import sys

sys.path.append(str(Path(__file__).parent.parent / "simulator"))

from power_system import PowerSystem


PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "ml" / "isolation_forest.joblib"

FEATURES = [
    "voltage",
    "current",
    "frequency",
    "power_factor",
    "active_power",
    "reactive_power",
]


def predict(system):
    model = joblib.load(MODEL_PATH)

    measurements = system.calculate_power()

    data = pd.DataFrame([{
        feature: measurements[feature]
        for feature in FEATURES
    }])

    prediction = model.predict(data)[0]
    score = model.decision_function(data)[0]

    label = "NORMAL" if prediction == 1 else "ANOMALY"

    return label, score, measurements


def test_condition(condition):
    system = PowerSystem()
    system.set_condition(condition)

    label, score, measurements = predict(system)

    print(f"\nCondition: {condition}")
    print(f"Voltage: {measurements['voltage']:.2f} V")
    print(f"Current: {measurements['current']:.2f} A")
    print(f"Frequency: {measurements['frequency']:.2f} Hz")
    print(f"Power Factor: {measurements['power_factor']:.2f}")
    print(f"ML Result: {label}")
    print(f"Anomaly Score: {score:.4f}")


if __name__ == "__main__":
    test_condition("normal")
    test_condition("overvoltage")
    test_condition("undervoltage")
    test_condition("overcurrent")
    test_condition("underfrequency")
    test_condition("overfrequency")