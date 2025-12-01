# colab-ask 🪄
<p align="center">
  <img src="https://github.com/NeuralVFX/colab-ask/raw/main/assets/ask-example.gif" width="600" alt="Ask Example Animation">
</p>

**Stop copy-pasting errors.** `colab-ask` gives your LLM eyes inside your notebook.

It’s a magic command that sends your **code, outputs, and even generated images** (matplotlib, etc.) directly to models like Claude or GPT-4 for context-aware help.

## ✨ Why use this?
* **👀 Context Aware:** It sees your text and code cells, and error traces.
* **📊 Vision Capable:** It can see embedded images an graphs.
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

**Set System Prompt:**
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

