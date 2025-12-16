from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
#toolbox = ToolboxSyncClient("https://toolbox-487826826516.us-central1.run.app")

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