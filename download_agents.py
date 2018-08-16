"""
download_agents.py
~~~
Downloads the agents from Dialogflow into project_files. Code adapted from app.py of DialogFlowTools.
Refer to https://dialogflow-python-client-v2.readthedocs.io/en/latest/gapic/v2beta1/api.html.
"""

import dialogflow_v2beta1
import os
import json
import zipfile

current_directory = os.path.dirname(os.path.realpath(__file__))
auth_json = os.path.join(current_directory, "nameidauth.json")


def download_agent(agent_name: str, project_id: str, auth_file: str) -> bytes:
    """
    Downloads an agent from Dialogflow.

    Args:
        agent_name (str): The name of the agent.
        project_id (str): The project id.
        auth_file (str): The name of the authorization file.
    Returns:
        bytes: Returns bytes for the zip file.
    """
    auth = os.path.join(current_directory, "authentication_tokens", auth_file)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth

    # Download agent agent_name as bytes.
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    response = client.export_agent(parent)

    def callback(operation_future):
        result = operation_future.result()

    response.add_done_callback(callback)
    data = response.result().agent_content

    print(data)

    return data


with open(auth_json) as auth_read:
    auth_dict = json.load(auth_read)

# Writes to the zip file and extracts from the zip file
for agent in auth_dict["configs"]:
    data = download_agent(agent["agent_name"], agent["project_id"], agent["authentication_file"])

    zip_loc = os.path.join(current_directory, "temp_zip_files", agent["agent_name"] + ".zip")
    zip_dest = os.path.join(current_directory, "project_files", agent["agent_name"])

    with open(zip_loc, "wb") as zw:
        zw.write(data)

    zip_ref = zipfile.ZipFile(zip_loc, 'r')
    zip_ref.extractall(zip_dest)
    zip_ref.close()
