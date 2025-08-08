import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- 1. Load the AI Model and Tokenizer ---
# We're using a small, but capable model for our MVP.
# This will download the model to your machine the first time you run it, which may take a few minutes.
print("Loading the Synapse AI core model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float32, trust_remote_code=True)
print("Model loaded successfully.")

# --- 2. Define the Core AI Interaction Function ---
def get_ai_response(user_query):
    """
    This function takes a user query and generates a human-like response from the AI model.
    It's designed to simulate the core conversation logic of our assistant.
    """
    try:
        # We craft a "prompt" to give the AI context and a persona.
        # This is crucial for making the AI act like a professional assistant.
        prompt = f"You are a helpful and professional creative business assistant named Synapse AI for a company that provides photography, videography, and other creative solutions. Your tone should be human-like, friendly, and formal. Based on the following user query, provide a concise and helpful response:\n\nUser: {user_query}\nAssistant:"

        # Convert the prompt text into tokens (numbers) that the model can understand.
        inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
        
        # Generate the AI's response.
        outputs = model.generate(**inputs, max_length=200)

        # Decode the generated tokens back into human-readable text.
        text = tokenizer.batch_decode(outputs)[0]
        
        # Clean up the output to only show the assistant's part of the conversation.
        response = text.split("Assistant:")[1].strip()

        # Basic validation to ensure the response isn't empty.
        if not response:
            raise ValueError("AI response was empty.")

        return response

    except Exception as e:
        # This block catches any errors (e.g., model not loading) and provides a graceful message.
        print(f"An error occurred: {e}")
        return "I apologize, but I'm unable to process your request right now. Please try again later."

# --- 3. Example Usage ---
# This part of the code runs when you execute the script directly, so we can test our function.
if __name__ == "__main__":
    test_query = "Hello, I am interested in your photography services for a wedding. What's the process?"
    print(f"User Query: {test_query}")
    ai_response = get_ai_response(test_query)
    print(f"\nSynapse AI Response: {ai_response}")

    print("\n--- Another Test Query ---")
    another_query = "What kind of video editing do you offer?"
    print(f"User Query: {another_query}")
    ai_response = get_ai_response(another_query)
    print(f"\nSynapse AI Response: {ai_response}")