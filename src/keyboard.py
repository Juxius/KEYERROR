import bpy
import os
import json
import time
import numpy
from mathutils import Matrix, Vector
from math import cos, sin ,radians ,pi
import presets
from . import load


def addKeyboard(file):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    keyb = scene.keyboardpg
    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    
    #collection names
    collections = [
    keyb.input_name + " Caps" , keyb.input_name + " Legends" , keyb.input_name + " Switches" , keyb.input_name + " Case"
    ]
    
    #define vars 
    addedKEYCAPS = []
    addedCARACTERS = []
    addedSWITCHES = []
    enabled = []
    
    #prepare scene
    bpy.context.space_data.overlay.show_relationship_lines = False#

    with open(file, 'r') as f:
        textinput = json.load(f) 

    #add main collection
    if not bpy.context.scene.collection.children.get( keyb.input_name ):    
        maincoll = data.collections.new( keyb.input_name )
        bpy.context.scene.collection.children.link(maincoll)
    else:
        maincoll = bpy.context.scene.collection.children.get(keyb.input_name)
    
    if keyb.booleancap == True: enabled.append(collections[0])
    if keyb.booleanlegends == True: enabled.append(collections[1])
    if keyb.booleanswitch == True: enabled.append(collections[2])
    if keyb.booleanplate == True or keyb.booleancase == True : enabled.append(collections[3])
    
    for coll in collections:
        if data.collections.get(coll):
            subcoll = data.collections[coll]
            delmeshes = set()
            delfont = set()
            for mesh in [o for o in subcoll.objects if o.type == 'MESH']:
                delmeshes.add( mesh.data )
                datao.remove( mesh )
            for font in [o for o in subcoll.objects if o.type == 'FONT']:
                delfont.add( font.data )
                datao.remove( font )

            for mesh in [m for m in delmeshes if m.users == 0]:
                data.meshes.remove( mesh )
            for font in [m for m in delfont if m.users == 0]:
                data.curves.remove( font )
                
            data.collections.remove(subcoll)
       
    #create main collection
    if not bpy.context.scene.collection.children.get( keyb.input_name ):    
        maincoll = data.collections.new( keyb.input_name )
        bpy.context.scene.collection.children.link(maincoll)
    else:
        maincoll = data.collections[ keyb.input_name ]

    for coll in enabled:
        if maincoll and not data.collections.get( coll ):
            subcoll = data.collections.new( coll )
            maincoll.children.link(subcoll)
        if coll == keyb.input_name + " Caps" and len(enabled) > 1 and enabled[1] == keyb.input_name + " Legends":
            subsubcoll = data.collections.new( enabled[1] )
            subcoll.children.link(subsubcoll)
            enabled.pop(1) 
    

    keyboard = load.load(file)
    platewidth = 0
    plateheight = 0
    vertices = []
    for key in keyboard:
        if keyb.booleancap == True:
            addedKEYCAPS.append( linkkeycaps ( key ))
        
        if keyb.booleanlegends == True and keyb.legendtype == "objleg":
            addedCARACTERS + addLegend( key )
            
        if keyb.booleanswitch == True:
            #addedSWITCHES + linkswitch( key )
            addedSWITCHES.append(linkswitch( key ))

        if keyb.booleanplate == True:
            vertices += [((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009, -(key.y + (key.h - 1) * 0.5 ) * 0.019  , -0.006)]
            
            if key.w >= 2 and key.w <= 6: 
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009) - 0.01195, -key.y * 0.019  , -0.012)]
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009) + 0.01195, -key.y * 0.019  , -0.012)]
            elif key.w > 6:
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009) - 0.0498, -key.y * 0.019  , -0.012)]
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009) + 0.0498, -key.y * 0.019  , -0.012)]
            if key.h >= 2:
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009), -(key.y + (key.h - 1) * 0.5 ) * 0.019 - 0.01195  , 0)]
                vertices += [(((key.x + (key.w - 1) * 0.5 ) * 0.019 + 0.009), -(key.y + (key.h - 1) * 0.5 ) * 0.019 + 0.01195  , 0)]
        
        

        if platewidth < key.x + key.w:
            platewidth = key.x + key.w
        if plateheight < key.y + key.h:
            plateheight = key.y + key.h
  
    scale = tuple([keyb.input_scale] * 3)
    if keyb.booleanplate == True:
        
        #import plate geometry nodes
        if not bpy.data.node_groups.get(keyb.input_name + "_Plate_Nodes"):
            with data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.node_groups = ["PLATE_NODES"]
            bpy.data.node_groups["PLATE_NODES"].name = keyb.input_name + "_Plate_Nodes"
        
        #material
        if not datam.get(keyb.input_name + " Plate"):
            platemat = addMaterial(keyb.input_name + " Plate", keyb.platecolor , keyb.platerought , keyb.platemetallic , keyb.platetrans , 0.2 , 0.045)
        else:
            platemat = bpy.data.materials[keyb.input_name + " Plate"]
            platemat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = keyb.platerought
            platemat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = keyb.platemetallic
            platemat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = keyb.platecolor
            platemat.node_tree.nodes["Principled BSDF"].inputs["Transmission"].default_value = keyb.platetrans
            
        faces = []
        edges = []
        
        pointmesh = bpy.data.meshes.new('new_mesh')
        pointmesh.from_pydata(vertices, edges, faces)
        pointmesh.update()
        # make object from mesh
        new_object = bpy.data.objects.new(keyb.input_name + " Plate", pointmesh)
        # make collection
        
        nodegroup = bpy.data.node_groups[keyb.input_name + "_Plate_Nodes"]
        geonodes = new_object.modifiers.new("Plate", "NODES")
        
        delnode = new_object.modifiers["Plate"].node_group
        bpy.data.node_groups.remove(delnode)
        geonodes.node_group = nodegroup
        nodegroup.nodes["INPUT_X"].outputs[0].default_value = platewidth 
        nodegroup.nodes["INPUT_Y"].outputs[0].default_value = plateheight 
        nodegroup.nodes["Transform"].inputs["Translation"].default_value = (0,0,-0.0061)
        bevel = new_object.modifiers.new("Bevel", "BEVEL")
        bevel.use_clamp_overlap = False
        bevel.width = 0.0001
        
        nodegroup.nodes["Set Material"].inputs[2].default_value = platemat
        
        new_object.data.materials.append(platemat)
        origin = Vector((platewidth * 0.5 * 0.019 - 0.0005, -(plateheight - 1) * 0.5 * 0.019, 0))
        new_object.data.transform(Matrix.Translation(-origin))
        
        collection = bpy.data.collections[ collections[3] ]
        collection.objects.link(new_object)
        if keyb.parenttocap == False and keyb.parenttoswitch == False and keyb.parenttoplate == False and keyb.parenttocase == False:
            new_object.scale = scale
            new_object.rotation_euler = (keyb.input_rotation, 0, 0)           
    if keyb.booleancase == True:
        
        #import case geometry nodes
        if not bpy.data.node_groups.get(keyb.input_name + "_Case_Nodes") and keyb.booleancase == True:
            with data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.node_groups = ["CASE_NODES"]
            bpy.data.node_groups["CASE_NODES"].name = keyb.input_name + "_Case_Nodes"    
        
        #material 
        if not datam.get(keyb.input_name + " Case"):
            casemat = addMaterial(keyb.input_name + " Case" , keyb.casecolor , keyb.caserought , keyb.casemetallic , 0 , 0 , 0.045)
        else:
            casemat = bpy.data.materials[keyb.input_name + " Case"]
            casemat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = keyb.caserought
            casemat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = keyb.casemetallic
            casemat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = keyb.casecolor
        
        faces = []
        edges = []
        vertices = [(0,0,0)]
        #print(vertices)
        pointmesh = bpy.data.meshes.new('Case')
        pointmesh.from_pydata(vertices, edges, faces)
        pointmesh.update()
        # make object from mesh
        new_object = bpy.data.objects.new(keyb.input_name + " Case", pointmesh)
        # make collection

        nodegroup = bpy.data.node_groups[keyb.input_name + "_Case_Nodes"]
        geonodes = new_object.modifiers.new("Case", "NODES")
        
        delnode = new_object.modifiers["Case"].node_group
        bpy.data.node_groups.remove(delnode)
        
        geonodes.node_group = nodegroup
        nodegroup.nodes["INPUT_X"].outputs[0].default_value = platewidth
        nodegroup.nodes["INPUT_Y"].outputs[0].default_value = plateheight
        nodegroup.nodes["INPUT_ANGLE"].outputs[0].default_value = keyb.input_rotation
        nodegroup.nodes["Set Material"].inputs[2].default_value = casemat
       
        new_object.data.materials.append(casemat)
        
        collection = bpy.data.collections[collections[3]]
        collection.objects.link(new_object)

        if True in {keyb.parenttocap, keyb.parenttoswitch, keyb.parenttoplate, keyb.parenttocase}: pass
        else:    
            new_object.scale = scale
            new_object.rotation_euler = (keyb.input_rotation, 0, 0)
 
    origin = Vector((platewidth * 0.5 * 0.019 - 0.0005, -(plateheight - 1) * 0.5 * 0.019, 0))
    
    
    #keycap join ----------------------------------------------------------------------------------------
    if keyb.booleancap == True:
        
        #adds all objs to list 
        meshescaps = []
        collection = data.collections[keyb.input_name + " Caps"]
        for obj in [o for o in collection.objects if o.type == 'MESH']:
            meshescaps.append( obj )
        #joins all obj in list by creating a copy of the scene and joining them there (copy is only temporary)
        ctx = bpy.context.copy()
        ctx['active_object'] = meshescaps[0]
        ctx['selected_editable_objects'] = meshescaps
        bpy.ops.object.join(ctx)
        
        #sets obj as the first obj in the caps collection and the name 
        obj = data.collections[keyb.input_name + " Caps"].objects[0]
        obj.name = keyb.input_name + " Caps"

        #removes all orphan meshes
        for mesh in [m for m in addedKEYCAPS if m.users == 0]:
            data.meshes.remove( mesh )


        #set obj origin to center of geometry
        obj.data.transform(Matrix.Translation(-origin))
      
        if keyb.parenttocap == False and keyb.parenttoswitch == False and keyb.parenttoplate == False and keyb.parenttocase == False:
            obj.scale = scale
            obj.rotation_euler = (keyb.input_rotation, 0, 0)

    #Shrinkwrap legends        
    if keyb.booleanlegends == True and keyb.legendtype == "objleg":
        collection =  data.collections[keyb.input_name + " Legends"] 
        for subobj in [o for o in collection.objects if o.type == 'FONT' or o.type == 'MESH']:
            subobj.location -= Vector(origin)
            if keyb.booleancap == True:
                subobj.parent = obj
                subobj.modifiers["Shrinkwrap"].target = obj
    
    #switches join 
    if keyb.booleanswitch == True:
        #adds all switches to list 
        meshesswitch = []
        dataswitch = []
        collection = data.collections[keyb.input_name + " Switches"]
        for swobj in [o for o in collection.objects if o.type == 'MESH']:
            meshesswitch.append( swobj )
            dataswitch.append(swobj.data)
        #joins all switches in list by creating a copy of the scene and joining them there (copy is only temporary)
        ctx = bpy.context.copy()
        ctx['active_object'] = meshesswitch[0]
        ctx['selected_editable_objects'] = meshesswitch
        bpy.ops.object.join(ctx)
        
        swobj = data.collections[keyb.input_name + " Switches"].objects[0]
        swobj.name = keyb.input_name + " Switches"
        for mesh in [m for m in dataswitch if m.users == 0]:
            data.meshes.remove( mesh )
            
        origin[0] -= 0.009
        origin[2] -= 0.005
        swobj.data.transform(Matrix.Translation(-origin))
        swobj.location = (0,0,0)
        origin = Vector((platewidth * 0.5 * 0.019 - 0.0005, -(plateheight - 1) * 0.5 * 0.019, 0))
        
        if keyb.parenttocap == False and keyb.parenttoswitch == False and keyb.parenttoplate == False and keyb.parenttocase == False:
            swobj.scale = scale
            swobj.rotation_euler = (keyb.input_rotation, 0, 0)
    
    #----------------------------PARENTING-------------------------------------
    if keyb.booleancap == True or keyb.booleanswitch == True or keyb.booleanplate == True or keyb.booleancase == True:
        if keyb.parenttocap == True:
            mainobj = bpy.data.objects[keyb.input_name + " Caps"]
            if keyb.booleanswitch == True:
                swobj.parent = mainobj
            if keyb.booleanplate == True:
                plateobj = bpy.data.objects[keyb.input_name + " Plate"]
                plateobj.parent = mainobj
                #bpy.data.node_groups[keyb.input_name + "_Plate_Nodes"].nodes["Transform"].inputs["Translation"].default_value = (0,0.0095,-0.0061)
            if keyb.booleancase == True:
                caseobj = bpy.data.objects[keyb.input_name + " Case"]
                caseobj.parent = mainobj
            mainobj.scale = scale
            mainobj.rotation_euler = (keyb.input_rotation, 0, 0)
            mainobj.location = bpy.context.scene.cursor.location
            
        elif keyb.parenttoswitch == True:  
            mainobj = bpy.data.objects[keyb.input_name + " Switches"]
            if keyb.booleancap == True:
                obj.parent = mainobj
            if keyb.booleanplate == True:
                plateobj = bpy.data.objects[keyb.input_name + " Plate"]
                plateobj.parent = mainobj
                #bpy.data.node_groups[keyb.input_name + "_Plate_Nodes"].nodes["Transform"].inputs["Translation"].default_value = (0,0.0095,-0.0061)
            if keyb.booleancase == True:
                caseobj = bpy.data.objects[keyb.input_name + " Case"]
                caseobj.parent = mainobj 
            mainobj.scale = scale
            mainobj.rotation_euler = (keyb.input_rotation, 0, 0)
            mainobj.location = bpy.context.scene.cursor.location
            
        elif keyb.parenttoplate == True:
            mainobj = bpy.data.objects[keyb.input_name + " Plate"]
            if keyb.booleanswitch == True:
                swobj.parent = mainobj
            if keyb.booleancap == True:
                obj.parent = mainobj
            if keyb.booleancase == True:
                caseobj = bpy.data.objects[keyb.input_name + " Case"]
                caseobj.parent = mainobj
            #bpy.data.node_groups[keyb.input_name + "_Plate_Nodes"].nodes["Transform"].inputs["Translation"].default_value = (0,0.0095,-0.0061)
            mainobj.scale = scale
            mainobj.rotation_euler = (keyb.input_rotation, 0, 0)
            mainobj.location = bpy.context.scene.cursor.location
            
        elif keyb.parenttocase == True:
            mainobj = bpy.data.objects[keyb.input_name + " Case"]
            if keyb.booleanswitch == True:
                swobj.parent = mainobj
            if keyb.booleanplate == True:
                plateobj = bpy.data.objects[keyb.input_name + " Plate"]
                plateobj.parent = mainobj
                #bpy.data.node_groups[keyb.input_name + "_Plate_Nodes"].nodes["Transform"].inputs["Translation"].default_value = (0,0.0095,-0.0061)
            if keyb.booleancap == True:
                obj.parent = mainobj
            mainobj.scale = scale
            mainobj.rotation_euler = (keyb.input_rotation, 0, 0)
            mainobj.location = bpy.context.scene.cursor.location

