Setup Procedure for MCP Server Python Code
=====================================

This guide covers steps required for setting up a Python project for MCP Server, writing MCP server tools, initializing the MCP environment, and correctly installing and configuring the MCP server.

---

### Pre-requisites
_Ensure the following are installed before starting:_

1. **Python**:
   - Install Python (version 3.7 or above recommended).
   - Verify the installation:
     ```
     python --version
     ```

2. **UV (Node.js-based tools)**:
   - Install UV globally using Node.js:
     ```
     npm install -g uv
     ```
   - Verify the installation:
     ```
     uv --version
     ```

---

### Step 1: Create a Python MCP Project

#### a. Create a Python Project
1. Create a directory for your MCP Server tools:
mkdir mcp-server-python cd mcp-server-python




2. Initialize a Python virtual environment (additional details in *Step 2*).

#### b. Write Python Code for MCP Server Tools
Write Python modules in the project directory. Ensure the following tools are defined:
- `import_deployed_resources.py`: For importing deployed resources.
- `read_lastdeployed_tfstates.py`: For reading the last-deployed Terraform state files.
- `read_imported_tfstates.py`: For reading imported Terraform state files.

Example code template for defining an MCP tool:
from mcp import tool

@tool(name="import_deployed_resources") def import_deployed_resources(param1, param2): """ Example: Imports deployed resources from a specific environment. """ # Your logic here return {"status": "success"}




---

### Step 2: MCP Environment Setup

_Activate and prepare the MCP environment:_

#### a. Run `uv init`
Initialize the MCP project:
uv init



_Output_:
Initialized project 'map-server'.




#### b. Create and Activate Virtual Environment
1. Create a virtual environment:
uv venv




2. Activate the virtual environment:
- **Mac/Linux**:
  ```
  source .venv/bin/activate
  ```
- **Windows**:
  ```
  .venv\Scripts\activate
  ```

#### c. Install MCP to the Virtual Environment
Install MCP CLI into your virtual environment:
uv add "mcp[cli]"




---

### Step 3: Testing MCP Server Code

_(Optional)_ Run your MCP Server tools in development mode to test functionality:
mcp dev mcp-server-code.py




---

### Step 4: Installing MCP Server Configuration

1. Install the MCP server configuration using MCP CLI:
mcp install mcp-server-code.py



2. Ensure the **full path** to your Python code (`mcp-server-code.py`) is added to the MCP configuration.
_Important_: If any filename or folder structure changes, re-run the `mcp install` command to update the configuration.

3. **Customizing MCP Tool Names**:
- Update tool names in the Python code by changing:
  - `@mcp.tool(name="tool-name")` decorator
  - `def tool_name(params):` function name

---

### Step 5: Verify MCP Server Installation

Once installed, your MCP server should appear in the **Claude Desktop Application** on the startup screen.

---

### Troubleshooting Tips

1. **Verify Installed Packages**:
Ensure that the `mcp[cli]` package is installed in the virtual environment by running:
uv list



This will display the installed modules.

2. **Reconfigure MCP Server**:
If there are any filename or folder name changes, re-run: 
mcp install mcp-server-code.py




---

### Summary

_Following these steps will enable you to:_
- Create a Python project for MCP server tools.
- Set up the MCP environment correctly.
- Register and configure your MCP server in the **Claude Desktop Application**.
- Use Python to define and manage MCP tools with maximum flexibility.
