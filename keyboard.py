import bpy
import os
import json
import time
from mathutils import Matrix, Vector
from math import cos, sin ,radians

 
def addKeyboard(file):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    mytool = scene.my_tool
    legendspg = scene.legends_pg
    switchespg = scene.switches_pg
    keycapspg = scene.keycaps_pg
    pcbplatepg = scene.pcbplate_pg
    
    #collection names
    capcollection = mytool.input_name + " Caps"
    switchcollection = mytool.input_name + " Switches"
    legendcollection = mytool.input_name + " Legends"
    casecollection = mytool.input_name + " Case"
    
    #define vars 
    addedKEYCAPS = []
    addedCARACTERS = []
    addedSWITCHES = []
    
    #save previous name
    global KeyError_NAME
    try:
        previousname = KeyError_NAME
    except:
        pass
    KeyError_NAME = mytool.input_name
    
    #prepare scene
    bpy.context.space_data.overlay.show_relationship_lines = False
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        materials = ("sUpper","sBase","sStem","sPins")
        for mat in materials:
            matr = datam[previousname + " " + mat + ".001"]
            datam.remove( matr )
    except:
        pass
    
    try:
        keycapmatr = datam[str(previousname) + "_Cap_Material"]
        datam.remove( keycapmatr )
    except:
        pass

    #open 
    with open(file, 'r') as f:
        textinput = json.load(f) 
    
    #textinput = [[{'p': 'R2', 'a': 6}, 'Esc', {'a': 4, 'f': 6}, 'Q', 'O', 'P', {'a': 6, 'f': 3}, 'Esc']]

    #add main collection
    if not bpy.context.scene.collection.children.get( mytool.input_name ):    
        main_coll = data.collections.new( mytool.input_name )
        bpy.context.scene.collection.children.link(main_coll)
    else:
        main_coll = bpy.context.scene.collection.children.get(mytool.input_name)
    
    
    #add sub collections
    if main_coll and not main_coll.children.get( capcollection ) and keycapspg.boolean == True:
        my_sub_coll = data.collections.new( capcollection )
        main_coll.children.link(my_sub_coll)
    elif main_coll and main_coll.children.get( capcollection ):
        collection = data.collections[ capcollection ]
        delmeshes = set()
        
        for obj in [o for o in collection.objects if o.type == 'MESH']:
            delmeshes.add( obj.data )
            datao.remove( obj )
            
        for mesh in [m for m in delmeshes if m.users == 0]:
            data.meshes.remove( mesh )
        if keycapspg.boolean == False:
            delcol = data.collections[ capcollection ]
            data.collections.remove(delcol)
    
    #switch collection
    if main_coll and not main_coll.children.get( switchcollection ) and switchespg.boolean == True:
        my_sub_coll = data.collections.new( switchcollection )
        main_coll.children.link(my_sub_coll)
    elif main_coll and main_coll.children.get( switchcollection ):
        collection = data.collections[ switchcollection ]
        delmeshes = set()
        
        for obj in [o for o in collection.objects if o.type == 'MESH']:
            delmeshes.add( obj.data )
            datao.remove( obj )
            
        for mesh in [m for m in delmeshes if m.users == 0]:
            data.meshes.remove( mesh )
        if switchespg.boolean == False:
            delcol = data.collections[ switchcollection ]
            data.collections.remove(delcol)        
    
    #legend collection
    if main_coll and not main_coll.children.get( legendcollection ) and legendspg.boolean == True:
        my_sub_coll1 = data.collections.new( legendcollection )
        main_coll.children.link(my_sub_coll1)
    elif main_coll and main_coll.children.get( legendcollection ):
        collection = data.collections[ legendcollection ]
        curvesleg = set()
        
        for obj in [o for o in collection.objects if o.type == 'FONT']:
            curvesleg.add( obj.data )
            datao.remove( obj )
            
        for curve in [m for m in curvesleg if m.users == 0]:
            data.curves.remove( curve )
        if legendspg.boolean == False:
            delcol = data.collections[ legendcollection ]
            data.collections.remove(delcol)   
    
    #case collection
    if main_coll and not main_coll.children.get( casecollection ) and pcbplatepg.platebool == True or pcbplatepg.casebool == True:
        my_sub_coll1 = data.collections.new( casecollection )
        main_coll.children.link(my_sub_coll1)
    elif main_coll and main_coll.children.get( casecollection ):
        collection = data.collections[ casecollection ]
        delmeshes = set()
        
        for obj in [o for o in collection.objects if o.type == 'MESH']:
            delmeshes.add( obj.data )
            datao.remove( obj )
            
        for mesh in [m for m in delmeshes if m.users == 0]:    
            data.meshes.remove( mesh )
        if pcbplatepg.platebool == False:
            delcol = data.collections[ casecollection ]
            data.collections.remove(delcol)   
    
    #import node groups
    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    
    #import plate nodes
    if not bpy.data.node_groups.get(mytool.input_name + "_Plate_Nodes") and pcbplatepg.platebool == True:
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.node_groups = ["PLATE_NODES"]
        bpy.data.node_groups["PLATE_NODES"].name = mytool.input_name + "_Plate_Nodes"
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not bpy.data.materials.get(mytool.input_name + " Plate") and pcbplatepg.platebool == True:
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["PlateMat"]
        bpy.data.materials["PlateMat"].name = mytool.input_name + " Plate"
    
    #import case nodes
    if not bpy.data.node_groups.get(mytool.input_name + "_Case_Nodes") and pcbplatepg.casebool == True:
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.node_groups = ["CASE_NODES"]
        bpy.data.node_groups["CASE_NODES"].name = mytool.input_name + "_Case_Nodes"    
    
    #setup
    vertices = []
    yoffset = 0
    platewidth = 0
    plateheight = 0
    
    #defaults (need to be defined for every change)
    legpos = 4
    profilerow = "R1"
    capcolor = "#cccccc" 
    legendcolor = "#000000" 
    textsize = 3
    
    rotation = 0
    rotoriginx = 0 
    rotoriginy = 0
    
    for row in textinput:
        #setup
        index = 0
        xoffset = 0
        textsize2 = 0
        
        for item in row:
            #defaults (need to be defined for every different cap)
            width = 1
            width2 = 0
            height = 1 
            stepped = "false"
            item2 =  ""
            
            if isinstance(item, dict):
                try: 
                    width = item["w"]
                except:
                    pass
                    
                try:    
                    height = item["h"]
                except:
                    pass
                    
                try:
                    xoffset += item["x"]
                except:
                    pass
                    
                try:
                    legpos = item["a"]
                except:
                    pass
                    
                try:
                    yoffset += item["y"]   
                except:
                    pass
                    
                try:
                    stepped = item["l"] 
                    stepped = "true"
                except:
                    pass

                try:
                    width2 = item["w2"]
                except:
                    pass    
                
                try:
                    textsize = item["f"] 
                except:
                    pass 
                    
                try:
                    textsize2 = item["f2"] 
                except:
                    pass  
                    
                try:
                    profilerow = item["p"] 
                except:
                    pass  
                    
                try:
                    capcolor = item["c"]
                except:
                    pass
 
                try:
                    legendcolor = item["t"]
                except:
                    pass
                    
                try:
                    rotation = item["r"]
                except:
                    pass
                
                try:
                    rotoriginx = item["rx"]
                except:
                    pass
                
                try:
                    rotoriginy = item["ry"]
                except:
                    pass
                 
 
                item = row[index+1]
                row.pop(index+1)
                
            if keycapspg.boolean == True:
                linkkeycaps( profilerow, width, height, item, xoffset, yoffset, capcolor, width2, rotation, rotoriginx, rotoriginy)
                addedmesh = data.collections[ capcollection ].objects[str(xoffset) + " " + str(yoffset)].data
                addedKEYCAPS.append(addedmesh)    
            
            if switchespg.boolean == True:
                linkswitch(xoffset,yoffset,width,height)
                addedswitch = data.collections[ switchcollection ].objects["S" + str(xoffset) + " " + str(yoffset)].data
                addedSWITCHES.append(addedswitch)
            
            if legendspg.boolean == True and legendspg.typeselector == "objleg":
                xcount = item.count("\n")
                if xcount > 2 and not isinstance(item, dict):
                        
                    stringindex = 0
                    lists = []
                    for x in range (0,len(item)):
                        
                        if stringindex == item.find("\n", x):
                            continue
                        stringindex = item.find("\n", x)
                        lists.append(stringindex)
                        
                    if len(lists) > 2 and lists[1] != "":
                        item2 = item[lists[1] + 1:]
                        item = item[:lists[1]]
                        addLegend( item2, width, width2, height, xoffset+0.3, yoffset, legpos, textsize, legendcolor)
                        addedleg = data.collections[ legendcollection ].objects[mytool.input_name + "_L_" + str(xoffset+0.3) + "_" + str(yoffset) + "_" +  str(legpos)].data
                        addedCARACTERS.append(addedleg)
                        
                if textsize2 != 0:
                    stringindex1 = item.find("\n")
                    if stringindex1 != -1:
                        item1 = item[:stringindex1]
                        item2 = item[stringindex1+1:]
                        item = item1
                    if item2 != "":
                        addLegend( item2, width, width2, height, xoffset, yoffset, 2, textsize2, legendcolor)
                        addedleg = data.collections[ legendcollection ].objects[mytool.input_name + "_L_" + str(xoffset) + "_" + str(yoffset) + "_" +  str(2)].data
                        addedCARACTERS.append(addedleg)
                if item != "":
                    addLegend( item, width, width2, height, xoffset, yoffset, legpos, textsize, legendcolor)
                    addedleg = data.collections[ legendcollection ].objects[mytool.input_name + "_L_" + str(xoffset) + "_" + str(yoffset) + "_" +  str(legpos)].data
                    addedCARACTERS.append(addedleg)
            
            point = [((xoffset + (width - 1) * 0.5 ) * 0.019 + 0.009, -yoffset * 0.019  , 0)]
            vertices += point
            
            xoffset += width 
            
            if platewidth < xoffset:
                platewidth = xoffset
            
            
            index += 1
        yoffset += 1
        if plateheight < yoffset:
                plateheight = yoffset
                
    
    
    if pcbplatepg.platebool == True:
        faces = []
        edges = []
        
        pointmesh = bpy.data.meshes.new('new_mesh')
        pointmesh.from_pydata(vertices, edges, faces)
        pointmesh.update()
        # make object from mesh
        new_object = bpy.data.objects.new(mytool.input_name + " Plate", pointmesh)
        # make collection

        nodegroup = bpy.data.node_groups[mytool.input_name + "_Plate_Nodes"]
        geonodes = new_object.modifiers.new("Plate", "NODES")
        
        delnode = new_object.modifiers["Plate"].node_group
        bpy.data.node_groups.remove(delnode)
        geonodes.node_group = nodegroup
        nodegroup.nodes["INPUT_X"].outputs[0].default_value = platewidth
        nodegroup.nodes["INPUT_Y"].outputs[0].default_value = plateheight
        nodegroup.nodes["Transform"].inputs["Translation"].default_value = (platewidth * 0.0095 - 0.0005, plateheight* -0.0095 + 0.0095,-0.0061)
        platemat = bpy.data.materials[mytool.input_name + " Plate"]
        
        nodegroup.nodes["Set Material"].inputs[2].default_value = platemat
        platemat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = pcbplatepg.platerought
        platemat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = pcbplatepg.platemetallic
        platemat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = pcbplatepg.platecolor
        platemat.node_tree.nodes["Principled BSDF"].inputs["Transmission"].default_value = pcbplatepg.platetrans
        
        new_object.data.materials.append(platemat)
        
        collection = bpy.data.collections[ casecollection ]
        collection.objects.link(new_object)
        
    if pcbplatepg.casebool == True:
        faces = []
        edges = []
        vertices = [(0,0,0)]
        #print(vertices)
        pointmesh = bpy.data.meshes.new('Case')
        pointmesh.from_pydata(vertices, edges, faces)
        pointmesh.update()
        # make object from mesh
        new_object = bpy.data.objects.new(mytool.input_name + " Case", pointmesh)
        # make collection

        nodegroup = bpy.data.node_groups[mytool.input_name + "_Case_Nodes"]
        geonodes = new_object.modifiers.new("Case", "NODES")
        
        delnode = new_object.modifiers["Case"].node_group
        bpy.data.node_groups.remove(delnode)
        
        geonodes.node_group = nodegroup
        nodegroup.nodes["INPUT_X"].outputs[0].default_value = platewidth
        nodegroup.nodes["INPUT_Y"].outputs[0].default_value = plateheight
        #nodegroup.nodes["Transform"].inputs["Translation"].default_value = (platewidth * 0.0095 - 0.0005, plateheight* -0.0095 + 0.0095,-0.0061)
        #platemat = bpy.data.materials[mytool.input_name + " Plate"]
        
        #nodegroup.nodes["Set Material"].inputs[2].default_value = platemat
        #platemat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = pcbplatepg.platerought
        #platemat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = pcbplatepg.platemetallic
        #platemat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = pcbplatepg.platecolor
        
        #new_object.data.materials.append(platemat)
        
        collection = bpy.data.collections[mytool.input_name + " Plate + PCB"]
        collection.objects.link(new_object)
    
    #if legendspg.boolean == True and legendspg.typeselector == "uvleg":
    #    genUV()
    
    #middle of object
    origin = Vector((platewidth * 0.5 * 0.019 - 0.0005, -plateheight * 0.5 * 0.019, 0))
    
    scale = (mytool.input_scale, mytool.input_scale, mytool.input_scale )
    #keycap join ----------------------------------------------------------------------------------------
    if keycapspg.boolean == True:
        #adds all objs to list 
        meshescaps = []
        collection = data.collections[mytool.input_name + " Caps"]
        for obj in [o for o in collection.objects if o.type == 'MESH']:
            meshescaps.append( obj )

        #joins all obj in list by creating a copy of the scene and joining them there (copy is only temporary)
        ctx = bpy.context.copy()
        ctx['active_object'] = meshescaps[0]
        ctx['selected_editable_objects'] = meshescaps
        bpy.ops.object.join(ctx)

        #sets obj as the first obj in the caps collection and the name 
        obj = data.collections[mytool.input_name + " Caps"].objects[0]
        obj.name = mytool.input_name + " Caps"

        #removes all orphan meshes
        for mesh in [m for m in addedKEYCAPS if m.users == 0]:
            data.meshes.remove( mesh )


        #set obj origin to center of geometry
        obj.data.transform(Matrix.Translation(-origin))

        #sets keyboard position to cursor
        #if mytool.parentobj == "Caps":
        #    obj.location = bpy.context.scene.cursor.location
        
        if mytool.parentbool == False and legendspg.boolean == False:
            obj.scale = scale
   
    if legendspg.boolean == True and legendspg.typeselector == "objleg":
        
        collection =  data.collections[mytool.input_name + " Legends"] 
        for subobj in [o for o in collection.objects if o.type == 'FONT' or o.type == 'MESH']:
            subobj.location -= Vector(origin)
            if keycapspg.boolean == True:
                subobj.parent = obj
                subobj.modifiers["Shrinkwrap"].target = obj
        if mytool.parentbool == False and keycapspg.boolean == True:
            obj.scale = scale
    
    if switchespg.boolean == True:
        #adds all switches to list 
        meshesswitch = []
        collection = data.collections[mytool.input_name + " Switches"]
        for swobj in [o for o in collection.objects if o.type == 'MESH']:
            meshesswitch.append( swobj )
        
        #joins all switches in list by creating a copy of the scene and joining them there (copy is only temporary)
        ctx = bpy.context.copy()
        ctx['active_object'] = meshesswitch[0]
        ctx['selected_editable_objects'] = meshesswitch
        bpy.ops.object.join(ctx)
        
        swobj = data.collections[mytool.input_name + " Switches"].objects[0]
        swobj.name = mytool.input_name + " Switches"
        
        for mesh in [m for m in addedSWITCHES if m.users == 0]:
            data.meshes.remove( mesh )
            
        origin[0] -= 0.009
        origin[2] -= 0.005
        swobj.data.transform(Matrix.Translation(-origin))
        swobj.location = (0,0,0)
        #if mytool.parentobj == "Switches":
        #    swobj.location = bpy.context.scene.cursor.location
        origin = Vector((platewidth * 0.5 * 0.019 - 0.0005, -plateheight * 0.5 * 0.019, 0))
        
        if mytool.parentbool == False:
            swobj.scale = scale
        
    if mytool.parentbool == True:
        mainobj = bpy.data.objects[mytool.input_name + " " + mytool.parentobj]
    
    if switchespg.boolean == True and mytool.parentbool == True and mytool.parentobj != "Switches":
        swobj.parent = mainobj
    
    if keycapspg.boolean == True and mytool.parentbool == True and mytool.parentobj != "Caps":
        obj.parent = mainobj
    
    
    if pcbplatepg.platebool == True:
        plateobj = bpy.data.objects[mytool.input_name + " Plate"]
        plateobj.data.transform(Matrix.Translation(-origin))
        if mytool.parentbool == True and mytool.parentobj != "Plate": 
            plateobj.parent = mainobj
        bpy.data.node_groups[mytool.input_name + "_Plate_Nodes"].nodes["Transform"].inputs["Translation"].default_value = (0,0.0095,-0.0061)
        if mytool.parentbool == False:
            plateobj.scale = scale
        
    if mytool.parentbool == True:
        mainobj.scale = scale
        mainobj.rotation_euler = (mytool.input_rotation, 0, 0)
        mainobj.location = bpy.context.scene.cursor.location

