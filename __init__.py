import bpy
import os
import json
import math
from bpy.types import (Operator, Panel, PropertyGroup)
from .src import keyboard
from .src import assets

bl_info = {
    "name": "KEYERROR Alpha",
    "author": "Juxius",
    "version": (1, 5),
    "blender": (3, 20, 0),
    "location": "",
    "description": "Import Keyboard",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}



def clearfunc(self,context):
    scene = bpy.context.scene
    keyb = scene.keyboardpg
    if keyb.booleancap == False and keyb.parenttocap == True:
        keyb.parenttocap = False
    if keyb.booleanswitch == False and keyb.parenttoswitch == True:
        keyb.parenttoswitch = False
    if keyb.booleanplate == False and keyb.parenttoplate == True:
        keyb.parenttoplate = False
    if keyb.booleancase == False and keyb.parenttocase == True:
        keyb.parenttocase = False
    if keyb.booleancap == False:
        keyb.booleanlegends = False
 

    
 
class KEYERROR_PG_keyboard(PropertyGroup):


    
    input_name : bpy.props.StringProperty(name= "Name",default= "Keyboard")
    
    input_scale : bpy.props.FloatProperty(name = "Scale", min = 0, max=1000,default=30)
    
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
    

# ----------------------------------------------------caps

    booleancap : bpy.props.BoolProperty(
        name = "Keycaps",
        description = "Include keycaps",
        default = True,
        update = clearfunc
    )
    parenttocap : bpy.props.BoolProperty(
        name = "Parent",
        description = "Parent to keycaps",
        default = True
    )
    
    capprofile : bpy.props.EnumProperty(
        name = "Profile",
        description = "overwrites cap profile",
        items = [("cherry", "Cherry", ""),
                ("dsa", "DSA", ""),
                ("sa", "SA", "")
        ]
    )
    
    capcolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
    
    capcolorpreset : bpy.props.EnumProperty(
        name = "Color",
        description = "overwrites cap color",
        items = [("preset", "from Preset", ""),
                ("custom", "Custom", ""),
                ("0x393B3B", "GMK N9", ""),
                ("0x67635B", "GMK CC", ""),
                ("0xE1DBD1", "GMK CP", "")
        ]
    )
    
