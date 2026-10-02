import pandas as pd
import yaml
import json
from typing import Any

def read_config(filename: str) -> dict[str, Any]:
    """Read settings from config.yml."""
    with open(filename, "r") as file:
        return yaml.safe_load(file)

def read_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read sensor and calibration data."""
    sensors = pd.read_excel("sensors.xlsx")
    calibrations = pd.read_csv("calibrations.csv")
    return sensors, calibrations

def join_data(
    sensors: pd.DataFrame,
    calibrations: pd.DataFrame
) -> pd.DataFrame:
    """Join sensor and calibration data using sensor_id."""
    return sensors.merge(
        calibrations,
        on="sensor_id",
        how="left"
    )

def find_overdue(
    data: pd.DataFrame,
    max_days: int
) -> pd.DataFrame:
    """Find sensors with more days since calibration than allowed."""
    return data[
        data["days_since_calibration"] > max_days
    ]

def export_json(
    overdue: pd.DataFrame,
    output_file: str
) -> None:
    """Export overdue sensor information to a formatted JSON file."""
    overdue_sensors = overdue[
        [
            "sensor_id",
            "lab_room",
            "owner",
            "days_since_calibration"
        ]
    ]

    overdue_list = overdue_sensors.to_dict(
        orient="records"
    )

    with open(output_file, "w") as file:
        json.dump(overdue_list, file, indent=2)


def main() -> None:
    """Run the complete sensor calibration pipeline."""
    config = read_config("config.yml")
    max_days = config["max_days_since_calibration"]
    output_file = config["output_file"]
    sensors, calibrations = read_data()
    data = join_data(sensors, calibrations)
    overdue = find_overdue(data, max_days)
    export_json(overdue, output_file)
    print(f"Overdue sensors saved to {output_file}")

if __name__ == "__main__":
    main()
    