def genUV():
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    keyb = scene.keyboardpg
    
    
    
    name = keyb.input_name + "_Cap_Material"
    
    legends = pictureSelector()
  
    obj = data.collections[keyb.input_name + " Caps"].objects[0]
    
    #add png to node
    if legends != "":
    
        shadernode = datam[name].node_tree.nodes["Principled BSDF"]
        mixnode = datam[name].node_tree.nodes["Mix"]
        datam[name].node_tree.links.new(mixnode.outputs["Color"], shadernode.inputs[0])
    
        new_img = data.images.load(legends)
        obj.material_slots[0].material.node_tree.nodes["template"].image = new_img
    
    # --------------
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    
    bpy.context.view_layer.objects.active = obj
    bpy.context.active_object.select_set(True)

    
    #uvunwrap
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group='UVGroup')
    bpy.ops.object.vertex_group_select()
    bpy.ops.uv.cube_project(cube_size=8,correct_aspect=True,scale_to_bounds=True) # 1.82s
    
    
    
    #scale other uv 0
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group='MaterialGroup')
    bpy.ops.object.vertex_group_select()
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.select_more()
    bpy.context.area.ui_type = 'UV'
    bpy.ops.uv.select_all(action='SELECT')
    bpy.context.space_data.cursor_location[1] = 0.9
    
    bpy.ops.uv.snap_selected(target='CURSOR')        # single: 1.36 block:1.84s
    
    #cleanup
    bpy.context.area.ui_type = 'VIEW_3D'
    bpy.ops.object.editmode_toggle()

