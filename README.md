# LLM-TabFlow: Logic Preservation in Tabular Data Generation

Official implementation of **LLM-TabFlow: Synthetic Tabular Data Generation with Inter-column Logical Relationship Preservation**.

[![arXiv](https://img.shields.io/badge/arXiv-2503.02161-b31b1b.svg)](https://arxiv.org/abs/2503.02161)



🚀 **Coming Soon**: Our new paper **"LLM-TabGEO: Prompt-Guided Geometric Diffusion for Logic-Preserving Tabular Data Generation"** will be available soon!

This tool provides automated hierarchical, mathematical, and temporal analysis of dataset columns using prompt-based reasoning with Large language Models for capturing the logical relationship among tabular columns.


## Installation

### Prerequisites

- Python 3.10+
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/yourusername/LLM-TabGEO.git
cd LLM-TabGEO
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```
data-column-analysis/
├── main.py                 # Main execution script
├── config.py              # Configuration and API key management
├── api_clients.py         # API client implementations
├── data_processing.py     # Data filtering and transformation
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Directory for input CSV files
│   └── icustays.csv      # Example dataset
└── results/              # Output directory (auto-created)
    └── {dataset_name}/   # Results organized by dataset
        ├── FilteredOutput.csv
        └── Restored.csv
```

## Configuration

### API Key Setup

1. **Set up your API key**: 
**`config.py` file**:
```python
def get_api_key(model_name):
    """Return API key for the specified model"""
    api_keys = {
        'deepseek': 'your_deepseek_api_key_here',
        # Add other models as needed
    }
    return api_keys.get(model_name)
```

2. **Set up your API key**:
   - Replace `'your_deepseek_api_key_here'` with your actual DeepSeek API key in `config.py`

### Dataset Preparation
**`config.py` file**:
```python
def get_column_descriptions(dataset_name):
    """Return column descriptions for the specified dataset"""
    descriptions = {
        'icustays': {
            'column1': 'Description of column 1',
            'column2': 'Description of column 2',
            # Add your column descriptions here
        }
    }
    return descriptions.get(dataset_name, {})
```
1. Place your CSV files in the project directory
2. Name them as `{dataset_name}.csv` (e.g., `icustays.csv`)
3. Add corresponding column descriptions in `config.py`

### Supported Datasets

This implementation has been tested on datasets across finance, healthcare, and logistics domains:

- **Healthcare**: [MIMIC-III](https://mimic.mit.edu/)
- **Population**: [UCI Adult Income Dataset](https://archive.ics.uci.edu/ml/datasets/adult)
- **Logistics**: [Dataco Dataset](https://data.mendeley.com/datasets/8gx2fvg2k6/3)

## Usage

### Basic Usage

```bash
python main.py --data icustays
```

### Advanced Usage with Custom Parameters

```bash
python main.py --data icustays --model deepseek --temp 0.2 --max_tok 1500
```

### Command Line Arguments

| Argument | Description | Default | Type |
|----------|-------------|---------|------|
| `--data` | Dataset name to analyze | `icustays` | string |
| `--model` | AI model to use | `deepseek` | string |
| `--temp` | Temperature for AI generation | `0.1` | float |
| `--max_tok` | Maximum tokens for AI response | `1000` | int |

## Output

The tool generates the following outputs in `results/{dataset_name}/`:
1. **FilteredOutput.csv**: Dataset after applying LLM-conditional compression
2. **Restored.csv**: Dataset with logical relationships restored from the compressed version

## Citation

If you use this code in your research, please cite our paper:

```bibtex
@article{long2025llm,
  title={LLM-TabFlow: Synthetic Tabular Data Generation with Inter-column Logical Relationship Preservation},
  author={Long, Yunbo and Xu, Liming and Brintrup, Alexandra},
  journal={arXiv preprint arXiv:2503.02161},
  year={2025}
}
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

