# Travel Copilot 🧳✈️

**AI Travel Companion** built using **FastMCP**, **Anthropic Claude**, and **Python**, helping users plan trips, generate captions, and create reel ideas—all in one place!

---

## Features

- 🗺️ **Itinerary Generator**: Generate detailed day-wise travel plans.  
- 📸 **Caption Generator**: AI-generated Instagram captions for destinations.  
- 🎬 **Reel Ideas**: Creative short video suggestions for social media.  
- 💬 **Polished Output**: Final output is human-readable, aesthetic, and influencer-style.  
- ⚡ **Real-time Interaction**: Powered by Streamlit UI and MCP client-server architecture.  

---

## Tech Stack

- **Python 3.14**  
- **MCP (FastMCP)** for tool orchestration  
- **Anthropic Claude LLM** for decision-making & text polishing  
- **Streamlit** for UI  
- **Asyncio** for concurrent tool execution  

---

## How it Works

1. User inputs a query (e.g., "Plan my trip to Jaisalmer").  
2. `Agent.py` decides which tools to call.  
3. `MCP Client` calls the tools (`itinerary`, `captions`, `reels`) on `MCP Server`.  
4. Raw tool outputs are sent back to the LLM for polishing.  
5. Final human-readable result is displayed in Streamlit.  

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/yourusername/travel-copilot.git
cd travel-copilot

# Install dependencies
uv sync
uv install

# Start MCP Server
uv run server/mcp_server.py

# Run Streamlit UI
streamlit run app.py

## Author
**Diya Karmakar** – Data Engineer | AI & Travel Enthusiast  
LinkedIn: [your-linkedin-profile]  