---
title: Agentic Data Analysis with LangChain
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: '4.29.0'
app_file: app.py
pinned: false
---

# 🤖 Agentic Data Analysis with LangChain

This is a data analysis agent that can answer questions, perform calculations, and generate visualizations from a CSV file you provide. This demo uses LangChain and OpenAI's GPT-3.5-Turbo model to power the agent's reasoning capabilities.

## 🚀 How to Use the Live Demo

1.  **Upload a CSV File:** Use the file uploader to select a `.csv` file from your computer.
2.  **Ask a Question:** In the textbox, ask a question about your data in plain English. You can ask for:
    * **Calculations:** "What is the average value in the 'sales' column?"
    * **Visualizations:** "Create a bar chart of sales by category."
    * **Insights & Recommendations:** "Show me the top 5 selling products and give me one recommendation."
3.  **Run Analysis:** Click the "Run Analysis" button and wait for the agent to respond with a text answer and a visualization (if requested).

---

## 🛠️ Local Setup and Execution (For Developers)

Follow these steps to run the application on your own machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Shiverion/Analyst-Agent.git](https://github.com/Shiverion/Analyst-Agent.git)
cd gradio-data-agent
```

### 2. Set Up the Environment with uv
This project uses uv for fast and reproducible environment management.

First, install uv if you haven't already:

# On macOS / Linux
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```
Then, sync the environment. This command creates a virtual environment and installs the exact package versions from the uv.lock file.

```bash
uv sync
```

### 3. Set Up Your API Key
Create a file named `.env` in the root of the project and add your OpenAI API key to it:
    OPENAI_API_KEY='your-secret-key-here'

### 4. Run the Application
Use `uv` to run the app within the managed environment:

``` bash
uv run app.py
```
--- 

Open the local URL (e.g., http://127.0.0.1:7860) in your browser.

📄 File Structure
- **app.py:** The main Gradio application script containing the agent logic.

- **requirements.txt:** A list of Python dependencies for Hugging Face Spaces.

- **uv.lock:** A definitive lockfile for reproducible environments with uv.

- **.env:** Local file for storing your secret API key (ignored by Git).

- **.gitignore:** Specifies files for Git to ignore.