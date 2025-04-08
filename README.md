# LLM API Explorer

A web-based explorer for free LLM API providers, based on the amazing work by [cheahjs/free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources).

## Description

This project creates a user-friendly web interface to explore and navigate the various free LLM API providers compiled by cheahjs. It presents the information in a searchable, sortable table format with detailed information about each provider and their available models.

## Features

- Interactive table of LLM API providers
- Detailed view of available models
- Provider-specific limits and credits information
- Direct links to provider services
- Responsive design
- Search and filter capabilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-api-explorer.git
cd llm-api-explorer
```

2. Install required packages:
```bash
pip install flask requests markdown
```

3. Run the application:
```bash
python src/app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
llm-api-explorer/
├── src/
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── index.html
│   │   └── provider.html
│   └── app.py
└── README.md
```

## Credits

This project would not be possible without the excellent work of:

- **[@cheahjs](https://github.com/cheahjs)** - Creator of the [free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources) repository
- All contributors to the original repository

## License

This project is licensed under the MIT License - see the original repository for details.

## Acknowledgments

Special thanks to:
- cheahjs for maintaining the comprehensive list of free LLM API resources
- The LLM provider community for making these services accessible