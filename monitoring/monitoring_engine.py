from pathlib import Path
import sys

import joblib
import pandas as pd


# ============================================================
# PROJECT SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent

# Add project modules to Python path
sys.path.append(str(PROJECT_ROOT / "simulator"))
sys.path.append(str(PROJECT_ROOT / "alarms"))
sys.path.append(str(PROJECT_ROOT / "logs"))


from power_system import PowerSystem
from alarm_engine import AlarmEngine
from event_logger import EventLogger


# ============================================================
# ML MODEL
# ============================================================

MODEL_PATH = PROJECT_ROOT / "ml" / "isolation_forest.joblib"


# Features used by the trained Isolation Forest model
FEATURES = [
    "voltage",
    "current",
    "frequency",
    "power_factor",
    "active_power",
    "reactive_power",
]


# ============================================================
# MONITORING ENGINE
# ============================================================

class MonitoringEngine:

    def __init__(self):

        # Rule-based alarm engine
        self.alarm_engine = AlarmEngine()

        # Load trained ML anomaly detection model
        self.ml_model = joblib.load(MODEL_PATH)

        # Event logger
        self.logger = EventLogger()

        # Currently active fault
        #
        # None = system is currently normal
        #
        # Example:
        # "OVERVOLTAGE"
        # "OVERCURRENT"
        # "ML_ANOMALY"
        self.active_fault = None


    # ========================================================
    # EVALUATE MEASUREMENTS
    # ========================================================

    def evaluate(self, measurements):

        # ----------------------------------------------------
        # 1. RULE-BASED DETECTION
        # ----------------------------------------------------

        rule_alarms = self.alarm_engine.evaluate(
            measurements
        )


        # ----------------------------------------------------
        # 2. ML ANOMALY DETECTION
        # ----------------------------------------------------

        ml_input = pd.DataFrame([{
            feature: measurements[feature]
            for feature in FEATURES
        }])

        # Isolation Forest prediction
        #
        #  1  = Normal
        # -1  = Anomaly

        prediction = self.ml_model.predict(
            ml_input
        )[0]

        # Anomaly score
        anomaly_score = self.ml_model.decision_function(
            ml_input
        )[0]

        ml_anomaly = prediction == -1


        # ----------------------------------------------------
        # 3. UNIFIED SYSTEM STATUS
        # ----------------------------------------------------

        # Rule alarms have priority over ML anomaly.

        if rule_alarms:

            overall_status = "ALARM"

        elif ml_anomaly:

            overall_status = "ML_ANOMALY"

        else:

            overall_status = "NORMAL"


        # ----------------------------------------------------
        # 4. DETERMINE CURRENT FAULT
        # ----------------------------------------------------

        if rule_alarms:

            # First rule alarm becomes the active fault.
            current_fault = rule_alarms[0]

        elif ml_anomaly:

            # No rule alarm, but ML detects anomaly.
            current_fault = "ML_ANOMALY"

        else:

            # No fault.
            current_fault = None


        # ----------------------------------------------------
        # 5. CREATE RESULT
        # ----------------------------------------------------

        result = {

            "rule_alarms": rule_alarms,

            "ml_anomaly": ml_anomaly,

            "anomaly_score": anomaly_score,

            "overall_status": overall_status,

            "current_fault": current_fault,

            # Will be updated by lifecycle logic below.
            "event_type": None,

        }


        # ====================================================
        # 6. FAULT LIFECYCLE MANAGEMENT
        # ====================================================


        # ----------------------------------------------------
        # CASE 1: NEW FAULT
        # ----------------------------------------------------
        #
        # Previous:
        #     NORMAL
        #
        # Current:
        #     OVERVOLTAGE
        #
        # Event:
        #     OVERVOLTAGE_STARTED
        # ----------------------------------------------------

        if (
            current_fault is not None
            and self.active_fault is None
        ):

            print(
                f"🚨 FAULT STARTED: {current_fault}"
            )

            event_type = (
                f"{current_fault}_STARTED"
            )

            result["event_type"] = event_type

            # Store active fault
            self.active_fault = current_fault

            # Log the event
            self.logger.log(
                measurements,
                result
            )


        # ----------------------------------------------------
        # CASE 2: SAME FAULT CONTINUES
        # ----------------------------------------------------
        #
        # Example:
        #
        # OVERVOLTAGE
        # OVERVOLTAGE
        # OVERVOLTAGE
        #
        # No new event is written to the event log.
        # ----------------------------------------------------

        elif (
            current_fault is not None
            and current_fault == self.active_fault
        ):

            result["event_type"] = (
                f"{current_fault}_ACTIVE"
            )

            # Intentionally do NOT log.
            #
            # This prevents:
            #
            # OVERVOLTAGE_STARTED
            # OVERVOLTAGE_ACTIVE
            # OVERVOLTAGE_ACTIVE
            # OVERVOLTAGE_ACTIVE
            #
            # from filling the event log every second.


        # ----------------------------------------------------
        # CASE 3: FAULT CHANGED
        # ----------------------------------------------------
        #
        # Example:
        #
        # OVERVOLTAGE
        #      ↓
        # OVERCURRENT
        #
        # Two events must be logged:
        #
        # 1. OVERVOLTAGE_CLEARED
        # 2. OVERCURRENT_STARTED
        # ----------------------------------------------------

        elif (
            current_fault is not None
            and self.active_fault is not None
            and current_fault != self.active_fault
        ):

            previous_fault = self.active_fault

            print(
                f"⚠️ FAULT CHANGED: "
                f"{previous_fault} -> {current_fault}"
            )


            # ----------------------------------------------
            # Clear previous fault
            # ----------------------------------------------

            clear_result = result.copy()

            clear_result["event_type"] = (
                f"{previous_fault}_CLEARED"
            )

            self.logger.log(
                measurements,
                clear_result
            )


            # ----------------------------------------------
            # Start new fault
            # ----------------------------------------------

            start_result = result.copy()

            start_result["event_type"] = (
                f"{current_fault}_STARTED"
            )

            self.logger.log(
                measurements,
                start_result
            )


            # Update active fault
            self.active_fault = current_fault


            # The returned result describes the NEW
            # current fault.

            result["event_type"] = (
                f"{current_fault}_STARTED"
            )


        # ----------------------------------------------------
        # CASE 4: FAULT CLEARED
        # ----------------------------------------------------
        #
        # Example:
        #
        # OVERVOLTAGE
        #      ↓
        # NORMAL
        #
        # Event:
        #
        # OVERVOLTAGE_CLEARED
        # ----------------------------------------------------

        elif (
            current_fault is None
            and self.active_fault is not None
        ):

            cleared_fault = self.active_fault

            print(
                f"✅ FAULT CLEARED: {cleared_fault}"
            )

            event_type = (
                f"{cleared_fault}_CLEARED"
            )

            result["event_type"] = event_type

            # Log fault-cleared event
            self.logger.log(
                measurements,
                result
            )

            # No active fault anymore
            self.active_fault = None


        # ----------------------------------------------------
        # CASE 5: NORMAL CONTINUES
        # ----------------------------------------------------
        #
        # Example:
        #
        # NORMAL
        # NORMAL
        # NORMAL
        #
        # No event is logged.
        # ----------------------------------------------------

        else:

            result["event_type"] = "NORMAL"


        # ----------------------------------------------------
        # Return complete monitoring result
        # ----------------------------------------------------

        return result