def inputSelector():
    scene = bpy.context.scene
    keyb = scene.keyboardpg
    
    preset = {
      "ansi40" : os.path.join(os.path.dirname(__file__), "presets/ansi40.json"), 
      "ansi60" : os.path.join(os.path.dirname(__file__), "presets/ansi60.json"),
      "ansi104" : os.path.join(os.path.dirname(__file__), "presets/ansi104.json"),
      "iso60" : os.path.join(os.path.dirname(__file__), "presets/iso60.json"),
      "iso105" : os.path.join(os.path.dirname(__file__), "presets/iso105.json")
    }
    
    if keyb.input_selector != "custom":
        output = preset[keyb.input_selector]
    else:
        output = keyb.input_jsonfile
    return output

def linkkeycaps( key ):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    keyb = scene.keyboardpg
        
    if keyb.capprofile == "cherry":
        obj_name = str(keyb.capprofile) + "_" + str(key.p) + "_high" 
    else: 
        obj_name = str(keyb.capprofile) + "_" + str(key.p) + "_" + str(key.w) + "," + str(key.h)
    obj_name = ''.join(obj_name.split())

    if key.w2 == 1.5:
        obj_name = "cherry_IsoEnter_high"
        key.x -= 0.25
    elif key.w2 == 2.25:
        obj_name = "cherry_BigEnter"
    elif key.w2 == 1.75:
        obj_name = "cherry_steppedCaps"

    #add materials if not already present
    if keyb.capcolorpreset == "preset":
        colorname = key.c
        color = hex_to_rgb(int(key.c.replace("#","0x"), 16))
    elif keyb.capcolorpreset == "custom":
        colorname = srgb_to_hex(linsrgb_to_srgb(keyb.capcolor))
        color = keyb.capcolor
    else: 
        colorname = keyb.capcolorpreset 
        color = hex_to_rgb(int(keyb.capcolorpreset.replace("#","0x"), 16))

    if not datam.get(keyb.input_name + "_Cap_Material" + colorname):
        plastic = addMaterial(keyb.input_name + "_Cap_Material" + colorname , color , 0.25 , 0 , 0 , 0 , 0)
        bump = plastic.node_tree.nodes.new("ShaderNodeBump")
        bump.inputs[1].default_value = 0.0001 * keyb.input_scale
        bump.inputs[0].default_value = 0.5
        noise = plastic.node_tree.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 10000
        coord = plastic.node_tree.nodes.new("ShaderNodeTexCoord")
        plastic.node_tree.links.new(bump.outputs[0], plastic.node_tree.nodes["Principled BSDF"].inputs["Normal"])
        plastic.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
        plastic.node_tree.links.new(coord.outputs["Object"], noise.inputs["Vector"])
    else:
        plastic = datam[keyb.input_name + "_Cap_Material" + colorname]

    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    if not bpy.context.scene.objects.get(obj_name):
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.objects = [obj_name]

        for obj in data_to.objects:
            if obj is not None:
                data.collections[keyb.input_name + " Caps"].objects.link(obj)
                
                obj.name = str(key.x) + " " + str(key.y)
                
                #scale keycaps key.w/key.h
                if key.w > 1 and keyb.capprofile == "cherry" and key.w2 == 0: 
                    for v in obj.data.vertices:
                        if v.co[0] > 0.013:
                            v.co[0] += (key.w - 1 ) * 0.019
                        elif v.co[0] > 0.012:
                            v.co[0] += (key.w - 1 ) * (0.019 / (1 + 1/3) )
                        elif v.co[0] > 0.006:
                            v.co[0] += (key.w - 1 ) * (0.019 / 2 )
                        elif v.co[0] > 0.005:
                            v.co[0] += (key.w - 1 ) * (0.019 / 4 )
                
                if key.h > 1 and keyb.capprofile == "cherry" and key.w2 == 0: 
                        for v in obj.data.vertices:
                            if v.co[1] < -0.003:
                                v.co[1] -= (key.h - 1 ) * 0.019
                            elif v.co[1] < 0.003:
                                v.co[1] -= (key.h - 1 ) * (0.019 / 2 )
                
                obj.location = bpy.context.scene.cursor.location
                loc = ((key.x * 0.019),-(key.y * 0.019), 0)
                obj.data.transform(Matrix.Translation(loc))
                
                if key.r != 0:
                    #set origin to rotorigin
                    obj.location[0] =  key.rx * 0.019
                    obj.location[1] = -(key.ry + 0.5) * 0.019
                    obj.data.transform(Matrix.Rotation(-radians(key.r), 4, 'Z'))
                    print(key.rx)
                    print(key.rx + 0.5)

                obj.data.materials.append(plastic) 
    
    #double shot 
    if keyb.booleanlegends == True:

        if keyb.legendcolorpreset == "preset":
            legendcolorname = key.lc
            legendcolor = hex_to_rgb(int(key.lc.replace("#","0x"), 16))
        elif keyb.legendcolorpreset == "custom":
            legendcolorname = srgb_to_hex(linsrgb_to_srgb(keyb.legendcolor))
            legendcolor = keyb.legendcolor
        else: 
            legendcolorname = keyb.legendcolorpreset 
            legendcolor = hex_to_rgb(int(keyb.legendcolorpreset.replace("#","0x"), 16))

        if not datam.get(keyb.input_name + "_Legend_Material" + str(legendcolorname)) :
            plastic = addMaterial(keyb.input_name + "_Legend_Material" + str(legendcolorname) , legendcolor , 0.25 , 0 , 0 , 0 , 0)
            bump = plastic.node_tree.nodes.new("ShaderNodeBump")
            bump.inputs[1].default_value = 0.0001 * keyb.input_scale
            bump.inputs[0].default_value = 0.5
            noise = plastic.node_tree.nodes.new("ShaderNodeTexNoise")
            noise.inputs["Scale"].default_value = 10000
            coord = plastic.node_tree.nodes.new("ShaderNodeTexCoord")
            plastic.node_tree.links.new(bump.outputs[0], plastic.node_tree.nodes["Principled BSDF"].inputs["Normal"])
            plastic.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
            plastic.node_tree.links.new(coord.outputs["Object"], noise.inputs["Vector"])
        else:
            plastic = datam[keyb.input_name + "_Legend_Material" + str(legendcolorname)]
        
        obj.data.materials.append(plastic) 
    
        for p in obj.data.polygons:
            count = 0
            for v in p.vertices:
                for g in obj.data.vertices[v].groups:
                    if g.group == 2:
                        count += 1
            if count > 3:
                p.material_index = 1
            else:
                p.material_index = 0
    if obj is not None:
        return obj.data

