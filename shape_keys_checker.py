import bpy
import bmesh

class ShapeKeysChecker(bpy.types.Operator):
    bl_idname = "object.shapekeyschecker"
    bl_label = "ShapeKeysChecker"
    bl_description = "select shape key's moved vertices"
    bl_options = {"REGISTER", "UNDO"}

    tolerance: bpy.props.FloatProperty(
        name="tolerance",
        description="maximum distance to consider motionless",
        default=0,
        min=0,
        step=1,
        precision=6,
        unit="LENGTH" 
    )

    def execute(self, context):
        if context.mode != "EDIT_MESH":
            print(context.mode)
            return {"CANCELLED"}

        obj = context.active_object

        # オブジェクトがメッシュか確認
        if(obj.type != "MESH"):
            print(obj.type)
            return {"CANCELLED"}

        # EDITモードだと選択の変更が反映されないのでOBJECTモードに変更
        bpy.ops.object.mode_set(mode = "OBJECT")

        # アクティブシェイプキーを取得
        active_key = obj.active_shape_key
        if active_key is None:
            print("Any shape key is not active.")
            return {"CANCELLED"}
        
        # Baseシェイプキーを取得
        base_key = active_key.relative_key
        
        # Baseと異なる頂点を取得
        select_vertices = [(vt_active.co - vt_base.co).length > self.tolerance for vt_active, vt_base in zip(active_key.data, base_key.data)]

        me = obj.data

        # Vertex選択モードに変更
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        
        # 変動があるverticesのみ選択
        me.polygons.foreach_set("select", (False,) * len(me.polygons))
        me.edges.foreach_set("select", (False,) * len(me.edges))
        me.vertices.foreach_set("select", select_vertices)
        me.update()

        bpy.ops.object.mode_set(mode="EDIT")

        print("ShapeKeysChecker finished.")

        return {"FINISHED"}
