import bpy
import os
import json
import math
from bpy.types import (Operator, Panel, PropertyGroup)
from .src import keyboard



class KEYERROR_PG_main(PropertyGroup):


    
    input_name : bpy.props.StringProperty(name= "Name",default= "Keyboard")
    
    input_scale : bpy.props.FloatProperty(name = "Scale", min = 0, max=1000,default=1)
    
    input_rotation : bpy.props.FloatProperty(name = "Rotation", min = -math.pi * 2, max= math.pi * 2,default=0 , step=100,  subtype ='ANGLE')
    
    input_jsonfile: bpy.props.StringProperty(name= ".json",subtype='FILE_PATH')
    
    input_image : bpy.props.StringProperty(name= "Image",subtype='FILE_PATH')
    
    input_selector : bpy.props.EnumProperty(
        name = "Preset",
        description = "description",
        items = [("custom", "Custom", ""),
                ("ansi40", "Ansi 40%", ""),
                ("ansi60", "Ansi 60%", ""),
                ("ansi104", "Ansi 100%", ""), 
                ("iso60", "Iso 60%", ""),
                ("iso105", "Iso 100%", "")
        ]
    )    
    
    join : bpy.props.BoolProperty(
        name = "Join Keys",
        description = "Include keycaps",
        default = True
    )
    
    parentbool : bpy.props.BoolProperty(
        name = "",
        description = "Include keycaps",
        default = True
    )
    
    parentobj : bpy.props.EnumProperty(
        name = "Parent",
        description = "description",
        items = [("Caps", "to Keycaps", ""),
                ("Switches", "to Switches", ""),
                ("Plate", "to Plate", ""),
                ("PCB", "to PCB", ""), 
                ("Case", "to Case", "")
        ]
    )    

class KEYERROR_PG_keycaps(PropertyGroup):

    boolean : bpy.props.BoolProperty(
        name = "Keycaps",
        description = "Include keycaps",
        default = True
    )
    
    profileselector : bpy.props.EnumProperty(
        name = "Profile",
        description = "overwrites cap profile",
        items = [("cherry", "Cherry", ""),
                ("dsa", "DSA", ""),
                ("sa", "SA", "")
        ]
    )
    
    
    
    color : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
    
    colorpreset : bpy.props.EnumProperty(
        name = "Color",
        description = "overwrites cap color",
        items = [("preset", "from Preset", ""),
                ("custom", "Custom", ""),
                ("(0.041,0.044,0.044,1)", "GMK N9", ""),
                ("(0.135,0.125,0.105,1)", "GMK CC", ""),
                ("(0.753,0.708,0.638,1)", "GMK CP", "")
        ]
    )
    

class KEYERROR_PG_switches(PropertyGroup):
    
    boolean : bpy.props.BoolProperty(
        name = "Switches",
        description = "Include switches",
        default = False
    )
    
    subdselector : bpy.props.EnumProperty(
        name = "keycap subdivision",
        description = "keycap subdivision:",
        items = [("lowpoly", "Lowpoly", ""),
                ("highpoly", "Highpoly", "")
        ]
    ) 
    
    presets : bpy.props.EnumProperty(
        name = "Switch Presets",
        description = "Switch Presets",
        items = [("custom", "Custom", ""),
                ("cherryred", "Cherry MX Red", ""),
                ("gateronyellow", "Gateron Yellow", ""),
                ("keebwerkbushi", "KEEBWERK. BUSHI", ""),
                ("tecseepurppand", "TECSEE PURPLE PANDAS", "")
                
        ]
    )
    
    colorupper : bpy.props.FloatVectorProperty(name = "Upper", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    uppertrans : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    colorbase : bpy.props.FloatVectorProperty(name = "Base", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    basetrans : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    colorstem : bpy.props.FloatVectorProperty(name = "Stem", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.5, 0.5, 0.5, 1.0))
    stemtrans : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    colorpins : bpy.props.FloatVectorProperty(name = "Pins", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.5, 0.2, 0.1, 1.0))
    
    
