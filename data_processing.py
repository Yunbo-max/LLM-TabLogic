import pandas as pd
from typing import Dict, List

def apply_column_filtering(df: pd.DataFrame,
                         hierarchical_dict: dict,
                         mathematical_dict: dict,
                         temporal_list: list,
                         args):
    """
    Modify df by:
    - Removing hierarchical value columns (keeping most specific)
    - Removing mathematical derived columns (keeping components)
    - Replacing temporal values with day differences
    Returns transformed df and a dict containing dropped/replaced data for reversal.
    """
    df = df.copy()
    backup = {
        "dropped_columns": {},
        "temporal_originals": {},
        "mathematical": {}
    }

    # Initialize empty structures if None is passed
    hierarchical_dict = hierarchical_dict or {}
    mathematical_dict = mathematical_dict or {}
    temporal_list = temporal_list or []

    # 1. Process hierarchical relationships
    hierarchical_keys = set(hierarchical_dict.keys())
    hierarchical_values = set()
    for values in hierarchical_dict.values():
        hierarchical_values.update(values)
    
    # Only drop values that aren't keys (less specific columns)
    drop_candidates = hierarchical_values - hierarchical_keys

    for col in drop_candidates:
        if col in df.columns:
            backup["dropped_columns"][col] = df[col].copy()
            df.drop(columns=col, inplace=True)
    
    # 2. Process mathematical relationships
    for group_name, components in mathematical_dict.items():
        # Last component is assumed to be the formula string
        formula_str = components[-1] if isinstance(components[-1], str) else None
        derived_col = components[-2] if len(components) >= 2 else None
        base_cols = components[:-2] if formula_str else components[:-1]

        if args.data == 'adult':
            # Skip if derived_col or any base_col is in dropped hierarchical columns
            if derived_col in hierarchical_values or any(col in hierarchical_values for col in base_cols):
                continue  # Skip this mathematical entry
        
        backup["mathematical"][derived_col] = {
            "base_columns": base_cols,
            "formula": formula_str
        }
        if derived_col and derived_col in df.columns:
            df.drop(columns=derived_col, inplace=True)

    # 3. Process temporal relationships
    for group in temporal_list:
        if len(group) < 2:
            continue
        base_col = group[0]
        if base_col not in df.columns:
            continue
            
        # Convert base column to datetime
        df[base_col] = pd.to_datetime(df[base_col], errors='coerce')
        
        for col in group[1:]:
            if col in df.columns:
                # Backup original before transformation
                backup["temporal_originals"][col] = df[col].copy()
                # Convert to datetime and calculate difference
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df[col] = (df[col] - df[base_col]).dt.days

    return df, backup

def restore_dataframe(df: pd.DataFrame, backup: dict, args) -> pd.DataFrame:
    """
    Restore dropped columns, recalculate mathematical relationships,
    and restore original temporal columns from backup.
    """
    df = df.copy()

    # 1. Restore hierarchical columns
    for col, series in backup.get("dropped_columns", {}).items():
        df[col] = series
    
    # 3. Restore temporal columns
    for col, series in backup.get("temporal_originals", {}).items():
        df[col] = series

    # 2. Recalculate mathematical relationships
    for derived_col, info in backup.get("mathematical", {}).items():
        base_cols = info["base_columns"]
        formula_str = info["formula"]
        
        try:
            if formula_str:
                if args.data == 'icustays' or args.data == 'transfers':
                    namespace = {col: pd.to_datetime(df[col]) for col in base_cols}
                else:
                    namespace = {col: df[col] for col in base_cols}

                exec(formula_str, namespace)
                if args.data == 'icustays' or args.data == 'transfers':
                    df[derived_col] = namespace.get(derived_col).dt.total_seconds() / 86400
                else:
                    df[derived_col] = namespace.get(derived_col)

        except Exception as e:
            print(f"Failed to restore {derived_col}: {str(e)}")

    return df