# LLM-TabGEO

# Data Column Analysis Tool

A Python tool for automated hierarchical, mathematical, and temporal analysis of dataset columns using AI-powered insights. This tool analyzes CSV datasets, applies intelligent column filtering, and provides comprehensive data transformations.

## Features

- 🤖 **AI-Powered Analysis**: Uses DeepSeek API for intelligent column analysis
- 📊 **Multi-dimensional Analysis**: Performs hierarchical, mathematical, and temporal analysis
- 🔄 **Data Transformation**: Applies filtering and provides restoration capabilities
- 📁 **Organized Output**: Saves results in structured directories
- ⚙️ **Configurable**: Flexible command-line arguments for customization

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/yourusername/data-column-analysis.git
cd data-column-analysis
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Python Packages

Create a `requirements.txt` file with the following dependencies:

```txt
pandas>=1.3.0
requests>=2.25.0
argparse
json
os
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

1. **Create a `config.py` file** with your API configuration:

```python
def get_api_key(model_name):
    """Return API key for the specified model"""
    api_keys = {
        'deepseek': 'your_deepseek_api_key_here',
        # Add other models as needed
    }
    return api_keys.get(model_name)

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

2. **Set up your API key**:
   - Replace `'your_deepseek_api_key_here'` with your actual DeepSeek API key
   - Add column descriptions for your datasets

### Dataset Preparation

1. Place your CSV files in the project directory
2. Name them as `{dataset_name}.csv` (e.g., `icustays.csv`)
3. Add corresponding column descriptions in `config.py`

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

1. **FilteredOutput.csv**: Dataset after applying intelligent filtering
2. **Restored.csv**: Restored version of the filtered dataset
3. **Console Output**: Detailed analysis results in JSON format

### Example Output Structure

```
results/
└── icustays/
    ├── FilteredOutput.csv
    └── Restored.csv
```

## Implementation Details

### Core Components

1. **main.py**: Entry point that orchestrates the analysis workflow
2. **config.py**: Manages API keys and dataset configurations
3. **api_clients.py**: Handles communication with AI APIs
4. **data_processing.py**: Implements data filtering and restoration logic
5. **utils.py**: Provides utility functions for data manipulation

### Analysis Types

- **Hierarchical Analysis**: Identifies relationships and hierarchies in data
- **Mathematical Analysis**: Detects numerical patterns and mathematical relationships
- **Temporal Analysis**: Analyzes time-based patterns and sequences

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API key is correctly set in `config.py`
2. **File Not Found**: Check that your CSV file exists and is named correctly
3. **Import Errors**: Install all required dependencies using `pip install -r requirements.txt`

### Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation
- Review the example configurations

## Acknowledgments

- DeepSeek AI for providing the analysis API
- pandas community for excellent data manipulation tools
- Contributors and maintainers of this project

---

**Note**: This tool requires an active internet connection and valid API keys for the AI analysis features.
