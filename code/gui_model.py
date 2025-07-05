import gradio as gr
import ollama

def generate_joke(joke_type, topic, max_tokens=150):
    # System prompt to set the comedian persona
    system_prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        "You are a professional comedian. Respond with exactly one joke in English.\n"
        "Rules:\n"
        "- Must be family-friendly\n"
        "- Maximum 2 sentences\n"
        "- No explanations\n"
        "- No hashtags\n<|eot_id|>"
        "<|start_header_id|>user<|end_header_id|>\n"
    )
    
    # Customize prompt based on joke type
    if joke_type == "Any":
        prompt = f"Tell me a joke about {topic}"
    elif joke_type == "Pun":
        prompt = f"Tell me a pun about {topic}"
    elif joke_type == "Dad Joke":
        prompt = f"Tell me a dad joke about {topic}"
    elif joke_type == "Knock-Knock":
        prompt = f"Tell me a knock-knock joke about {topic}"
    else:
        prompt = f"Tell me a {joke_type.lower()} joke about {topic}"
    
    full_prompt = system_prompt + prompt + "\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

    response = ollama.generate(
        model="http://hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF",
        prompt=full_prompt,
        options={
            "temperature": 1.0,  # Higher for more creativity
            "num_predict": max_tokens,
            "top_k": 60  # Helps with joke variety
        }
    )
    return response['response']

with gr.Blocks(title="AI Joke Generator") as demo:
    gr.Markdown(
        "# 🤣 AI Joke Generator\n"
        "Select joke type and enter a topic to get a funny joke!\n"
        "*(Powered by Llama 3.2 1B Instruct on Ollama)*"
    )
    with gr.Row():
        joke_type = gr.Dropdown(
            label="Joke Type",
            choices=["Any", "Pun", "Dad Joke", "Knock-Knock", "Programming", "Animal"],
            value="Any"
        )
        topic = gr.Textbox(
            label="Topic",
            placeholder="e.g., programmers, animals, food..."
        )
    with gr.Row():
        out = gr.Textbox(
            label="Generated Joke",
            lines=4
        )
    btn = gr.Button("Generate Joke")
    btn.click(fn=generate_joke, inputs=[joke_type, topic], outputs=out)

demo.launch()