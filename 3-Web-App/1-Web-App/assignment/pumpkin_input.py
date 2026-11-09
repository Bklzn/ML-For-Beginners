import pandas as pd

COLUMNS = {
    "city_name": "City Name",
    "item_size": "Item Size",
    "package": "Package",
    "variety": "Variety",
    "origin": "Origin",
}


def build_input_row(values, allowed):
    missing = set(COLUMNS) - set(values)
    extra = set(values) - set(COLUMNS)
    if missing or extra:
        raise ValueError(f"missing={missing or '-'}, extra={extra or '-'}")

    for key, value in values.items():
        if value not in allowed[key]:
            raise ValueError(f"Invalid value for {key}: {value!r}")

    return pd.DataFrame({COLUMNS[key]: [values[key]] for key in COLUMNS})