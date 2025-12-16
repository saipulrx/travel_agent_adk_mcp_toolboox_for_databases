# 🏨 Building Intelligent Travel Agents with the ADK and MCP Toolbox for Database

This Python-based AI Agent is built using the Agent Development Kit (ADK) and connects to data via the MCP Toolbox for Databases. The project functions as a travel agent capable of answering user queries about hotels, searching by location, or searching by hotel name, using data stored in Google Cloud SQL for PostgreSQL.

It based on codelabs [Build a Travel Agent using MCP Toolbox for Databases and Agent Development Kit (ADK)](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk) with little update llm model use gemini 3 pro and app name.

📋 Table of Contents
1. [Introduction](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#1-introduction)
2. [Technologies Used](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#2-technologies-used-)
3. [Key Features](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#3-key-features)
4. [Prerequisites](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#4-prerequisite)
5. [Setup Steps](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#5-setup-steps)
   - 5.1. [Google Cloud Setup](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#51-google-cloud-setup)
   - 5.2. [Hotels Database Preparation](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#52-hotels-database-preparation)
   - 5.3. [MCP Toolbox Configuration](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#53-mcp-toolbox-configuration)
   - 5.4. [Agent Development Kit (ADK) Setup](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#54-agent-development-kit-adk-setup)
6. [How to Run the Agent](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#6-how-to-run-the-agent)
7. [Deployment](https://github.com/saipulrx/travel_agent_adk_mcp_toolboox_for_databases/blob/main/README.md#7-deployment-optional) (Optional)

## 1. Introduction
This project demonstrates how to build a stateful AI agent capable of interacting with a relational database. The MCP Toolbox acts as a control plane that simplifies the agent's access to SQL data, while the ADK provides the framework for designing, building, and running an agent that can utilize these tools.

## 2. Technologies Used :
- Agentic AI Framework : Google Agent Development Kit
- LLM Model : Gemini 3 Pro
- Backend Agentic AI : Vertex AI
- MCP Server : MCP Toolbox for Databases
- Databases : Cloud SQL for PostgreSQL
- Containers Services : Google Cloud Run
- Programming Language : Python

## 3. Key Features
- Search for hotels by name (search-hotels-by-name).
- Search for hotels by location (search-hotels-by-location).
- Integrate Agentic AI with MCP Toolbox for Databases.
- Options for local testing and deployment to Cloud Run.

## 4. Prerequisite
- Have Google Cloud Credits
- Have at least 1 project in Google Cloud. If not have then create new Project in Google Cloud
- Make sure that billing is enabled for your Cloud project. Learn how to [check if billing is enabled on a project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled)

## 5. Setup Steps
### 5.1. Google Cloud Setup
- You'll use Cloud Shell, a command-line environment running in Google Cloud that comes preloaded with bq. Click Activate Cloud Shell at the top of the Google Cloud console
- Enable the required APIs via the command shown below. This could take a few minutes, so please be patient
```
gcloud services enable cloudresourcemanager.googleapis.com \
                       servicenetworking.googleapis.com \
                       run.googleapis.com \
                       cloudbuild.googleapis.com \
                       cloudfunctions.googleapis.com \
                       aiplatform.googleapis.com \
                       sqladmin.googleapis.com \
                       compute.googleapis.com 
```


### 5.2. Hotels Database Preparation
1. Run the following command in Cloud Shell to create the instance:
```
gcloud sql instances create hoteldb-instance \
--database-version=POSTGRES_15 \
--tier db-g1-small \
--region=us-central1 \
--edition=ENTERPRISE \
--root-password=postgres
```
2. Sign in to the Cloud SQL Studio. Select postgres for the Database option and for both User and Password, the value to use is postgres. Click on AUTHENTICATE.
3. In one of the Editor panes in Cloud SQL Studio, execute the following SQL for create the hotel table:
```
CREATE TABLE hotels(
 id            INTEGER NOT NULL PRIMARY KEY,
 name          VARCHAR NOT NULL,
 location      VARCHAR NOT NULL,
 price_tier    VARCHAR NOT NULL,
 checkin_date  DATE    NOT NULL,
 checkout_date DATE    NOT NULL,
 booked        BIT     NOT NULL
);
```
4. Execute the following SQL to populate the hotels table with sample data:
```
INSERT INTO hotels(id, name, location, price_tier, checkin_date, checkout_date, booked)
VALUES
 (1, 'Hilton Basel', 'Basel', 'Luxury', '2024-04-20', '2024-04-22', B'0'),
 (2, 'Marriott Zurich', 'Zurich', 'Upscale', '2024-04-14', '2024-04-21', B'0'),
 (3, 'Hyatt Regency Basel', 'Basel', 'Upper Upscale', '2024-04-02', '2024-04-20', B'0'),
 (4, 'Radisson Blu Lucerne', 'Lucerne', 'Midscale', '2024-04-05', '2024-04-24', B'0'),
 (5, 'Best Western Bern', 'Bern', 'Upper Midscale', '2024-04-01', '2024-04-23', B'0'),
 (6, 'InterContinental Geneva', 'Geneva', 'Luxury', '2024-04-23', '2024-04-28', B'0'),
 (7, 'Sheraton Zurich', 'Zurich', 'Upper Upscale', '2024-04-02', '2024-04-27', B'0'),
 (8, 'Holiday Inn Basel', 'Basel', 'Upper Midscale', '2024-04-09', '2024-04-24', B'0'),
 (9, 'Courtyard Zurich', 'Zurich', 'Upscale', '2024-04-03', '2024-04-13', B'0'),
 (10, 'Comfort Inn Bern', 'Bern', 'Midscale', '2024-04-04', '2024-04-16', B'0');
```
5. Let's validate the data by running a SELECT SQL as shown below:
```
SELECT * FROM hotels;
```

### 5.3. MCP Toolbox Configuration
1. In Cloud Shell, create a project directory (mcp-toolbox).
2. Download the MCP Toolbox binary (appropriate for your OS).
```
export VERSION=0.19.1
curl -O https://storage.googleapis.com/genai-toolbox/v$VERSION/linux/amd64/toolbox
chmod +x toolbox
```
3. Create the configuration file tools.yaml which defines the connection to Cloud SQL (my-cloud-sql-source) and the two SQL tools (search-hotels-by-name and search-hotels-by-location) along with the toolset (my_first_toolset). Remember to replace YOUR_PROJECT_ID with your actual project ID.
(Note: The full tools.yaml content can be found in [here]().)

### 5.4. Agent Development Kit (ADK) Setup
1. Open a new terminal tab in Cloud Shell and create a folder named my-agents as follows. Navigate to the my-agents folder too
   ```
   mkdir my-agents
   cd my-agents
   ```
2. Create a virtual Python environment using venv as follows:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment as follows:
   ```
   source .venv/bin/activate
   ```
5. Install the ADK Python library and the MCP Toolbox for Databases packages along with langchain dependency as follows:
   ```
   pip install google-adk toolbox-core
   ```
6. Create the agent application scaffold:
   ```
   adk create hotel_agent_app
   ```
   Choose Others models for root agent and choose Vertex AI as backend. Input project ID based on your GCP project ID and input region us-central1
   
7. In the hotel_agent_app folder, modify the agent.py file to import the tools from the MCP Toolbox.
   (Example modification in agent.py):
   ```
   from google.adk.agents import Agent
   from toolbox_core import ToolboxSyncClient

   toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

   # Load single tool
   # tools = toolbox.load_tool('search-hotels-by-location')

   # Load all the tools
   tools = toolbox.load_toolset('my_first_toolset')

   root_agent = Agent(
    name="hotel_agent",
    model="gemini-3-pro-preview",
    description=(
        "Agent to answer questions about hotels in a city or hotels by name."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the hotels in a specific city or hotels by name. Use the tools to answer the question"
    ),
    tools=tools,
   )
   ```

## 6. How to Run the Agent
You need to run the MCP Toolbox server and the agent concurrently, ideally in two separate terminal windows.

Terminal 1 (Running MCP Toolbox):

From the mcp-toolbox folder, start the toolbox server to load the tools:
```
./toolbox --tools_file "tools.yaml"
```
Terminal 2 (Running the ADK Agent via CLI):

From the directory containing the hotel-agent-app folder, run the agent:
```
adk run hotel_agent_app
```
If you want run the agent using UI Web Browser then just run command ``` adk web ```

## 7. Deployment (Optional)
To run the agent and the toolbox in a production environment, you can deploy both as separate services on Google Cloud Run. Detailed steps for Service Account, Secrets Manager, and Container Image deployment are available in the original Codelab.
(Note: If you want follow this [codelabs](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk?hl=en#8) just change environment variable AGENT_PATH="hotel_agent_app/" and APP_NAME="hotels_app")
