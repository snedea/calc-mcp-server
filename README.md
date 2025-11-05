# Calculator MCP Server

A simple Model Context Protocol (MCP) server that provides basic calculator operations as tools for Claude Desktop and other MCP clients.

## Features

- **Add**: Sum two numbers
- **Subtract**: Find the difference between two numbers
- **Multiply**: Calculate the product of two numbers
- **Divide**: Divide numbers with proper zero-division handling

All operations support integers, floating-point numbers, and negative numbers.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. **Clone or download this repository**

```bash
git clone https://github.com/snedea/calc-mcp-server.git
cd calc-mcp-server
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

This installs:
- `fastmcp>=2.0.0` - MCP framework
- `pytest>=7.0.0` - Testing framework

## Usage

### Testing the Server

Run the server standalone to verify it works:

```bash
python3 calc_server.py
```

You should see:

```
🧮 Calculator MCP Server Starting

📋 Available tools:
   - add(a, b): Add two numbers
   - subtract(a, b): Subtract b from a
   - multiply(a, b): Multiply two numbers
   - divide(a, b): Divide a by b (handles zero)

💡 Configure in Claude Desktop to use these tools!
```

Press `Ctrl+C` to stop the server.

### Configuring in Claude Desktop

To use these calculator tools in Claude Desktop:

1. **Locate your Claude Desktop config file:**

   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Edit the config file** (create it if it doesn't exist):

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python3",
      "args": ["/absolute/path/to/calc-mcp-server/calc_server.py"]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/calc-mcp-server/` with the actual full path to this directory.

3. **Restart Claude Desktop**

The calculator tools will now be available! Claude can use them automatically when you ask questions involving calculations.

## Available Tools

### add(a, b)

Add two numbers together.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:** JSON with operation details and result

**Example:**
```
Input: add(5, 3)
Output: {
  "operation": "add",
  "a": 5,
  "b": 3,
  "result": 8
}
```

### subtract(a, b)

Subtract the second number from the first.

**Parameters:**
- `a` (float): Number to subtract from
- `b` (float): Number to subtract

**Returns:** JSON with operation details and result

**Example:**
```
Input: subtract(10, 3)
Output: {
  "operation": "subtract",
  "a": 10,
  "b": 3,
  "result": 7
}
```

### multiply(a, b)

Multiply two numbers together.

**Parameters:**
- `a` (float): First number
- `b` (float): Second number

**Returns:** JSON with operation details and result

**Example:**
```
Input: multiply(4, 5)
Output: {
  "operation": "multiply",
  "a": 4,
  "b": 5,
  "result": 20
}
```

### divide(a, b)

Divide the first number by the second.

**Parameters:**
- `a` (float): Numerator
- `b` (float): Denominator

**Returns:** JSON with operation details and result, or error if dividing by zero

**Example:**
```
Input: divide(10, 2)
Output: {
  "operation": "divide",
  "a": 10,
  "b": 2,
  "result": 5
}

Input: divide(10, 0)
Output: {
  "error": "Cannot divide by zero"
}
```

## Testing

Run the test suite to verify all operations work correctly:

```bash
pytest tests/test_calculator.py -v
```

Expected output:

```
tests/test_calculator.py::TestAddition::test_add_positive_numbers PASSED
tests/test_calculator.py::TestAddition::test_add_negative_numbers PASSED
... (30+ tests)
================================ 30 passed in 0.XX s ================================
```

All tests should pass, covering:
- Basic arithmetic operations
- Edge cases (zero, negatives, decimals)
- Error handling (division by zero)
- JSON response format validation

## Project Structure

```
calc-mcp-server/
├── calc_server.py          # Main MCP server with calculator tools
├── requirements.txt        # Python dependencies
├── tests/
│   └── test_calculator.py  # Comprehensive unit tests
├── README.md               # This file
└── .gitignore              # Git exclusions
```

## Troubleshooting

### Tools don't appear in Claude Desktop

- ✅ Check that the config file path is correct for your OS
- ✅ Verify the `args` path is **absolute** (not relative)
- ✅ Ensure Python 3.10+ is installed: `python3 --version`
- ✅ Confirm FastMCP is installed: `pip show fastmcp`
- ✅ Restart Claude Desktop completely

### Import errors when running server

- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Use Python 3.10 or higher
- ✅ Consider using a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Tests failing

- ✅ Ensure pytest is installed: `pip install pytest`
- ✅ Run from the project root directory
- ✅ Check Python version is 3.10+

## Technologies Used

- **Python 3.10+**: Modern Python with type hints
- **FastMCP 2.0+**: Official MCP framework for Python
- **pytest**: Testing framework

## How It Works

MCP (Model Context Protocol) is a standard for connecting AI assistants like Claude to external tools and data sources. This server:

1. Defines calculator operations as Python functions
2. Decorates them with `@mcp.tool()` to expose them via MCP
3. Communicates with Claude Desktop using standard input/output (stdio transport)
4. Returns structured JSON responses for reliable parsing

Claude can then call these tools automatically when needed for calculations!

## License

MIT

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest new calculator features
- Improve documentation
- Add more tests

## Created By

🤖 Generated with [Context Foundry](https://contextfoundry.dev) - Autonomous Development Platform
