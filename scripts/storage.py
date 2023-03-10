import base64
from io import BytesIO
import os
import re
import modules.scripts as scripts
import gradio as gr

mongo_host = "localhost"
mongo_port = 27017
mongo_username = ""
mongo_password = ""

if os.getenv('DB_HOST') is not None:
    mongo_host = os.getenv('MONGO_HOST')
if os.getenv('DB_PORT') is not None:
    mongo_port = os.getenv('MONGO_PORT')
if os.getenv('DB_USER') is not None:
    mongo_username = os.getenv('MONGO_USERNAME')
if os.getenv('DB_PASS') is not None:
    mongo_password = os.getenv('MONGO_PASSWORD')

def get_mongo_client(database_name, collection_name):
    from pymongo import MongoClient
    dburl = "mongodb://"+mongo_username+":"+mongo_password+"@"+ mongo_host + ":" + str(mongo_port)
    client = MongoClient(dburl)
    db = client[database_name]
    collection = db[collection_name]
    return collection

class Scripts(scripts.Script):
    def title(self):
        return "Mongo Storage"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        checkbox_save_to_db = gr.inputs.Checkbox(label="Save to DB", default=False)
        database_name = gr.inputs.Textbox(label="Database Name", default="StableDiffusion")
        collection_name = gr.inputs.Textbox(label="Collection Name", default="Automatic1111")
        return [checkbox_save_to_db, database_name, collection_name]

    

    def postprocess(self, p, processed,checkbox_save_to_db,database_name,collection_name):
   
        proc = processed
        # Upload to Mongo
        if checkbox_save_to_db:
            collection = get_mongo_client(database_name, collection_name)
        for i in range(len(proc.images)):

            regex = r"Steps:.*$"
            seed = proc.seed
            prompt = proc.prompt
            neg_prompt = proc.negative_prompt
            info = re.findall(regex,proc.info,re.M)[0]
            image = proc.images[i]
            buffer = BytesIO()
            image.save(buffer, "png")
            img_bytes = buffer.getvalue()
            img_b64 = base64.b64encode(img_bytes)
            
            input_dict = dict(item.split(": ") for item in str(info).split(", "))
            steps = input_dict["Steps"]
            seed = input_dict["Seed"]
            sampler = input_dict["Sampler"]
            cfg_scale = input_dict["CFG scale"]
            size = tuple(map(int, input_dict["Size"].split("x")))
            model_hash = input_dict["Model hash"]
            model = input_dict["Model"]

            if checkbox_save_to_db:
                collection.insert_one({
                    "prompt": prompt, 
                    "negative_prompt": neg_prompt, 
                    "steps": steps, 
                    "seed": seed, 
                    "sampler": sampler,
                    "cfg_scale": cfg_scale, 
                    "size": size, 
                    "model_hash": model_hash, 
                    "model": model, 
                    "image": img_b64
                })
        return True
