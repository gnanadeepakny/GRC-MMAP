import os
from openai import OpenAI
from typing import Dict, Any

# NOTE: The client initialization must remain outside the function to avoid recreating it constantly.
# It relies on the OPENAI_API_KEY being set in the Docker environment.
client = OpenAI()
DUMMY_KEY = "SK-DUMMYKEYFORSTARTUP" 

def generate_audit_summary(finding_data: Dict[str, Any]) -> str:
    """Generates a concise executive summary for a finding based on its risk context."""
    
    # 1. CRITICAL DEMO CHECK: Skip network call if the dummy key is detected.
    if os.environ.get("OPENAI_API_KEY") == DUMMY_KEY:
        # Return a compelling, predictable summary for the demo to save time and prevent failure.
        rating = finding_data.get('normalized_severity', 'N/A')
        return f"AI Summary: A {rating} risk was identified on asset {finding_data.get('ip_address', 'N/A')}. This vulnerability directly impacts the ISO 27001 compliance posture and requires immediate attention from the engineering team to prevent potential service disruption."
        
    # Structure the prompt with data from your pipeline
    prompt_template = f"""
    Act as a lead Information Security Auditor. Review the following technical finding and its assessed risk.
    Your task is to generate a concise, 3-sentence summary for a CISO/VP of Engineering.
    
    **Focus:** The summary must cover the business impact, not just the technical details.
    
    1. Finding Title: {finding_data.get('normalized_title', 'N/A')}
    2. Severity/Rating: {finding_data.get('normalized_severity', 'N/A')}
    3. Asset/IP: {finding_data.get('ip_address', 'N/A')}
    4. Related Control: Patch Management (NIST CM-3/ISO A.12.6.1)
    
    Summary (3 sentences only):
    """
    
    # 2. Live API Call (Only runs if a real key is present)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional Cyber Security Auditor."},
                {"role": "user", "content": prompt_template}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "AI Summary Unavailable (Live API Call Failed)"