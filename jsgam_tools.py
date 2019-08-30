# coding: utf-8
#!/usr/bin/env python

# GIMP JSGAM plug-in.

import os
import json
from gimpfu import *

def message_data(info):
  pdb.gimp_message(info)

def dumpStroke(stroke):
	polygon_points=[]
	length=stroke.get_length(.1)
	(points,closed)=stroke.points
	for i in range(0,len(points),6):
		polygon_points.append(int(points[i+2]))
		polygon_points.append(int(points[i+3]))
	polygon_points.append(int(points[2]))
	polygon_points.append(int(points[3]))
	return polygon_points

def path_dump(image):
    totalLength=0
    totalPoints=0
    strokesCount=0
    polygons={
        "Scenes":[
            {"Obstacles":{}}
        ]
    }

    for num,path in enumerate(image.vectors, start=1):
        if num==len(image.vectors):
            polygons["Scenes"][0].update({"WalkArea":dumpStroke(stroke)})
        else:
        	for stroke in path.strokes:
        		strokesCount=strokesCount+1
        		(strokePoints,closed)=stroke.points
        		totalPoints=totalPoints+(len(strokePoints)/6)
        		length=pdb.gimp_vectors_stroke_get_length(path, stroke.ID, .1)
        		totalLength=totalLength+length
        		polygons["Scenes"][0]["Obstacles"].update(
        		{
        			path.name:dumpStroke(stroke)
			    })

    return polygons

def layer_offsets(img, path, name):
    capas ={
        "Objects":[]
    }

    for num,layer in enumerate(img.layers, start=1):
        if num!=len(img.layers):
            pos=[layer.offsets[0]+layer.width/2,layer.offsets[1]+layer.height]
            capas["Objects"].append(
            {
                "Name":"Object_Name_Here",
                "Texture":layer.name,
                "Position":pos,
            })

    return capas

def export_JSGAM(img, path, name):
    jsgamInfo={}
    jsgamInfo.update(layer_offsets(img, path, name))
    jsgamInfo.update(path_dump(img))

    json_data=json.dumps(jsgamInfo,
               indent=4, separators=(',', ': '), sort_keys=True)

    json_file = open(path+"/"+name+".json", 'w')
    json_file.write(json_data)
    json_file.close()


register(
    "python_fu_jsgamtools",
    "JSGAM Tools",
    "Tools for JSGAM engine",
    "R.Vañes",
    "R.Vañes",
    "2019",
    "Export to JSGAM...",
    "*",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc.
    [
        (PF_IMAGE, "img", "Image", None),
        (PF_DIRNAME, "path", "Export to:", os.getcwd()),
        (PF_STRING, "name", "Name:", 'scene_name'),
    ],
    [],
    export_JSGAM, menu="<Image>/File/Export")

main()

