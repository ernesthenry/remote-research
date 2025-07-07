# MCP Research Project

A Model Context Protocol (MCP) powered chatbot that enables intelligent academic paper search and analysis using arXiv. This project demonstrates how to integrate Claude AI with MCP tools to create a research assistant that can search, store, and analyze academic papers.

## Features

- **Paper Search**: Search for academic papers on arXiv by topic
- **Information Extraction**: Extract detailed information about specific papers
- **Local Storage**: Store paper metadata locally for quick access
- **Interactive Chat**: Natural language interface for research queries
- **Resource Management**: Organize papers by topic with easy access

## Project Structure

```
mcp-project/
├── main.py                 # Entry point (basic hello world)
├── mcp_chatbot.py         # Main chatbot implementation
├── research_server.py     # MCP server with research tools
├── requirements.txt       # Project dependencies
├── papers/               # Directory for storing paper data
│   └── {topic}/          # Topic-specific folders
│       └── papers_info.json  # Paper metadata
└── .env                  # Environment variables (you need to create this)
```

## Prerequisites

- Python 3.8+
- UV package manager (recommended) or pip
- Anthropic API key

## Installation

1. **Clone or download the project files**

2. **Install UV (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```
   
   Or with regular pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   
   Get your API key from: https://console.anthropic.com/

## Usage

### Running the Chatbot

1. **Start the research server** (in one terminal):
   ```bash
   uv run research_server.py
   ```

2. **Start the chatbot** (in another terminal):
   ```bash
   uv run mcp_chatbot.py
   ```

### Example Queries

Once the chatbot is running, you can ask questions like:

- "Search for papers about machine learning"
- "Find recent papers on quantum computing"
- "Extract information about paper 2301.12345"
- "Show me papers on natural language processing"

### Available Commands

- Type your research queries in natural language
- Type `quit` to exit the chatbot
- The system will automatically search arXiv and store results

## MCP Tools

The research server provides the following tools:

### Tools
- **search_papers**: Search arXiv for papers on a specific topic
- **extract_info**: Get detailed information about a specific paper by ID

### Resources
- **papers://folders**: List all available topic folders
- **papers://{topic}**: Get detailed information about papers on a specific topic

### Prompts
- **generate_search_prompt**: Generate structured prompts for paper research

## How It Works

1. **Search Phase**: The chatbot uses the `search_papers` tool to query arXiv
2. **Storage Phase**: Paper metadata is stored locally in JSON files organized by topic
3. **Analysis Phase**: Claude AI analyzes the papers and provides insights
4. **Interaction Phase**: Users can query specific papers or topics through natural language

## File Structure Details

- **mcp_chatbot.py**: Implements the main chatbot logic with MCP integration
- **research_server.py**: FastMCP server that provides research tools and resources
- **papers/**: Directory where all paper data is stored, organized by topic
- **requirements.txt**: All Python dependencies needed for the project

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**: Make sure all dependencies are installed
   ```bash
   uv pip install -r requirements.txt
   ```

2. **"API Key Error"**: Verify your `.env` file contains the correct API key
   ```bash
   ANTHROPIC_API_KEY=your_actual_api_key
   ```

3. **"Connection Error"**: Ensure the research server is running before starting the chatbot

4. **"Permission Error"**: Make sure the script has permission to create the `papers/` directory

### Debug Mode

To see more detailed logging, you can modify the print statements in the code or add debug flags.

## Dependencies

Key dependencies include:
- `mcp`: Model Context Protocol library
- `anthropic`: Anthropic AI API client
- `arxiv`: ArXiv API client
- `fastmcp`: FastMCP server implementation
- `python-dotenv`: Environment variable management

## Contributing

This is a demonstration project showing MCP integration with research tools. Feel free to extend it with additional features like:

- PDF download and processing
- Citation analysis
- Paper similarity matching
- Export functionality
- Web interface

## License

This project is for educational and research purposes. Please respect arXiv's terms of service and API usage guidelines.

## Support

For issues with:
- MCP: Check the Model Context Protocol documentation
- Anthropic API: Visit https://docs.anthropic.com/
- ArXiv API: See https://arxiv.org/help/api/

## Notes

- The chatbot stores paper metadata locally but doesn't download full PDFs
- Search results are cached to avoid repeated API calls
- The system is designed for research and educational use
- Make sure to respect API rate limits for both Anthropic and arXiv
