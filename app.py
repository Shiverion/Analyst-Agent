import gradio as gr
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Changed from OpenAI to ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# --- Load Environment Variables ---
# This line reads the .env file and loads the variables into the environment
load_dotenv()

# --- Configuration ---
# Define a constant for the plot filename to ensure consistency.
PLOT_FILENAME = "temp_analysis_plot.png"

# --- Agent Logic ---
def data_analyst_agent(file_obj, user_prompt):
    """
    This is the core function that orchestrates the agent's work.
    It takes a file object from Gradio and a user's text prompt,
    runs the LangChain agent, and returns the analysis and any generated plot.
    """
    # 1. Input Validation
    if file_obj is None:
        return "Error: Please upload a CSV file first.", None
    if not user_prompt:
        return "Error: Please enter a question or instruction.", None

    # --- API Key Check ---
    # Explicitly check for the OpenAI API key from environment variables.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "Error: OPENAI_API_KEY not found. Please add it to your .env file."
        print(error_msg)
        return error_msg, None

    # 2. Cleanup: Remove any old plot file to prevent showing stale results.
    if os.path.exists(PLOT_FILENAME):
        os.remove(PLOT_FILENAME)
    
    # 3. Main execution block with error handling
    try:
        # Load Data: The file_obj from Gradio has a .name attribute
        # which holds the temporary path to the uploaded file.
        df = pd.read_csv(file_obj.name)

        # Initialize LLM: Use a chat model that supports tool calling.
        llm = ChatOpenAI(
            api_key=api_key, 
            temperature=0, 
            model="gpt-3.5-turbo" # Specify a tool-calling model
        )

        # Create Agent: This is the heart of the operation.
        # `create_pandas_dataframe_agent` equips the LLM with tools
        # to execute pandas operations on the DataFrame.
        agent_executor = create_pandas_dataframe_agent(
            llm,
            df,
            agent_type="openai-tools",
            verbose=True,  # Set to True to see the agent's thought process in the terminal
            allow_dangerous_code=True # Opt-in to allow the agent to execute Python code
        )

        # Craft a Detailed Prompt: We augment the user's prompt to give the
        # agent explicit instructions on how to handle visualizations.
        # This makes the agent much more reliable.
        full_prompt = f"""
        User Question: {user_prompt}

        Instructions for the agent:
        - First, analyze the provided data to answer the user's question.
        - If you generate a plot or visualization, you MUST save it as a file named '{PLOT_FILENAME}'.
        - In your final answer, you must explicitly describe the visualization you created (e.g., "I have created a bar chart that shows the total sales for each product category.").
        - Also, mention that the plot has been saved.
        - Use Markdown formatting for all text in your output. This includes headings, bullet points, code blocks (if any), and emphasis for clarity.
        """

        # Run the Agent: Invoke the agent with the detailed prompt.
        response = agent_executor.invoke({"input": full_prompt})
        
        # Extract the text output from the agent's response.
        text_output = response.get('output', "I couldn't generate a text response. Please check the logs.")

        # Check for and Return the Plot: After the agent runs, check if the
        # plot file was created. If so, return it alongside the text answer.
        if os.path.exists(PLOT_FILENAME):
            return text_output, PLOT_FILENAME
        else:
            # If no plot was created, return None for the image output.
            return text_output, None

    
    except Exception as e:
        
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message) 
        return error_message, None

# --- Gradio UI ---
# Using gr.Blocks for a custom layout.
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        """
        # 🤖 Agentic Data Analysis with LangChain
        Upload your CSV file, ask a question in natural language, and the AI agent will work to find the answer.
        It can perform calculations, data manipulation, and even generate visualizations.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input components
            file_input = gr.File(label="Upload your CSV", file_types=[".csv"])
            text_input = gr.Textbox(
                label="What would you like to know?",
                placeholder="e.g., 'What is the correlation between column A and B?' or 'Create a bar chart of sales by category.'"
            )
            submit_button = gr.Button("🚀 Run Analysis", variant="primary")
        
        with gr.Column(scale=2):
            # Output components
            text_output = gr.Markdown(label="📝 Agent's Answer")
            plot_output = gr.Image(label="📊 Generated Visualization", type="filepath")

    # Connect the button to the agent function
    submit_button.click(
        fn=data_analyst_agent,
        inputs=[file_input, text_input],
        outputs=[text_output, plot_output]
    )

# This block allows the script to be run directly from the command line.
if __name__ == "__main__":
    # Launch the Gradio app
    demo.launch()

