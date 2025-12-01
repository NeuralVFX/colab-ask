# colab-ask

An LLM assistant magic command for Google Colab notebooks. Ask questions about your notebook with full context including code, outputs, and images.

## Installation
`pip install colab-ask`

## Quick Start
`%load_ext colab_ask`

Then use `%%ask` in any cell:
```
%%ask
What does this notebook do so far?
```
## Features
- 📝 Full notebook context (code, markdown, outputs)
- 🖼️ Image understanding (plots, diagrams)
- 💬 Conversation history across cells
- 🎨 Syntax-highlighted code responses
- ⚡ Streaming responses
- 🔧 Multiple LLM support (Claude, GPT, Gemini)

## Configuration

**Change model:**
`%set_model claude-haiku-4-5-20251001`

Copied!
**Change system prompt:**
```
%%set_sys
You are a teacher, and the user is your student.\n
Please be kind, and helpfull in all situations.\n
Help the student explore the problems they encounter playfully!
```

## API Keys

Automatically uses your API keys in Colab Secrets:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`

## Requirements
- Google Colab
- API key for your chosen LLM
