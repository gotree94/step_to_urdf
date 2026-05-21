import os, sys, re, FreeCAD, Import, Mesh, Part

STEP_FILE = "C:/Users/user/Desktop/URDFly/RB10-1300E.stp"
OUT_DIR = "C:/Users/user/Desktop/URDFly/output2"
os.makedirs(OUT_DIR, exist_ok=True)

doc = FreeCAD.newDocument("RB10")
Import.insert(STEP_FILE, doc.Label)
doc.recompute()
print(f"Objects: {len(doc.Objects)}")

def get_link_group(label):
    if "BASE" in label:
        return "base_link"
    m = re.search(r'LINK(\d+)', label)
    if not m:
        return None
    n = int(m.group(1))
    if n == 1:
        return "link_1"
    elif 2 <= n <= 9:
        return "link_1"
    elif n == 10:
        return "link_2"
    elif 11 <= n <= 17:
        return "link_2"
    elif n == 18:
        return "link_3"
    elif 19 <= n <= 21:
        return "link_3"
    elif n == 22:
        return "link_4"
    elif 23 <= n <= 25:
        return "link_4"
    elif n == 26:
        return "link_5"
    elif 27 <= n <= 29:
        return "link_5"
    elif 30 <= n <= 36:
        return "link_6"
    return None

link_order = ["base_link", "link_1", "link_2", "link_3", "link_4", "link_5", "link_6"]
link_items = {ln: [] for ln in link_order}

for obj in doc.Objects:
    label = obj.Label
    if not hasattr(obj, "Shape") or obj.Shape.Volume < 1e-10:
        continue
    group = get_link_group(label)
    if group:
        link_items[group].append(obj)
        print(f"  -> {group}: {label} vol={obj.Shape.Volume:.0f}")

import trimesh

link_meshes = {}
link_placements = {}

for ln in link_order:
    objs = link_items[ln]
    if not objs:
        print(f"\n[SKIP] {ln}: no objects")
        continue
    print(f"\n[PROCESS] {ln}: {len(objs)} objects")

    meshes = []
    for obj in objs:
        m = Mesh.Mesh(obj.Shape.tessellate(0.5))
        verts = m.Topology[0]
        facets = m.Topology[1]
        pts = [[v.x, v.y, v.z] for v in verts]
        tri = [[int(t[0]), int(t[1]), int(t[2])] for t in facets]
        tmesh = trimesh.Trimesh(vertices=pts, faces=tri)
        meshes.append(tmesh)

    if len(meshes) == 1:
        merged = meshes[0]
    else:
        merged = trimesh.util.concatenate(meshes)

    stl_path = os.path.join(OUT_DIR, f"{ln}.stl")
    merged.export(stl_path)
    link_meshes[ln] = f"{ln}.stl"
    print(f"  STL: {stl_path} ({len(merged.vertices)} verts)")

    main_obj = max(objs, key=lambda o: o.Shape.Volume)
    link_placements[ln] = main_obj.Placement
    p = main_obj.Placement
    print(f"  POS: ({p.Base.x:.1f}, {p.Base.y:.1f}, {p.Base.z:.1f})")

JOINT_CONFIG = [
    ("joint_1", "base_link", "link_1", "revolute", "0 0 1"),
    ("joint_2", "link_1", "link_2", "revolute", "0 1 0"),
    ("joint_3", "link_2", "link_3", "revolute", "0 1 0"),
    ("joint_4", "link_3", "link_4", "revolute", "0 0 1"),
    ("joint_5", "link_4", "link_5", "revolute", "0 1 0"),
    ("joint_6", "link_5", "link_6", "revolute", "0 0 1"),
]

urdf_path = os.path.join(OUT_DIR, "rb10.urdf")
with open(urdf_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<robot name="RB10_1300E">\n')
    for ln in link_order:
        if ln not in link_meshes:
            continue
        stl = link_meshes[ln]
        f.write(f'  <link name="{ln}">\n')
        f.write(f'    <visual><geometry><mesh filename="{stl}" scale="1 1 1"/></geometry></visual>\n')
        f.write(f'    <collision><geometry><mesh filename="{stl}" scale="1 1 1"/></geometry></collision>\n')
        f.write(f'    <inertial><mass value="1.0"/><inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/></inertial>\n')
        f.write(f'  </link>\n')
    for jname, parent, child, jtype, axis in JOINT_CONFIG:
        if parent in link_placements and child in link_placements:
            pp = link_placements[parent].Base
            cp = link_placements[child].Base
            rel = cp - pp
            xyz = f"{rel.x:.4f} {rel.y:.4f} {rel.z:.4f}"
        else:
            xyz = "0 0 0"
        f.write(f'  <joint name="{jname}" type="{jtype}">\n')
        f.write(f'    <parent link="{parent}"/>\n')
        f.write(f'    <child link="{child}"/>\n')
        f.write(f'    <origin xyz="{xyz}" rpy="0 0 0"/>\n')
        f.write(f'    <axis xyz="{axis}"/>\n')
        f.write(f'    <limit lower="-3.1416" upper="3.1416" effort="100" velocity="1"/>\n')
        f.write(f'  </joint>\n')
    f.write('</robot>\n')

print(f"\nURDF: {urdf_path}")
print(f"STLs: {OUT_DIR}")
print("DONE")

FreeCAD.closeDocument("RB10")