# ----------------------------------------------------switches
    
    booleanswitch : bpy.props.BoolProperty(
        name = "Switches",
        description = "Include switches",
        default = False,
        update = clearfunc
    )
    
    parenttoswitch : bpy.props.BoolProperty(
        name = "Parent",
        description = "Parent to keycaps",
        default = False
    )
    
    switchsubd : bpy.props.EnumProperty(       
        name = "Switch subdivision",
        description = "Switch subdivision:",
        items = [("lowpoly", "Lowpoly", ""),
                ("highpoly", "Highpoly", "")
        ]
    ) 
    
    switchpresets : bpy.props.EnumProperty(
        name = "Switch",
        description = "Switch Presets",
        items = [("custom", "Custom", ""),
                ("cherryred", "Cherry MX Red", ""),
                ("gateronyellow", "Gateron Yellow", ""),
                ("keebwerkbushi", "KEEBWERK. BUSHI", ""),
                ("tecseepurppand", "TECSEE PURPLE PANDAS", "")
                
        ]
    )
    
    stabpresets : bpy.props.EnumProperty(
        name = "Stabilizer",
        description = "Stabilizer Presets",
        items = [("custom", "Custom", ""),
                ("bblack", "Basic Black", ""),
                ("btransparent", "Basic Transparent", ""),
                ("studiorx78gold", "STUDIO RX78 GOLD", "")
        ]
    )
    
    switchcolorupper : bpy.props.FloatVectorProperty(name = "Upper", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    switchtransupper : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    switchcolorbase : bpy.props.FloatVectorProperty(name = "Base", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    switchtransbase : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    switchcolorstem : bpy.props.FloatVectorProperty(name = "Stem", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.5, 0.5, 0.5, 1.0))
    switchtransstem : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    switchcolorpins : bpy.props.FloatVectorProperty(name = "Pins", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.5, 0.2, 0.1, 1.0))
    
    stabcolorbase : bpy.props.FloatVectorProperty(name = "Base", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    stabtransbase : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    stabcolorstem : bpy.props.FloatVectorProperty(name = "Stem", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.5, 0.5, 0.5, 1.0))
    stabtransstem : bpy.props.BoolProperty( name = "", description = "Transparent", default = False )
    
    stabcolorbar : bpy.props.FloatVectorProperty(name = "Bar", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
       
# ----------------------------------------------------legends
    
    booleanlegends : bpy.props.BoolProperty(
        name = "Legends",
        description = "Include Legends",
        default = False
    )
    
    legendtype : bpy.props.EnumProperty(
        name = "legend type",
        description = "legend type:",
        items = [("objleg", "Text Objects", ""),
                 ("uvleg", "Image Texture", "")
        ]
    )
    
    legendfile : bpy.props.StringProperty(name= "Image", subtype='FILE_PATH')  # ?
    
    legendquality : bpy.props.BoolProperty(
        name = "High Poly Caracters",
        description = "High Poly Caracters",
        default = False
    )
    
    legendfont : bpy.props.EnumProperty(
        name = "Legend Font",
        description = "legend font:",
        items = [("Open Cherry Regular", "Open Cherry Regular", ""),
#                 ("Helvetica Rounded Bold", "Helvetica Rounded Bold", ""),
#                 ("Univers 57 Condensed Oblique", "Univers 57 Condensed Oblique", "")
        ]
    )
    
    legendresolution : bpy.props.IntProperty(name = "Resolution", soft_min = 3, soft_max=9, default=4 ,step = 1)
    
    legendcolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
    
    legendcolorpreset : bpy.props.EnumProperty(
        name = "Color",
        description = "overwrites cap color",
        items = [("preset", "from Preset", ""),
                ("custom", "Custom", ""),
                ("#393B3B", "GMK N9", ""),
                ("#67635B", "GMK CC", ""),
                ("#E1DBD1", "GMK CP", "")
        ]
    )
   
# ----------------------------------------------------plate
    
    booleanplate : bpy.props.BoolProperty(
        name = "Plate",
        description = "Include Plate",
        default = False,
        update = clearfunc
    )
    
    parenttoplate : bpy.props.BoolProperty(
        name = "Parent",
        description = "Parent to keycaps",
        default = False
    )
    
    platecolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.7, 0.7, 0.7, 1.0))
    platemetallic : bpy.props.FloatProperty(name = "Metallic", min = 0, max=1,default=1)
    platerought : bpy.props.FloatProperty(name = "Roughness", min = 0, max=1,default=0.5)
    platetrans : bpy.props.FloatProperty(name = "Transmission", min = 0, max=1,default=0)
    
# ----------------------------------------------------case

    booleancase : bpy.props.BoolProperty(
        name = "Case",
        description = "Include Case",
        default = False,
        update = clearfunc
    )
    
    parenttocase : bpy.props.BoolProperty(
        name = "Parent",
        description = "Parent to keycaps",
        default = False
    )
    
    casecolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.1, 0.1, 0.1, 1.0))
    casemetallic : bpy.props.FloatProperty(name = "Metallic", min = 0, max=1,default=1)
    caserought : bpy.props.FloatProperty(name = "Roughness", min = 0, max=1,default=0.5)
       
