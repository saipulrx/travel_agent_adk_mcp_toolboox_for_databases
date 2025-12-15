# Building Intelligent Travel Agents with the ADK and MCP Toolbox for Database

This github for Workshop Devfest Jogjakarta 2025. 
It based on codelabs [Build a Travel Agent using MCP Toolbox for Databases and Agent Development Kit (ADK)](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk) with little update llm model use gemini 3 pro and app name.

Technology Stack :
- Agentic AI Framework : Google Agent Development Kit
- LLM Model : Gemini 3 Pro
- Backend Agentic AI : Vertex AI
- MCP Server : MCP Toolbox for Databases
- Databases : Cloud SQL for PostgreSQL
- Containers Services : Google Cloud Run

## Prerequisite
- Have Google Cloud Credits
- Have at least 1 project in Google Cloud. If not have then create new Project in Google Cloud
- Make sure that billing is enabled for your Cloud project. Learn how to [check if billing is enabled on a project](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled)

## Step by Steps hands on Workshop
### Task 1 : Enable the required API
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

On successful execution of the command, you should see a message similar to the one shown below:
```
Operation "operations/..." finished successfully.
```

### Task 2 : Create a Cloud SQL instance
We will be using a Google Cloud SQL for PostgreSQL instance to store our hotels data. Cloud SQL for PostgreSQL is a fully-managed database service that helps you set up, maintain, manage, and administer your PostgreSQL relational databases on Google Cloud Platform.

Run the following command in Cloud Shell to create the instance:
```
gcloud sql instances create hoteldb-instance \
--database-version=POSTGRES_15 \
--tier db-g1-small \
--region=us-central1 \
--edition=ENTERPRISE \
--root-password=postgres
```
