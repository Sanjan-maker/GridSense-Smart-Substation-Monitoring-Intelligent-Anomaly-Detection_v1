from pathlib import Path
import sys
import time
from datetime import datetime

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Add simulator to Python path
sys.path.append(str(PROJECT_ROOT / "simulator"))

from power_system import PowerSystem
from monitoring_engine import MonitoringEngine


def run_realtime_monitor():

    system = PowerSystem()
    engine = MonitoringEngine()

    print("=" * 70)
    print("       SMART SUBSTATION - FAULT INJECTION DEMO")
    print("=" * 70)
    print("Starting real-time monitoring...")
    print("Fault scenario:")
    print("  0-10 sec  : NORMAL")
    print(" 10-20 sec  : OVERVOLTAGE")
    print(" 20-30 sec  : NORMAL")
    print(" 30-40 sec  : OVERCURRENT")
    print(" 40-50 sec  : NORMAL")
    print(" 50-60 sec  : UNDERFREQUENCY")
    print(" 60+ sec    : NORMAL")
    print()
    print("Press Ctrl+C to stop.\n")

    start_time = time.time()

    try:

        while True:

            elapsed = int(time.time() - start_time)

            # --------------------------------
            # Select operating condition
            # --------------------------------

            if elapsed < 10:
                condition = "normal"

            elif elapsed < 20:
                condition = "overvoltage"

            elif elapsed < 30:
                condition = "normal"

            elif elapsed < 40:
                condition = "overcurrent"

            elif elapsed < 50:
                condition = "normal"

            elif elapsed < 60:
                condition = "underfrequency"

            else:
                condition = "normal"

            # Apply condition
            system.set_condition(condition)

            # Generate measurement
            measurements = system.calculate_power()

            # Analyze measurement
            result = engine.evaluate(measurements)

            timestamp = datetime.now().strftime("%H:%M:%S")

            # --------------------------------
            # Display live status
            # --------------------------------

            print(
                f"[{timestamp}] "
                f"{condition.upper():<15} | "
                f"V={measurements['voltage']:>6.2f} V | "
                f"I={measurements['current']:>5.2f} A | "
                f"F={measurements['frequency']:>5.2f} Hz | "
                f"STATUS={result['overall_status']}"
            )

            # Display rule alarm
            if result["rule_alarms"]:
                print(
                    f"    🚨 RULE ALARM: "
                    f"{', '.join(result['rule_alarms'])}"
                )

            # Display ML anomaly
            if result["ml_anomaly"]:
                print(
                    f"    🤖 ML ANOMALY: "
                    f"score={result['anomaly_score']:.4f}"
                )

            time.sleep(1)

    except KeyboardInterrupt:

        print("\n")
        print("=" * 70)
        print("Monitoring stopped by user.")
        print("=" * 70)


if __name__ == "__main__":
    run_realtime_monitor()