class KEYERROR_PG_assets(PropertyGroup):
    
    casesize : bpy.props.EnumProperty(
        name = "Size",
        description = "Case sizes",
        items = [("type40", "40%", ""),
                ("type60", "60%", ""),
                ("type65", "65%", ""),
                ("type75", "75%", ""),
                ("typeTKL", "TKL", "")
        ]
    )
    casescale : bpy.props.FloatProperty(name = "Scale", min = 0, max=1000,default=30)
    
    type40 : bpy.props.EnumProperty(
        name = "40%",
        description = "40%",
        items = [("Garbage Truck", "Garbage Truck", ""),
                ("V4N4G0N", "V4N4G0N", "")
        ]
    )
    
    type60 : bpy.props.EnumProperty(
        name = "60%",
        description = "60%",
        items = [("RWM60B", "RAMAWORKS M60-B", ""),
                ("RWTHERMAL", "RAMAWORKS THERMAL", "")
        ]
    )
    
    type65 : bpy.props.EnumProperty(
        name = "65%",
        description = "65%",
        items = [("KCQ2", "KEYCHRON Q2", ""),
                ("DISCIPLINEV2", "DISCIPLINEV2", "")
        ]
    )
    
    type75 : bpy.props.EnumProperty(
        name = "75%",
        description = "75%",
        items = [("HMKB75", "HMKB 75", ""),
                ("CYBERBOARD", "CYBERBOARD", "")
        ]
    )
    
    typeTKL : bpy.props.EnumProperty(
        name = "TKL",
        description = "TKL",
        items = [("RWU80A", "RAMAWORKS U80-A", "")
        ]
    )
    
    cables : bpy.props.EnumProperty(
        name = "Type",
        description = "Cable types",
        items = [("KBDhand", "KBDfans Handmade", "")]
    )
    cablecolor : bpy.props.EnumProperty(
        name = "Color",
        description = "Cable types",
        items = [("white","White",""),
        ("lgray","Light Gray",""),
        ("purple","Purple",""),
        ("grayblack","Gray and Black",""),
        ("black","Black",""),
        ("pinkblack","Pink and Black",""),
        ("blueblack","Blue and Black",""),
        ("green","Green",""),
        ("blue","Blue",""),
        ("olive","Olive",""),
        ]
    )
    
    mats : bpy.props.EnumProperty(
        name = "Type",
        description = "Mat types",
        items = [("custom","Custom",""),
        ("kbdbnw","KBD BnW Japanese",""),
        ("topographic","Topographic",""),
        ("gmkart","GMK Art",""),
        ]
    ) 
    
    kbdbnw : bpy.props.EnumProperty(
        name = "Colors",
        description = "Mat types",
        items = [("blacka","Black A",""),
        ("blackb","Black B",""),
        ("blackc","Black C",""),
        ("blackd","Black D",""),
        ("graya","Gray A",""),
        ("grayb","Gray B",""),
        ]
    ) 
    
    topographic : bpy.props.EnumProperty(
        name = "Colors",
        description = "Mat types",
        items = [("bnw","Black and White",""),
        ("bluepurple","Blue and Purple",""),
        ]
    ) 
    
    gmkart : bpy.props.EnumProperty(
        name = "Colors",
        description = "Mat types",
        items = [("bow","Black on White",""),
        ("wob","White on Black",""),
        ]
    ) 
    
    matcolor : bpy.props.FloatVectorProperty(name = "Color", subtype = "COLOR", size=4, min = 0.0, max = 1.0,default=(0.8, 0.8, 0.8, 1.0))
    
    matpic : bpy.props.StringProperty(name= "Image", subtype='FILE_PATH')  
    
    matbool : bpy.props.BoolProperty( name = "from Image", description = "from Image", default = False )
    
    
class KEYERROR_OP_case(Operator):
    bl_idname = "add.case"
    bl_label = "Add Case"
    bl_description = "Adds Case"
    bl_options = {'REGISTER', 'UNDO'}   
    def execute(self, context):
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        assetspg = scene.assets_pg
        
        
        assets.addCase(assets.case())
        
        return {"FINISHED"} 
 
