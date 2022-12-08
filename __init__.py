bl_info = {
        "name": "Vertex Tool",
        "description": "Copy vertex coords, for creating Codewalker MLO portal.",
        "author": "MasNana",
        "version": (1, 0),
        "blender": (3, 3, 1),
        "location": "N Menu > Vertex Tool",
        "warning": "",
        "support": "COMMUNITY",
        "category": "Tool"
        }

import bpy, bmesh, mathutils
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

class OBJECT_PT_Vertex(bpy.types.Panel):
    bl_label = "Vertex Tool"
    bl_idname = "OBJECT_PT_Vertex"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Tool"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.operator("mesh.copycoords")
        
        
class CopyVertex(bpy.types.Operator):
    bl_label = "Copy Coords"
    bl_idname = "mesh.copycoords"
                
    def execute(self, context):
        obj = context.active_object
        if obj is not None and obj.mode == 'EDIT':
            mat = obj.matrix_world
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            if bm.select_history:
                elem = bm.select_history.active
                loc = mat @ elem.co
                x = str(round(loc.x, 6))
                y = str(round(loc.y, 6))
                z = str(round(loc.z, 6))
                coord = '{x}, {y}, {z}'.format(x=x, y=y, z=z)
                if isinstance(elem, bmesh.types.BMVert):
#                    print(coord)
                    copy2clip(coord)
                    return {'FINISHED'}
            else : 
                self.report({'ERROR'}, "Vertex Tool: no active vertices.") 
                return {'CANCELLED'}
        else : 
            self.report({'ERROR'}, "Vertex Tool: must be in editmode.") 
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(OBJECT_PT_Vertex)
    bpy.utils.register_class(CopyVertex)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_Vertex)
    bpy.utils.unregister_class(CopyVertex)

if __name__ == "__main__":
    register()