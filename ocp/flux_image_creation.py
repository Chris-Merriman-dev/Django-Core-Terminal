"""
Created By : Christian Merriman
Purpose: Used to create Flux Image inside a Django Environment.

"""
import time
import os
import gc
import asyncio
import uuid
from pathlib import Path
from django.conf import settings
from .wan22_handler_async import Wan22_Handler

####################
# Directories (Django-Ready)
####################
COMFYUI_URL = "http://localhost:8188"

# Django-Native Paths
BASE_OCP_DIR = Path(__file__).resolve().parent
FILES_DIRECTORY = str(BASE_OCP_DIR / "files")

# The subfolder name within ComfyUI Output
COMFY_SUBFOLDER = "visions"

# Resolves to: your_project/media/visions/
DIRECTORY_OUTPUT_STORY = os.path.join(settings.MEDIA_ROOT, COMFY_SUBFOLDER)

# External ComfyUI Paths
COMFYUI_DIRECTORY_OUTPUT = "C:\\Programming 1\\2025 New PC\\Python\\ComfyUI\\ComfyUI\\output"

####################
# File Names
####################
WORKFLOW_FLUX_NO_IMAGE_FILE1 = "Flux_No_Image_APP_1_API_1.json"
WORKFLOW_FREEMEM = "free_mem_API_1.json"
MAIN_FLUX_FILENAME = "Flux_img"
IMAGE_FILE = ""

####################
# Variables
####################
IMAGE_COUNTER = 1
FLUX_WIDTH = 1280
FLUX_HEIGHT = 720
FLUX_BATCH_SIZE = 1

class Flux_Image:
    def __init__(self):
        #ensure the Django Media directory exists
        os.makedirs(DIRECTORY_OUTPUT_STORY, exist_ok=True)
        #create a unique ID for this instance to prevent filename collisions
        self.session_id = uuid.uuid4().hex[:6]

    #will create ouf flux kontext (or non kontext) images with the directory we want
    async def create_fluxschnell_kontext_images_with_directory(self, prompt: str, filename, in_directory: str, workflow: str, kontext_workflow: bool, kontext_image_1: str = "", kontext_image_2="", batchsize: int = FLUX_BATCH_SIZE, image_to_use=""):
        all_images = []
        seed = 0

        #make sure we have a valid call
        if prompt == "" or not os.path.isfile(workflow):
            print(f"❌ Error! Invalid input or Workflow missing at: {workflow}")
            print(f"input is : {prompt}")
            return all_images, seed
        
        #init
        wan_handler = Wan22_Handler(
            IMAGE_COUNTER, 
            filename,
            f"{filename}_enhanced_",
            FLUX_WIDTH, 
            FLUX_HEIGHT, 
            batchsize, 
            image_to_use, 
            in_directory,
            IMAGE_FILE
        )
        
        #open and setup our workflow
        await wan_handler.open_workflow(workflow)

        #do we want to use flux kontext (with images) or not. (for ed-209 we will not use kontext)
        if kontext_workflow:
            seed = await wan_handler.update_workflow_fluxs_kontext(positive_prompt=prompt, kontext_image1=kontext_image_1, kontext_image2=kontext_image_2)
        else:
            seed = await wan_handler.update_workflow_fluxschnell(positive_prompt=prompt)
        
        #ensure no old file with this name exists in the output folder before we start
        expected_name = f"{filename}{IMAGE_COUNTER}_00001_.png"
        old_file_path = os.path.join(COMFYUI_DIRECTORY_OUTPUT, in_directory, expected_name)
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
                print(f"🧹 Cleaned up old image file: {expected_name}")
            except Exception as e:
                print(f"⚠️ Could not remove old file: {e}")

        #send to ComfyUI
        response = await wan_handler.send_wrapped_workflow()
        
        #make sure we get our image (will always return array)
        if response and "error" not in response:
            all_images = await wan_handler.track_image_response()
        else:
            print(f"⚠️ ComfyUI Error: {response}")

        #make sure we free mem for future uses
        del wan_handler
        gc.collect()

        return all_images, seed
    
    #calls our workflow to free up vram. the workflow already does this, but sometimes comfyui bugs out and loves to hold onto your vram and memory.
    async def comfyui_freemem(self, workflow: str):
        print('\nFreeing up VRAM...')
        wan_handler = Wan22_Handler(
            IMAGE_COUNTER, '', '',
            FLUX_WIDTH, FLUX_HEIGHT, 0, '', '', IMAGE_FILE
        )
        
        await wan_handler.open_workflow(workflow)
        await wan_handler.send_wrapped_workflow()
        await asyncio.sleep(5) 

        del wan_handler
        gc.collect()
        await asyncio.sleep(1)

    #we call this to create our image
    async def create_flux_kontext_image(self, prompt_for_flux: str, workflow: str = None, Kontext_Workflow: bool = False, kontext_image1: str = "", kontext_image2: str = "") -> str:
        #make sure we have our workflow to load
        if workflow is None:
            workflow = os.path.join(FILES_DIRECTORY, WORKFLOW_FLUX_NO_IMAGE_FILE1)
            
        image_used = ""
        get_flux_image = True
        seed = 0
        
        #unique filename per request: e.g., Flux_img_a1b2c3
        unique_filename = f"{MAIN_FLUX_FILENAME}_{self.session_id}"
        main_direct = COMFY_SUBFOLDER 
        
        image_loop_count = 0
        MAX_LOOP_COUNT = 1

        #we will loop through until we get an image
        #for ed-209 we will just loop once.
        while get_flux_image:
            #create the image
            #this sends back our image list and seed number we used for the image
            images, seed = await self.create_fluxschnell_kontext_images_with_directory(
                prompt=prompt_for_flux, 
                filename=unique_filename, 
                in_directory=main_direct,
                workflow=workflow,
                kontext_workflow=Kontext_Workflow,
                kontext_image_1=kontext_image1,
                kontext_image_2=kontext_image2,
                batchsize=FLUX_BATCH_SIZE
            )

            #make sure we created an image
            if len(images) > 0:
                image_used = images[0]
                print(f"✅ NEW IMAGE CREATED : {image_used}")
                get_flux_image = False          
            else:
                print('❌ ERROR! NO NEW IMAGES FOUND!')
                get_flux_image = False 

            #now free up vram
            freemem_workflow = os.path.join(FILES_DIRECTORY, WORKFLOW_FREEMEM)
            if os.path.exists(freemem_workflow):
                await self.comfyui_freemem(freemem_workflow)   

            image_loop_count += 1

        return image_used, seed