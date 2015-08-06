import bpy
from bpy.props import *
from ... tree_info import keepNodeLinks
from ... base_types.node import AnimationNode
from ... sockets.info import getDataTypeItems, toIdName

class ConvertNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ConvertNode"
    bl_label = "Convert"
    isDetermined = True

    inputNames = { "Old" : "old" }
    outputNames = { "New" : "new"}

    def assignedTypeChanged(self, context):
        self.targetIdName = toIdName(self.assignedType)
        self.recreateOutputSocket()

    selectedType = EnumProperty(name = "Type", items = getDataTypeItems)
    assignedType = StringProperty(update = assignedTypeChanged)
    targetIdName = StringProperty()

    def create(self):
        self.inputs.new("an_GenericSocket", "Old")
        self.selectedType = "String"
        self.assignedType = "String"

    def draw_buttons_ext(self, context, layout):
        col = layout.column(align = True)
        col.prop(self, "selectedType", text = "")
        self.callFunctionFromUI(col, "assignSelectedListType",
            text = "Assign",
            description = "Remove all sockets and set the selected socket type")

    def edit(self):
        socket = self.outputs[0]
        targets = socket.dataTargetSockets
        if len(targets) == 1:
            self.assignType(targets[0].dataType)

    def assignSelectedListType(self):
        self.assignedType = self.selectedType

    @keepNodeLinks
    def assignType(self, dataType = "Float"):
        self.assignedType = dataType
        self.selectedType = dataType

    def recreateOutputSocket(self):
        self.outputs.clear()
        self.outputs.new(self.targetIdName, "New")

    def getExecutionCode(self):
        t = self.assignedType
        if t == "Float": return ("try: $new$ = float(%old%) \n"
                                 "except: $new$ = 0")
        elif t == "Integer": return ("try: $new$ = int(%old%) \n"
                                     "except: $new$ = 0")
        elif t == "String": return ("try: $new$ = str(%old%) \n"
                                    "except: $new$ = ''")
        elif t == "Vector": return ("try: $new$ = mathutils.Vector(%old%) \n"
                                    "except: $new$ = mathutils.Vector((0, 0, 0))")
        else:
            return "$new$ = %old%"

    def getModuleList(self):
        t = self.assignedType
        if t == "Vector": return ["mathutils"]
        return []