def genUV():
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    legendspg = scene.legends_pg
    switchespg = scene.switches_pg
    keycapspg = scene.keycaps_pg
    mytool = scene.my_tool
    
    
    
    name = mytool.input_name + "_Cap_Material"
    
    legends = pictureSelector()
  
    obj = data.collections[mytool.input_name + " Caps"].objects[0]
    
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
    mytool = scene.my_tool
  
    preset = {
      "ansi40" : os.path.join(os.path.dirname(__file__), "presets/ansi40.json"), 
      "ansi60" : os.path.join(os.path.dirname(__file__), "presets/ansi60.json"),
      "ansi104" : os.path.join(os.path.dirname(__file__), "presets/ansi104.json"),
      "iso60" : os.path.join(os.path.dirname(__file__), "presets/iso60.json"),
      "iso105" : os.path.join(os.path.dirname(__file__), "presets/iso105.json")
    }
    
    if mytool.input_selector != "custom":
        output = preset[mytool.input_selector]
    else:
        output = mytool.input_jsonfile
    return output

def linkkeycaps( profilerow, width, height, item, xoffset, yoffset, capcolor, width2, rotation, rotoriginx, rotoriginy):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    mytool = scene.my_tool
    keycapspg = scene.keycaps_pg
    legendspg = scene.legends_pg
    
    name = str(xoffset) + " " + str(yoffset)
    
    
    h = capcolor.replace('#', "0x")
    
    
    obj_name = str(keycapspg.profileselector) + "_" + str(profilerow) + "_" + str(width) + "," + str(height)
    obj_name = ''.join(obj_name.split())

    if width2 == 1.5:
        obj_name = "cherry_IsoEnter"
        xoffset -= 0.25
    elif width2 == 2.25:
        obj_name = "cherry_BigEnter"
    elif width2 == 1.75:
        obj_name = "cherry_steppedCaps"

    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    if not bpy.context.scene.objects.get(obj_name):
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.objects = [obj_name]

        for obj in data_to.objects:
            if obj is not None:
                data.collections[mytool.input_name + " Caps"].objects.link(obj)
                
                obj.name = name 
    
                if rotation == 0:
                    obj.location.y = yoffset * 0.019
                    obj.location.x = xoffset * -0.019
                    obj.location = bpy.context.scene.cursor.location
                    origin = ((xoffset * 0.019),-(yoffset * 0.019), 0)
                    obj.data.transform(Matrix.Translation(origin))
                else:
                    obj.location.y = 0
                    obj.location.x = xoffset * 0.019
                    x = obj.location[0]
                    y = obj.location[1]
                    rotoriginx = rotoriginx * 0.019
                    rotoriginy = rotoriginy * -0.019
                    rotation = -rotation
                    print("loc", x,y)
                    print("rot origin", rotoriginx,rotoriginy)
                    x1 =  (x-rotoriginx) * cos(radians(rotation)) - (y - rotoriginy) * sin(radians(rotation)) + rotoriginx #compute x 
                    y1 =  (x-rotoriginx) * sin(radians(rotation)) + (y - rotoriginy) * cos(radians(rotation)) + rotoriginy #compute y
                    print("locnew",x1,y1)
                    obj.rotation_euler[2] = radians(rotation) #local rotate
                    obj.location[0] = x1 #set global pos x
                    obj.location[1] = y1 #set global pos y
                    
    
    #loads materials if not already present
    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    if not datam.get("Plastic") and not datam.get(mytool.input_name + "_Cap_Material" + capcolor):
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["Plastic"]
    
    if datam.get("Plastic"):
        plastic = datam.get("Plastic") 
        plastic.name = mytool.input_name + "_Cap_Material" + capcolor
    else:
        plastic = datam.get(mytool.input_name + "_Cap_Material" + capcolor)
        
    if keycapspg.colorpreset == "custom":
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = keycapspg.color
    elif keycapspg.colorpreset == "preset":
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = hex_to_rgb(int(h, 16))
    else:
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = [float(x) for x in list(keycapspg.colorpreset[1:-1].split(","))]
    
    #links or append loaded materials
    obj.data.materials.append(plastic) 