class KEYERROR_OP_copytotop(Operator):
    bl_idname = "copy.totop"
    bl_label = "Set as Layout"
    bl_description = "Sets as Layout"
    bl_options = {'REGISTER', 'UNDO'}  
    def execute(self, context):
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        assetspg = scene.assets_pg
        
        keyb.input_jsonfile = os.path.join(os.path.dirname(__file__), "src/assets/" + assets.case() + ".json")
        
        return {"FINISHED"}    

class KEYERROR_OP_copyscale(Operator):
    bl_idname = "copy.scale"
    bl_label = "Copy Scale"
    bl_description = "Copy Scale"
    bl_options = {'REGISTER', 'UNDO'}  
    def execute(self, context):
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        assetspg = scene.assets_pg
        
        keyb.input_scale = assetspg.casescale
        return {"FINISHED"}   
 
class KEYERROR_OP_cable(Operator):
    bl_idname = "add.cable"
    bl_label = "Add Cable"
    bl_description = "Adds Cable"
    bl_options = {'REGISTER', 'UNDO'}   
    def execute(self, context):
        assets.addCable()
        return {"FINISHED"}         

class KEYERROR_OP_deskmat(Operator):
    bl_idname = "add.deskmat"
    bl_label = "Add Deskmat"
    bl_description = "Adds Deskmat"
    bl_options = {'REGISTER', 'UNDO'}   
    def execute(self, context):
        return {"FINISHED"}     



class KEYERROR_OP_main(Operator):
    bl_idname = "add.keyboard"
    bl_label = "Add Default"
    bl_description = "Adds Keyboard"
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        scene = bpy.context.scene
        keyb = scene.keyboardpg
  
        keyboard.addKeyboard(keyboard.inputSelector())
        
        return {"FINISHED"}     

