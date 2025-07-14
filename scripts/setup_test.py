#!/usr/bin/env python3
"""
Setup Test Script for AI Docs Lab

This script verifies that the AI documentation pipeline is properly installed
and configured. It runs through all components to ensure everything works.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header for each test section."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_warning(message):
    """Print a warning message."""
    print(f"⚠️  {message}")

def check_python_version():
    """Check if Python version meets requirements."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print_success("Python version is compatible (3.7+)")
        return True
    else:
        print_error("Python version must be 3.7 or higher")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Checking Dependencies")
    
    required_packages = ['openai', 'httpx']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is configured."""
    print_header("Checking OpenAI API Key")
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        # Don't print the full key for security
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print_success(f"OpenAI API key is set: {masked_key}")
        return True
    else:
        print_error("OpenAI API key is not set")
        print("Set your API key with: export OPENAI_API_KEY='your-key-here'")
        return False

def check_directory_structure():
    """Check if required directories exist."""
    print_header("Checking Directory Structure")
    
    required_dirs = [
        'src',
        'scripts', 
        'docs',
        'docs/generated',
        'docs/drafts',
        'logs'
    ]
    
    all_exist = True
    
    for directory in required_dirs:
        path = Path(directory)
        if path.exists():
            print_success(f"Directory exists: {directory}")
        else:
            print_error(f"Directory missing: {directory}")
            print(f"  Create with: mkdir -p {directory}")
            all_exist = False
    
    return all_exist

def test_math_utilities():
    """Test the math utility functions."""
    print_header("Testing Math Utilities")
    
    try:
        # Add current directory to path to import from src
        sys.path.insert(0, '.')
        from src.example import add, multiply
        
        # Test add function
        result = add(5, 3)
        if result == 8:
            print_success(f"add(5, 3) = {result} ✓")
        else:
            print_error(f"add(5, 3) = {result}, expected 8")
            return False
        
        # Test multiply function
        result = multiply(4, 6)
        if result == 24:
            print_success(f"multiply(4, 6) = {result} ✓")
        else:
            print_error(f"multiply(4, 6) = {result}, expected 24")
            return False
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import math utilities: {e}")
        return False
    except Exception as e:
        print_error(f"Error testing math utilities: {e}")
        return False

def create_test_log():
    """Create a sample log file for testing."""
    print_header("Creating Test Log File")
    
    log_content = """2024-01-15 10:30:22 INFO Application started successfully
2024-01-15 10:30:25 ERROR Database connection failed - timeout after 30s
2024-01-15 10:30:26 WARN Retrying database connection in 5 seconds
2024-01-15 10:30:31 INFO Database connection restored
2024-01-15 10:30:32 ERROR Failed to process user request - invalid token
2024-01-15 10:30:33 WARN High memory usage detected: 85%
2024-01-15 10:30:34 INFO System performance normalized
"""
    
    try:
        log_path = Path('logs/sample.log')
        log_path.parent.mkdir(exist_ok=True)
        log_path.write_text(log_content)
        print_success(f"Test log file created: {log_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create test log: {e}")
        return False

def test_log_extraction():
    """Test the log extraction script."""
    print_header("Testing Log Extraction")
    
    try:
        # Run the log extraction script
        result = subprocess.run(
            [sys.executable, 'scripts/extract_logs.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_success("Log extraction script executed successfully")
            
            # Check if output file was created
            output_path = Path('docs/generated/log_summary.md')
            if output_path.exists():
                content = output_path.read_text()
                if 'ERROR' in content and 'WARN' in content:
                    print_success("Log summary contains expected content")
                    print(f"  Generated: {output_path}")
                    return True
                else:
                    print_error("Log summary doesn't contain expected ERROR/WARN entries")
                    return False
            else:
                print_error("Log summary file was not created")
                return False
        else:
            print_error(f"Log extraction failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Log extraction script timed out")
        return False
    except Exception as e:
        print_error(f"Error running log extraction: {e}")
        return False

def test_ai_generation():
    """Test the AI report generation (requires API key)."""
    print_header("Testing AI Report Generation")
    
    if not os.getenv('OPENAI_API_KEY'):
        print_warning("Skipping AI test - no OpenAI API key configured")
        return True
    
    try:
        # Run the AI generation script
        result = subprocess.run(
            [sys.executable, 'scripts/gen_llm.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print_success("AI report generation completed successfully")
            
            # Check if output file was created
            output_path = Path('docs/drafts/incident_narrative.md')
            if output_path.exists():
                content = output_path.read_text()
                if len(content.strip()) > 100:  # Basic content check
                    print_success("AI-generated report contains substantial content")
                    print(f"  Generated: {output_path}")
                    return True
                else:
                    print_error("AI-generated report seems too short")
                    return False
            else:
                print_error("AI report file was not created")
                return False
        else:
            print_error(f"AI generation failed: {result.stderr}")
            if "api_key" in result.stderr.lower():
                print_warning("This might be an API key issue")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("AI generation script timed out")
        return False
    except Exception as e:
        print_error(f"Error running AI generation: {e}")
        return False

def run_complete_test():
    """Run the complete test suite."""
    print_header("AI Docs Lab - Installation Test")
    print("This script will verify your installation and run all components.")
    
    tests = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("OpenAI API Key", check_openai_key),
        ("Directory Structure", check_directory_structure),
        ("Math Utilities", test_math_utilities),
        ("Test Log Creation", create_test_log),
        ("Log Extraction", test_log_extraction),
        ("AI Report Generation", test_ai_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Results Summary")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        emoji = "✅" if success else "❌"
        print(f"{emoji} {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your AI Docs Lab installation is ready.")
        print("\nNext steps:")
        print("1. Try: mkdocs serve")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Check out the API documentation")
    else:
        print_error("Some tests failed. Please review the errors above.")
        print("\nFor help, check:")
        print("1. Installation guide: docs/installation-guide.md")
        print("2. API documentation: docs/api-documentation.md")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_complete_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)