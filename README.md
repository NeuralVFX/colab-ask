# colab-ask
An LLM assistant magic command for Google Colab notebooks. Ask questions about your notebook with full context including code, outputs, and images.
<p align="center">
<img src="https://github.com/NeuralVFX/colab-ask/raw/main/assets/ask-example.gif" width="600" alt="Ask Example Animation">
</p>
## Quick Start
In a Colab session, run this:
```
!pip install colab-ask
load_ext colab_ask
```

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
Please be kind, and helpful in all situations.
Help the student explore the problems they encounter playfully!
```

## Supported Models
This uses LiteLLM under the hood, you can use any model it can load. 
- I'm gettin the most helpfull results with: `claude-sonnet-4-5-20250929`


*Note: You must have the corresponding API key in your Colab Secrets for the model you choose.*

## Requirements
- Google Colab
- API key for your chosen LLM

## 🔒 Privacy & Data
* **Direct Communication:** Your notebook data is sent directly from your Colab instance to the LLM provider (OpenAI/Anthropic/Google). It does not pass through any intermediate middleware servers.
* **Secrets Safety:** `colab-ask` automatically filters Colab Secrets from the context to prevent leaking API keys to the LLM.
