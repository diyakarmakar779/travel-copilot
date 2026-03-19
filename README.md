# Travel Copilot 🌏✈️

**Travel Copilot** is an AI-powered assistant that helps travelers generate **itineraries**, **Instagram captions**, and **reel ideas** for any destination. Built after completing the **MCP Server course by Anthropic**, this project solves the common challenge of manually planning trips and creating engaging content for travel enthusiasts.

> I’m a data engineer and AI enthusiast who loves traveling — this tool is my way of combining AI with travel experiences.  

---

## Features

- 🗺 **Automated Itineraries:** Get a day-by-day plan for your trips.  
- 📝 **Captions Generator:** Generate engaging Instagram captions for destinations.  
- 🎥 **Reels Suggestions:** Creative short-video ideas for your trips.  
- 💡 **Human-friendly Responses:** AI output is polished, aesthetic, and ready to share.  

---

## Tech Stack

- **Python 3.14**  
- **FastMCP** – Modular AI tool orchestration  
- **Anthropic API** – LLM powering decisions & responses  
- **Streamlit** – Frontend UI for interacting with Travel Copilot  
- **AsyncIO** – Handles tool calls and AI responses asynchronously  

---

## Repo Structure

```text
travel-copilot/
├── README.md
├── .gitignore
├── app.py                  # Streamlit UI
├── server/
│   ├── __init__.py
│   ├── agent.py            # LLM orchestration
│   ├── ai_client.py        # Calls LLM API
│   ├── mcp_server.py       # FastMCP server with tools
│   ├── mcp_client.py       # MCP client wrapper
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── itinerary.py
│   │   ├── captions.py
│   │   └── reels.py
│   ├── prompts/
│   │   └── styles.py
│   └── resources/
│       └── travel_data.json
├── pyproject.toml
├── uv.lock