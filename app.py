import gradio as gr
from core_logic import get_ai_response 
from fastapi import FastAPI
import random
import time

# A simple list to simulate storing call summaries
call_summaries = []

def process_call_summary(query, call_id):
    """
    This function simulates processing a call and generating a summary.
    In a real-world scenario, this would involve audio transcription and summarization.
    For our MVP, we'll use our AI logic to create a sample summary.
    """
    # Use our AI model to "summarize" the call.
    summary_prompt = f"The following is a transcript of a customer call: '{query}'. Based on this, please provide a brief summary of the customer's needs, their contact details if available, and whether they are a high-priority lead. Format the response cleanly."
    
    summary = get_ai_response(summary_prompt)
    
    # Store the summary with a unique ID for our dashboard
    new_summary = {
        "id": call_id,
        "query": query,
        "summary": summary,
        "status": "Pending Approval",
        "action_taken": None
    }
    call_summaries.append(new_summary)
    
    # Return a success message and a notification to the UI
    return f"Call {call_id} processed. Summary saved.", f"New call summary available for Call {call_id}!"

def approve_action(call_id):
    """Simulates approving a follow-up action for a specific call."""
    for summary in call_summaries:
        if summary["id"] == call_id:
            summary["status"] = "Approved"
            summary["action_taken"] = f"Email with a preliminary quote has been sent to the client."
            return f"Action for Call {call_id} approved. Follow-up email sent."
    return "Error: Call not found."

def decline_action(call_id):
    """Simulates declining a follow-up action for a specific call."""
    for summary in call_summaries:
        if summary["id"] == call_id:
            summary["status"] = "Declined"
            summary["action_taken"] = "No action taken."
            return f"Action for Call {call_id} declined. Client will not be contacted."
    return "Error: Call not found."

def get_dashboard_data():
    """
    Generates the dashboard content dynamically.
    The Gradio output will update automatically with this function.
    """
    if not call_summaries:
        return "No call summaries to display yet.", ""
    
    # Create the HTML for our dashboard display
    html_output = "<div style='font-family: sans-serif;'>"
    for summary in call_summaries:
        status_color = "orange" if summary['status'] == "Pending Approval" else "green" if summary['status'] == "Approved" else "red"
        
        html_output += f"""
        <div style='border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 8px;'>
            <h3 style='margin-top: 0;'>Call ID: {summary['id']}</h3>
            <p><strong>Original Query:</strong> {summary['query']}</p>
            <p><strong>AI Summary:</strong> {summary['summary']}</p>
            <p><strong>Status:</strong> <span style='color: {status_color}; font-weight: bold;'>{summary['status']}</span></p>
            {f'<p><strong>Action:</strong> {summary["action_taken"]}</p>' if summary['action_taken'] else ''}
        </div>
        """
    html_output += "</div>"
    
    return "Dashboard updated!", html_output

# Create the Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Synapse AI - Creative Business Assistant Dashboard")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Simulate a New Call")
            call_input = gr.Textbox(lines=5, label="Enter simulated call details here:")
            call_id_input = gr.Number(label="Call ID (e.g., 101)", value=101)
            submit_btn = gr.Button("Simulate Call & Get Summary")
            call_status_output = gr.Textbox(label="Processing Status")
            
        with gr.Column():
            gr.Markdown("### Action Center")
            approval_id_input = gr.Number(label="Enter Call ID for Approval", value=101)
            approve_btn = gr.Button("Approve & Send Follow-up")
            decline_btn = gr.Button("Decline & Do Nothing")
            action_output = gr.Textbox(label="Action Log")

    gr.Markdown("---")
    gr.Markdown("### Live Dashboard")
    with gr.Row():
        dashboard_notification = gr.Textbox(label="Notifications")
        dashboard_data = gr.HTML(label="Call Summaries & Status")
        refresh_btn = gr.Button("Refresh Dashboard")

    # Connect UI components to our Python functions
    submit_btn.click(fn=process_call_summary, inputs=[call_input, call_id_input], outputs=[call_status_output, dashboard_notification])
    
    approve_btn.click(fn=approve_action, inputs=approval_id_input, outputs=action_output).then(fn=get_dashboard_data, outputs=[dashboard_notification, dashboard_data])
    
    decline_btn.click(fn=decline_action, inputs=approval_id_input, outputs=action_output).then(fn=get_dashboard_data, outputs=[dashboard_notification, dashboard_data])
    
    refresh_btn.click(fn=get_dashboard_data, outputs=[dashboard_notification, dashboard_data])

# Mount the Gradio app to FastAPI for Vercel deployment
app = gr.mount_gradio_app(FastAPI(), demo, path="/")
