# Installation Guide - AI Docs Lab

## 📋 Overview

This guide will help you install and configure the AI-powered documentation pipeline for automated log processing and incident report generation.

## � Quick Start (Recommended)

For the fastest setup, use our automated installation script:

```bash
# Run the quick-start script
./quick-start.sh
```

This script will automatically:
- Check prerequisites and dependencies
- Set up a virtual environment
- Install all required packages
- Create necessary directories
- Generate sample files
- Run tests to verify installation

**Continue reading for manual installation steps or troubleshooting.**

## �🔧 Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.7 or higher
- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Storage**: At least 100MB free space
- **Internet**: Active connection for OpenAI API calls

### Required Accounts & API Keys

- **OpenAI Account**: Sign up at [platform.openai.com](https://platform.openai.com)
- **API Credits**: Ensure your OpenAI account has available credits
- **API Key**: Generate an API key from your OpenAI dashboard

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd ai-docs-lab

# Verify project structure
ls -la
```

**Expected output:**
```
├── README.md
├── mkdocs.yml
├── requirements.txt
├── src/
├── scripts/
├── docs/
└── logs/
```

### Step 2: Python Environment Setup

#### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv ai-docs-env

# Activate virtual environment
# On Linux/macOS:
source ai-docs-env/bin/activate

# On Windows:
ai-docs-env\Scripts\activate

# Verify activation (should show virtual env path)
which python
```

#### Option B: Using Conda

```bash
# Create conda environment
conda create -n ai-docs-lab python=3.9
conda activate ai-docs-lab
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "openai|httpx"
```

**Expected output:**
```
httpx                 0.24.1
openai                1.3.7
```

### Step 4: Environment Configuration

#### Set Up OpenAI API Key

**Option A: Environment Variable (Recommended)**
```bash
# Linux/macOS - Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="your-actual-api-key-here"

# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc

# Verify the key is set
echo $OPENAI_API_KEY
```

**Option B: Create .env file**
```bash
# Create environment file
echo "OPENAI_API_KEY=your-actual-api-key-here" > .env

# Note: You'll need to modify scripts to load from .env
```

**Windows PowerShell:**
```powershell
# Set environment variable
$env:OPENAI_API_KEY="your-actual-api-key-here"

# For permanent setup, use System Properties > Environment Variables
```

### Step 5: Directory Structure Setup

```bash
# Create necessary directories
mkdir -p docs/generated
mkdir -p docs/drafts
mkdir -p logs

# Verify directory structure
tree . || find . -type d
```

### Step 6: Test Installation

#### Create Sample Log File

```bash
# Create a sample log for testing
cat > logs/sample.log << EOF
2024-01-15 10:30:22 INFO Application started successfully
2024-01-15 10:30:25 ERROR Database connection failed - timeout after 30s
2024-01-15 10:30:26 WARN Retrying database connection in 5 seconds
2024-01-15 10:30:31 INFO Database connection restored
2024-01-15 10:30:32 ERROR Failed to process user request - invalid token
2024-01-15 10:30:33 WARN High memory usage detected: 85%
EOF
```

#### Test Log Extraction

```bash
# Run log extraction script
python scripts/extract_logs.py

# Verify output
cat docs/generated/log_summary.md
```

**Expected output:**
```markdown
# Log Summary

- 2024-01-15 10:30:25 ERROR Database connection failed - timeout after 30s
- 2024-01-15 10:30:26 WARN Retrying database connection in 5 seconds
- 2024-01-15 10:30:32 ERROR Failed to process user request - invalid token
- 2024-01-15 10:30:33 WARN High memory usage detected: 85%
```

#### Test AI Report Generation

```bash
# Generate AI-powered incident report
python scripts/gen_llm.py

# Check if report was generated
ls -la docs/drafts/
cat docs/drafts/incident_narrative.md
```

#### Test Math Utilities

```bash
# Test the math utilities
python3 -c "
from src.example import add, multiply
print('Add test:', add(5, 3))
print('Multiply test:', multiply(4, 6))
"
```

**Expected output:**
```
Add test: 8
Multiply test: 24
```

#### Run Complete Installation Test

For a comprehensive verification of your setup:

```bash
# Run the automated test suite
python scripts/setup_test.py
```

This script will:
- Check Python version compatibility
- Verify all dependencies are installed
- Test API key configuration
- Validate directory structure
- Test all components end-to-end
- Generate a detailed report

**Expected output:** All tests should pass with ✅ symbols.

---

## 📖 Documentation Setup (Optional)

### Install MkDocs for Web Documentation

```bash
# Install MkDocs and theme
pip install mkdocs mkdocs-material

# Start development server
mkdocs serve

# Visit http://127.0.0.1:8000 in your browser
```

### Build Static Documentation

```bash
# Build documentation site
mkdocs build

# Serve built site
cd site
python -m http.server 8000
```

---

## ✅ Verification Checklist

Run through this checklist to ensure everything is working:

- [ ] Python 3.7+ is installed and accessible
- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip list` shows openai, httpx)
- [ ] OpenAI API key is set and accessible
- [ ] Directory structure is created correctly
- [ ] Log extraction script runs without errors
- [ ] AI report generation works (requires API credits)
- [ ] Math utilities are importable and functional
- [ ] MkDocs serves documentation (if installed)

---

## 🔧 Configuration Options

### Customize Input/Output Paths

Edit `scripts/extract_logs.py`:
```python
# Modify these paths as needed
input_path = "logs/your-custom-log.log"
output_path = "docs/generated/your-summary.md"
```

Edit `scripts/gen_llm.py`:
```python
# Modify these paths as needed
input_path = Path("docs/generated/your-summary.md")
output_path = Path("docs/drafts/your-report.md")
```

### Customize AI Model Settings

In `scripts/gen_llm.py`, you can modify:
```python
response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo" for lower cost
    temperature=0.7,  # Add for more creative responses
    max_tokens=2000,  # Limit response length
    messages=[...]
)
```

### SSL Configuration

For production environments, enable SSL verification:
```python
# In scripts/gen_llm.py, replace:
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False)  # ⛔ REMOVE THIS LINE
)

