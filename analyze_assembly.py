import os, FreeCAD, Import

step_path = "C:/Users/user/Desktop/URDFly/RB10-1300E.stp"
out_dir = "C:/Users/user/Desktop/URDFly/output"
os.makedirs(out_dir, exist_ok=True)

doc = FreeCAD.newDocument("Analyze")
Import.insert(step_path, doc.Label)
doc.recompute()

log_path = os.path.join(out_dir, "assembly_hierarchy.txt")
with open(log_path, "w", encoding="utf-8") as log:
    log.write(f"Total objects: {len(doc.Objects)}\n\n")
    log.write(f"{'='*80}\n")
    log.write("OBJECT DETAILS\n")
    log.write(f"{'='*80}\n")

    for i, obj in enumerate(doc.Objects):
        label = obj.Label
        has_shape = hasattr(obj, "Shape")
        vol = obj.Shape.Volume if has_shape and obj.Shape.Volume > 1e-10 else 0
        placement = obj.Placement if has_shape else None

        log.write(f"\n[{i:3d}] {label}\n")
        log.write(f"      Type: {obj.TypeId}\n")
        if placement:
            log.write(f"      Pos:  ({placement.Base.x:.4f}, {placement.Base.y:.4f}, {placement.Base.z:.4f})\n")
            r = placement.Rotation
            q = r.Q
            log.write(f"      Quat: ({q[0]:.6f}, {q[1]:.6f}, {q[2]:.6f}, {q[3]:.6f})\n")
            log.write(f"      Euler: ({r.toEuler()[0]:.4f}, {r.toEuler()[1]:.4f}, {r.toEuler()[2]:.4f})\n")
        if has_shape and vol > 0:
            log.write(f"      Volume: {vol:.4f} mm3\n")

        # show InList (parent objects in document tree)
        if hasattr(obj, "InList") and obj.InList:
            log.write(f"      Parents: {[p.Label for p in obj.InList]}\n")
        if hasattr(obj, "OutList") and obj.OutList:
            log.write(f"      Children: {[p.Label for p in obj.OutList]}\n")

    log.write(f"\n{'='*80}\n")
    log.write("GROUP BY PREFIX\n")
    log.write(f"{'='*80}\n")

    groups = {}
    for obj in doc.Objects:
        label = obj.Label
        if label.startswith("RB10-1300E_"):
            suffix = label[len("RB10-1300E_"):]
            # extract main group (BASE, LINK1, LINK2... or just numeric)
            if suffix == "BASE":
                group = "BASE"
            elif suffix.startswith("LINK"):
                rest = suffix[4:]  # after "LINK"
                if rest.isdigit():
                    group = f"LINK{rest}"
                else:
                    group = f"LINK"
            else:
                group = "OTHER"
            if group not in groups:
                groups[group] = []
            groups[group].append(label)

    for g in sorted(groups.keys()):
        items = groups[g]
        log.write(f"\n{g}: {len(items)} objects")
        for item in items:
            log.write(f"\n    - {item}")

log.close()
print(f"Hierarchy log: {log_path}")

# Also extract joint positions between consecutive links
with open(os.path.join(out_dir, "joint_origins.txt"), "w", encoding="utf-8") as f:
    f.write("Joint origin extraction (relative positions between main links)\n")
    f.write("="*60 + "\n\n")

    link_names = ["BASE", "LINK1", "LINK2", "LINK3", "LINK4", "LINK5", "LINK6"]
    link_objs = {}
    for obj in doc.Objects:
        for ln in link_names:
            if obj.Label == f"RB10-1300E_{ln}":
                link_objs[ln] = obj
                break

    # Find the frame/axis reference objects
    for obj in doc.Objects:
        if "Origin" in obj.Label and hasattr(obj, "Placement"):
            f.write(f"[Reference] {obj.Label}: pos=({obj.Placement.Base.x:.4f}, {obj.Placement.Base.y:.4f}, {obj.Placement.Base.z:.4f})\n")
        if "X-axis" in obj.Label and hasattr(obj, "Placement"):
            f.write(f"[Reference] {obj.Label}: pos=({obj.Placement.Base.x:.4f}, {obj.Placement.Base.y:.4f}, {obj.Placement.Base.z:.4f})\n")
        if "Y-axis" in obj.Label and hasattr(obj, "Placement"):
            f.write(f"[Reference] {obj.Label}: pos=({obj.Placement.Base.x:.4f}, {obj.Placement.Base.y:.4f}, {obj.Placement.Base.z:.4f})\n")

    f.write("\n\nMain link positions (absolute):\n")
    for ln in link_names:
        if ln in link_objs:
            obj = link_objs[ln]
            p = obj.Placement
            f.write(f"{ln}: pos=({p.Base.x:.4f}, {p.Base.y:.4f}, {p.Base.z:.4f})\n")

    f.write("\n\nRelative positions (child - parent):\n")
    prev = None
    for ln in link_names:
        if ln in link_objs and prev in link_objs:
            cp = link_objs[ln].Placement.Base
            pp = link_objs[prev].Placement.Base
            rel = cp - pp
            f.write(f"{prev} -> {ln}: ({rel.x:.4f}, {rel.y:.4f}, {rel.z:.4f})\n")
        prev = ln

f.close()
print(f"Joint origins: {os.path.join(out_dir, 'joint_origins.txt')}")

FreeCAD.closeDocument("Analyze")
print("DONE")
