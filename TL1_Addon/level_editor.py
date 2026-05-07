import bpy
import math
import bpy_extras
bl_info={
    "name": "レベルエディタ",
    "author": "Fuku Akira",
    "version": (1,0),
    "blender": (3,3,1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# オペレータ 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types. Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}
    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0 
        print("頂点を伸ばしました。")
        #オペレータの命令終了を通知
        return {'FINISHED'}   
# オペレータ ICO球生成
class MYADDON_OT_ICO_sphere(bpy.types. Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}
    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました")
        #オペレータの命令終了を通知
        return {'FINISHED'}   
# オペレータ シーン出力
class MYADDON_OT_export_scene(bpy.types. Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportする"
    filename_ext = ".scene"
    #メニューを実行したときに呼ばれるコールバック関数
    def execute(self, context):
        print("シーン情報をExportします")
        self.export()
        print("シーン情報をExportしました")
        self.report({'INFO'}, "シーン情報をExportしました")
        #オペレータの命令終了を通知
        return {'FINISHED'}   
    def export(self):
        """シーン情報をExportする処理"""
        print("シーン情報出力開始...%r" % self.filepath)
        with open(self.filepath, 'wt') as file:
            self.Write_and_print(file, "SCENE")
            for object in bpy.context.scene.objects:
                if(object.parent):
                    continue
                self.parse_scene_recursive(file, object, 0)
                if object.parent is not None:
                    self.Write_and_print(file, "parent: " + object.parent.name)
                self.Write_and_print(file, "")
    def Write_and_print(self, file, text):
        """ファイルにテキストを書き込み、同時にコンソールにも出力する"""
        print(text)
        file.write(text + "\n")
    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再帰関数"""
        #インデントを作成
        indent =''
        for i in range(level):
            indent += "\t"
        #オブジェクトの情報を出力
        self.Write_and_print(file, indent + object.type + " - " + object.name)
        trans, rot, scale =object.matrix_local.decompose()
        rot = rot.to_euler()
        rot.x=math.degrees(rot.x)
        rot.y=math.degrees(rot.y)
        rot.z=math.degrees(rot.z)

        self.Write_and_print(file, indent + "Trans(%f, %f, %f)" % (trans.x, trans.y, trans.z))
        self.Write_and_print(file, indent + "Rot(%f, %f, %f)" % (rot.x, rot.y, rot.z))
        self.Write_and_print(file, indent + "Scale(%f, %f, %f)" % (scale.x, scale.y, scale.z))
        self.Write_and_print(file, "" )
        #子オブジェクトがある場合は再帰的に解析
        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)


    #トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types. Menu):
    #Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]
    # サブメニューの描画
    def draw(self, context):
    #トップバーの「エディターメニュー」に項目(オペレータ)を追加 
         self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label)
         self.layout.operator(MYADDON_OT_ICO_sphere.bl_idname, text=MYADDON_OT_ICO_sphere.bl_label)
         self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)
        #既存のメニューにサブメニューを追加
    def submenu(self, context):
    # ID指定でサブメニューを追加
            self.layout.menu(TOPBAR_MT_my_menu.bl_idname)
classes=(
     MYADDON_OT_export_scene,
     MYADDON_OT_ICO_sphere,
     MYADDON_OT_stretch_vertex,
     TOPBAR_MT_my_menu,
     )
#class MYADDON_OT_stretch_vertex(bpy.types.Operator):

     
#メニュー項目
def draw_menu_manual(self, context):
    self.layout.operator("wm.url_open_preset",text="manual",icon='HELP')

def register():
    for cls in classes:
         bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")

def unregister():
    for cls in classes:
         bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが無効化されました。")





if __name__ == "__main__":
    register()

