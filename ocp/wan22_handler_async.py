'''
Created By : Christian Merriman

Purpose : this is used to connect to COMFYUI and use with Flux image generation
'''
import json
import os
import random
import asyncio
import httpx
import psutil
import subprocess

#directories need to be changed for your installation
COMFYUI_DIRECTORY_MAIN = "C:\\Programming 1\\2025 New PC\\Python\\ComfyUI\\ComfyUI"
COMFYUI_DIRECTORY_OUTPUT = "C:\\Programming 1\\2025 New PC\\Python\\ComfyUI\\ComfyUI\\output"
COMFYUI_URL = "http://localhost:8188"

#our class that will take care of our calls to comfyui for our flux image creation
class Wan22_Handler:
    def __init__(self, image_count, file_name, file_name_enchanced, width, height, batchsize, image_filename, savedirectory, image_reference):
        self.image_counter = image_count
        self.main_file_name = file_name
        self.main_file_name_enchanced = file_name_enchanced
        self.video_width = width
        self.video_height = height
        self.batch_size = batchsize
        self.image_file_name = image_filename
        self.save_directory = savedirectory 
        self.image_reference_filename = image_reference
        self.raw_workflow = None

    #opens our workflow
    async def open_workflow(self, workflow_path):
        """Loads the JSON workflow file."""
        try:
            with open(workflow_path, "r", encoding="utf-8") as f:
                self.raw_workflow = json.load(f)
        except Exception as e:
            print(f"❌ Error opening workflow: {e}")

    #this will send the workflow to comfyui
    async def send_wrapped_workflow(self):
        if not self.raw_workflow:
            return {"error": "No workflow loaded"}

        payload = {"prompt": self.raw_workflow}
        
        #connect timeout prevents hanging if server is totally offline
        timeout = httpx.Timeout(30.0, connect=5.0) 
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(f"{COMFYUI_URL}/prompt", json=payload)
                response.raise_for_status()
                return response.json()
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                print(f"⚠️ ComfyUI Connection Failed: {e}")
                return {"error": "ComfyUI unreachable"}
            except Exception as e:
                print(f"⚠️ API Error: {e}")
                return {"error": str(e)}

    #this will keep track of our responses by polling comfyui
    async def track_image_response(self):

        #comfyUI's standard SaveImage naming: prefix + _ + counter + _.png
        #because main_file_name now includes a UUID, this is unique to the session.
        expected_filename = f"{self.main_file_name}{self.image_counter}_00001_.png"
        
        full_path = os.path.join(COMFYUI_DIRECTORY_OUTPUT, self.save_directory, expected_filename)
        
        print(f"🔍 Monitoring for: {expected_filename}")
        
        #120 seconds total wait with await asyncio.sleep(1)
        for i in range(120):
            try:
                if os.path.exists(full_path):
                    #check if file is finished being written (size > 0)
                    if os.path.getsize(full_path) > 0:
                        print(f"✅ Image Found: {full_path}")
                        return [full_path]
            except OSError:
                #file might be locked by ComfyUI while writing
                pass
            
            #nonblocking sleep keeps Django responsive
            await asyncio.sleep(1)
            
        print(f"❌ Timeout: {expected_filename} not found.")
        return []

    #we use this to update our json workflow file
    async def update_workflow_fluxschnell(self, positive_prompt=""):
        #do a random seed or always the same
        seed = random.randint(0, 18446744073709551615)
        
        #build prefix as a RELATIVE path for ComfyUI's internal 'output' folder
        filename_prefix = f"{self.save_directory}\\{self.main_file_name}{self.image_counter}"

        #now go through and setup the data needed
        for node_id, node in self.raw_workflow.items():
            if isinstance(node, dict) and "class_type" in node:
                class_type = node["class_type"]
                title = node.get("_meta", {}).get("title", "")

                if class_type == "CLIPTextEncode" and "Positive Prompt" in title:
                    node["inputs"]["text"] = positive_prompt

                elif class_type == "KSampler":
                    node["inputs"]["seed"] = seed

                elif "Save Image" in title or class_type == "SaveImage":
                    node["inputs"]["filename_prefix"] = filename_prefix

                elif class_type == "EmptySD3LatentImage":
                    node["inputs"]["width"] = self.video_width
                    node["inputs"]["height"] = self.video_height
                    node["inputs"]["batch_size"] = self.batch_size
        
        return seed

    #this is used for flux kontext. add up to 2 images to our flux image to work with
    async def update_workflow_fluxs_kontext(self, positive_prompt="", kontext_image1="", kontext_image2=""):
        #make seed
        seed = random.randint(0, 18446744073709551615)
        filename_prefix = f"{self.save_directory}\\{self.main_file_name}{self.image_counter}"

        #setup the data for our workflow json file nodes
        for node_id, node in self.raw_workflow.items():
            if isinstance(node, dict) and "class_type" in node:
                class_type = node["class_type"]
                title = node.get("_meta", {}).get("title", "")

                if class_type == "CLIPTextEncode" and "Positive Prompt" in title:
                    node["inputs"]["text"] = positive_prompt

                elif class_type == "KSampler":
                    node["inputs"]["seed"] = seed

                elif class_type == "LoadImage":
                    if "Image1" in title:
                        node["inputs"]["image"] = kontext_image1
                    elif "Image2" in title:
                        node["inputs"]["image"] = kontext_image2

                elif "Save Image" in title or class_type == "SaveImage":
                    node["inputs"]["filename_prefix"] = filename_prefix

        return seed

    #restart comfyui if needed
    async def restart_comfyui(self):
        print("🔄 Restarting ComfyUI...")
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if proc.info['name'] == "python.exe":
                    cmdline = proc.info.get('cmdline', [])
                    if any("main.py" in arg for arg in cmdline):
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        await asyncio.sleep(2)
        subprocess.Popen(["python.exe", "main.py"], cwd=COMFYUI_DIRECTORY_MAIN)
        await asyncio.sleep(60) # slightly longer wait for model loading, normally can take a minute to load