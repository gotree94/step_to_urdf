import os, FreeCAD, Import, Mesh

doc = FreeCAD.newDocument("RB10")
Import.insert("C:/Users/user/Desktop/URDFly/RB10-1300E.stp", doc.Label)
doc.recompute()

OUT = "C:/Users/user/Desktop/URDFly/output2"
os.makedirs(OUT, exist_ok=True)

link_map = {
    "RB10-1300E_BASE": "base_link",
    "RB10-1300E_LINK1": "link_1",
    "RB10-1300E_LINK3": "link_2",
    "RB10-1300E_LINK4": "link_3",
    "RB10-1300E_LINK5": "link_4",
    "RB10-1300E_LINK6": "link_5",
    # LINK2 is sub-component of LINK1 assembly, skip
    # LINK10-17 are sub-components of LINK2, skip
    # etc.
}

placements = {}
for obj in doc.Objects:
    label = obj.Label
    if label not in link_map:
        continue
    link_name = link_map[label]
    if not hasattr(obj, "Shape") or obj.Shape.Volume < 1e-10:
        continue
    mesh = Mesh.Mesh(obj.Shape.tessellate(0.5))
    mesh.write(os.path.join(OUT, f"{link_name}.stl"))
    placements[link_name] = obj.Placement
    p = obj.Placement
    print(f"{label} -> {link_name} ({p.Base.x:.1f}, {p.Base.y:.1f}, {p.Base.z:.1f})")

# Add link_6 manually from remaining large objects
# Find any remaining LINK objects with significant volume
for obj in doc.Objects:
    if obj.Label in link_map:
        continue
    if not hasattr(obj, "Shape") or obj.Shape.Volume < 1e-10:
        continue
    label = obj.Label
    vol = obj.Shape.Volume
    print(f"  leftover: {label} vol={vol:.0f}")

print(f"\nSTLs: {list(placements.keys())}")
FreeCAD.closeDocument("RB10")
