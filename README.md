# colab-ask 🪄
<p align="center">
  <img src="https://github.com/NeuralVFX/colab-ask/raw/main/assets/ask-example.gif" width="600" alt="Ask Example Animation">
</p>

**Stop copy-pasting errors.** `colab-ask` gives your LLM eyes inside your notebook.

It’s a magic command that sends your **code, outputs, and even generated images** (matplotlib, etc.) directly to models like Claude or GPT-4 for context-aware help.

## ✨ Why use this?
* **👀 Context Aware:** It sees your variables, previous cells, and error traces.
* **📊 Vision Capable:** It "looks" at your charts and graphs to explain data trends.
* **⚡ Native Integration:** Lives inside Colab. No alt-tabbing to ChatGPT.
* **🔒 Privacy First:** Your data goes straight to the API. No middleman servers.

---

## 🚀 Quick Start
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

## ⚙️ Configuration

**Change Model:**
Uses LiteLLM under the hood. Any supported model string works.
```python
%set_model claude-3-5-sonnet-20241022
```

**Set Custom Persona:**
Want a specific teaching style?
```python
%%set_sys
You are a senior Python engineer. Be concise. 
Focus on performance optimization and vectorized operations.
```

## 🔑 Requirements
1.  **Google Colab**
2.  **API Keys:** Add your keys (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) to **Colab Secrets** (the key icon on the left sidebar).

## 🔒 Privacy & Data
We take security seriously:
* **Direct Communication:** Notebook data is sent directly from your browser/runtime to the LLM provider (OpenAI/Anthropic/Google).
* **Zero Logs:** We do not run a middleware server. We do not store your code.
* **Secrets Safety:** `colab-ask` automatically filters Colab Secrets from the context to prevent leaking API keys to the LLM.
```python
!pip install colab-ask
%load_ext colab_ask
```


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