class KEYERROR_PG_legends(PropertyGroup):
    
    boolean : bpy.props.BoolProperty(
        name = "Legends",
        description = "Include Legends",
        default = False
    )
        
    
    typeselector : bpy.props.EnumProperty(
        name = "legend type",
        description = "legend type:",
        items = [("objleg", "Text Objects", ""),
                 ("uvleg", "Image Texture", "")
        ]
    )
    
    file : bpy.props.StringProperty(name= "Image", subtype='FILE_PATH')  
    
    quality : bpy.props.BoolProperty(
        name = "High Poly Caracters",
        description = "High Poly Caracters",
        default = False
    )
    
    font : bpy.props.EnumProperty(
        name = "Legend Font",
        description = "legend font:",
        items = [("Open Cherry Regular", "Open Cherry Regular", "")
        ]
    )
    
    resolution : bpy.props.IntProperty(name = "Resolution", soft_min = 3, soft_max=9, default=4 ,step = 1)
    
    color : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
    
    colorpreset : bpy.props.EnumProperty(
        name = "Color",
        description = "overwrites cap color",
        items = [("preset", "from Preset", ""),
                ("custom", "Custom", ""),
                ("(0.041,0.044,0.044,1)", "GMK N9", ""),
                ("(0.135,0.125,0.105,1)", "GMK CC", ""),
                ("(0.753,0.708,0.638,1)", "GMK CP", "")
        ]
    )
   


class KEYERROR_PG_pcbplate(PropertyGroup):
    
    platebool : bpy.props.BoolProperty(
        name = "Plate",
        description = "Include Plate",
        default = False
    )
    
    platecolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    platemetallic : bpy.props.FloatProperty(name = "Metallic", min = 0, max=1,default=1)
    platerought : bpy.props.FloatProperty(name = "Roughness", min = 0, max=1,default=0.5)
    platetrans : bpy.props.FloatProperty(name = "Transmission", min = 0, max=1,default=0)
    
    casebool : bpy.props.BoolProperty(
        name = "Case",
        description = "Include Case",
        default = False
    )
    
    casecolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    casemetallic : bpy.props.FloatProperty(name = "Metallic", min = 0, max=1,default=1)
    caserought : bpy.props.FloatProperty(name = "Roughness", min = 0, max=1,default=0.5)
    
    
