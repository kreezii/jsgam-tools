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

    points=stroke.points[0]

    for i in range(2,len(points),6):

        x, y = points[i: i + 2]

        polygon_points.extend([int(x), int(y)])


    polygon_points.extend([int(points[2]),int(points[3])])

    return polygon_points

def path_dump(image,name):
    polygons={
        "Scenes":[
            {
                "Name":name,
                "Obstacles":[],
                "Background":""
            }
        ]
    }

    objects=[]

    for num,path in enumerate(image.vectors, start=1):
        stroke=path.strokes[0]
        if num==len(image.vectors):
            polygons["Scenes"][0].update({"WalkArea":dumpStroke(stroke)})
        else:
            if "obj" in path.name.lower():
                objects.append(
                {
                    "Name":path.name,
                    "Area":dumpStroke(stroke)
                })

            else:
        	    polygons["Scenes"][0]["Obstacles"].append(
        		[
        			dumpStroke(stroke)
                ])

    return polygons,objects

def layer_offsets(img):
    capas ={
        "Objects":[]
    }

    fondo=img.layers[len(img.layers)-1].name

    for num,layer in enumerate(img.layers, start=1):
        if num!=len(img.layers):
            pos=[layer.offsets[0]+layer.width/2,layer.offsets[1]+layer.height]
            capas["Objects"].append(
            {
                "Name":layer.name,
                "Texture":layer.name,
                "Position":pos,
            })

    return capas,fondo;

def export_JSGAM(img, path, name):
    jsgamInfo={}

    capas,fondo=layer_offsets(img)
    poligonos,objetos=path_dump(img,name)

    jsgamInfo.update(capas)
    jsgamInfo.update(poligonos)

    jsgamInfo["Scenes"][0]["Background"]=fondo
    jsgamInfo["Objects"].extend(objetos)

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
