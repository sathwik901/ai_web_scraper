from groq import Groq
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Initializing Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_groq(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Formating the prompt with actual content
        formatted_prompt = template.format(
            dom_content=chunk, 
            parse_description=parse_description
        )
        
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ],
                temperature=0.1,  
                max_tokens=1000,  
                top_p=0.9
            )
            
            result = response.choices[0].message.content
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(result)
            
        except Exception as e:
            print(f"Error parsing batch {i}: {str(e)}")
            parsed_results.append("") 
            continue

    return "\n".join(parsed_results)