import random
import math


class PowerSystem:

    def __init__(self):
        self.condition = "normal"

    def set_condition(self, condition):
        self.condition = condition

    def calculate_power(self):

        # --------------------------------
        # Normal operating values
        # --------------------------------
        voltage = 230.0 + random.uniform(-1.5, 1.5)
        current = 10.0 + random.uniform(-0.3, 0.3)
        frequency = 50.0 + random.uniform(-0.05, 0.05)
        power_factor = 0.92 + random.uniform(-0.01, 0.01)

        # --------------------------------
        # Fault conditions
        # --------------------------------
        if self.condition == "overvoltage":
            voltage = 265.0

        elif self.condition == "undervoltage":
            voltage = 180.0

        elif self.condition == "overcurrent":
            current = 30.0

        elif self.condition == "underfrequency":
            frequency = 47.0

        elif self.condition == "overfrequency":
            frequency = 53.0

        # --------------------------------
        # Electrical power calculations
        # --------------------------------
        apparent_power = voltage * current

        active_power = apparent_power * power_factor

        reactive_power = apparent_power * math.sqrt(
            max(0, 1 - power_factor ** 2)
        )

        return {
            "voltage": voltage,
            "current": current,
            "frequency": frequency,
            "power_factor": power_factor,
            "active_power": active_power,
            "reactive_power": reactive_power,
        }


if __name__ == "__main__":

    system = PowerSystem()

    for _ in range(5):

        measurements = system.calculate_power()

        print(f"voltage: {measurements['voltage']:.2f}")
        print(f"current: {measurements['current']:.2f}")
        print(f"frequency: {measurements['frequency']:.2f}")
        print(f"power_factor: {measurements['power_factor']:.2f}")
        print(f"active_power: {measurements['active_power']:.2f}")
        print(f"reactive_power: {measurements['reactive_power']:.2f}")
        print("-" * 30)