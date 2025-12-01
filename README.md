# colab-ask

An LLM assistant magic command for Google Colab notebooks. Ask questions about your notebook with full context including code, outputs, and images.

## Quick Start
In a Colab session, run this:
'''!pip install colab-ask
load_ext colab_ask'''

**Then use `%%ask` in any cell:**
```
%%ask
What does this notebook do so far?
```
**Change model:**
`%set_model claude-haiku-4-5-20251001`

**Change system prompt:**
```
%%set_sys
You are a teacher, and the user is your student.
Please be kind, and helpfull in all situations.
Help the student explore the problems they encounter playfully!
```

## Supported Models
This uses LiteLLM under the hood, you can use any model it can
You can switch models using `%set_model`. Common options include:
* `gpt-4o` / `gpt-4-turbo`
* `claude-3-5-sonnet` / `claude-3-opus`
* `gemini-1.5-pro`

*Note: You must have the corresponding API key in your Colab Secrets for the model you choose.*

## Requirements
- Google Colab
- API key for your chosen LLM

## 🔒 Privacy & Data
* **Direct Communication:** Your notebook data is sent directly from your Colab instance to the LLM provider (OpenAI/Anthropic/Google). It does not pass through any intermediate middleware servers.
* **Secrets Safety:** `colab-ask`  Colab Secrets from the context context to prevent leaking API keys to the LLM.