def addLegend( item, width, width2, height, xoffset, yoffset, posindex, textsize, legendcolor):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    mytool = scene.my_tool
    keycapspg = scene.keycaps_pg
    legendspg = scene.legends_pg
    
    h = legendcolor.replace('#', "0x")
    
    item = item.replace("<br>", "\n")
    name = mytool.input_name + "_L_" + str(xoffset) + "_" + str(yoffset) + "_" +  str(posindex)
    
    if width2 == 1.5:
        xoffset -= 0.25
    
    textsize = textsize * 0.001 
    #if legendspg.font == "Open Cherry Regular":
    #    textsize = textsize * 1.15
    textsize = round(textsize,5)
    
    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    if not bpy.context.blend_data.fonts.get(legendspg.font):
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.fonts = [legendspg.font]
    
    loadedfont = data.fonts[legendspg.font]

    data.curves.new(type="FONT", name=name).body = item
    curve_obj = data.curves[name]
    
    curve_obj.font = loadedfont
    curve_obj.size = textsize
    font_obj = datao.new(name=name, object_data=data.curves[name])
    #print(font_obj.name)
    data.collections[mytool.input_name + " Legends"].objects.link(font_obj)

    
    font_obj.location[0] += xoffset * 0.019
    font_obj.location[1] -= yoffset * 0.019 
    font_obj.location[2] += 0.017 

    
        
    if keycapspg.profileselector == "cherry":
        texttransform = (0.004,0.0067,0.0007,0.0045,1.25,1.4)
    elif keycapspg.profileselector == "dsa":
        texttransform = (0.004,0.0053,0,0.0035,1.1,1.4)
    elif keycapspg.profileselector == "sa":
        texttransform = (0.004,0.0053,0,0.0035,1.1,1.4)
    
    if posindex == 4:
        curve_obj.align_y = "TOP"
        font_obj.location[0] += texttransform[0]
        font_obj.location[1] += texttransform[1]
    elif posindex == 6:
        curve_obj.align_y = "CENTER"
        font_obj.location[0] += texttransform[0]
        font_obj.location[1] += texttransform[2]
    elif posindex == 2:
        curve_obj.align_y = "BOTTOM"
        font_obj.location[0] += texttransform[0]
        font_obj.location[1] -= texttransform[3]
    if textsize == 0.0045:
        curve_obj.space_line = texttransform[5]
    if textsize == 0.005:
        curve_obj.space_line = texttransform[4]    
            

    if legendspg.quality == True:
        solidify = font_obj.modifiers.new("Solidify","SOLIDIFY")
        solidify.thickness = 0.0001
        
        remesh = font_obj.modifiers.new("Remesh","REMESH")
        remesh.mode = 'SHARP'
        remesh.octree_depth = legendspg.resolution
        remesh.use_remove_disconnected = False

    shrinkwrap = font_obj.modifiers.new("Shrinkwrap","SHRINKWRAP")
    shrinkwrap.wrap_method = 'PROJECT'
    shrinkwrap.use_project_z = True
    shrinkwrap.use_project_x = False
    shrinkwrap.use_negative_direction = True
    shrinkwrap.use_positive_direction = False
    shrinkwrap.offset = 0.00001 
    
    
    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")
    if not datam.get("PlasticLeg") and not datam.get(mytool.input_name + "_Legend_Material" + legendcolor) :
        with data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.materials = ["PlasticLeg"]
    
    if datam.get("PlasticLeg"):
        plastic = datam.get("PlasticLeg")
        plastic.name = mytool.input_name + "_Legend_Material" + legendcolor
    else:
        plastic = datam.get(mytool.input_name + "_Legend_Material" + legendcolor)
    
    if legendspg.colorpreset == "custom":
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = legendspg.color 
    elif legendspg.colorpreset == "preset":
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = hex_to_rgb(int(h, 16))
    else:
        plastic.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = [float(x) for x in list(legendspg.colorpreset[1:-1].split(","))]
    
    font_obj.data.materials.append(plastic) 

