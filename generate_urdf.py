import os

OUT_DIR = "C:/Users/user/Desktop/URDFly/output2"
LINK_ORDER = ["base_link", "link_1", "link_2", "link_3", "link_4", "link_5"]

JOINT_DATA = [
    {
        "name": "joint_1", "type": "revolute",
        "parent": "base_link", "child": "link_1",
        "xyz": "300.0 187.5 187.5",
        "rpy": "0 0 0", "axis": "0 0 1",
        "lower": "-3.1416", "upper": "3.1416",
    },
    {
        "name": "joint_2", "type": "revolute",
        "parent": "link_1", "child": "link_2",
        "xyz": "0.0 1099.3871 -76.6",
        "rpy": "0 0 0", "axis": "0 1 0",
        "lower": "-2.0944", "upper": "2.0944",
    },
    {
        "name": "joint_3", "type": "revolute",
        "parent": "link_2", "child": "link_3",
        "xyz": "-100.0 10.6508 42.8871",
        "rpy": "0 0 0", "axis": "0 1 0",
        "lower": "-2.0944", "upper": "2.0944",
    },
    {
        "name": "joint_4", "type": "revolute",
        "parent": "link_3", "child": "link_4",
        "xyz": "200.0 106.4992 10.6508",
        "rpy": "0 0 0", "axis": "0 0 1",
        "lower": "-3.1416", "upper": "3.1416",
    },
    {
        "name": "joint_5", "type": "revolute",
        "parent": "link_4", "child": "link_5",
        "xyz": "-100.0 5.9258 -99.5",
        "rpy": "0 0 0", "axis": "0 1 0",
        "lower": "-2.0944", "upper": "2.0944",
    },
]

urdf_path = os.path.join(OUT_DIR, "rb10.urdf")
with open(urdf_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<robot name="RB10_1300E">\n')

    for ln in LINK_ORDER:
        f.write(f'\n  <link name="{ln}">\n')
        f.write(f'    <visual>\n')
        f.write(f'      <geometry>\n')
        f.write(f'        <mesh filename="{ln}.stl" scale="1 1 1"/>\n')
        f.write(f'      </geometry>\n')
        f.write(f'    </visual>\n')
        f.write(f'    <collision>\n')
        f.write(f'      <geometry>\n')
        f.write(f'        <mesh filename="{ln}.stl" scale="1 1 1"/>\n')
        f.write(f'      </geometry>\n')
        f.write(f'    </collision>\n')
        f.write(f'    <inertial>\n')
        f.write(f'      <mass value="1.0"/>\n')
        f.write(f'      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>\n')
        f.write(f'    </inertial>\n')
        f.write(f'  </link>\n')

    for j in JOINT_DATA:
        f.write(f'\n  <joint name="{j["name"]}" type="{j["type"]}">\n')
        f.write(f'    <parent link="{j["parent"]}"/>\n')
        f.write(f'    <child link="{j["child"]}"/>\n')
        f.write(f'    <origin xyz="{j["xyz"]}" rpy="{j["rpy"]}"/>\n')
        f.write(f'    <axis xyz="{j["axis"]}"/>\n')
        f.write(f'    <limit lower="{j["lower"]}" upper="{j["upper"]}" effort="100" velocity="1"/>\n')
        f.write(f'  </joint>\n')

    f.write('\n</robot>\n')

print(f"URDF: {urdf_path}")
print(f"STL: {OUT_DIR}")
print("Files:")
for ln in LINK_ORDER:
    stl = os.path.join(OUT_DIR, f"{ln}.stl")
    sz = os.path.getsize(stl)
    print(f"  {ln}.stl ({sz//1024} KB)")
print(f"  rb10.urdf")