def addLegend(key):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    keyb = scene.keyboardpg
    
    added = []
    for pos, label in enumerate(key.labels):
        if label.text != "":
            name = keyb.input_name + "_L_" + str(key.x) + "_" + str(key.y) + "_" + str(label.text) + "_" + str(pos)
            filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
            if not bpy.context.blend_data.fonts.get(keyb.legendfont):
                with data.libraries.load(filepath, link=False) as (data_from, data_to):
                    data_to.fonts = [keyb.legendfont]

            loadedfont = data.fonts[keyb.legendfont]

            curve_obj = data.curves.new(type="FONT", name=name)
            curve_obj.body = label.text

            curve_obj.font = loadedfont
            curve_obj.size = label.size * 0.001 
            font_obj = datao.new(name=name, object_data=data.curves[name])
            data.collections[keyb.input_name + " Legends"].objects.link(font_obj)
            
            font_obj.location[0] += key.x * 0.019
            font_obj.location[1] -= key.y * 0.019 
            font_obj.location[2] += 0.017 
            
            if keyb.legendquality == True:
                solidify = font_obj.modifiers.new("Solidify","SOLIDIFY")
                solidify.thickness = 0.0001
                remesh = font_obj.modifiers.new("Remesh","REMESH")
                remesh.mode = 'SHARP'
                remesh.octree_depth = keyb.legendresolution
                remesh.use_remove_disconnected = False

            shrinkwrap = font_obj.modifiers.new("Shrinkwrap","SHRINKWRAP")
            shrinkwrap.wrap_method = 'PROJECT'
            shrinkwrap.use_project_z = True
            shrinkwrap.use_project_x = False
            shrinkwrap.use_negative_direction = True
            shrinkwrap.use_positive_direction = False
            shrinkwrap.offset = 0.00001 

            if keyb.capprofile == "cherry":
                texttransform = (0.004,0.0079,0.0014,-0.0037,1.25,1.4)
            elif keyb.capprofile == "dsa":
                texttransform = (0.004,0.0053,0,0.0035,1.1,1.4)
            elif keyb.capprofile == "sa":
                texttransform = (0.004,0.0053,0,0.0035,1.1,1.4)
            
            if pos in {0, 1, 2}:
                curve_obj.align_y = "TOP"
                font_obj.location[1] += texttransform[1]
            if pos in {3, 4, 5}:
                curve_obj.align_y = "CENTER"
                font_obj.location[1] += texttransform[2]
                font_obj.location[1] -= (key.h - 1) * 0.0095  
            if pos in {6, 7, 8}:
                font_obj.location[1] += texttransform[3]
                font_obj.location[1] -= (key.h - 1) * 0.019  
            if pos in {0, 3, 6}:
                font_obj.location[0] += 0.004
            
            if pos in {1, 4, 7}:
                curve_obj.align_x = "CENTER"
                font_obj.location[0] += 0.009 + (key.w - 1) * 0.0095
            if pos in {2, 5, 8}:
                curve_obj.align_x = "RIGHT"
                font_obj.location[0] += 0.014 + (key.w - 1) * 0.019
            
            if key.w2 > 1:
                font_obj.location[0] += 0.00475

            #material
            if keyb.legendcolorpreset == "preset":
                colorname = key.lc
                color = hex_to_rgb(int(key.lc.replace("#","0x"), 16))
            elif keyb.legendcolorpreset == "custom":
                colorname = srgb_to_hex(linsrgb_to_srgb(keyb.legendcolor))
                color = keyb.legendcolor
            else: 
                colorname = keyb.legendcolorpreset 
                color = hex_to_rgb(int(keyb.legendcolorpreset.replace("#","0x"), 16))

            if not datam.get(keyb.input_name + "_Legend_Material" + colorname):
                plastic = addMaterial(keyb.input_name + "_Legend_Material" + colorname , color , 0.25 , 0 , 0 , 0 , 0)
                bump = plastic.node_tree.nodes.new("ShaderNodeBump")
                bump.inputs[1].default_value = 0.0001 * keyb.input_scale
                bump.inputs[0].default_value = 0.5
                noise = plastic.node_tree.nodes.new("ShaderNodeTexNoise")
                noise.inputs["Scale"].default_value = 10000
                coord = plastic.node_tree.nodes.new("ShaderNodeTexCoord")
                plastic.node_tree.links.new(bump.outputs[0], plastic.node_tree.nodes["Principled BSDF"].inputs["Normal"])
                plastic.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
                plastic.node_tree.links.new(coord.outputs["Object"], noise.inputs["Vector"])
                
            else:
                plastic = datam[keyb.input_name + "_Legend_Material" + colorname]

            font_obj.data.materials.append(plastic) 
            
            added.append(font_obj.data)
    return added

