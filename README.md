# Lingokeun App

Daily English learning task generator for Software Engineers using AI with personalized weakness tracking.

## Features

- 🤖 AI-powered daily tasks (4 types)
  - Word transformations (verb/noun/adjective/adverb/opposite)
  - Indonesian→English translations (statements, negative, question)
  - English→Indonesian conversations (real tech roles: Backend, Frontend, PM, DevOps)
  - Grammar challenges (Simple Present/Past/Future tenses)
- 📝 Editor-based review system with spinner loading
- 📊 Automatic weakness tracking and profiling
- 📚 Personalized B1 learning material generator
- 💡 Daily tips focused on casual workplace conversation
- 🎯 Smart suggestions based on your actual weaknesses

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

### Generate Daily Task
```bash
make generate
# or
uv run lingokeun generate
```

Tasks are saved in `tasks/task_YYYY-MM-DD.md`

### Review Task
```bash
make review DATE=2026-02-05 TASK=1
# or
uv run lingokeun review 2026-02-05 -t 1
```

- Opens editor for your answers
- AI reviews with accuracy scores, nativeness ratings
- Provides advanced tips (phrasal verbs, collocations, idioms)
- Auto-tracks weaknesses to profile
- Appends review to task file

### View Learning Profile
```bash
make profile
# or
uv run lingokeun profile
```

Shows:
- 🔴 Urgent areas (need immediate attention)
- 🟡 Practice areas (keep working on)
- 🟢 Maintain areas (doing well)
- ⚠️ Persistent issues (3+ mistakes)
- ✨ Improving areas
- 📚 Vocabulary gaps

### Generate Learning Materials
```bash
# List suggestions based on your weaknesses
make material

# Generate specific material
make material TOPIC="Prepositions In English"
# or
uv run lingokeun material --topic "Casual Conversational Responses"
```

Materials are saved in `material/` folder with:
- Overview
- Key Concepts
- Common Patterns in Tech Workplace
- Practice Exercises
- Common Mistakes to Avoid
- Quick Reference

## Project Structure

```
lingokeun-app/
├── src/lingokeun/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── ai_service.py        # Gemini AI integration
│   ├── user_profile.py      # Weakness tracking system
│   └── config.py            # Configuration settings
├── tasks/                   # Generated daily tasks
├── material/                # Learning materials (B1 level)
├── profile/
│   └── user_profile.json    # Your learning profile & weaknesses
├── .env                     # Environment variables (not committed)
├── .env.example             # Environment template
├── Makefile                 # Quick commands
└── pyproject.toml           # Project dependencies
```

## Development

Install dev dependencies:
```bash
uv sync --group dev
```

Run linter:
```bash
make lint
# or
uv run ruff check .
```

Auto-fix issues:
```bash
make fix
# or
uv run ruff check . --fix
```

Format code:
```bash
make format
# or
uv run ruff format .
```

## How It Works

1. **Generate**: AI creates personalized daily tasks based on your weakness profile
2. **Practice**: Complete tasks in the generated markdown file
3. **Review**: Submit answers via editor, AI reviews and provides feedback
4. **Track**: System automatically tracks your weaknesses (grammar, translation, vocabulary)
5. **Improve**: Get personalized material suggestions to target your weak areas
6. **Repeat**: Daily practice with AI adapting to your progress

## Learning Path

1. Start with `make generate` to get your first task
2. Complete the 4 tasks in the file
3. Review each task: `make review DATE=YYYY-MM-DD TASK=1-4`
4. Check your profile: `make profile`
5. Generate materials for weak areas: `make material`
6. Study materials and repeat daily

## Tips

- Review tasks regularly to build your weakness profile
- Focus on urgent areas shown in your profile
- Use generated materials to study specific topics
- Practice casual conversational phrases (Sure, Exactly, Got it, etc.)
- Daily tips rotate between grammar, vocabulary, and conversation skills

## License

MIT
