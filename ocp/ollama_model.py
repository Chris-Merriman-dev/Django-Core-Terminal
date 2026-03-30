'''
    Created By : Christian Merriman

    Updated : 2/2026

    Purpose : To connect to local Ollama server, to use LLM.
'''
import requests
from asgiref.sync import sync_to_async


#stores local models to use
ollama_crew = "ollama/llama3.1:8b"
ollama_normal = "llama3.1:8b"
gemma = "gemma3:12b"
deepseek_uncensored_crew = "ollama/huihui_ai/deepseek-r1-abliterated:14b"
deepseek_uncensored_normal = "huihui_ai/deepseek-r1-abliterated:14b"
gpt_local = "gpt-oss:20b"

model_used_crew = ollama_crew
model_used_normal = ollama_normal

import random

class Ask_Model():
    def __init__(self):
        pass
    
    #closes model to free vram
    async def close_model(self):
        response = Ask_Model().ask_model("hi", keep_alive=0)

    #sends in the prompt with chat history, so the LLM has context of it
    def ask_model_with_chat_history(self, prompt, chat_history, temperature=0.8, keep_alive = 0, system_instructions = ""):

        if not chat_history:
            chat_history.append({"role": "system", "content": system_instructions})

        #add the newest message to our 'long term' history
        chat_history.append({"role": "user", "content": prompt})

        #CREATE A SLICE (The 'Short Term' Memory)
        #We always keep the first message (The System Instructions)
        #Plus the last 6 messages (3 questions, 3 answers)
        context_window = [chat_history[0]] + chat_history[-6:]

        #setup data and send to local LLM
        url = "http://localhost:11434/api/chat"
        data = {
            "model": model_used_normal,
            "messages": context_window,
            "stream": False,
            "keep_alive" : keep_alive,
            #"options": {
            #    "temperature": temperature  #temp for llm
            #}
        }

        try:
            response = requests.post(url, json=data)
            ai_reply = response.json()['message']['content']
        except Exception as e:
            ai_reply = f"LLM Error: {str(e)}"

        #add to list
        chat_history.append({"role": "assistant", "content": ai_reply})

        #return response and the chat history
        return ai_reply, chat_history
    
    import requests

    #just sends in 1 prompt to get a response
    def ask_model(self, prompt, temperature=0.8, keep_alive=0, system_instructions=""):
        url = "http://localhost:11434/api/chat"
        
        #setup data
        data = {
            "model": model_used_normal,
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "keep_alive": f"{keep_alive}m" # "1m" or "0m"
        }

        try:
            #post to LLM
            response = requests.post(url, json=data, timeout=90)
            result = response.json()

            #extracting data
            if 'message' in result and 'content' in result['message']:
                return result['message']['content'].strip()
            else:
                return f"LLM Error: {result.get('error', 'Unknown response format')}"

        except Exception as e:
            return f"LLM Error: {str(e)}"
    