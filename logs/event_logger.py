from pathlib import Path
from datetime import datetime
import csv


class EventLogger:

    def __init__(self):

        # ----------------------------------------------------
        # Project root
        # ----------------------------------------------------

        PROJECT_ROOT = Path(__file__).parent.parent

        # ----------------------------------------------------
        # Event file
        # ----------------------------------------------------

        self.data_dir = PROJECT_ROOT / "data"
        self.event_file = self.data_dir / "events.csv"

        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Create CSV file with header if it doesn't exist
        if not self.event_file.exists():

            with open(
                self.event_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "event_type",
                    "voltage",
                    "current",
                    "frequency",
                    "power_factor",
                    "active_power",
                    "reactive_power",
                    "ml_anomaly",
                    "anomaly_score",
                    "overall_status"
                ])

    # ========================================================
    # LOG EVENT
    # ========================================================

    def log(self, measurements, result):

        event_type = result.get(
            "event_type",
            "UNKNOWN"
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.event_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                event_type,

                measurements.get("voltage"),
                measurements.get("current"),
                measurements.get("frequency"),
                measurements.get("power_factor"),
                measurements.get("active_power"),
                measurements.get("reactive_power"),

                result.get("ml_anomaly"),
                result.get("anomaly_score"),
                result.get("overall_status"),
            ])

        print(f"Event logged: {event_type}")