# ============================================================
# TEST MONITORING ENGINE
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("          SMART SUBSTATION MONITORING ENGINE")
    print("=" * 65)


    engine = MonitoringEngine()


    # --------------------------------------------------------
    # Test sequence
    # --------------------------------------------------------
    #
    # This intentionally tests:
    #
    # NORMAL
    #   ↓
    # OVERVOLTAGE START
    #   ↓
    # OVERVOLTAGE ACTIVE
    #   ↓
    # OVERVOLTAGE ACTIVE
    #   ↓
    # NORMAL / OVERVOLTAGE CLEARED
    #   ↓
    # OVERCURRENT START
    #   ↓
    # OVERCURRENT ACTIVE
    #   ↓
    # NORMAL / OVERCURRENT CLEARED
    #
    # And the same for frequency faults.
    # --------------------------------------------------------

    test_conditions = [

        "normal",

        "overvoltage",
        "overvoltage",
        "overvoltage",

        "normal",

        "overcurrent",
        "overcurrent",

        "normal",

        "underfrequency",
        "underfrequency",

        "normal",

        "overfrequency",
        "overfrequency",

        "normal",
    ]


    # --------------------------------------------------------
    # Run monitoring tests
    # --------------------------------------------------------

    for condition in test_conditions:

        system = PowerSystem()

        system.set_condition(condition)

        measurements = system.calculate_power()

        result = engine.evaluate(
            measurements
        )


        # ----------------------------------------------------
        # Display measurements
        # ----------------------------------------------------

        print()

        print(
            f"Condition: {condition}"
        )

        print(
            f"Voltage: "
            f"{measurements['voltage']:.2f} V"
        )

        print(
            f"Current: "
            f"{measurements['current']:.2f} A"
        )

        print(
            f"Frequency: "
            f"{measurements['frequency']:.2f} Hz"
        )

        print(
            f"Power Factor: "
            f"{measurements['power_factor']:.2f}"
        )

        print(
            f"Rule alarms: "
            f"{result['rule_alarms']}"
        )

        print(
            f"ML anomaly: "
            f"{result['ml_anomaly']}"
        )

        print(
            f"Anomaly score: "
            f"{result['anomaly_score']:.4f}"
        )

        print(
            f"Overall status: "
            f"{result['overall_status']}"
        )

        print(
            f"Event type: "
            f"{result['event_type']}"
        )


    # --------------------------------------------------------
    # Test complete
    # --------------------------------------------------------

    print()

    print("=" * 65)
    print("                 TEST COMPLETE")
    print("=" * 65)