import torch
from transformers import pipeline

# We're switching to a smaller model to fit within Vercel's memory limits.
# This model is a tiny version of BERT, perfect for text-based tasks.
print("Loading the Synapse AI core model...")
model = pipeline("summarization", model="prajjwal1/bert-tiny", framework="pt")
print("Model loaded successfully.")

# We'll adapt our function to use this new, smaller model.
def get_ai_response(user_query):
    """
    This function takes a user query and returns a summary.
    """
    try:
        # Create the prompt for the summarization pipeline.
        # This model doesn't generate conversation, it summarizes text.
        summary_text = model(user_query, max_length=100, min_length=30, do_sample=False)
        response = summary_text[0]['summary_text']

        if not response:
            raise ValueError("AI response was empty.")

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "I apologize, but I'm unable to process your request right now. Please try again later."

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

