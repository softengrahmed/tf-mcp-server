#from fastmcp.server import MCPServer, mcp_tool
from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import subprocess
import json
import os

mcp = FastMCP(name="Epam-InfraDriftDetector", description="MCP Server enabling importing of deployed AWS resources as tfstate-files using Terraformer tool and reading of Terraform tfstate files to return resources lists maintained in these tfstate-files.")

@mcp.tool(name="import_deployed_resources", description="Imports AWS resources deployed in aws cloud account using Terraformer commandline tool using the provided switches to filter what deployed artifacts are exactly imported. Use filter like sg, ec2, s3, policies etc. to limit the import to specific resources. Only in case when user specifically asked for ALL resources, import * resoruces but never import * if a filter is provided. The path_output parameter is the folder where the tfstate files will be stored. The regions parameter is a comma-separated list of AWS regions to scan for resources.")
def import_deployed_resources(cloud: str, resources: str, regions: str, path_output:str) -> dict:
    try:
        command = [
            "/usr/local/bin/terraformer",
            "import",
            cloud,
            "--resources", resources,
            "--regions", regions,
            "--path-output", path_output
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "stdout": e.stdout,
            "stderr": e.stderr
        }


# Helper function to load a JSON file
def read_lastdeployed_tfstates(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load tfstate file: {e}")

# Tool to read tfstate file and return resources
@mcp.tool(name="read_lastdeployed-tfstates", description="Reads Terraform tfstate file showing the last state deployed with terraform script and returns its resources list")
def read_lastdeployed_tfstates(last_deployed_file_path: str) -> List[Dict]:

    with open(last_deployed_file_path, "r", encoding="utf-8") as tfstate:
        last_deployed_text = tfstate.read()
        last_deployed_data = json.loads(last_deployed_text)  # Parse the JSON string
        last_deployed_resources = last_deployed_data.get("resources", [])
        print([item["type"] for item in last_deployed_resources]) 
    return last_deployed_resources

@mcp.tool(name="read_imported_tfstates", description="Reads Terraform tfstate files imported from aws-account showing the actual state of infra, with any post deployment drifts introduced. These tfstate files are stored in separate folders under the main-folder path provided in the parameter. The tool returns a merged resource list after loading lists from multiple terraform.tfstate")
def read_imported_tfstates(post_deployed_tfstates_path: str) -> Dict[str, Dict]:
    all_resources: Dict[str, Dict] = {}

    #print(f"Starting scan in: {post_deployed_tfstates_path}\n" + "-" * 50)

    # Walk the folder tree
    for root, dirs, files in os.walk(post_deployed_tfstates_path):
        #print(f"[DIR] Entering: {root}")                     # <- shows every directory visited

        for file in files:
            if file == "terraform.tfstate":
                file_path = os.path.join(root, file)
                #print(f"  └─ Found tfstate: {file_path}")     # <- shows every tfstate file discovered

                try:
                    with open(file_path, "r", encoding="utf-8") as tfstate_file:
                        tfstate_data = json.load(tfstate_file)

                    # Terraform 0.12+ style: modules[0]["resources"]
                    modules = tfstate_data.get("modules", [])
                    if modules and isinstance(modules[0], dict):
                        resources = modules[0].get("resources", {})
                        for key, value in resources.items():
                            all_resources[key] = value      # duplicates overwrite
                            #print(f"      • Loaded: {key}  (type={value.get('type')})")

                except Exception as e:
                    print(f"      ! Error loading {file_path}: {e}")

        # Optional visual separator between sibling folders
       # if dirs or files:
          #  print("-" * 50)

    #print(f"\nCompleted scan. Total resources loaded: {len(all_resources)}")
    return all_resources


if __name__ == "__main__":
    mcp.run()

