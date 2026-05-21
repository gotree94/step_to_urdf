import os, sys, FreeCAD, Import, Mesh

step_path = "C:/Users/user/Desktop/URDFly/RB10-1300E.stp"
out_dir = "C:/Users/user/Desktop/URDFly/output"

os.makedirs(out_dir, exist_ok=True)

doc = FreeCAD.newDocument("Robot")
Import.insert(step_path, doc.Label)
doc.recompute()

print("Objects: " + str(len(doc.Objects)))

meshes = []
for i, obj in enumerate(doc.Objects):
    if hasattr(obj, "Shape") and obj.Shape.Volume > 1e-10:
        name = "part_" + str(i)
        stl_path = os.path.join(out_dir, name + ".stl")
        print("  mesh: " + obj.Label)
        mesh = Mesh.Mesh(obj.Shape.tessellate(0.5))
        mesh.write(stl_path)
        meshes.append(name)
    else:
        print("  skip: " + obj.Label)

if meshes:
    lines = ['<?xml version="1.0"?>', '<robot name="RB10">']
    for i, name in enumerate(meshes):
        lines.append('  <link name="link_' + str(i) + '">')
        lines.append('    <visual>')
        lines.append('      <geometry>')
        lines.append('        <mesh filename="' + name + '.stl" scale="1 1 1"/>')
        lines.append('      </geometry>')
        lines.append('    </visual>')
        lines.append('    <collision>')
        lines.append('      <geometry>')
        lines.append('        <mesh filename="' + name + '.stl" scale="1 1 1"/>')
        lines.append('      </geometry>')
        lines.append('    </collision>')
        lines.append('  </link>')
        if i > 0:
            lines.append('  <joint name="joint_' + str(i) + '" type="fixed">')
            lines.append('    <parent link="link_' + str(i-1) + '"/>')
            lines.append('    <child link="link_' + str(i) + '"/>')
            lines.append('    <origin xyz="0 0 0" rpy="0 0 0"/>')
            lines.append('  </joint>')
    lines.append('</robot>')

    urdf_path = os.path.join(out_dir, "robot.urdf")
    with open(urdf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("OK: " + urdf_path)
    print("STL in: " + out_dir)
else:
    print("ERROR: no meshes created")

FreeCAD.closeDocument("Robot")
