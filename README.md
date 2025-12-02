# colab-ask 🪄
<p align="center">
  <img src="https://github.com/NeuralVFX/colab-ask/raw/main/assets/ask-example.gif" width="600" alt="Ask Example Animation">
</p>

Colab-Ask is a magic command that sends your **code, outputs, and even generated images** (matplotlib, etc.) directly to models like Claude or GPT-4 for context-aware help.
## Why use this?
* **Context Aware:** It sees your text and code cells, and error traces.
* **Vision Capable:** It can see embedded images and graphs.
* **Native Integration:** Lives inside Colab. No alt-tabbing to ChatGPT.
* **Privacy First:** Your data goes straight to the API. No middleman servers.

## Prerequisites (Before you start)
1. **Google Colab:** This extension is designed specifically for the Colab environment.
2. **API Keys:** You need an API key for your preferred provider (OpenAI, Anthropic, Gemini, etc.).
   * Click the **Key Icon** (Secrets) on the left sidebar in Colab.
   * Add a new secret (e.g., `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`).
   * Toggle "Notebook access" **ON**.
---
## Quick Start
Run this in a cell to install and load the extension:

```python
!pip install colab-ask
%load_ext colab_ask
```

### 1. The Basic Ask
Use `%%ask` to chat about your current notebook state.

```python
%%ask
My training loop is stalling at epoch 5. based on the logs above, why?
```

### 2. The Vision Ask
Since `colab-ask` sees images, you can ask about plots:

```python
# (After generating a matplotlib chart)
%%ask
Look at the plot above. Is the model overfitting?
```

---

## Configuration

**Change Model:**
Uses LiteLLM under the hood. Any supported model string works. Check [https://docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)
```python
%set_model claude-3-5-sonnet-20241022
```

**Set System Prompt:**
Want a specific teaching style?
```python
%%set_sys
You are a senior Python engineer. Be concise. 
Focus on performance optimization and vectorized operations.
```

## Privacy & Data
* **Direct Communication:** Notebook data is sent directly from your browser/runtime to the LLM provider (OpenAI/Anthropic/Google).
* **Zero Logs:** We do not run a middleware server. We do not store your code.

