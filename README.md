# RB10-1300E (Rainbow Robotics 협동로봇) STEP → URDF 변환 가이드

> 최종 업데이트: 2026-05-21  
> 작업 위치: `C:\Users\user\Desktop\URDFly`

https://github.com/Democratizing-Dexterous/URDFly

---

## 목차

1. [전체 워크플로우 개요](#1-전체-워크플로우-개요)
2. [설치된 도구](#2-설치된-도구)
3. [생성한 스크립트 목록](#3-생성한-스크립트-목록)
4. [STEP → STL → URDF 상세 과정](#4-step--stl--urdf-상세-과정)
5. [생성된 출력 파일](#5-생성된-출력-파일)
6. [URDFly 사용법](#6-urdfly-사용법)
7. [URDF 구조 설명](#7-urdf-구조-설명)
8. [추후 개선 사항](#8-추후-개선-사항)
9. [문제 해결](#9-문제-해결)

---

## 1. 전체 워크플로우 개요

```
STEP 파일 (RB10-1300E.stp)
    │
    ▼
[1] freecadcmd 로 STEP 로드
    │  - Import.insert() 로 85개 객체 불러오기
    │  - 객체명: RB10-1300E_BASE, LINK1~LINK6, LINK001~LINK029, Origin, 축 등
    ▼
[2] 링크 그룹핑
    │  - BASE          → base_link
    │  - LINK1         → link_1 (숄더)
    │  - LINK3         → link_2 (상완)  ← ※ LINK2는 LINK1의 서브어셈블리
    │  - LINK4         → link_3 (엘보)
    │  - LINK5         → link_4 (전완)
    │  - LINK6         → link_5 (리스트)
    │  - LINK001~029   → 각 링크의 서브컴포넌트 (볼트, 커버 등)
    │  - Origin/X/Y/Z  → 기준 좌표계 (참조용)
    ▼
[3] STL 메시 내보내기
    │  - 각 링크 메인 바디를 tessellate(0.5) 로 STL 변환
    │  - 서브컴포넌트는 추후 병합 가능 (trimesh)
    ▼
[4] URDF 생성
    │  - 5개 revolute 조인트 + base_link
    │  - joint origin = 부모 링크 기준 자식 링크의 상대 위치
    │  - 회전축: Z/Y/Y/Z/Y 순 (일반적 6축 협동로봇 패턴)
    ▼
[5] URDFly 로 시각화 및 편집
```

---

## 2. 설치된 도구

| 도구 | 용도 | 위치 |
|---|---|---|
| **FreeCAD 1.1.1** | STEP 파일 읽기 및 STL 변환 | `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` |
| **Python 3.x** | URDF 생성 스크립트 | 시스템 PATH |
| **URDFly** | URDF 시각화 및 편집 GUI | `C:\Users\user\Desktop\URDFly\main.py` |
| **trimesh** | STL 메시 병합 (Python 라이브러리) | pip 설치 완료 |

### FreeCAD 실행 파일 구분

| 실행 파일 | 용도 |
|---|---|
| `freecad.exe` | GUI 모드 (화면 있음) |
| `freecadcmd.exe` | 콘솔 모드 (화면 없음, 스크립트 자동 실행) |

> ⚠️ `freecad.exe -c script.py` 는 콘솔만 열고 스크립트를 실행하지 않습니다.  
> **반드시 `freecadcmd.exe` 를 사용해야 합니다.**

---

## 3. 생성한 스크립트 목록

모든 스크립트는 `C:\Users\user\Desktop\URDFly\` 에 있습니다.

### 3.1 `step2urdf_full.py` — 통합 변환 스크립트

STEP을 직접 읽어 링크별 STL을 생성합니다.

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" step2urdf_full.py
```

**동작 과정:**
1. STEP 파일 로드
2. 객체명 패턴(`BASE`, `LINK\d+`)으로 링크 그룹 자동 분류
3. 각 링크의 메인 바디를 STL로 내보내기
4. 결과 → `output2/` 폴더

### 3.2 `step2urdf_simple.py` — 단순 변환 (메인 바디만)

링크별 메인 바디만 추출. 서브컴포넌트 제외. (가장 빠름)

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" step2urdf_simple.py
```

### 3.3 `analyze_assembly.py` — STEP 어셈블리 분석

링크 계층 구조와 각 파트의 Placement(위치) 를 텍스트 파일로 출력합니다.

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" analyze_assembly.py
```

출력: `output/assembly_hierarchy.txt`, `output/joint_origins.txt`

### 3.4 `run_convert.py` — 1차 변환 (전체 객체 → part_N.stl)

STEP의 모든 객체를 순서대로 `part_0.stl` ~ `part_N.stl` 로 내보냅니다.  
(37개 STL 파일 생성 — 서브컴포넌트 포함)

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" run_convert.py
```

### 3.5 `generate_rb10_urdf.py` — URDF 생성기 (trimesh 병합)

`run_convert.py` 로 만든 `part_*.stl` 파일들을 읽어 trimesh로 병합하고 URDF 생성.

```powershell
python generate_rb10_urdf.py
```

### 3.6 `generate_urdf.py` — URDF 최종 생성

`output2/` 의 STL 파일들에 맞춰 URDF를 생성합니다.

```powershell
python generate_urdf.py
```

---

## 4. STEP → STL → URDF 상세 과정

### 4.1 STEP 파일 구조 분석 결과

`RB10-1300E.stp` 파일은 총 **85개 객체**로 구성:

| 객체명 | 설명 | 볼륨 (mm³) |
|---|---|---|
| `RB10-1300E` | 최상위 어셈블리 (컨테이너) | — |
| `RB10-1300E_BASE` | 베이스 (고정부) | 1,908,041 |
| `RB10-1300E_LINK1` | 링크 1 본체 (숄더) | 3,678,979 |
| `RB10-1300E_LINK2` | LINK1 서브어셈블리에 포함 | 5,413,453 |
| `RB10-1300E_LINK3` | 링크 2 본체 (상완) | 3,076,216 |
| `RB10-1300E_LINK4` | 링크 3 본체 (엘보) | 540,847 |
| `RB10-1300E_LINK5` | 링크 4 본체 (전완) | 540,847 |
| `RB10-1300E_LINK6` | 링크 5 본체 (리스트) | 281,068 |
| `RB10-1300E_LINK001~029` | 서브컴포넌트들 | 670 ~ 10,909,299 |
| `Origin`, `X-axis`, `Y-axis`, `Z-axis`, `XY-plane` 등 | 기준 좌표계 | 참조 형상 |

> ⚠️ LINK2는 숫자와 달리 LINK3~LINK6 과 동등한 링크가 아니라  
> LINK1 어셈블리 내부에 속한 서브컴포넌트입니다.  
> 실제 관절 구조: LINK1 → LINK3 → LINK4 → LINK5 → LINK6

### 4.2 조인트 위치 (상대 좌표)

분석 결과 추출한 각 링크 간 상대 위치:

| 조인트 | 기준 링크 | 대상 링크 | 상대 위치 (xyz, mm) | 회전축 |
|---|---|---|---|---|
| joint_1 | base_link | link_1 | (300.0, 187.5, 187.5) | Z (0 0 1) |
| joint_2 | link_1 | link_2 | (0.0, 1099.4, -76.6) | Y (0 1 0) |
| joint_3 | link_2 | link_3 | (-100.0, 10.7, 42.9) | Y (0 1 0) |
| joint_4 | link_3 | link_4 | (200.0, 106.5, 10.7) | Z (0 0 1) |
| joint_5 | link_4 | link_5 | (-100.0, 5.9, -99.5) | Y (0 1 0) |

---

## 5. 생성된 출력 파일

### `output/` 폴더 — 1차 변환 결과 (전체 객체)

```
C:\Users\user\Desktop\URDFly\output\
├── part_0.stl    ~ part_76.stl   (37개 STL 파일)
├── robot.urdf                      (1차 URDF, fixed joint)
├── assembly_hierarchy.txt          (어셈블리 분석 결과)
└── joint_origins.txt               (조인트 위치 분석)
```

### `output2/` 폴더 — 최종 URDF

```
C:\Users\user\Desktop\URDFly\output2\
├── base_link.stl   (6,204 KB) — 베이스
├── link_1.stl      (3,127 KB) — 숄더
├── link_2.stl      ( 491 KB) — 상완
├── link_3.stl      ( 206 KB) — 엘보
├── link_4.stl      ( 206 KB) — 전완
├── link_5.stl      (1,452 KB) — 리스트
└── rb10.urdf                  — 최종 URDF (5축 revolute)
```

---

## 6. URDFly 사용법

### 6.1 실행

```powershell
cd C:\Users\user\Desktop\URDFly
python main.py
```

### 6.2 URDF 불러오기

| 방법 | 조작 |
|---|---|
| 드래그앤드롭 | `output2/rb10.urdf` 파일을 URDFly 창에 끌어다 놓기 |
| 메뉴 | `File → Open` → `output2/rb10.urdf` 선택 |
| CLI | `python main.py output2/rb10.urdf` |

### 6.3 화면 조작

| 조작 | 기능 |
|---|---|
| 마우스 좌클릭 + 드래그 | 회전 |
| 마우스 우클릭 + 드래그 | 팬 |
| 마우스 휠 | 확대/축소 |
| 좌측 링크 리스트 클릭 | 해당 링크 하이라이트 |

### 6.4 주요 기능 버튼

| 버튼 | 기능 |
|---|---|
| **Edit URDF** | XML 편집기 열기 — URDF 속성 직접 수정 |
| **MDH** | Modified Denavit-Hartenberg 파라미터 변환 |
| **Simplify** | 메시 폴리곤 수 줄이기 (단순화) |
| **Show Axes** | 각 링크의 좌표축 표시 |
| **Collision** | collision mesh 표시 |

### 6.5 XML 편집기로 조인트 조정

`Edit URDF` 버튼을 누르면 URDF의 XML을 직접 편집할 수 있습니다.

```xml
<!-- 조인트 위치 수정 예시 -->
<joint name="joint_1" type="revolute">
    <parent link="base_link"/>
    <child link="link_1"/>
    <origin xyz="300.0 187.5 187.5" rpy="0 0 0"/>   <!-- ← 위치 조정 -->
    <axis xyz="0 0 1"/>                               <!-- ← 회전축 조정 -->
    <limit lower="-3.1416" upper="3.1416" effort="100" velocity="1"/>
</joint>
```

---

## 7. URDF 구조 설명

### URDF 기본 개념

```
<link> : 로봇의 각 파트 (강체)
<joint> : 링크 간 연결 관계 (관절)
```

### RB10 URDF 구조 (트리)

```
base_link (세계 좌표계에 고정)
  └── joint_1 (revolute, Z축 회전)
       └── link_1 (숄더)
            └── joint_2 (revolute, Y축 회전)
                 └── link_2 (상완)
                      └── joint_3 (revolute, Y축 회전)
                           └── link_3 (엘보)
                                └── joint_4 (revolute, Z축 회전)
                                     └── link_4 (전완)
                                          └── joint_5 (revolute, Y축 회전)
                                               └── link_5 (리스트)
```

### 파일 참조 방식

URDF의 `<mesh filename="...">` 는 URDF 파일 **기준 상대 경로**로 STL을 찾습니다.

```
output2/
├── rb10.urdf          ← 이 파일에서 "base_link.stl" 참조
├── base_link.stl      ← 같은 폴더에 있어야 함
├── link_1.stl
└── ...
```

---

## 8. 추후 개선 사항

### 8.1 서브컴포넌트 병합

현재는 각 링크의 메인 바디만 포함되어 있습니다.  
더 정밀한 모델링을 위해 서브컴포넌트(볼트, 커버 등)를 병합하려면:

```python
import trimesh
import os

OUT = r"C:\Users\user\Desktop\URDFly\output2"

# link_1: 메인 STL + 서브컴포넌트 병합 예시
main = trimesh.load(os.path.join(OUT, "link_1.stl"))
sub_parts = ["part_3.stl", "part_4.stl", "part_5.stl"]  # output/ 폴더에서

meshes = [main]
for p in sub_parts:
    path = os.path.join(r"C:\Users\user\Desktop\URDFly\output", p)
    if os.path.exists(path):
        meshes.append(trimesh.load(path))

merged = trimesh.util.concatenate(meshes)
merged.export(os.path.join(OUT, "link_1_merged.stl"))
```

### 8.2 정확한 회전축 설정

STEP 파일 내부의 Origin, X/Y/Z-axis 참조 형상을 분석하여  
각 조인트의 실제 회전축 방향을 정확히 설정할 수 있습니다.

### 8.3 6축 완성

LINK6 이후의 추가 파트(`RB10-1300E` 마지막 바디)를 찾아 link_6로 추가하면  
6자유도 완전체 URDF가 됩니다.

### 8.4 관성(Inertia) 값

현재는 가상의 값(`mass="1.0"`, `ixx="0.01"`)을 사용 중입니다.  
실제 시뮬레이션을 위해서는 FreeCAD에서 각 링크의 질량과 관성 모멘트를 계산하여 반영해야 합니다.

### 8.5 메시 최적화

고폴리곤 메시는 시뮬레이션 성능을 저하시킵니다.  
URDFly의 `Simplify` 버튼이나 MeshLab으로 폴리곤 수를 줄일 수 있습니다.

---

## 9. 문제 해결

### 9.1 freecadcmd.exe 에서 "WinError 183" 오류

**증상:** STEP 파일 처리 중 `파일이 이미 있으므로 만들 수 없습니다` 오류

**원인:** FreeCAD 1.1 Windows 버전에서 `freecadcmd.exe` 가 추가 인자를 파일로 잘못 처리

**해결:** 스크립트 내에 경로를 하드코딩하고 추가 인자 없이 실행

```powershell
# ❌ 오류 발생
freecadcmd.exe script.py input.stp output/

# ✅ 정상 동작
freecadcmd.exe script.py                (경로는 스크립트 내부에)
```

### 9.2 ImportGui 는 콘솔 모드에서 사용 불가

**증상:** `ModuleNotFoundError: No module named 'ImportGui'`

**해결:** `ImportGui.insert()` 대신 `Import.insert()` 사용

### 9.3 freecad.exe -c 가 스크립트를 실행하지 않음

**증상:** FreeCAD 콘솔만 열리고 아무 일도 안 일어남

**해결:** `freecadcmd.exe` 사용

```powershell
# ❌
& "C:\Program Files\FreeCAD 1.1\bin\freecad.exe" -c script.py

# ✅
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" script.py
```

### 9.4 URDFly 에서 메시가 안 보임

**원인:** URDF의 `<mesh filename>` 경로가 STL 파일 위치와 일치하지 않음

**해결:** URDF 파일과 STL 파일을 **같은 폴더**에 두고, filename에는 파일명만 적기

---

## 부록: 빠른 실행 요약

```powershell
# === 최초 1회: FreeCAD로 STEP → STL 변환 ===
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" step2urdf_full.py

# === STL → URDF 생성 ===
python generate_urdf.py

# === URDFly 실행 ===
python main.py
# → File → Open → output2/rb10.urdf

# === (선택) 어셈블리 분석 ===
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" analyze_assembly.py
# → output/assembly_hierarchy.txt 확인
```

---

> **참고 리소스**  
> - URDFly: https://github.com/Democratizing-Dexterous/URDFly  
> - FreeCAD: https://www.freecad.org  
> - URDF 스펙: http://wiki.ros.org/urdf  
> - 현대로보틱스 RB10: https://www.hyundai-robot.com
