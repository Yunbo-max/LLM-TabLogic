import requests
import json
import openai
from typing import Dict, List, Union

import ast
import re
from typing import Union, Dict, List, Optional

def extract_python_structure(content: str) -> Optional[Union[Dict, List]]:
    """
    Extract Python dictionary or list from a string response that may contain mixed content.
    
    Args:
        content: String response that may contain a Python structure
        
    Returns:
        Extracted Python dict/list or None if no valid structure found
    """
    # First try to find complete code blocks
    code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', content, re.DOTALL)
    for block in code_blocks:
        try:
            parsed = ast.literal_eval(block.strip())
            if isinstance(parsed, (dict, list)):
                return parsed
        except (SyntaxError, ValueError):
            continue
    
    # If no code blocks, look for standalone structures
    pattern = r'(?P<structure>\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}|\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\])'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        try:
            parsed = ast.literal_eval(match.group('structure'))
            if isinstance(parsed, (dict, list)):
                return parsed
        except (SyntaxError, ValueError):
            continue
    
    return None




def analyze_columns_with_deepseek(api_key: str, column_descriptions: str, args) -> Dict[str, Union[Dict, List]]:
    if args.model == 'gpt':
        client = openai.OpenAI(api_key=api_key)
    
    # Define the prompts for each analysis type
    prompts_deepseek = {

        "hierarchical": {
    "system": "You are a data analysis expert that identifies hierarchical relationships between columns, where columns represent the SAME CONCEPT at DIFFERENT LEVELS OF GRANULARITY (e.g., City→State→Country). Only consider relationships that are EXPLICIT and DEFINITIVE.",
    "user": f"""Given these column descriptions:
{column_descriptions}

**Strict Requirements:**
1. Identify ONLY clear parent-child relationships where:
   - Columns represent THE SAME CONCEPT at different scales without time series data
   - Relationships are LOGICALLY NECESSARY (not just correlated)
   - There is DIRECT DEPENDENCY (e.g., City→Country)

2. For each VALID hierarchy:
   - Select the MOST SPECIFIC column as key
   - Include AT LEAST TWO RELATED COLUMNS per group
   - Each column must appear ONLY ONCE in the keys and values in total in the output.

3. Return ONLY a Python dictionary with this EXACT format:
   {{"specific_column": ["specific_column", "broader_column", ...]}}



Example VALID output:
{{"City": ["City", "State", "Country"]}}

Example INVALID output (would be rejected):
{{"Age": ["Age", "Income"]}}  # Not same concept"""
}
,
        
"mathematical": {
    "system": "You are a data analysis expert that identifies EXPLICIT mathematical equations between columns. Only consider relationships where columns are DIRECTLY CALCULATED from other columns through KNOWN FORMULAS.",
    "user": f"""Given these column descriptions:
{column_descriptions}

**Strict Requirements:**
1. Identify ONLY definitive calculation relationships where:
   - One column is MATHEMATICALLY DERIVED from others
   - The formula is UNAMBIGUOUS (e.g., Total = PartA + PartB)
   - The relationship is ALWAYS TRUE (not just correlated)

2. For each VALID mathematical group:
   - List ALL COMPONENT COLUMNS needed for the calculation
   - Include the DERIVED COLUMN in the value list
   - Each column must appear ONLY ONCE in the entire output
   - Minimum 2 columns per relationship

3. Return ONLY a Python dictionary with this EXACT format:
   {{"base_column": ["base_column", "derived_column","formula without additional description"]}}


Example VALID output:
{{
    "Price, Quantity": ["Price","Quantity","Total Price","Total Price = Price * Quantity"],
    "Benefit_per_order": ["Benefit_per_order", "Order_Profit_Per_Order","Benefit_per_order = Order_Profit_Per_Order"]
}}

"""
}
,
       "temporal": {
    "system": "You are a data analysis expert that identifies temporal relationships between columns.",
    "user": f"""Given these column descriptions:{column_descriptions}

**Strict Requirements:**
1. Review the description for each column and only consider those columns include time series data in t rather than the time gap or counting number data (e.g., "Order Date", "Arrival Date").
2. For each group, order the column names based on the time sequence.
3. Return a list of different lists of column names in chronological order for each group with different temporal relationships .

Example VALID output:
[
    ["Order Date", "Ship Date"],
    ["Check-in Time", "Check-out Time"]
]

"""
 }
    }


    prompts_gpt = {
        "hierarchical": {
            "system": "You are a data analysis expert that identifies hierarchical relationships between columns, where columns represent the SAME CONCEPT at DIFFERENT LEVELS OF GRANULARITY (e.g., City→State→Country). Only consider relationships that are EXPLICIT and DEFINITIVE.",
            "user": f"""Given the following column descriptions:
{column_descriptions}

**Instructions:** 
1. Identify ONLY clear parent-child relationships where:
   - Columns represent THE SAME CONCEPT at different scales without time series data
   - Relationships are LOGICALLY NECESSARY (not just correlated)
   - There is DIRECT DEPENDENCY (e.g., City→Country)

2. For each VALID hierarchy:
   - Select the MOST SPECIFIC column as key
   - Include AT LEAST TWO RELATED COLUMNS per group
   - Each column must appear ONLY ONCE in the keys and values in total in the output.

3. Return ONLY a Python dictionary with this EXACT format:
   {{"specific_column": ["specific_column", "broader_column", ...]}}



Example VALID output:
{{"City": ["City", "State", "Country"]}}

Example INVALID output (would be rejected):
{{"Age": ["Age", "Income"]}}  # Not same concept"""

        },
        "mathematical": {
            "system": "You are a data analysis expert that identifies EXPLICIT mathematical equations between columns. Only consider relationships where columns are DIRECTLY CALCULATED from other columns through KNOWN FORMULAS.",
            "user": f"""Given the following column descriptions:
{column_descriptions}

**Instructions:** 
**Strict Requirements:**
1. Identify ONLY definitive calculation relationships where:
   1.1 One column is MATHEMATICALLY DERIVED from others
   1.2 The formula is UNAMBIGUOUS (e.g., Total = PartA + PartB)
   1.3 The relationship is ALWAYS TRUE (not just correlated)

2. For each VALID mathematical group:
   2.1 List ALL COMPONENT COLUMNS needed for the calculation
   2.2 Include the DERIVED COLUMN in the value list
   2.3 Each column must appear ONLY ONCE in the entire output
   2.4 Minimum 2 columns per relationship

3. Return ONLY a Python dictionary with this EXACT format:
   {{"base_column": ["base_column", "derived_column","formula without additional description"]}}

Example VALID output:
{{
    "Price, Quantity": ["Price","Quantity","Total Price","Total Price = Price * Quantity"],
    "Benefit_per_order": ["Benefit_per_order", "Order_Profit_Per_Order","Benefit_per_order = Order_Profit_Per_Order"]
}}


Return ONLY the dictionary in proper Python syntax, nothing else."""
        },
        "temporal": {
            "system": "You are a data analysis expert that identifies temporal relationships between columns.",
            "user": f"""Given the following column descriptions:
{column_descriptions}

**Instructions:** 
1. Review the description for each column and only consider those columns include time series data in t rather than the time gap or counting number data (e.g., "Order Date", "Arrival Date").
2. For each group, order the column names based on the time sequence.
3. Return a list of different lists of column names in chronological order for each group with different temporal relationships .

Example format:
[
    ["Order Date", "Ship Date", "Arrival Date"],
    ["Check-in Time", "Check-out Time"]
]

Return ONLY the list in proper Python syntax, nothing else."""
        }
    }
    
    results = {}
    
    if args.model == 'gpt':
        return _process_gpt_analysis(client, prompts_gpt, args)
    elif args.model == 'deepseek':
        return _process_deepseek_analysis(api_key, prompts_deepseek, args)

