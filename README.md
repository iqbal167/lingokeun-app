# Lingokeun App

Daily English learning task generator for Software Engineers using AI.

## Features

- 🤖 AI-powered vocabulary selection (5 words per day)
- 📝 Word transformation challenges
- 🌐 Translation exercises (Indonesian to English, B1 level)
- 💡 Daily professional communication tips
- 📅 Automatic task file generation

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lingokeun-app
```

2. Install dependencies:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://aistudio.google.com/apikey

## Usage

Generate daily task:
```bash
uv run lingokeun
```

Tasks are saved in `tasks/task_YYYY-MM-DD.md`

## Project Structure

```
lingokeun-app/
├── src/lingokeun/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── ai_service.py    # Gemini AI integration
│   └── config.py        # Configuration settings
├── tasks/               # Generated task files
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment template
└── pyproject.toml       # Project dependencies
```

## Development

Install dev dependencies:
```bash
uv sync --group dev
```

Run linter:
```bash
uv run ruff check .
```

Run type checker:
```bash
uv run mypy src/
```

## License

MIT
