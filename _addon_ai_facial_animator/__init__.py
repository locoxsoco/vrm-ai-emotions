bl_info = {
    "name": "AI Face Animator",
    "author": "Luis Carranza",
    "version": (0,0,1),
    "blender": (4,0,0),
    "location": "3D Viewport > Sidebar",
    "description": "AI Face Animator tool for VRM avatars",
    "category": "Development",
}

import bpy
# import sys
# import pip
# pip.main(['install', 'openai', '--target', (sys.exec_prefix) + '\\lib\\site-packages'])
# pip.main(['install', 'langchain-nvidia-ai-endpoints', '--target', (sys.exec_prefix) + '\\lib\\site-packages'])
packages_path = ".\\4.1\\python\\lib\\site-packages"
import sys
sys.path.insert(0, packages_path)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import os
import re
import json

# Define a property in your add-on or script
class MyProperties(bpy.types.PropertyGroup):
    api_key_visibility: bpy.props.BoolProperty(name="Show API Key", description="Press to show/hide Nvidia API Key")
    api_key: bpy.props.StringProperty(name="API Key", description="Enter the Nvidia API Key")
    prompt: bpy.props.StringProperty(name="Prompt", description="Enter the prompt to animate")

class VIEW3D_PT_UIFaceAnimator(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    bl_category = "c"
    bl_label = "Nvidia AI Face Animator"
    
    def draw(self, context):
        scene = context.scene
        my_props = scene.my_props
        row = self.layout.row()
        row.prop(my_props, "api_key_visibility")
        if(context.scene.my_props.api_key_visibility == True):
            row.prop(my_props, "api_key")
        row = self.layout.row()
        row.prop(my_props, "prompt")
        row = self.layout.row()
        row.operator("addonname.myop_operator")

class ADDONNAME_OT_my_op(bpy.types.Operator):
    bl_label = "Generate animation"
    bl_idname = "addonname.myop_operator"
    
    def getShapeKeysNames(self):
        active_object = bpy.context.view_layer.objects.active
        shapekeys = active_object.data.shape_keys.key_blocks
        shapekey_names = [shape_key.name for shape_key in shapekeys]
        return shapekey_names
    
    def animateLLM(self, shape_key_names, user_prompt):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are generating face animations for vrm avatars. For this goal, the input will be the list of blendshape names from the vrm avatar and the prompt to animate. The output is the sequence of blendshape values to generate the facial animation and the frame in which the values are changing. The animation runs at 30 frames per second  and it will last 1 second so you have to return 30 frames maximum. The output format needs to be a list of jsons containing only the frames in which the blendshape is changing, and a the list of blendshapes with its value for each frame. The blendshape values range from 0 to 1. Return only the json, do not give me more information than that.",
                ),
                ("user", "{input}"),
            ]
        )
        llm = ChatNVIDIA(
            model="meta/llama3-70b-instruct"
        )
        chain = prompt | llm | JsonOutputParser()
        message = f"The blendshape names are the following: {shape_key_names}\nThe prompt to animate is {user_prompt}"
        print(f'{message}')
        
        result = chain.invoke({"input": message})
        print(result)
        return result
    
    def clear_keyframes(self):
        active_object = bpy.context.view_layer.objects.active
        active_object_shape_keys = active_object.data.shape_keys
        if active_object_shape_keys.animation_data:
            print("Clearing previous animation data")
            active_object_shape_keys.animation_data_clear()
        else:
            print("No previous animation data to clear")
        return
    
    def generate_keyframes(self,key_shape_names,keyshapes_frames_json):
        active_object = bpy.context.view_layer.objects.active
        active_object_shape_keys = active_object.data.shape_keys.key_blocks
        for keyshapes_frame_json in keyshapes_frames_json:
            frame_json = keyshapes_frame_json["frame"]
            keyshapes_names_json = list(keyshapes_frame_json["blendshapes"].keys())
            for key_shape_name in key_shape_names:
                if(key_shape_name not in keyshapes_names_json):
                    active_object_shape_keys[key_shape_name].value = 0
                else:
                    active_object_shape_keys[key_shape_name].value = keyshapes_frame_json["blendshapes"][key_shape_name]
                active_object_shape_keys[key_shape_name].keyframe_insert(data_path="value", frame=frame_json)
                    
    
    def execute(self, context):
        api_key = context.scene.my_props.api_key
        prompt = context.scene.my_props.prompt
        key_shape_names = self.getShapeKeysNames()
        os.environ["NVIDIA_API_KEY"] = api_key
        keyshapes_frames_json = self.animateLLM(key_shape_names,prompt)
        if(keyshapes_frames_json != None):
            self.clear_keyframes()
            self.generate_keyframes(key_shape_names, keyshapes_frames_json)
        return {"FINISHED"}
    
classes = [MyProperties, VIEW3D_PT_UIFaceAnimator, ADDONNAME_OT_my_op]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_props

def main(context):
    for ob in context.scene.objects:
        print(ob)

if __name__ == "__main__":
    register()