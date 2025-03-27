import bpy

from .login import login


tenant_id = "e55df843-27da-4824-bf76-9bbf0a598f59"
client_id = "deb27bec-956b-447e-8084-c37534a345fa"
scopes = ["User.Read"]


class VIEW3D_PT_msal(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "msal"
    bl_label = "msal"

    def draw(self, context):
        row = self.layout.row(align=True)

        self.layout.label(text="Client ID")
        self.layout.label(text=client_id)
        self.layout.label(text="Tenant ID")
        self.layout.label(text=tenant_id)

        row.operator("msal.login", text="Login")


class MSAL_OT_msal_login(bpy.types.Operator):
    bl_idname = "msal.login"
    bl_label = "SSO login"

    def execute(self, context):
        self.invoke(self, context, None)

    def invoke(self, context, event):
        result = login(
            tenant_id=tenant_id,
            client_id=client_id,
            scopes=scopes,
        )

        print(result)

        return {"FINISHED"}


classes = (VIEW3D_PT_msal, MSAL_OT_msal_login)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
