from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)

def generate_workflow_documentation(title: str, raw_input: str, input_type: str) -> str:
    try:
        if input_type == "json":
            input_section = f"Workflow JSON Definition:\n{raw_input}"
        else:
            input_section = f"Workflow Description (plain English):\n{raw_input}"

        prompt = f"""
        You are a technical documentation writer specializing in workflow automation.
        
        Generate clear, professional documentation for the following workflow.
        
        Workflow Title: {title}
        {input_section}
        
        Your documentation should include:
        1. Overview - what this workflow does in 2-3 sentences
        2. Trigger - what starts this workflow
        3. Steps - explain each step clearly
        4. Output - what the workflow produces
        5. Notes - any important considerations
        
        Format the output in clean markdown.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content # type: ignore

    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")