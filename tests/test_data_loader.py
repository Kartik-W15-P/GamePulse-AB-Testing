import pandas as pd
import pytest

from src.data_loader import (
    validate_schema,
    validate_data_quality
)


@pytest.fixture
def valid_dataset():
    return pd.DataFrame({
        "userid": [101, 102, 103],
        "version": ["gate_30", "gate_40", "gate_30"],
        "sum_gamerounds": [10, 20, 30],
        "retention_1": [True, False, True],
        "retention_7": [False, True, True]
    })


def test_valid_schema(valid_dataset):
    validate_schema(valid_dataset)


def test_missing_column():
    df = pd.DataFrame({
        "userid": [101],
        "version": ["gate_30"]
    })

    with pytest.raises(ValueError):
        validate_schema(df)


def test_valid_data_quality(valid_dataset):
    validate_data_quality(valid_dataset)


def test_empty_dataset(valid_dataset):
    df = valid_dataset.iloc[0:0]

    with pytest.raises(ValueError):
        validate_data_quality(df)


def test_duplicate_user_ids(valid_dataset):
    valid_dataset.loc[1, "userid"] = 101

    with pytest.raises(ValueError):
        validate_data_quality(valid_dataset)


def test_invalid_experiment_version(valid_dataset):
    valid_dataset.loc[0, "version"] = "gate_50"

    with pytest.raises(ValueError):
        validate_data_quality(valid_dataset)


def test_negative_game_rounds(valid_dataset):
    valid_dataset.loc[0, "sum_gamerounds"] = -10

    with pytest.raises(ValueError):
        validate_data_quality(valid_dataset)


def test_missing_values(valid_dataset):
    valid_dataset["retention_1"] = (
        valid_dataset["retention_1"].astype("object")
    )
    valid_dataset.loc[0, "retention_1"] = None

    with pytest.raises(ValueError):
        validate_data_quality(valid_dataset)


def test_invalid_retention_type(valid_dataset):
    valid_dataset["retention_1"] = [1, 0, 1]

    with pytest.raises(ValueError):
        validate_data_quality(valid_dataset)