class KEYERROR_PT_main(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Add Keyboard"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg

        row = layout.row()
        row.prop(keyb, "input_name")
        row = layout.row()
        row.prop(keyb, "input_selector")
        
        if keyb.input_selector == "custom":
            row = layout.row()
            row.prop(keyb, "input_jsonfile")
        
        row = layout.row()
        row.prop(keyb, "input_scale")
        
        row = layout.row()
        row.prop(keyb, "input_rotation")
        
        
        sub = layout.row()
        sub.scale_y = 2
        if keyb.input_selector != "custom":
            sub.enabled = True
        elif os.path.isfile(keyb.input_jsonfile) == True and keyb.input_jsonfile[-4:] == "json":
            sub.enabled = True
        else: 
            sub.enabled = False
        if keyb.legendtype == "uvleg" and keyb.legendfile == "":
            sub.enabled = False
        if keyb.booleancap == False and keyb.booleanswitch == False and keyb.booleanplate == False and keyb.booleancase == False:
            sub.enabled = False
        sub.operator('add.keyboard', icon='IMPORT',text = "Add Keyboard")

class KEYERROR_PT_caps(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = ""
    bl_parent_id = "KEYERROR_PT_main"
    def draw_header(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        row = layout.row()
        row.prop(keyb, "booleancap")
        sub = row.row()
        sub.enabled = keyb.booleancap is True
        if keyb.parenttoswitch == False and keyb.parenttocase == False and keyb.parenttoplate == False:
            sub.prop(keyb, "parenttocap")
    
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.column()
        sub.enabled = keyb.booleancap is True
        row = sub.row()
        split = row.split(factor=0.05)
        c = split.column()
        split = split.split()
        c = split.column()
  
        row = c.row()
        row.prop(keyb, "capprofile")
        
        row = c.row()
        row = c.row()
        row.prop(keyb, "capcolorpreset")
        
        if keyb.capcolorpreset == "custom":
            row = c.row()
            row = c.row()
            row.prop(keyb, "capcolor")

class KEYERROR_PT_legend(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = ""
    bl_parent_id = "KEYERROR_PT_caps"
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        row = layout.row()
        row.enabled = keyb.booleancap is True
        row.prop(keyb, "booleanlegends")
        
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.column()
        sub.enabled = keyb.booleanlegends is True and keyb.booleancap is True
        row = sub.row()
        split = row.split(factor=0.1)
        c = split.column()
        split = split.split()
        c = split.column()
       
        #row = c.row()
        #row.prop(keyb, "legendtype", expand = True)
        
        
        if keyb.legendtype == "uvleg":
            row = c.row()
            row = c.row()
            row = c.row()
            row = c.row()
            row.prop(keyb, "legendfile", icon ='IMAGE_DATA')
        else:
            #row = c.row()
            #row = c.row()
            #row = c.row()
            row = c.row()
            row.prop(keyb, "legendfont")
            row = c.row()
            row = c.row()
            row.prop(keyb, "legendcolorpreset")
            
            if keyb.legendcolorpreset == "custom":
                row = c.row()
                row = c.row()
                row.prop(keyb, "legendcolor")
            row = c.row()
            row = c.row()
            row.prop(keyb, "legendquality")
            
            if keyb.legendquality == True:
                row = c.row()
                row = c.row()
                row.prop(keyb, "legendresolution")

class KEYERROR_PT_switch(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = ""
    bl_parent_id = "KEYERROR_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        row = layout.row()
        row.prop(keyb, "booleanswitch")
        
        sub = row.row()
        
        sub.enabled = keyb.booleanswitch is True
        if keyb.parenttocap == False and keyb.parenttocase == False and keyb.parenttoplate == False:
            sub.prop(keyb, "parenttoswitch")
        
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.column()
        sub.enabled = keyb.booleanswitch is True
        row = sub.row()
        split = row.split(factor=0.05)
        c = split.column()
        split = split.split()
        c = split.column()
        row = c.row()
        row.prop(keyb, "switchsubd", expand = True)
        row = c.row()
        row.prop(keyb, "switchpresets")
        
        if keyb.switchpresets == "custom":
            row = c.row()
            row.prop(keyb, "switchcolorupper")
            row.prop(keyb, "switch")
            row = c.row()
            row.prop(keyb, "switch")
            row.prop(keyb, "switch")
            row = c.row()
            row.prop(keyb, "switch")
            row.prop(keyb, "switch")
            row = c.row()
            row.prop(keyb, "switch")
            
        row = c.row()
        row.prop(keyb, "stabpresets")
        if keyb.stabpresets == "custom":
            row = c.row()
            row.prop(keyb, "stabcolorbase")
            row.prop(keyb, "stabtransbase")
            row = c.row()
            row.prop(keyb, "stabcolorstem")
            row.prop(keyb, "stabtransstem")
            row = c.row()
            row.prop(keyb, "stabcolorbar")
 
class KEYERROR_PT_plate(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = ""
    bl_parent_id = "KEYERROR_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.row()
        sub.enabled = bpy.app.version[0] >= 3 and bpy.app.version[1] >= 2
        sub.prop(keyb, "booleanplate")
        sub = sub.row()
        sub.enabled = keyb.booleanplate is True
        if keyb.parenttoswitch == False and keyb.parenttocase == False and keyb.parenttocap == False:
            sub.prop(keyb, "parenttoplate")
        
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.column()
        sub.enabled = keyb.booleanplate is True
        row = sub.row()
        split = row.split(factor=0.05)
        c = split.column()
        split = split.split()
        c = split.column()
        row = c.row()
        row.prop(keyb, "platecolor")
        row = c.row()
        row.prop(keyb, "platemetallic")
        row = c.row()
        row.prop(keyb, "platerought")
        row = c.row()
        row.prop(keyb, "platetrans")
    
class KEYERROR_PT_case(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = ""        
    bl_parent_id = "KEYERROR_PT_main" 
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.row()
        sub.enabled = bpy.app.version[0] >= 3 and bpy.app.version[1] >= 2
        sub.prop(keyb, "booleancase")
        sub = sub.row()
        sub.enabled = keyb.booleancase is True
        if keyb.parenttoswitch == False and keyb.parenttocap == False and keyb.parenttoplate == False:
            sub.prop(keyb, "parenttocase")
        
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        keyb = scene.keyboardpg
        
        sub = layout.column()
        sub.enabled = keyb.booleancase is True 
        row = sub.row()
        split = row.split(factor=0.05)
        c = split.column()
        split = split.split()
        c = split.column()
        row = c.row()
        row.prop(keyb, "casecolor")
        row = c.row()
        row.prop(keyb, "casemetallic")
        row = c.row()
        row.prop(keyb, "caserought")
    
    
class KEYERROR_PT_assets(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Assets"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        pass
    def draw(self, context):
        layout = self.layout 
        scene = bpy.context.scene
        assets = scene.assets_pg
        
        row = layout.row()
        row.prop(assets,"casescale")
        row.operator("copy.scale",text = "", icon= "COPY_ID", emboss = False)
#cases
#cables
#desksmat
#lighting
#single component

class KEYERROR_PT_cases(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Cases"
    bl_parent_id = "KEYERROR_PT_assets"
    #bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        pass
    def draw(self, context):
        layout = self.layout   
        scene = bpy.context.scene
        assets = scene.assets_pg
        row = layout.row()
        row.prop(assets,"casesize")
        row = layout.row()
        row.prop(assets,assets.casesize)
        row = layout.row()
        row.operator('add.case',text="Add Case")
        row.operator("copy.totop",text="", icon="COPY_ID",emboss=False)

class KEYERROR_PT_cables(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Cables"
    bl_parent_id = "KEYERROR_PT_assets"
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        pass
    def draw(self, context):       
        layout = self.layout   
        scene = bpy.context.scene
        assets = scene.assets_pg
        row = layout.row()
        row.prop(assets,"cables")
        row = layout.row()
        row.prop(assets,"cablecolor")
        row = layout.row()
        row.operator('add.cable',text="Add Cable")

class KEYERROR_PT_mats(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KeyError'    
    bl_label = "Deskmats"
    bl_parent_id = "KEYERROR_PT_assets"
    bl_options = {'DEFAULT_CLOSED'}
    def draw_header(self, context):
        pass
    def draw(self, context):       
        layout = self.layout   
        scene = bpy.context.scene
        assets = scene.assets_pg
        row = layout.row()
        row.prop(assets,"mats")
        if assets.mats == "custom":
            if assets.matbool == False:
                row = layout.row()
                row.prop(assets,"matcolor")
            else:
                row = layout.row()
                row.prop(assets,"matpic")
            row = layout.row()
            row.prop(assets,"matbool")
        else:
            row = layout.row()
            row.prop(assets,assets.mats)
        
        row = layout.row()
        row.operator('add.deskmat',text="Add Deskmat")
                
        
classes = (
            KEYERROR_OP_main,
            #KEYERROR_OP_case,
            #KEYERROR_OP_copytotop,
            #KEYERROR_OP_copyscale,
            #KEYERROR_OP_cable,
            #KEYERROR_OP_deskmat,
            KEYERROR_PT_main,
            KEYERROR_PT_caps,
            KEYERROR_PT_legend,
            KEYERROR_PT_switch,
            KEYERROR_PT_plate,
            KEYERROR_PT_case,
            #KEYERROR_PT_assets,
            #KEYERROR_PT_cases,
            #KEYERROR_PT_cables,
            #KEYERROR_PT_mats,
            KEYERROR_PG_keyboard,
            #KEYERROR_PG_assets,
        )
        
def menu_func(self, context):
    self.layout.operator(AddKeyboard.bl_idname)

def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.keyboardpg = bpy.props.PointerProperty(type= KEYERROR_PG_keyboard)
    #bpy.types.Scene.assets_pg = bpy.props.PointerProperty(type= KEYERROR_PG_assets)
    
def unregister(): 
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.keyboardpg
    #del bpy.types.Scene.assets_pg
    print ("UnRegistred!")

if __name__ == "__main__":
    register()