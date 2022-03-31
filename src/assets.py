import bpy
import os

def case():
    scene = bpy.context.scene
    data = bpy.data
    assets = scene.assets_pg
    
    typ = assets.casesize
    
    
    if typ == "type40":
        case = assets.type40
    elif typ == "type60":
        case = assets.type60
    elif typ == "type65":
        case = assets.type65
    elif typ == "type75":
        case = assets.type75
    elif typ == "typeTKL":
        case = assets.typeTKL
    return case
    
def addCase(case):
    scene = bpy.context.scene
    data = bpy.data
    assets = scene.assets_pg
   
    #main collection
    if not bpy.context.scene.collection.children.get( "Assets" ):    
        main_coll = data.collections.new( "Assets" )
        bpy.context.scene.collection.children.link(main_coll)
    else:
        main_coll = bpy.context.scene.collection.children.get( "Assets" )
        
    #case collection
    if main_coll and not main_coll.children.get( "Cases" ):
        case_coll = data.collections.new( "Cases" )
        main_coll.children.link( case_coll )
    else:
        case_coll = bpy.data.collections[ "Cases" ]
        
    #importing case
    filepath = os.path.join(os.path.dirname(__file__), "assets.blend")
    
    with data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [ case ]
    for obj in data_to.objects:
        if obj is not None:
            case_coll.objects.link(obj)
            obj.location = bpy.context.scene.cursor.location
            obj.scale = (assets.casescale,assets.casescale,assets.casescale)
                
                
def addCable():
    scene = bpy.context.scene
    data = bpy.data
    assets = scene.assets_pg
    
    typ = assets.cables
    
    if typ == "KBDhand":
        cable = assets.cablecolor
    
    #main collection
    if not bpy.context.scene.collection.children.get( "Assets" ):    
        main_coll = data.collections.new( "Assets" )
        bpy.context.scene.collection.children.link(main_coll)
    else:
        main_coll = bpy.context.scene.collection.children.get( "Assets" )
    
    #cable collection
    if main_coll and not main_coll.children.get( "Cables" ):
        cable_coll = data.collections.new( "Cables" )
        main_coll.children.link( cable_coll )
    else:
        cable_coll = bpy.data.collections[ "Cables" ]
        
    filepath = os.path.join(os.path.dirname(__file__), "assets.blend")
    
    with data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [ cable ]
    for obj in data_to.objects:
        if obj is not None:
            cable_coll.objects.link(obj)
            obj.location = bpy.context.scene.cursor.location
            obj.scale = (assets.casescale,assets.casescale,assets.casescale)