def _process_gpt_analysis(client, prompts_gpt, args):
    results = {}
    for analysis_type, prompt in prompts_gpt.items():
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ],
            temperature=args.temp,
            max_tokens=args.max_tok
        )
        
        try:
            content = response.choices[0].message.content
            content = content.replace("```python", "").replace("```", "").strip()
            result = eval(content)
            results[analysis_type] = result
        except Exception as e:
            print(f"Error parsing {analysis_type} response: {e}")
            results[analysis_type] = None
    
    return results

def _process_deepseek_analysis(api_key, prompts, args):

    
    results = {}
    
    for analysis_type, prompt in prompts.items():
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ],
            "temperature": args.temp,
            "max_tokens": args.max_tok
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            response.raise_for_status()
            response_json = response.json()
            
            if not all(key in response_json for key in ['choices', 'model']):
                raise ValueError("Invalid API response structure")
                
            if len(response_json['choices']) == 0:
                raise ValueError("Empty choices in API response")
                
            content = response_json['choices'][0]['message']['content']
            
            print(f"\n=== Raw {analysis_type} response ===")
            print(content)
            
            extracted_content = extract_python_structure(content)
            
            if extracted_content is None:
                raise ValueError("No valid Python structure found in response")
                
            if analysis_type in ['hierarchical', 'mathematical'] and not isinstance(extracted_content, dict):
                raise ValueError(f"Expected dictionary for {analysis_type}, got {type(extracted_content)}")
                
            if analysis_type == 'temporal' and not isinstance(extracted_content, list):
                raise ValueError(f"Expected list for temporal, got {type(extracted_content)}")
            
            results[analysis_type] = extracted_content
            
        except requests.exceptions.RequestException as e:
            print(f"\n⚠️ API request failed for {analysis_type}: {str(e)}")
            results[analysis_type] = {"error": f"API request failed: {str(e)}"}
            
        except json.JSONDecodeError as e:
            print(f"\n⚠️ JSON decode failed for {analysis_type}: {str(e)}")
            print(f"Response text: {response.text[:200]}...")
            results[analysis_type] = {"error": f"JSON decode failed: {str(e)}"}
            
        except ValueError as e:
            print(f"\n⚠️ Validation failed for {analysis_type}: {str(e)}")
            results[analysis_type] = {"error": f"Validation failed: {str(e)}"}
            
        except Exception as e:
            print(f"\n⚠️ Unexpected error processing {analysis_type}: {str(e)}")
            results[analysis_type] = {"error": f"Unexpected error: {str(e)}"}
    
    return results