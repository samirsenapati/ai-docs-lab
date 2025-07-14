# AI Docs Lab - API Documentation

## Overview

AI Docs Lab is an AI-powered documentation pipeline that provides utilities for mathematical operations, log processing, and automated incident report generation using Large Language Models.

## Table of Contents

1. [Math Utilities Module (`src/example.py`)](#math-utilities-module)
2. [Log Extraction Script (`scripts/extract_logs.py`)](#log-extraction-script)
3. [LLM Report Generator (`scripts/gen_llm.py`)](#llm-report-generator)
4. [Getting Started](#getting-started)
5. [Examples](#examples)

---

## Math Utilities Module

**Location:** `src/example.py`

This module provides basic mathematical utility functions with clean, documented interfaces.

### Functions

#### `add(a, b)`

Calculates the sum of two numbers.

**Parameters:**
- `a` (int/float): First number
- `b` (int/float): Second number

**Returns:**
- (int/float): The sum of `a` and `b`

**Example:**
```python
from src.example import add

result = add(5, 3)
print(result)  # Output: 8

# Works with floats too
result = add(2.5, 1.7)
print(result)  # Output: 4.2
```

#### `multiply(a, b)`

Calculates the product of two numbers.

**Parameters:**
- `a` (int/float): First number
- `b` (int/float): Second number

**Returns:**
- (int/float): The product of `a` and `b`

**Example:**
```python
from src.example import multiply

result = multiply(4, 6)
print(result)  # Output: 24

# Works with floats too
result = multiply(2.5, 4)
print(result)  # Output: 10.0
```

---

## Log Extraction Script

**Location:** `scripts/extract_logs.py`

This script processes log files to extract ERROR and WARN entries, generating a markdown summary.

### Functionality

- **Input:** `logs/sample.log` (configurable via `input_path` variable)
- **Output:** `docs/generated/log_summary.md` (configurable via `output_path` variable)
- **Processing:** Filters lines containing "ERROR" or "WARN"
- **Format:** Generates a markdown file with bullet-pointed error/warning entries

### Configuration

```python
input_path = "logs/sample.log"      # Path to input log file
output_path = "docs/generated/log_summary.md"  # Path to output markdown
```

### Usage

```bash
# Run the log extraction script
python scripts/extract_logs.py
```

### Input Format

The script expects standard log files where errors and warnings contain the keywords "ERROR" or "WARN":

```
2024-01-15 10:30:22 INFO Application started
2024-01-15 10:30:25 ERROR Database connection failed
2024-01-15 10:30:26 WARN Retrying connection in 5 seconds
2024-01-15 10:30:31 INFO Connection restored
```

### Output Format

Generated markdown summary:

```markdown
# Log Summary

- 2024-01-15 10:30:25 ERROR Database connection failed
- 2024-01-15 10:30:26 WARN Retrying connection in 5 seconds
```

---

## LLM Report Generator

**Location:** `scripts/gen_llm.py`

This script uses OpenAI's GPT-4 to convert log summaries into professional incident reports and Root Cause Analysis (RCA) documentation.

### Dependencies

```bash
pip install openai httpx pathlib
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Configuration

- **Model:** GPT-4o
- **Input:** `docs/generated/log_summary.md`
- **Output:** `docs/drafts/incident_narrative.md`
- **SSL Verification:** Disabled (⚠️ Security Note: Consider enabling in production)

### Usage

```bash
# Ensure log summary exists first
python scripts/extract_logs.py

# Generate incident report
python scripts/gen_llm.py
```

### System Prompt

The script uses a specialized system prompt:
> "You are a senior technical writer. Convert log summaries into incident narratives and RCA documentation."

### Example Workflow

1. **Input Log Summary:**
```markdown
# Log Summary

- 2024-01-15 10:30:25 ERROR Database connection failed
- 2024-01-15 10:30:26 WARN Retrying connection in 5 seconds
```

2. **Generated Output:** Professional incident report with:
   - Timeline of events
   - Impact assessment
   - Root cause analysis
   - Recommended actions

---

## Getting Started

### Prerequisites

1. Python 3.7+
2. OpenAI API key (for LLM functionality)
3. Log files in the expected format

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-docs-lab
```

2. Set up environment:
```bash
export OPENAI_API_KEY="your-api-key"
```

3. Install dependencies:
```bash
pip install openai httpx
```

### Basic Usage

1. **Use Math Utilities:**
```python
from src.example import add, multiply

sum_result = add(10, 20)
product_result = multiply(5, 6)
```

2. **Process Logs:**
```bash
python scripts/extract_logs.py
```

3. **Generate Incident Report:**
```bash
python scripts/gen_llm.py
```

---

## Examples

### Complete Workflow Example

```bash
# 1. Start with a log file in logs/sample.log
echo "2024-01-15 10:30:25 ERROR Database connection failed" > logs/sample.log

# 2. Extract errors and warnings
python scripts/extract_logs.py

# 3. Generate AI-powered incident report
python scripts/gen_llm.py

# 4. View the generated documentation
cat docs/drafts/incident_narrative.md
```

### Integration Example

```python
# example_integration.py
from src.example import add, multiply
import subprocess
import os

# Use math utilities
def calculate_metrics(base_value, multiplier, offset):
    """Calculate system metrics using utility functions."""
    scaled = multiply(base_value, multiplier)
    return add(scaled, offset)

# Process logs programmatically
def process_system_logs():
    """Extract logs and generate reports."""
    # Extract logs
    result = subprocess.run(['python', 'scripts/extract_logs.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Generate AI report
        subprocess.run(['python', 'scripts/gen_llm.py'])
        return True
    return False

# Usage
metrics = calculate_metrics(100, 1.5, 25)  # 175
success = process_system_logs()
```

---

## API Reference Summary

| Component | Type | Purpose | Input | Output |
|-----------|------|---------|-------|--------|
| `add()` | Function | Math utility | Two numbers | Sum |
| `multiply()` | Function | Math utility | Two numbers | Product |
| `extract_logs.py` | Script | Log processing | Log file | Markdown summary |
| `gen_llm.py` | Script | AI report generation | Markdown summary | Incident report |

---

## Error Handling

### Common Issues

1. **Missing OpenAI API Key:**
   ```
   Error: OpenAI API key not found
   Solution: Set OPENAI_API_KEY environment variable
   ```

2. **Input File Not Found:**
   ```
   Error: [Errno 2] No such file or directory: 'logs/sample.log'
   Solution: Ensure input log file exists at specified path
   ```

3. **Output Directory Missing:**
   ```
   Error: [Errno 2] No such file or directory: 'docs/generated/'
   Solution: Create necessary directories before running scripts
   ```

### Best Practices

1. **Validate inputs** before processing
2. **Check file permissions** for read/write operations
3. **Handle network errors** when calling OpenAI API
4. **Use environment variables** for sensitive configuration
5. **Enable SSL verification** in production environments

---

## Contributing

When extending this API:

1. **Follow docstring conventions** for all public functions
2. **Add type hints** where appropriate
3. **Include usage examples** in documentation
4. **Test error conditions** thoroughly
5. **Update this documentation** with new APIs

---

*Last updated: Generated automatically by AI Docs Lab*