def linkswitch(xoffset,yoffset,width,height):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    mytool = scene.my_tool
    keycapspg = scene.keycaps_pg
    switchespg = scene.switches_pg
    
    if switchespg.subdselector == "lowpoly":
        obj_name = "mxswitch_lowpoly"
    else:
        obj_name = "mxswitch"
    
    width = width * 0.0095

    filepath = os.path.join(os.path.dirname(__file__), "caps.blend")

    link = False
    
    
    if not bpy.context.scene.objects.get(obj_name):
        with data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.objects = [obj_name]


        #link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                data.collections[mytool.input_name + " Switches"].objects.link(obj)
                obj.location.y = yoffset * -0.019 + 0.0095 - 0.0095 * height
                obj.location.x = xoffset * 0.019 + width
                
                obj.name = "S" + str(xoffset) + " " + str(yoffset)
    
    if not datam.get("switch_base") and not datam.get(mytool.input_name + "_Switch_Base"):
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
            mater.name = mytool.input_name + "_Switch_" + mat
        materials = (mytool.input_name + "_Switch_Upper",mytool.input_name + "_Switch_Base",mytool.input_name + "_Switch_Stem",mytool.input_name + "_Switch_Pins")
    else:
        materials = (mytool.input_name + "_Switch_Upper",mytool.input_name + "_Switch_Base",mytool.input_name + "_Switch_Stem",mytool.input_name + "_Switch_Pins")
    
    for mat in materials:
        mater = datam[mat]
        obj.data.materials.append(mater)
        mater.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = switchcolor(mat[-5:])
        mater.node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = switchtrans(mat[-5:])
        
    #if switchespg.uppertrans == True and switchespg.presets == "custom":
    #    obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1
    #if switchespg.basetrans == True and switchespg.presets == "custom":  
    #    obj.data.materials[1].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1
    #if switchespg.stemtrans == True and switchespg.presets == "custom":  
    #    obj.data.materials[2].node_tree.nodes["Principled BSDF"].inputs['Transmission'].default_value = 1
    
    o = datao["S" + str(xoffset) + " " + str(yoffset)]
    for p in o.data.polygons:
        verts_vertexGroups = [ g.group for v in p.vertices for g in o.data.vertices[ v ].groups ]
        
        counts    = [ verts_vertexGroups.count( idx ) for idx in verts_vertexGroups ]
        modeIndex = counts.index( max( counts ) )
        mode      = verts_vertexGroups[ modeIndex ]
        
        groupName = o.vertex_groups[ mode ].name
        groupName = groupName[7:].capitalize()
        groupName = mytool.input_name + "_Switch_" + groupName
        
        ms_index = o.material_slots.find( groupName  )
        
        if ms_index != -1: # material found
            p.material_index = ms_index
            
 
