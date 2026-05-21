"""
RB10-1300E URDF Generator
STEP → STL 변환 결과물로부터 6축 로봇 URDF를 생성합니다.
생성된 URDF는 URDFly GUI(main.py)로 열어서 확인/편집할 수 있습니다.

1. 먼저 run_convert.py 로 STL 파일 생성 (이미 완료)
2. 이 스크립트 실행: python generate_rb10_urdf.py
3. 생성된 output/rb10.urdf를 URDFly로 열기
"""

import os
import trimesh
import numpy as np

OUT_DIR = "C:/Users/user/Desktop/URDFly/output"

# =====================================================
# 링크/조인트 정의 (분석 결과 기반)
# =====================================================

# 각 메인 링크에 속하는 STL 파일 목록
# LINK1 = RB10-1300E_LINK1 + LINK001~LINK009 (서브컴포넌트)
# LINK2 = RB10-1300E_LINK2 + LINK010~LINK017
# LINK3 = RB10-1300E_LINK3 + LINK018~LINK021
# LINK4 = RB10-1300E_LINK4 + LINK022~LINK025
# LINK5 = RB10-1300E_LINK5 + LINK026~LINK029
# LINK6 = RB10-1300E_LINK6

LINK_PARTS = {
    "base_link": ["part_0"],  # RB10-1300E_BASE
    "link_1":    ["part_1"],  # RB10-1300E_LINK1 (main)
    "link_2":    ["part_2"],  # RB10-1300E_LINK2 (main)
    "link_3":    ["part_12"], # RB10-1300E_LINK3 (main)
    "link_4":    ["part_14"], # RB10-1300E_LINK4 (main)
    "link_5":    ["part_19"], # RB10-1300E_LINK5 (main)
    "link_6":    ["part_25"], # RB10-1300E_LINK6 (main)
}

# 어셈블리 분석으로 추출한 조인트 상대 위치 (mm)
# parent → child 의 origin xyz
JOINT_DATA = [
    {
        "name": "joint_1",
        "type": "revolute",
        "parent": "base_link",
        "child": "link_1",
        "xyz": "300.0 40.7565 0.0",
        "rpy": "0 0 0",
        "axis": "0 0 1",
        "limit_lower": "-3.1416",
        "limit_upper": "3.1416",
    },
    {
        "name": "joint_2",
        "type": "revolute",
        "parent": "link_1",
        "child": "link_2",
        "xyz": "0.0 187.5 187.5",
        "rpy": "0 0 0",
        "axis": "0 1 0",
        "limit_lower": "-2.0944",
        "limit_upper": "2.0944",
    },
    {
        "name": "joint_3",
        "type": "revolute",
        "parent": "link_2",
        "child": "link_3",
        "xyz": "0.0 1099.3871 -76.6",
        "rpy": "0 0 0",
        "axis": "0 1 0",
        "limit_lower": "-2.0944",
        "limit_upper": "2.0944",
    },
    {
        "name": "joint_4",
        "type": "revolute",
        "parent": "link_3",
        "child": "link_4",
        "xyz": "-100.0 10.6508 42.8871",
        "rpy": "0 0 0",
        "axis": "0 0 1",
        "limit_lower": "-3.1416",
        "limit_upper": "3.1416",
    },
    {
        "name": "joint_5",
        "type": "revolute",
        "parent": "link_4",
        "child": "link_5",
        "xyz": "200.0 106.4992 10.6508",
        "rpy": "0 0 0",
        "axis": "0 1 0",
        "limit_lower": "-2.0944",
        "limit_upper": "2.0944",
    },
    {
        "name": "joint_6",
        "type": "revolute",
        "parent": "link_5",
        "child": "link_6",
        "xyz": "-100.0 5.9258 -99.5",
        "rpy": "0 0 0",
        "axis": "0 0 1",
        "limit_lower": "-3.1416",
        "limit_upper": "3.1416",
    },
]

# 각 링크의 관성 정보 (대략적 추정)
INERTIA_TEMPLATE = {
    "mass": "1.0",
    "ixx": "0.01", "ixy": "0", "ixz": "0",
    "iyy": "0.01", "iyz": "0", "izz": "0.01",
}


def link_name_to_stl(name):
    return f"{name}.stl"


def get_stl_path(part_name):
    return os.path.join(OUT_DIR, f"{part_name}.stl")


