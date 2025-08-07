import json
import pandas as pd
import argparse
import os
from config import get_api_key, get_column_descriptions
from api_clients import analyze_columns_with_deepseek
from data_processing import apply_column_filtering, restore_dataframe


def lowercase_analysis_results(analysis_results):
    """
    Convert all string values in the analysis results dictionary to lowercase.
    
    Args:
        analysis_results (dict): Dictionary containing hierarchical, mathematical, 
                               and temporal analysis results.
                               
    Returns:
        dict: New dictionary with all string values converted to lowercase.
    """
    lowercased_results = {
        "hierarchical": {},
        "mathematical": {},
        "temporal": {}
    }
    
    # Process hierarchical analysis
    for col, categories in analysis_results["hierarchical"].items():
        lowercased_results["hierarchical"][col] = {
            k: v.lower() if isinstance(v, str) else v 
            for k, v in categories.items()
        }
    
    # Process mathematical analysis
    for col, operations in analysis_results["mathematical"].items():
        lowercased_results["mathematical"][col] = [
            op.lower() if isinstance(op, str) else op 
            for op in operations
        ]
    
    # Process temporal analysis
    for col, patterns in analysis_results["temporal"].items():
        lowercased_results["temporal"][col] = [
            pattern.lower() if isinstance(pattern, str) else pattern 
            for pattern in patterns
        ]
    
    return lowercased_results


def main():
    # Setup argument parser directly in main
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="dataset to be used", type=str, default='icustays')
    parser.add_argument("--model", help="generative model", type=str, default='deepseek')
    parser.add_argument("--temp", type=float, default=0.1)
    parser.add_argument("--max_tok", type=int, default=1000)
    args = parser.parse_args()
    
    # Get API key and column descriptions
    API_KEY = get_api_key(args.model)
    COLUMN_DESCRIPTIONS = get_column_descriptions(args.data)
    
    if not COLUMN_DESCRIPTIONS:
        print(f"No column descriptions found for dataset: {args.data}")
        return
    
    # Load dataset
    df = pd.read_csv(f"data/{args.data}.csv")
    
    # Perform the analysis
    analysis_results = analyze_columns_with_deepseek(API_KEY, COLUMN_DESCRIPTIONS, args)
    
    # Print results
    print("=== Hierarchical Analysis ===")
    print(json.dumps(analysis_results["hierarchical"], indent=2))
    
    print("\n=== Mathematical Analysis ===")
    print(json.dumps(analysis_results["mathematical"], indent=2))
    
    print("\n=== Temporal Analysis ===")
    print(json.dumps(analysis_results["temporal"], indent=2))
    
    # Convert to lowercase
    analysis_results = lowercase_analysis_results(analysis_results)
    
    # Apply filtering
    df_transformed, backup = apply_column_filtering(
        df,
        analysis_results["hierarchical"],
        analysis_results["mathematical"],
        analysis_results["temporal"],
        args
    )
    
    # Create results directory if it doesn't exist
    results_dir = f"results/{args.data}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Save filtered output
    filtered_output_path = os.path.join(results_dir, "FilteredOutput.csv")
    df_transformed.to_csv(filtered_output_path, index=False)
    print(f"Filtered output saved to: {filtered_output_path}")
    
    # Restore when needed
    df_restored = restore_dataframe(df_transformed, backup, args)
    restored_output_path = os.path.join(results_dir, "Restored.csv")
    df_restored.to_csv(restored_output_path, index=False)
    print(f"Restored output saved to: {restored_output_path}")

if __name__ == "__main__":
    main()