def linkswitch( key):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    keyb = scene.keyboardpg
    
    added = []

    if keyb.switchsubd == "lowpoly":
        obj_name = "mxswitch_lowpoly"
    else:
        obj_name = "mxswitch"

    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")

    link = False
    
    
    if not bpy.context.scene.objects.get(obj_name):
        with data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.objects = [obj_name]


        #link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                data.collections[keyb.input_name + " Switches"].objects.link(obj)
                
                obj.location = bpy.context.scene.cursor.location
                origin = ((key.x * 0.019 + (key.w * 0.0095) - 0.0095),(key.y * -0.019 + 0.0095 - 0.0095 * key.h), 0)
                obj.data.transform(Matrix.Translation(origin))
                
                obj.name = "S" + str(key.x) + " " + str(key.y)

                if key.w2 > 1:
                    obj.data.transform(Matrix.Translation((0.0048,0.0008, 0)))

    if not datam.get("switch_base") and not datam.get(keyb.input_name + "_Switch_Base"):
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["switch_base"]
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["switch_upper"]
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["switch_stem"]
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["switch_pins"]
    if datam.get("switch_base"):
        materials = ("switch_upper","switch_base","switch_stem","switch_pins")
        for mat in materials:
            mater = datam[mat]
            mat = mat[7:].capitalize()
            mater.name = keyb.input_name + "_Switch_" + mat
        materials = (keyb.input_name + "_Switch_Upper",keyb.input_name + "_Switch_Base",keyb.input_name + "_Switch_Stem",keyb.input_name + "_Switch_Pins")
    else:
        materials = (keyb.input_name + "_Switch_Upper",keyb.input_name + "_Switch_Base",keyb.input_name + "_Switch_Stem",keyb.input_name + "_Switch_Pins")
    
    for mat in materials:
        mater = datam[mat]
        obj.data.materials.append(mater)
        mater.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = switchcolor(mat[-5:])
        mater.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = switchtrans(mat[-5:])
        
    #if keyb.uppertrans == True and keyb.switchpresets == "custom":
    #    obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1
    #if keyb.basetrans == True and keyb.switchpresets == "custom":  
    #    obj.data.materials[1].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1
    #if keyb.stemtrans == True and keyb.switchpresets == "custom":  
    #    obj.data.materials[2].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1xoffset
    
    o = datao["S" + str(key.x) + " " + str(key.y)]
    for p in o.data.polygons:
        verts_vertexGroups = [ g.group for v in p.vertices for g in o.data.vertices[ v ].groups ]
        
        counts    = [ verts_vertexGroups.count( idx ) for idx in verts_vertexGroups ]
        modeIndex = counts.index( max( counts ) )
        mode      = verts_vertexGroups[ modeIndex ]
        
        groupName = o.vertex_groups[ mode ].name
        groupName = groupName[7:].capitalize()
        groupName = keyb.input_name + "_Switch_" + groupName
        
        ms_index = o.material_slots.find( groupName  )
        
        if ms_index != -1: # material found
            p.material_index = ms_index
    added.append( obj.data )


    if key.w >= 2 or key.h >= 2:
        sobj = obj
        obj_name = "stabilizer"
        if not bpy.context.scene.objects.get(obj_name):
            with data.libraries.load(filepath, link=link) as (data_from, data_to):
                data_to.objects = [obj_name]
                
            for obj in data_to.objects:
                if obj is not None:
                    data.collections[keyb.input_name + " Switches"].objects.link(obj)
                    cursor = bpy.context.scene.cursor.location
                    obj.location = cursor
                    if key.w > 6:
                        for v in obj.data.vertices:
                            if v.co[0] < cursor[0]:
                                v.co[0] -= 0.03785
                            else:
                                v.co[0] += 0.03785
                    if key.h >= 2:
                        obj.data.transform(Matrix.Rotation(pi/2, 4, 'Z'))
                    else:
                        obj.data.transform(Matrix.Rotation(pi, 4, 'Z'))
                    origin = ((key.x * 0.019 + (key.w * 0.0095) - 0.0095),(key.y * -0.019 + 0.0095 - 0.0095 * key.h), 0)
                    obj.data.transform(Matrix.Translation(origin))
                    obj.name = "St" + str(key.x) + " " + str(key.y) 
        if key.w2 > 1:
             obj.data.transform(Matrix.Translation((0.0048,0.0008, 0)))

        if not datam.get("stab_base") and not datam.get(keyb.input_name + "_Stab_BaseS"):
            with data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.materials = ["stab_base"]
            with data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.materials = ["stab_stem"]
            with data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.materials = ["stab_metal"]
        if datam.get("stab_base"):
            materials = ("stab_base","stab_stem","stab_metal")
            for mat in materials:
                mater = datam[mat]
                mat = mat[5:].capitalize()
                mater.name = keyb.input_name + "_Stab_" + mat + "S"
            materials = (keyb.input_name + "_Stab_BaseS",keyb.input_name + "_Stab_StemS",keyb.input_name + "_Stab_MetalS")
        else:
            materials = (keyb.input_name + "_Stab_BaseS",keyb.input_name + "_Stab_StemS",keyb.input_name + "_Stab_MetalS")
        
        for mat in materials:
            mater = datam[mat]
            obj.data.materials.append(mater)
            mater.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = switchcolor(mat[-5:])
            mater.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = switchtrans(mat[-5:])
 
        for p in obj.data.polygons:
            for v in p.vertices:
                for g in obj.data.vertices[v].groups:
                    if g.group == 0:
                        p.material_index = 0
                    if g.group == 1:
                        p.material_index = 1
                    if g.group == 2:
                        p.material_index = 2
        return sobj.data
    return obj.data