bl_info = {
    "name": "KEYERROR Alpha",
    "author": "Juxius",
    "version": (1, 2),
    "blender": (3, 00, 0),
    "location": "",
    "description": "Import Keyboard",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

class KEYERROR_OP_main(Operator):
    bl_idname = "add.keyboard"
    bl_label = "Add Default"
    bl_description = "Adds Keyboard"
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        scene = bpy.context.scene
        mytool = scene.my_tool
  
        keyboard.addKeyboard(keyboard.inputSelector())
        
        return {"FINISHED"}     

class KEYERROR_PT_main(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Add Keyboard"
    
    def draw(self, context):
        
        layout = self.layout   
        scene = bpy.context.scene
        mytool = scene.my_tool
        keycapspg = scene.keycaps_pg
        legendspg = scene.legends_pg
        
        row = layout.row()
        row.prop(mytool, "input_name")
        row = layout.row()
        row.prop(mytool, "input_selector")
        
        if mytool.input_selector == "custom":
            row = layout.row()
            row.prop(mytool, "input_jsonfile")
      
        row = layout.row()
        row.prop(mytool, "input_scale")
        
        row = layout.row()
        row.prop(mytool, "input_rotation")
        
        row = layout.row()
        #row.prop(mytool, "join")
        row.prop(mytool, "parentbool")
        sub = row.column() 
        sub.enabled = mytool.parentbool is True
        sub.prop(mytool, "parentobj")
        
        sub = layout.row()
        sub.scale_y = 2
        if mytool.input_selector != "custom":
            sub.enabled = True
        elif os.path.isfile(mytool.input_jsonfile) == True and mytool.input_jsonfile[-1] == "n":
            sub.enabled = True
        else: 
            sub.enabled = False
        if legendspg.boolean == True and keycapspg.boolean == False:
            if legendspg.typeselector == "uvleg":
                sub.enabled = False
        if legendspg.boolean == True and keycapspg.boolean == True and legendspg.typeselector == "uvleg" and mytool.join != True:      
            sub.enabled = False
        sub.operator('add.keyboard', icon='IMPORT',text = "Add Keyboard")

class KEYERROR_PT_keycaps(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'KeyError'    
    bl_label = "Keycaps"
    
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keycapspg = scene.keycaps_pg
        
        box = layout.box()
        
        box.prop(keycapspg, "boolean")

        sub = layout.box()
        sub.enabled = keycapspg.boolean is True
        sub.prop(keycapspg, "profileselector")
        
        
        
        row = sub.row()
        row.prop(keycapspg, "colorpreset")
        
        if keycapspg.colorpreset == "custom":
            row = sub.row()
            row.prop(keycapspg, "color")
        
        
class KEYERROR_PT_switches(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'KeyError'    
    bl_label = "Switches"
    
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        switchespg = scene.switches_pg
        
        box = layout.box()
        
        box.prop(switchespg, "boolean")

        
        
        sub = layout.box()
        sub.enabled = switchespg.boolean is True
        row = sub.row()
        row.prop(switchespg, "subdselector", expand = True)
        row = sub.row()
        row.prop(switchespg, "presets")
        
        if switchespg.presets == "custom":
            row = sub.row()
            row.prop(switchespg, "colorupper")
            row.prop(switchespg, "uppertrans")
            row = sub.row()
            row.prop(switchespg, "colorbase")
            row.prop(switchespg, "basetrans")
            row = sub.row()
            row.prop(switchespg, "colorstem")
            row.prop(switchespg, "stemtrans")
            row = sub.row()
            row.prop(switchespg, "colorpins")
            
        
class KEYERROR_PT_legends(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'KeyError'    
    bl_label = "Legends"
    
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        legendspg = scene.legends_pg
        keycapspg = scene.keycaps_pg
        
        box = layout.box()
        box.prop(legendspg, "boolean")

        sub = layout.box()
        sub.enabled = legendspg.boolean is True
        row = sub.row()
        row.prop(legendspg, "typeselector", expand = True)
        
        
        if legendspg.typeselector == "uvleg":
            row = sub.row()
            row.prop(legendspg, "file", icon ='IMAGE_DATA')
        else:
            row = sub.row()
            row.prop(legendspg, "quality")
            
            if legendspg.quality == True:
                row = sub.row()
                row.prop(legendspg, "resolution")
            
            row = sub.row()
            row.prop(legendspg, "font")
            
            row = sub.row()
            row.prop(legendspg, "colorpreset")
            
            if legendspg.colorpreset == "custom":
                row = sub.row()
                row.prop(legendspg, "color")
            
class KEYERROR_PT_pcbplate(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'KeyError'    
    bl_label = "Plate and PCB"
    
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        legendspg = scene.legends_pg
        keycapspg = scene.keycaps_pg
        pcbplatepg = scene.pcbplate_pg
        
        box = layout.box()
        box.prop(pcbplatepg, "platebool")
        
        sub = layout.box()
        sub.enabled = pcbplatepg.platebool is True
        row = sub.row()
        row.prop(pcbplatepg, "platecolor")
        row = sub.row()
        row.prop(pcbplatepg, "platemetallic")
        row = sub.row()
        row.prop(pcbplatepg, "platerought")
        row = sub.row()
        row.prop(pcbplatepg, "platetrans")
        
        #box = layout.box()
        #box.prop(pcbplatepg, "casebool")
        #
        #sub = layout.box()
        #sub.enabled = pcbplatepg.casebool is True
        #row = sub.row()
        #row.prop(pcbplatepg, "casecolor")
        #row = sub.row()
        #row.prop(pcbplatepg, "casemetallic")
        #row = sub.row()
        #row.prop(pcbplatepg, "caserought")
        
classes = (
            KEYERROR_OP_main,
            KEYERROR_PT_main,
            KEYERROR_PT_keycaps,
            KEYERROR_PT_switches,
            KEYERROR_PT_legends,
            KEYERROR_PT_pcbplate,
            KEYERROR_PG_main,
            KEYERROR_PG_keycaps,
            KEYERROR_PG_switches,
            KEYERROR_PG_legends,
            KEYERROR_PG_pcbplate
        )
        
def menu_func(self, context):
    self.layout.operator(AddKeyboard.bl_idname)

def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= KEYERROR_PG_main)
    bpy.types.Scene.keycaps_pg = bpy.props.PointerProperty(type= KEYERROR_PG_keycaps)
    bpy.types.Scene.switches_pg = bpy.props.PointerProperty(type= KEYERROR_PG_switches)
    bpy.types.Scene.legends_pg = bpy.props.PointerProperty(type= KEYERROR_PG_legends)
    bpy.types.Scene.pcbplate_pg = bpy.props.PointerProperty(type= KEYERROR_PG_pcbplate)
    
def unregister(): 
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.keycaps_pg
    del bpy.types.Scene.switches_pg
    del bpy.types.Scene.legends_pg
    del bpy.types.Scene.pcbplate_pg
    print ("UnRegistred!")

if __name__ == "__main__":
    register()