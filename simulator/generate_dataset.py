import csv
from pathlib import Path

from power_system import PowerSystem


def generate_normal_dataset(samples=1000):
    system = PowerSystem()

    # Go from simulator/ back to the project root, then into data/
    output_path = (
        Path(__file__).parent.parent
        / "data"
        / "normal_operation.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "voltage",
        "current",
        "frequency",
        "power_factor",
        "active_power",
        "reactive_power",
        "apparent_power",
    ]

    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(samples):
            system.set_condition("normal")
            system.add_normal_variation()

            measurements = system.calculate_power()

            writer.writerow({
                "voltage": measurements["voltage"],
                "current": measurements["current"],
                "frequency": measurements["frequency"],
                "power_factor": measurements["power_factor"],
                "active_power": measurements["active_power"],
                "reactive_power": measurements["reactive_power"],
                "apparent_power": measurements["apparent_power"],
            })

    print(f"Generated {samples} normal-operation samples.")
    print(f"Dataset saved to: {output_path}")


if __name__ == "__main__":
    generate_normal_dataset()