def pictureSelector():
    scene = bpy.context.scene
    keyb = scene.keyboardpg
    
    preset = {
      "ansi40" : os.path.join(os.path.dirname(__file__), "presets/ansi40preset.png"), 
      "ansi60" : os.path.join(os.path.dirname(__file__), "presets/ansi60preset.png"),
      "ansi104" : ""
    }
    
    if keyb.legendfile != "" :
        output = keyb.legendfile
    else:
        output = preset[keyb.input_selector]
        
    return output

def switchcolor(part):
    #print(part)
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    keyb = scene.keyboardpg
    
    if keyb.switchpresets == "custom":
        custom = {
        "Upper" : keyb.switchcolorupper,
        "_Base" : keyb.switchcolorbase,
        "_Stem" : keyb.switchcolorstem,
        "_Pins" : keyb.switchcolorpins,
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            return custom[part]
        
    if keyb.stabpresets == "custom":
        custom = {
        "BaseS" : keyb.stabcolorbase,
        "StemS" : keyb.stabcolorstem,
        "etalS" : keyb.stabcolorbar,
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            pass
        else:
            return custom[part]
            
    if keyb.switchpresets != "custom":
        presets = {
        "cherryred" : {"Upper" : (0,0,0,1),
                        "_Base" : (0,0,0,1),
                        "_Stem" : (0.5,0,0,1),
                        "_Pins" : (0.5,0.2,0.1,1)
                        },
        "gateronyellow" : {"Upper" : (1,1,1,1),
                        "_Base" : (1,1,1,1),
                        "_Stem" : (1,0.7,0.1,1),
                        "_Pins" : (0.5,0.2,0.1,1)
                        },
        "keebwerkbushi" : {"Upper" : (0.6,0.02,0.02,1),
                        "_Base" : (0.03,0.03,0.1,1),
                        "_Stem" : (0.8,0.8,0.8,1),
                        "_Pins" : (0.5,0.2,0.1,1)
                        },
        "tecseepurppand" : {"Upper" : (0.2,0.14,0.4,1),
                        "_Base" : (0.2,0.14,0.4,1),
                        "_Stem" : (0.8,0.8,0.8,1),
                        "_Pins" : (0.5,0.2,0.1,1)
                        },                
        }
        
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            return presets[keyb.switchpresets][part]
    
    if keyb.stabpresets != "custom":
        presets = {
        "bblack" : {"BaseS" : (0,0,0,1),
                        "StemS" : (0,0,0,1),
                        "etalS" : (0.8,0.8,0.8,1)
                        },         
        "btransparent" : {"BaseS" : (0.9,0.9,0.9,1),
                        "StemS" : (0.9,0.9,0.9,1),
                        "etalS" : (0.8,0.8,0.8,1)},    
        "studiorx78gold" : {"BaseS" : (0.2,0.5,1,1),
                        "StemS" : (1,0.3,0.2,1),
                        "etalS" : (1,0.5,0.2,1)},                    
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            pass
        else:
            return presets[keyb.stabpresets][part]

def switchtrans(part):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials

    keyb = scene.keyboardpg
    
    upper = keyb.switchtransupper
    base = keyb.switchtransbase
    stem = keyb.switchtransstem
    baseS = keyb.stabtransbase
    stemS = keyb.stabtransstem
    
    if keyb.switchpresets == "custom":
        
        custom = {
        "Upper" : upper,
        "_Base" : base,
        "_Stem" : stem,
        "_Pins" : 0,
        "BaseS" : baseS,
        "StemS" : stemS,
        "etalS" : 0
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            return custom[part]
    if keyb.stabpresets == "custom":
        custom = {
        "BaseS" : baseS,
        "StemS" : stemS,
        "etalS" : 0
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            pass
        else:
            return custom[part]
    
    
    if keyb.switchpresets != "custom":
        presets = {
        "cherryred" : {"Upper" : 0,
                        "_Base" : 0,
                        "_Stem" : 0,
                        "_Pins" : 0
                        },
        "gateronyellow" : {"Upper" : 1,
                        "_Base" : 1,
                        "_Stem" : 0,
                        "_Pins" : 0
                        },
        "keebwerkbushi" : {"Upper" : 0,
                        "_Base" : 0,
                        "_Stem" : 0,
                        "_Pins" : 0
                        },
        "tecseepurppand" : {"Upper" : 0,
                        "_Base" : 0,
                        "_Stem" : 0,
                        "_Pins" : 0
                        },              
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            return presets[keyb.switchpresets][part]
            
    if keyb.stabpresets != "custom":
        presets = {
        "bblack" : {"BaseS" : 0,
                        "StemS" : 0,
                        "etalS" : 0},         
        "btransparent" : {"BaseS" : 1,
                        "StemS" : 1,
                        "etalS" : 0},    
        "studiorx78gold" : {"BaseS" : 1,
                        "StemS" : 1,
                        "etalS" : 0},                    
        }
        if part == "Upper" or part == "_Base" or part == "_Stem" or part == "_Pins":
            pass
        else:
            return presets[keyb.stabpresets][part]

def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])

def linsrgb_to_srgb(linsrgb):
    srgb = [0,0,0,0]
    for idx, col in enumerate(linsrgb):
        gamma = 1.055 * col**(1./2.4) - 0.055
        scale = col * 12.92
        srgb[idx] = round(numpy.where(col > 0.0031308, gamma, scale)*255)
    if len(srgb) > 3: srgb.pop(3)
    return tuple(srgb)

def srgb_to_hex(srgb):
    return '#%02x%02x%02x' % srgb


def addMaterial(name,color,rough,metal,trans,transrough,bevel):

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = rough
    mat.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = metal
    mat.node_tree.nodes['Principled BSDF'].inputs['Transmission'].default_value = trans
    mat.node_tree.nodes['Principled BSDF'].inputs['Transmission Roughness'].default_value = transrough
    
    if bevel > 0:
        bevelnode = mat.node_tree.nodes.new("ShaderNodeBevel")
        bevelnode.samples = 5
        bevelnode.inputs[0].default_value = bevel
        mat.node_tree.links.new(bevelnode.outputs[0], mat.node_tree.nodes["Principled BSDF"].inputs["Normal"])
    return mat