def main():
    # 1. 서브컴포넌트 STL을 메인 링크에 병합
    print("=" * 60)
    print("RB10-1300E URDF Generator")
    print("=" * 60)

    # part_0..36 = FreeCAD 객체 순서 (run_convert.py 출력)
    # part_0=BASE, part_1=LINK1, part_12=LINK3, part_14=LINK4, part_19=LINK5, part_25=LINK6

    # sub-component 범위 정의
    SUB_MAP = {
        "link_1": list(range(3, 12)),   # part_3 ~ part_11 (LINK001-009)
        "link_2": [13, 15, 16, 17, 18], # LINK010-017 중 일부
        "link_3": [20, 21, 22, 23],     # LINK018-021
        "link_4": [24],                  # LINK022-025 중
        "link_5": [26, 27, 28, 29],     # LINK026-029
        "link_6": [],                    # 서브컴포넌트 없음
        "base_link": [],                 # 서브컴포넌트 없음
    }

    # trimesh로 서브컴포넌트 병합
    os.makedirs(os.path.join(OUT_DIR, "merged"), exist_ok=True)

    print("\n[Mesh Merge]")
    link_stl_map = {}

    for link_name, main_parts in LINK_PARTS.items():
        all_meshes = []

        # 메인 파트 로드
        main_part = main_parts[0]
        stl_path = get_stl_path(main_part)
        if os.path.exists(stl_path):
            mesh = trimesh.load(stl_path)
            if hasattr(mesh, 'vertices'):
                all_meshes.append(mesh)
                print(f"  {link_name}: main = {stl_path} ({len(mesh.vertices)} verts)")
        else:
            print(f"  {link_name}: WARNING main STL not found: {stl_path}")

        # 서브컴포넌트 로드 및 병합
        if link_name in SUB_MAP:
            for idx in SUB_MAP[link_name]:
                sub_path = get_stl_path(f"part_{idx}")
                if os.path.exists(sub_path):
                    sub_mesh = trimesh.load(sub_path)
                    if hasattr(sub_mesh, 'vertices'):
                        all_meshes.append(sub_mesh)
                        print(f"           + sub part_{idx} ({len(sub_mesh.vertices)} verts)")

        if len(all_meshes) >= 1:
            merged = trimesh.util.concatenate(all_meshes)
            merged_path = os.path.join(OUT_DIR, "merged", f"{link_name}.stl")
            merged.export(merged_path)
            link_stl_map[link_name] = merged_path
            print(f"           = merged: {merged_path} ({len(merged.vertices)} verts)")
        else:
            print(f"  {link_name}: ERROR no meshes")

    # 2. URDF 생성
    print("\n[URDF Generation]")

    urdf_path = os.path.join(OUT_DIR, "rb10.urdf")
    with open(urdf_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(f'<robot name="RB10_1300E">\n')

        # 각 링크 정의
        for link_name in LINK_PARTS.keys():
            stl_file = os.path.basename(link_stl_map.get(link_name, ""))
            f.write(f'\n  <link name="{link_name}">\n')
            f.write(f'    <visual>\n')
            f.write(f'      <geometry>\n')
            f.write(f'        <mesh filename="merged/{stl_file}" scale="1 1 1"/>\n')
            f.write(f'      </geometry>\n')
            f.write(f'    </visual>\n')
            f.write(f'    <collision>\n')
            f.write(f'      <geometry>\n')
            f.write(f'        <mesh filename="merged/{stl_file}" scale="1 1 1"/>\n')
            f.write(f'      </geometry>\n')
            f.write(f'    </collision>\n')
            f.write(f'    <inertial>\n')
            f.write(f'      <mass value="{INERTIA_TEMPLATE["mass"]}"/>\n')
            f.write(f'      <inertia ixx="{INERTIA_TEMPLATE["ixx"]}" ixy="{INERTIA_TEMPLATE["ixy"]}" ixz="{INERTIA_TEMPLATE["ixz"]}"')
            f.write(f' iyy="{INERTIA_TEMPLATE["iyy"]}" iyz="{INERTIA_TEMPLATE["iyz"]}" izz="{INERTIA_TEMPLATE["izz"]}"/>\n')
            f.write(f'    </inertial>\n')
            f.write(f'  </link>\n')

        # 각 조인트 정의
        for j in JOINT_DATA:
            f.write(f'\n  <joint name="{j["name"]}" type="{j["type"]}">\n')
            f.write(f'    <parent link="{j["parent"]}"/>\n')
            f.write(f'    <child link="{j["child"]}"/>\n')
            f.write(f'    <origin xyz="{j["xyz"]}" rpy="{j["rpy"]}"/>\n')
            f.write(f'    <axis xyz="{j["axis"]}"/>\n')
            f.write(f'    <limit lower="{j["limit_lower"]}" upper="{j["limit_upper"]}" effort="100" velocity="1"/>\n')
            f.write(f'  </joint>\n')

        f.write(f'\n</robot>\n')

    print(f"\n  URDF: {urdf_path}")
    print(f"\n{'=' * 60}")
    print("DONE")
    print(f"\nURDFly로 열기:")
    print(f"  cd C:\\Users\\user\\Desktop\\URDFly")
    print(f"  python main.py")
    print(f"  → File 메뉴 또는 드래그앤드롭으로 rb10.urdf 열기")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