# With:
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. OpenAI API Key Not Found
```bash
Error: The api_key client option must be set
```
**Solution:**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, set it:
export OPENAI_API_KEY="your-key-here"
```

#### 2. Module Import Errors
```bash
ModuleNotFoundError: No module named 'openai'
```
**Solution:**
```bash
# Ensure virtual environment is activated
source ai-docs-env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Permission Denied Errors
```bash
Permission denied: 'docs/generated/log_summary.md'
```
**Solution:**
```bash
# Check directory permissions
ls -la docs/
chmod 755 docs/generated/
```

#### 4. SSL Certificate Errors
```bash
SSL: CERTIFICATE_VERIFY_FAILED
```
**Solution:**
```bash
# Option 1: Update certificates (recommended)
pip install --upgrade certifi

# Option 2: Temporarily disable SSL (not recommended for production)
# Already configured in the script
```

#### 5. API Rate Limiting
```bash
Error: Rate limit exceeded
```
**Solution:**
- Wait before retrying
- Check your OpenAI usage limits
- Consider upgrading your OpenAI plan

#### 6. No Log Entries Found
```bash
# Log Summary

No ERROR or WARN lines found.
```
**Solution:**
- Verify your log file contains "ERROR" or "WARN" keywords
- Check the log file path in `scripts/extract_logs.py`
- Ensure log file is not empty

### Debug Mode

Enable verbose output for troubleshooting:
```python
# Add to scripts for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🚀 Next Steps

After successful installation:

1. **Create your first incident report**:
   ```bash
   python scripts/extract_logs.py
   python scripts/gen_llm.py
   ```

2. **Explore the API documentation**:
   ```bash
   mkdocs serve
   # Visit: http://127.0.0.1:8000/api-documentation/
   ```

3. **Integrate with your existing logs**:
   - Update input paths in extraction script
   - Customize log filtering patterns
   - Set up automated processing workflows

4. **Set up production deployment**:
   - Configure proper SSL verification
   - Set up log rotation
   - Implement error monitoring
   - Schedule automated processing

---

## 📞 Support

If you encounter issues not covered in this guide:

1. Check the [API Documentation](api-documentation.md)
2. Review error logs and outputs
3. Verify your OpenAI API key and credits
4. Ensure all dependencies are correctly installed

---

*Installation guide for AI Docs Lab v1.0*