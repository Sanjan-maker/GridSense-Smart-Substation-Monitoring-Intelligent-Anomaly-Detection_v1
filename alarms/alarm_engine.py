class AlarmEngine:

    LIMITS = {
        "voltage_high": 250.0,
        "voltage_low": 200.0,
        "current_high": 20.0,
        "frequency_high": 52.0,
        "frequency_low": 48.0,
    }

    def evaluate(self, measurements):
        alarms = []

        voltage = measurements["voltage"]
        current = measurements["current"]
        frequency = measurements["frequency"]

        if voltage > self.LIMITS["voltage_high"]:
            alarms.append("OVERVOLTAGE")

        if voltage < self.LIMITS["voltage_low"]:
            alarms.append("UNDERVOLTAGE")

        if current > self.LIMITS["current_high"]:
            alarms.append("OVERCURRENT")

        if frequency > self.LIMITS["frequency_high"]:
            alarms.append("OVERFREQUENCY")

        if frequency < self.LIMITS["frequency_low"]:
            alarms.append("UNDERFREQUENCY")

        return alarms


if __name__ == "__main__":
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent / "simulator"))

    from power_system import PowerSystem

    engine = AlarmEngine()

    test_conditions = [
        "normal",
        "overvoltage",
        "undervoltage",
        "overcurrent",
        "underfrequency",
        "overfrequency",
    ]

    for condition in test_conditions:
        system = PowerSystem()
        system.set_condition(condition)

        measurements = system.calculate_power()
        alarms = engine.evaluate(measurements)

        print(f"{condition:18} -> {alarms}")