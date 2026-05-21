# Blender + Phobos 로 URDF 생성하기

> 작성일: 2026-05-21

---

## 목차

1. [Phobos란?](#1-phobos란)
2. [설치 방법](#2-설치-방법)
3. [STEP → Blender 워크플로우 개요](#3-step--blender-워크플로우-개요)
4. [Phobos 기본 개념](#4-phobos-기본-개념)
5. [URDF 생성 상세 워크플로우](#5-urdf-생성-상세-워크플로우)
6. [고급 기능](#6-고급-기능)
7. [CLI (Command Line Interface) 사용법](#7-cli-command-line-interface-사용법)
8. [문제 해결](#8-문제-해결)
9. [참고 링크](#9-참고-링크)

---

## 1. Phobos란?

**Phobos**는 독일 인공지능 연구소(DFKI)와 브레멘 대학이 개발한 **오픈소스 로봇 모델링 툴**입니다.

| 항목 | 내용 |
|---|---|
| **개발 기관** | DFKI Robotics Innovation Center, University of Bremen |
| **라이선스** | LGPL (오픈소스, 완전 무료) |
| **최신 버전** | v2.0.0 (코드명 "Perilled Pangolin") |
| **대상 Blender** | **Blender v3.3 LTS** (권장) |
| **GitHub** | https://github.com/dfki-ric/phobos |
| **Stars** | ⭐ 886 |

### Phobos가 제공하는 것

Phobos는 두 가지 형태로 제공됩니다:

| 형태 | 용도 |
|---|---|
| **Blender Add-on** | GUI 환경에서 WYSIWYG 로봇 모델 편집 |
| **Python CLI** | CI/CD 파이프라인에서 자동화 처리 |

### 지원하는 입출력 포맷

| 포맷 | 가져오기(Import) | 내보내기(Export) |
|---|---|---|
| **URDF** | ✅ | ✅ |
| **SDF** | ✅ | ✅ |
| **SMURF** | ✅ | ✅ |
| **STL** | Blender 기본 | ✅ |
| **OBJ** | Blender 기본 | ✅ |
| **DAE (Collada)** | Blender 기본 | ✅ |

> ⚠️ STEP 파일은 Blender가 **직접 읽을 수 없습니다.**  
> FreeCAD 등에서 STL/OBJ로 변환한 후 Blender로 가져와야 합니다.

---

## 2. 설치 방법

### 2.1 사전 준비

| 요구사항 | 상세 |
|---|---|
| **Blender v3.3 LTS** | Phobos 2.0 공식 타겟 (최신 Blender에서도 작동 가능) |
| **Python 3.10+** | Blender 내장 Python 사용 |
| **Windows / Linux / macOS** | 모두 지원 |

#### Blender v3.3 LTS 다운로드

https://www.blender.org/download/lts/3-3/

> Blender 4.x에서도 Phobos가 동작할 수 있지만, 공식 지원은 v3.3 LTS입니다.

### 2.2 방법 A: Blender Add-on 설치 (권장)

가장 간단한 방법입니다.

```text
1. Blender 실행
2. 메뉴: Edit → Preferences → Add-ons
3. 우측 상단 ▼ 버튼 → Install from Repository...
   (또는 "Install..." 버튼)
4. Phobos GitHub 저장소에서 ZIP 다운로드
   https://github.com/dfki-ric/phobos/archive/refs/heads/master.zip
5. 다운로드한 ZIP 파일 선택
6. 검색창에 "Phobos" 입력
7. 체크박스 클릭하여 Add-on 활성화
8. (선택) Save Preferences
```

#### 상세 경로 (Windows)

Blender Add-on 설치 폴더:
```
C:\Users\<사용자명>\AppData\Roaming\Blender Foundation\Blender\3.3\scripts\addons\
```

수동 설치 시 이 폴더에 `phobos-master` 폴더를 복사한 후, Blender Add-on 설정에서 활성화해도 됩니다.

### 2.3 방법 B: pip 설치 (CLI 전용)

CLI 도구만 필요한 경우 pip로 설치 가능합니다.

```bash
pip install phobos
```

또는 GitHub에서 직접:

```bash
pip install git+https://github.com/dfki-ric/phobos.git
```

### 2.4 설치 확인

Blender 실행 후 `3D Viewport` 우측 패널에 **Phobos** 탭이 나타나면 설치 완료입니다.

```
3D Viewport 영역에서 키보드 N 키 → 우측 패널 → "Phobos" 탭 확인
```

---

## 3. STEP → Blender 워크플로우 개요

Phobos는 STEP 파일을 직접 읽을 수 없으므로, 아래 경로를 거쳐야 합니다.

```
방법 1: FreeCAD 경유 (권장)
  STEP 파일
    ↓ (FreeCAD)
  STL 파일 (링크별로 분리)
    ↓ (Blender Import)
  Blender Scene
    ↓ (Phobos)
  URDF


방법 2: Online Converter 경유
  STEP 파일
    ↓ (step2urdf.top 등)
  STL 파일
    ↓ (Blender Import)
  Blender Scene
    ↓ (Phobos)
  URDF


방법 3: CAD Import Add-on (유료)
  STEP 파일
    ↓ (Blender CAD Import Add-on)
  Blender Scene (직접 STEP 불러오기)
    ↓ (Phobos)
  URDF
```

> **추천:** FreeCAD로 STEP → STL 변환 후 Blender/Phobos로 가져오는 방법이  
> 가장 안정적이고 비용이 들지 않습니다.

---

## 4. Phobos 기본 개념

Phobos는 Blender의 **Armature(뼈대)** 시스템을 기반으로 로봇 모델을 표현합니다.

```
Blender 개념          →  URDF 개념
─────────────────────────────────────
Armature (Object)     →  robot
Bone (뼈)             →  joint
Object (메시 오브젝트)  →  link (visual + collision)
Phobos Tag 속성        →  URDF 속성 (질량, 관성 등)
```

### Phobos 요소 구성

```
Robot Model (Phobos Scene Root)
├── Joint (Blender Bone)
│   ├── Parent Link (메시 Object)
│   │   ├── Visual Mesh (STL/OBJ)
│   │   ├── Collision Mesh
│   │   └── Inertial (COM 표시자)
│   └── Child Link (메시 Object) ...
```

### Phobos 패널 (Blender 우측, N 키)

Phobos를 활성화하면 Blender 화면 우측에 전용 패널이 나타납니다:

| 섹션 | 기능 |
|---|---|
| **Scene** | 로봇 이름, 모델 속성 |
| **Object** | 선택된 객체의 URDF 속성 |
| **Bone** | 선택된 뼈대의 조인트 속성 |
| **Tools** | 자동화 도구 모음 |
| **Export** | URDF/SDF/SMURF 내보내기 |

---

## 5. URDF 생성 상세 워크플로우

### 5.1 사전 준비: STEP → STL 변환

FreeCAD로 STEP 파일에서 링크별 STL 분리:

```bash
# 이미 만들어 둔 스크립트 사용
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" step2urdf_full.py
# → output2/base_link.stl, link_1.stl, ... link_5.stl
```

또는 Blender 내에서 개별 STL로 가져올 수 있도록 준비합니다.

### 5.2 Blender에서 STL 가져오기

```text
1. Blender 실행 (시작 Scene의 큐브는 삭제: X 키)
2. File → Import → STL (.stl)
3. 첫 번째 링크 STL 선택 (예: base_link.stl)
4. 필요에 따라 Scale, 위치 조정
5. 모든 링크에 대해 반복 (File → Import → STL)
```

> **팁:** 모든 STL을 한 번에 Import 하려면 여러 파일을 Shift+클릭으로 선택 가능합니다.

### 5.3 Armature(뼈대) 생성

Phobos를 사용하여 로봇의 관절 구조를 정의합니다.

```text
1. Blender 우측 패널에서 "Phobos" 탭 선택
2. Scene 패널에서 "Initialize Robot Model" 버튼 클릭
   → 자동으로 Armature(Object)가 생성됨
3. 로봇 이름 설정 (예: RB10_1300E)
```

또는 수동으로 생성:

```text
1. Add → Armature → Single Bone
2. Armature 이름을 로봇 이름으로 변경
3. Edit Mode(Tab)에서 Bone을 관절 위치에 배치
4. 각 Bone의 이름을 조인트 이름으로 설정 (예: joint_1, joint_2...)
5. Object Mode로 복귀
```

### 5.4 링크-조인트 연결 (부모-자식 관계 설정)

Phobos는 Blender의 **Bone(뼈대)** 계층 구조로 URDF의 joint tree를 표현합니다.

#### 계층 구조 설정

```text
1. Scene 패널에서 "Create Robot Scene" 실행
2. Armature 선택 → Edit Mode(Tab)
3. Bone 선택 → G 키로 관절 위치로 이동
4. Bone 계층 구조:
   - base_link (Armature 자체)
   - └── joint_1 (Bone)
   -     └── link_1 (Object, Bone에 Child of Constraint)
   -         └── joint_2 (Bone)
   -             └── link_2 (Object)
   -                 └── joint_3 ...
```

#### Object를 Bone에 연결

```text
1. 링크 메시(Object) 선택
2. Shift+클릭으로 대상 Bone이 속한 Armature 선택
3. Ctrl+P → "Bone" 선택 (Parent to Bone)
4. 또는 Phobos Tools 패널의 "Parent Selected to Bone" 버튼 사용
```

### 5.5 URDF 속성 설정

Phobos 패널에서 각 요소의 URDF 속성을 설정합니다.

#### 링크 속성 (Object 선택 시)

| Phobos 패널 항목 | URDF 요소 | 설명 |
|---|---|---|
| Link Name | `<link name="...">` | 링크 이름 |
| Visual Mesh | `<mesh filename="...">` | 시각용 메시 파일 |
| Collision Mesh | `<mesh filename="...">` | 충돌용 메시 |
| Mass | `<mass value="...">` | 질량 (kg) |
| Inertia | `<inertia ixx="..." ...>` | 관성 모멘트 |
| COM | `<origin xyz="..." rpy="..."/>` | 무게중심 위치 |

#### 조인트 속성 (Bone 선택 시)

| Phobos 패널 항목 | URDF 요소 | 설명 |
|---|---|---|
| Joint Name | `<joint name="...">` | 조인트 이름 |
| Joint Type | `type="..."` | revolute, prismatic, fixed 등 |
| Parent Link | `<parent link="...">` | 부모 링크 |
| Child Link | `<child link="...">` | 자식 링크 |
| Axis | `<axis xyz="..."/>` | 회전/이동 축 방향 |
| Lower Limit | `<limit lower="..."/>` | 최소 각도 (rad) |
| Upper Limit | `<limit upper="..."/>` | 최대 각도 (rad) |
| Effort | `<limit effort="..."/>` | 최대 토크 |
| Velocity | `<limit velocity="..."/>` | 최대 속도 |

### 5.6 Collision Mesh 자동 생성

Phobos는 Visual Mesh로부터 Collision Mesh를 자동 생성할 수 있습니다.

```text
1. 대상 링크 Object 선택
2. Phobos → Tools → "Generate Collision" 버튼
   - 옵션: "Convex Hull" (볼록 껍질) 또는 "Primitive" (박스/구/실린더)
3. (선택) Decimation Modifier로 폴리곤 수 감소
```

### 5.7 Inertia 자동 계산

Phobos는 메시 형상과 밀도로부터 관성 텐서를 자동 계산합니다.

```text
1. 대상 링크 Object 선택
2. Phobos → Tools → "Calculate Inertia" 버튼
3. 밀도 값 입력 (예: steel = 7800 kg/m³)
   또는 질량 직접 입력
4. COM(무게중심) 위치 확인 및 조정
```

### 5.8 URDF 내보내기

```text
1. Phobos → Export 패널
2. Export Format: "URDF" 선택
3. Export Path: 출력 폴더 지정 (예: C:\Users\user\Desktop\URDFly\phobos_output)
4. Mesh Format: "STL" (또는 OBJ, DAE)
5. 옵션:
   - [x] Export collision meshes
   - [x] Export inertial data
   - [ ] Use relative paths
   - Precision: 6 (소수점 자리수)
6. "Export" 버튼 클릭
```

#### 출력 구조

```
phobos_output/
├── robot.urdf
├── meshes/
│   ├── base_link.stl
│   ├── link_1.stl
│   ├── link_2.stl
│   ├── ...
│   ├── base_link_collision.stl
│   └── ...
└── (선택) config/  (ROS 패키지 설정)
```

### 5.9 내보낸 URDF 검증

```bash
# URDF 구문 체크
python -c "from xml.etree import ElementTree as ET; ET.parse('robot.urdf')"

# ROS가 설치되어 있다면
check_urdf robot.urdf

# URDF 구조 시각화
urdf_to_graphiz robot.urdf
# → robot.pdf 생성 (트리 구조 확인)
```

---

## 6. 고급 기능

### 6.1 Batch 속성 편집

여러 링크의 속성을 한 번에 편집:

```text
1. 여러 Object를 Shift+클릭으로 선택
2. Phobos → Tools → "Batch Edit"
3. 변경할 속성 선택 (Mass, Friction, Color 등)
4. 값 입력 → Apply
```

### 6.2 Merged Inertia 계산

여러 개의 하위 링크를 하나의 복합 링크로 합칠 때 관성 계산:

```text
1. 병합할 모든 Object 선택
2. Phobos → Tools → "Calculate Merged Inertia"
3. 결과를 부모 링크에 적용
```

### 6.3 모델 무결성 검사

내보내기 전에 누락된 속성이 없는지 검사:

```text
1. Phobos → Tools → "Check Model Integrity"
2. 결과 패널에서 경고/오류 확인
   - 누락된 collision mesh
   - 설정되지 않은 inertial
   - Bone-Object 연결 누락
   - etc.
```

### 6.4 Joint Constraint 시각화

조인트의 회전 범위를 Blender에서 시각적으로 확인:

```text
1. Armature 선택 → Pose Mode
2. Bone 선택
3. Phobos 속성에 Limit 값 설정
4. Blender의 Bone Constraint 속성에서 Limit 확인 가능
```

### 6.5 SMURF 포맷으로 저장 (중간 저장)

Phobos 고유의 SMURF 포맷으로 저장하면 URDF 속성을 모두 보존하면서  
언제든 다시 불러와서 편집할 수 있습니다.

```text
Export → Format: SMURF → Save
→ 추후 Import → SMURF → 불러오기 → 계속 편집 가능
```

---

## 7. CLI (Command Line Interface) 사용법

Phobos는 Blender 없이도 Python CLI로 사용할 수 있습니다.

### 7.1 CLI 설치

```bash
pip install phobos
```

### 7.2 기본 명령어

```bash
# 도움말
phobos --help

# URDF → SMURF 변환
phobos convert --input robot.urdf --output robot.smurf

# SMURF → URDF 변환
phobos convert --input robot.smurf --output robot.urdf

# 모델 검증
phobos validate --model robot.urdf

# 일괄 처리 스크립트
phobos run-script my_script.py
```

### 7.3 CI/CD 파이프라인 예시

```yaml
# .github/workflows/urdf-ci.yml
name: URDF Validation
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Phobos
        run: pip install phobos
      - name: Validate URDF
        run: phobos validate --model robot.urdf
      - name: Export all formats
        run: |
          phobos convert --input robot.smurf --output robot.urdf
          phobos convert --input robot.smurf --output robot.sdf
```

### 7.4 Python API 예제

```python
import phobos

# SMURF 파일 로드
model = phobos.load("robot.smurf")

# 링크 목록
for link in model.links:
    print(f"Link: {link.name}, Mass: {link.inertial.mass}")

# 조인트 정보
for joint in model.joints:
    print(f"Joint: {joint.name}, Type: {joint.type}")
    print(f"  Parent: {joint.parent}, Child: {joint.child}")
    print(f"  Axis: {joint.axis}")

# URDF로 내보내기
model.export("robot.urdf", format="urdf")

# SDF로 내보내기
model.export("robot.sdf", format="sdf")
```

---

## 8. 문제 해결

### 8.1 Phobos 탭이 안 보여요

```
원인: Add-on이 활성화되지 않음 또는 Blender 버전 불일치
해결:
  1. Edit → Preferences → Add-ons → "Phobos" 검색 → 체크
  2. N 키 눌러서 우측 패널 열기
  3. 그래도 안 보이면 Blender 3.3 LTS 사용 확인
```

### 8.2 STEP 파일을 Blender로 직접 가져올 수 없나요?

```
원인: Blender는 STEP 포맷을 기본 지원하지 않음
해결:
  1. 무료: FreeCAD에서 STL로 변환 후 Import
  2. 유료: Blender Market의 "CAD Import Add-on" 구매 (약 $20)
     - STEP, IGES, STEP 등 다양한 CAD 포맷 지원
  3. 무료 대안: OnlineCAD Converter 사용
```

### 8.3 내보낸 URDF의 메시 경로가 깨져요

```
원인: 상대 경로 설정 문제
해결:
  1. Export 옵션에서 "Use relative paths" 체크 확인
  2. URDF 파일과 meshes/ 폴더가 같은 위치에 있는지 확인
  3. URDF를 직접 열어서 경로 수정:
     <mesh filename="meshes/base_link.stl"/>
```

### 8.4 Collision Mesh가 너무 정밀해요 (성능 문제)

```
원인: Visual Mesh를 그대로 Collision으로 사용
해결:
  1. Phobos "Generate Collision" → "Convex Hull" 선택
  2. 또는 Blender의 Decimate Modifier로 폴리곤 수 90% 감소
  3. 박스/구/실린더 같은 Primitive 사용 권장
```

### 8.5 관성 계산 값이 이상해요

```
원인: 밀도 또는 스케일 단위 불일치
해결:
  1. Blender의 기본 단위는 meters, URDF는 meters
  2. STL Import 시 Scale을 mm → m 로 변환했는지 확인
  3. 밀도 값을 실제 재질에 맞게 입력 (steel ≈ 7800, aluminum ≈ 2700)
```

### 8.6 조인트 회전축이 반대 방향이에요

```
원인: Bone 방향 설정 오류
해결:
  1. Armature → Edit Mode
  2. Bone 선택 → N 키 → Item 탭
  3. Bone의 Roll 값 조정 (회전축 방향 변경)
  4. 또는 Phobos 속성에서 Axis 값을 반전:
     axis="0 0 1" → axis="0 0 -1"
```

---

## 9. 참고 링크

| 리소스 | URL |
|---|---|
| Phobos GitHub | https://github.com/dfki-ric/phobos |
| Phobos Wiki | https://github.com/dfki-ric/phobos/wiki |
| Phobos API 문서 | https://dfki-ric.github.io/phobos/ |
| Blender v3.3 LTS 다운로드 | https://www.blender.org/download/lts/3-3/ |
| Blender Add-on 설치 가이드 | https://docs.blender.org/manual/en/latest/editors/preferences/addons.html |
| ROS URDF 튜토리얼 | http://wiki.ros.org/urdf/Tutorials |
| FreeCAD (STEP→STL 변환용) | https://www.freecad.org |

---

## 부록: 빠른 시작 체크리스트

```
[ ] Blender v3.3 LTS 설치
[ ] Phobos Add-on 설치 (ZIP 다운로드 → Blender Add-on 설정)
[ ] STEP 파일을 FreeCAD로 → STL 변환
[ ] Blender 실행, 기본 큐브 삭제
[ ] STL 파일 Import (File → Import → STL)
[ ] Phobos 탭에서 "Initialize Robot Model"
[ ] Armature (Bone) 생성 및 관절 위치 배치
[ ] 각 메시 Object를 Bone에 Parent (Ctrl+P → Bone)
[ ] 링크 속성 설정 (Name, Mass, Inertia)
[ ] 조인트 속성 설정 (Type, Axis, Limit)
[ ] Collision Mesh 자동 생성
[ ] "Check Model Integrity" 로 검증
[ ] URDF Export
[ ] check_urdf 또는 Python으로 검증
[ ] 완료!
```
