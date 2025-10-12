# /check_env - Verify Python Environment

Verify that the Python environment is properly configured for wepublic_defender.

## Checks to Perform

1. **Python Version**
   - Check: `python --version`
   - Required: Python 3.9 or higher
   - Warn if not 3.9+

2. **Environment Type**
   - Check: `$CONDA_DEFAULT_ENV` or `$VIRTUAL_ENV`
   - Warn if not in a dedicated conda/venv environment
   - Recommend creating: `conda create -n wepublic_defender python=3.11`

3. **wepublic_defender Installation**
   - Check: `pip list | grep wepublic`
   - If not found, recommend: `pip install -e wepublic_defender/`

4. **Required Packages**
   Check if installed:
   - `openai` (version >= 1.0.0)
   - `pydantic` (version >= 2.0.0)
   - `python-dotenv` (>= 1.0.0)
   - `python-docx` (>= 0.8.11)
   - `PyPDF2` (>= 3.0.0)
   - `pdfplumber` (>= 0.10.0)
   - `rich` (>= 13.0.0)

5. **API Keys**
   - Check: `echo $OPENAI_API_KEY`
   - Check: `echo $XAI_API_KEY`
   - Warn if not set (don't display actual values!)

## Implementation

```bash
echo "======================================"
echo "  wepublic_defender Environment Check"
echo "======================================"
echo ""

# Python version
echo "1. Python Version:"
python --version || echo "   ERROR: Python not found in PATH!"
echo ""

# Check environment
echo "2. Environment Type:"
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "   ✓ Conda environment: $CONDA_DEFAULT_ENV"
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "   ✓ Virtual environment: $VIRTUAL_ENV"
else
    echo "   WARNING: Not in a dedicated environment!"
    echo "   Recommend: conda create -n wepublic_defender python=3.11"
fi
echo ""

# Check wepublic_defender installation
echo "3. wepublic_defender Installation:"
if pip list | grep -i wepublic > /dev/null; then
    echo "   ✓ wepublic_defender is installed"
    pip list | grep -i wepublic
else
    echo "   WARNING: wepublic_defender not found!"
    echo "   Install with: pip install -e wepublic_defender/"
fi
echo ""

# Check required packages
echo "4. Required Packages:"
for pkg in openai pydantic python-dotenv python-docx PyPDF2 pdfplumber rich; do
    if pip list | grep -i "^$pkg " > /dev/null; then
        version=$(pip list | grep -i "^$pkg " | awk '{print $2}')
        echo "   ✓ $pkg ($version)"
    else
        echo "   ✗ $pkg - NOT INSTALLED"
    fi
done
echo ""

# Check API keys (without revealing values)
echo "5. API Keys:"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "   ✓ OPENAI_API_KEY is set"
else
    echo "   WARNING: OPENAI_API_KEY not set!"
fi

if [ -n "$XAI_API_KEY" ]; then
    echo "   ✓ XAI_API_KEY is set"
else
    echo "   WARNING: XAI_API_KEY not set!"
fi

echo ""
echo "======================================"
echo "  Environment Check Complete"
echo "======================================"
```

## Example Output

```
======================================
  wepublic_defender Environment Check
======================================

1. Python Version:
   Python 3.11.5

2. Environment Type:
   ✓ Conda environment: wepublic_defender

3. wepublic_defender Installation:
   ✓ wepublic_defender is installed
   wepublic-defender  0.1.0  /path/to/wepublic_defender

4. Required Packages:
   ✓ openai (1.14.0)
   ✓ pydantic (2.6.1)
   ✓ python-dotenv (1.0.0)
   ✓ python-docx (0.8.11)
   ✓ PyPDF2 (3.0.1)
   ✓ pdfplumber (0.10.3)
   ✓ rich (13.7.0)

5. API Keys:
   ✓ OPENAI_API_KEY is set
   ✓ XAI_API_KEY is set

======================================
  Environment Check Complete
======================================
```