def pictureSelector():
    scene = bpy.context.scene
    mytool = scene.my_tool
    legendspg = scene.legends_pg
    
    preset = {
      "ansi40" : os.path.join(os.path.dirname(__file__), "presets/ansi40preset.png"), 
      "ansi60" : os.path.join(os.path.dirname(__file__), "presets/ansi60preset.png"),
      "ansi104" : ""
    }
    
    if legendspg.file != "" :
        output = legendspg.file
    else:
        output = preset[mytool.input_selector]
        
    return output

def switchcolor(part):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    legendspg = scene.legends_pg
    switchespg = scene.switches_pg
    keycapspg = scene.keycaps_pg
    mytool = scene.my_tool
    
    if switchespg.presets == "custom":
        custom = {
        "Upper" : switchespg.colorupper,
        "_Base" : switchespg.colorbase,
        "_Stem" : switchespg.colorstem,
        "_Pins" : switchespg.colorpins
        }
        output = custom[part]
       
    else:
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
        
        output = presets[switchespg.presets][part]
       
    return output
    
def switchtrans(part):
    scene = bpy.context.scene
    data = bpy.data
    datao = data.objects
    datam = data.materials
    
    legendspg = scene.legends_pg
    switchespg = scene.switches_pg
    keycapspg = scene.keycaps_pg
    mytool = scene.my_tool
    
    if switchespg.presets == "custom":
        upper = switchespg.uppertrans
        base = switchespg.basetrans
        stem = switchespg.stemtrans
        
        if upper == True:
            upper = 1
        else:
            upper = 0
        if base == True:
            base = 1
        else:
            base = 0
        if stem == True:
            stem = 1
        else:
            stem = 0
        
        custom = {
        "Upper" : upper,
        "_Base" : base,
        "_Stem" : stem,
        "_Pins" : 0
        }
        output = custom[part]
        
    else:
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
        
        output = presets[switchespg.presets][part]
        
    return output

def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])