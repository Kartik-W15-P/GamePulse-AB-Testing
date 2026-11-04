
"""
GamePulse - Dataset Loading and Validation

Loads the original Cookie Cats A/B testing dataset
and performs basic data integrity checks.
"""

from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "cookie_cats.csv"

REQUIRED_COLUMNS = [
    "userid",
    "version",
    "sum_gamerounds",
    "retention_1",
    "retention_7",
]

VALID_VERSIONS = {"gate_30", "gate_40"}


# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

def load_dataset(file_path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Load the Cookie Cats dataset from a CSV file.

    Parameters
    ----------
    file_path : Path
        Location of the original CSV dataset.

    Returns
    -------
    pd.DataFrame
        Loaded player dataset.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)
    except (OSError, pd.errors.ParserError) as error:
        raise ValueError(
            f"Unable to read dataset: {error}"
        ) from error

    print(f"Dataset loaded successfully: {file_path.name}")
    print(f"Dataset shape: {df.shape}")

    return df


# --------------------------------------------------
# 3. VALIDATE DATASET STRUCTURE
# --------------------------------------------------

def validate_schema(df: pd.DataFrame) -> None:
    """
    Check whether all required columns exist.
    """

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    print("Schema validation passed.")


# --------------------------------------------------
# 4. VALIDATE DATA QUALITY
# --------------------------------------------------

def validate_data_quality(df: pd.DataFrame) -> None:
    """
    Validate basic data quality rules.
    """

    if df.empty:
        raise ValueError("Dataset is empty.")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Missing values detected.")

    if df["userid"].duplicated().any():
        raise ValueError("Duplicate player IDs detected.")

    invalid_versions = set(df["version"].unique()) - VALID_VERSIONS

    if invalid_versions:
        raise ValueError(
            f"Invalid experiment versions: {invalid_versions}"
        )

    if (df["sum_gamerounds"] < 0).any():
        raise ValueError("Negative game rounds detected.")

    if not pd.api.types.is_bool_dtype(df["retention_1"]):
        raise ValueError("retention_1 must contain Boolean values.")

    if not pd.api.types.is_bool_dtype(df["retention_7"]):
        raise ValueError("retention_7 must contain Boolean values.")

    print("Data quality validation passed.")


# --------------------------------------------------
# 5. COMPLETE VALIDATION PIPELINE
# --------------------------------------------------

def get_validated_dataset(
    file_path: Path = DATA_PATH
) -> pd.DataFrame:
    """
    Load the dataset and perform all validations.
    """

    df = load_dataset(file_path)

    validate_schema(df)

    validate_data_quality(df)

    print("\nAll dataset validations passed!")
    print(f"Total players: {len(df):,}")

    return df


# --------------------------------------------------
# 6. MODULE EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    dataset = get_validated_dataset()

    print("\nExperiment group distribution:")
    print(dataset["version"].value_counts())

    print("\nFirst five records:")
    print(dataset.head())
