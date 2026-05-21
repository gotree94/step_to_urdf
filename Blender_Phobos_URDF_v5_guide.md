# Blender 5.x + Phobos 4.x (커뮤니티 포크) URDF 생성 가이드

> **대상: Blender 5.1.2 / Windows 11**
> 작성일: 2026-05-21

---

## ⚠️ 중요: 원본 Phobos(dfki-ric/phobos)와의 차이

| 항목 | 원본 Phobos v2.0.0 | Phobos 4.x 포크 |
|---|---|---|
| **대상 Blender** | 3.3 LTS 한정 | **4.2 LTS ~ 5.0+** |
| **설치 방식** | Legacy Add-on (ZIP) | **Extension** (blender_manifest.toml) |
| **의존성** | 수동 설치 필요 | **자동 설치** (ZIP에 wheel 번들) |
| **Windows 지원** | ✅ | ✅ (win_amd64 wheel 포함) |
| **관리 상태** | 방치 (2021년 이후) | **활발히 유지보수 중** (2026) |
| **GitHub** | dfki-ric/phobos | **marcelizer/phobos-4.0-linux** |
| **Blender 5.x 작동** | ❌ (GitHub Issue #402) | ✅ |

> **Blender 5.1.2에서는 반드시 이 포크(fork) 버전을 사용해야 합니다.**
> 원본 Phobos는 Blender 3.3 LTS 전용이며, 4.2+ Extensions 시스템과 호환되지 않습니다.

---

## 목차

1. [Phobos 4.x 포크란?](#1-phobos-4x-포크란)
2. [설치 방법](#2-설치-방법)
3. [STEP → Blender 워크플로우 개요](#3-step--blender-워크플로우-개요)
4. [Phobos 기본 개념](#4-phobos-기본-개념)
5. [URDF 생성 상세 워크플로우](#5-urdf-생성-상세-워크플로우)
6. [문제 해결 (Blender 5.x 특화)](#6-문제-해결-blender-5x-특화)
7. [참고 링크](#7-참고-링크)

---

## 1. Phobos 4.x 포크란?

**Phobos 4.x**는 원본 Phobos(dfki-ric/phobos)를 Blender 4.2+ / 5.0+ 에서 동작하도록 포팅한 커뮤니티 포크입니다.

- **포크 저장소**: https://github.com/marcelizer/phobos-4.0-linux
- **미러 저장소**: https://github.com/elasticdotventures/phobos-4.0
- **최소 Blender 버전**: 4.2.0
- **테스트 완료**: Blender 5.0 beta (Windows 11)

### 이름이 "linux" 인데 Windows에서 되나요?

**됩니다.** 저장소 이름은 `phobos-4.0-linux` 이지만, 실제로는 **Windows 전용 wheel 파일을 포함한 크로스플랫폼 Extension**입니다.

`blender_manifest.toml` 에 포함된 wheel 목록:
```
numpy-2.3.4-cp311-cp311-win_amd64.whl
scipy-1.16.2-cp311-cp311-win_amd64.whl
pyyaml-6.0.3-cp311-cp311-win_amd64.whl
pycollada-0.9.2-py3-none-any.whl
pydot-4.0.1-py3-none-any.whl
pyparsing-3.2.5-py3-none-any.whl
```

### 원본 Phobos와의 차이점

| 기능 | 원본 Phobos | Phobos 4.x 포크 |
|---|---|---|
| Extension 시스템 | 미지원 (Legacy) | ✅ `blender_manifest.toml` |
| Wheel 번들 의존성 | ❌ 수동 설치 | ✅ ZIP 안에 포함 |
| Blender 4.2+ UI | 호환 안 됨 | ✅ 완전 지원 |
| SMURF 저장 | ✅ 동일 | ✅ 동일 |
| URDF 내보내기 | ✅ 동일 | ✅ 동일 |

---

## 2. 설치 방법

### 2.1 사전 준비

| 요구사항 | 내용 |
|---|---|
| **Blender 5.1.2** | 현재 사용 중인 버전 (4.2 LTS 이상이면 모두 가능) |
| **Microsoft Visual C++ 재배포 가능 패키지** | Blender Python이 정상 동작하기 위해 필요 |
| **인터넷 연결** | 최초 설치 시 wheels 추출 |

> Visual C++ 재배포 가능 패키지가 없으면 아래에서 다운로드:
> https://aka.ms/vs/17/release/vc_redist.x64.exe

### 2.2 설치 방법 (Extension, 권장)

Blender 4.2+ 의 새로운 **Extensions 시스템**을 통해 설치합니다.

```text
1. Blender 실행
2. 메뉴: Edit → Preferences → Add-ons
   ⚠️ Blender 5.x 에서는 "Get Extensions" 탭이 기본이지만,
      "Add-ons" 탭에서 설치해야 합니다.
3. 우측 상단 ▼ (드롭다운 메뉴) 클릭
4. "Install from Disk..." 선택
   ⚠️ "Install from Repository..."는 존재하지 않습니다.
5. 파일 선택 창에서 ZIP 파일 선택:
   https://github.com/marcelizer/phobos-4.0-linux/archive/refs/heads/main.zip
   (직접 다운로드 후 선택)
6. ZIP 선택 → "Install from Disk..." 버튼 클릭
7. 설치 완료 후 Add-ons 목록에서 "Phobos 4" 검색
8. 체크박스 클릭하여 활성화
   → 의존성 wheel이 자동으로 설치됩니다.
   → "Requirements installed" 팝업이 나타나면 정상
9. Blender 재시작
10. 재시작 후 다시 Edit → Preferences → Add-ons → "Phobos 4" 체크 활성화
```

> **설치 확인**: 3D Viewport 우측 패널(N 키)에 **"Phobos"** 탭이 나타나면 성공입니다.

### 2.3 수동 설치 (ZIP 해제 방식)

Extension 시스템이 동작하지 않을 경우 대체 방법:

```text
1. 포크 ZIP 다운로드:
   https://github.com/marcelizer/phobos-4.0-linux/archive/refs/heads/main.zip
2. ZIP 파일을 적절한 위치에 압축 해제
   예: C:\Users\user\Desktop\phobos-4.0-linux-main\
3. Blender 설정 폴더에 복사:
   C:\Users\user\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\
   (주의: Blender 5.1에서 Extensions는 다른 폴더 구조 사용)
4. Blender 실행
5. Edit → Preferences → Add-ons → "Phobos 4" 검색 → 체크
```

### 2.4 의존성 수동 설치 (필요한 경우)

포크가 `blender_manifest.toml`을 통해 자동 설치하지만, 실패 시 Blender 내장 Python으로 직접 설치:

```bash
# Blender 내장 Python 경로 (Windows)
& "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pip install numpy scipy pyyaml pycollada pydot
```

---

## 3. STEP → Blender 워크플로우 개요

Phobos는 STEP 파일을 직접 읽을 수 없습니다. 아래 파이프라인을 따릅니다:

```
방법 1: FreeCAD 경유 (권장, 무료)
  STEP 파일 (RB10-1300E.stp)
    ↓ (FreeCAD freecadcmd.exe)
  STL 파일 (링크별 분리, 6개)
    ↓ (Blender Import STL)
  Blender Scene
    ↓ (Phobos 4.x)
  URDF + meshes/

방법 2: Online Converter
  STEP 파일
    ↓ (step2urdf.top 등)
  STL 파일
    ↓ (Blender Import STL)
  Blender Scene → Phobos → URDF

방법 3: Blender CAD Import Add-on (유료, $20)
  STEP 파일
    ↓ (Blender CAD Import Add-on)
  Blender Scene (직접 STEP 불러오기)
    ↓ (Phobos 4.x)
  URDF + meshes/
```

> **권장:** FreeCAD로 STEP → STL 변환 후 Blender/Phobos로 가져오는 방법이
> 가장 안정적이고 비용이 없습니다 (이전에 만든 `step2urdf_full.py` 스크립트 활용).

---

## 4. Phobos 기본 개념

### Blender ↔ URDF 매핑

```
Blender 개념                URDF 개념
─────────────────────────────────────
Armature (Object)          robot
Bone (뼈)                  joint
Object (메시 오브젝트)      link (visual + collision)
Phobos Tag 속성             URDF 속성 (질량, 관성 등)
```

### 모델 계층 구조

```
Robot Model (Phobos Scene Root)
├── Joint (Blender Bone)
│   ├── Parent Link (메시 Object)
│   │   ├── Visual Mesh (STL)
│   │   ├── Collision Mesh
│   │   └── Inertial (COM 표시자)
│   └── Child Link (메시 Object) ...
```

### Phobos 패널 구성 (Blender 우측, N 키)

| 섹션 | 기능 |
|---|---|
| **Scene** | 로봇 이름, 모델 속성 설정 |
| **Object** | 선택된 메시의 URDF 속성 (Link name, mass 등) |
| **Bone** | 선택된 Bone의 조인트 속성 (type, axis, limit 등) |
| **Tools** | Collision 자동 생성, Inertia 계산, 모델 검증 |
| **Export** | URDF/SDF/SMURF 내보내기 |

---

## 5. URDF 생성 상세 워크플로우

### 5.1 사전 준비: STEP → STL 변환 (FreeCAD)

이전에 만든 스크립트를 사용하여 RB10-1300E.stp 에서 링크별 STL 추출:

```bash
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" C:\Users\user\Desktop\URDFly\step2urdf_full.py
```

결과물:
```
C:\Users\user\Desktop\URDFly\output2\
├── base_link.stl
├── link_1.stl
├── link_2.stl
├── link_3.stl
├── link_4.stl
├── link_5.stl
└── rb10.urdf        (FreeCAD 기반 1차 URDF)
```

> STL 파일 6개는 Phobos에서 사용할 준비가 된 상태입니다.

### 5.2 Blender에서 STL 가져오기

```text
1. Blender 실행
2. 시작 Scene의 기본 큐브, 카메라, 라이트 모두 삭제 (A 키 전체 선택 → X 키 삭제)
3. File → Import → STL (.stl)
4. base_link.stl 선택 → Import
5. 나머지 STL도 동일하게 Import
   (팁: Shift+클릭으로 여러 파일 동시 선택 가능)
```

### 5.3 본(Bone) 계층 구조 생성

Phobos로 로봇 관절 구조를 정의합니다.

#### 방법 A: Phobos 자동 초기화 (권장)

```text
1. 3D Viewport 우측 패널에서 "Phobos" 탭 선택
2. Scene 패널에서 "Initialize Robot Model" 버튼 클릭
   → 자동으로 Armature(Object) 생성
3. 로봇 이름 설정 (예: RB10_1300E)
```

#### 방법 B: 수동 생성

```text
1. Add → Armature → Single Bone
2. Armature 이름을 로봇 이름으로 변경 (예: RB10_1300E)
3. Tab 키 → Edit Mode
4. Bone을 관절 위치로 이동 (G 키)
5. Bone 계층 구조 만들기:
   - 첫 번째 Bone 선택 → E 키 (Extrude)로 자식 Bone 생성
   - 각 Bone 이름을 조인트 이름으로 설정 (예: joint_1, joint_2, ...)
6. Tab 키 → Object Mode로 복귀
```

#### RB10-1300E 기준 Bone 계층

RB10은 6축 협동로봇이므로 아래와 같이 Bone 구조를 만듭니다:

```
Armature: RB10_1300E
├── base_link (Armature 자체 = root)
├── joint_1 (Bone) ───── link_1 (STL Object)
│   ├── joint_2 (Bone) ── link_2 (STL Object)
│   │   ├── joint_3 (Bone) ── link_3 (STL Object)
│   │   │   ├── joint_4 (Bone) ── link_4 (STL Object)
│   │   │   │   ├── joint_5 (Bone) ── link_5 (STL Object)
│   │   │   │   │   ├── joint_6 (Bone) ── link_6 (STL Object, 추가 필요시)
```

### 5.4 링크(Object)를 Bone에 연결

각 STL 메시를 해당 Bone의 자식으로 설정:

```text
1. Object 모드에서 link_1 STL 선택
2. Shift+클릭으로 Armature (RB10_1300E) 선택
3. Ctrl+P → "Bone" 선택 (Armature의 활성 Bone에 자식으로 연결)
   ⚠️ "Armature"가 아닌 "Bone"을 선택해야 합니다.
4. 나머지 링크도 반복
```

> 정확히 연결하려면:
> 1. 먼저 연결할 Bone을 클릭하여 활성화
> 2. Shift+클릭으로 연결할 Object 선택
> 3. Ctrl+P → Bone

### 5.5 URDF 속성 설정

Phobos 패널에서 각 요소의 URDF 속성을 설정합니다.

#### 링크 속성 (Object 선택 시 Phobos → Object 패널)

| 항목 | URDF 요소 | 설명 |
|---|---|---|
| Link Name | `<link name="...">` | 링크 이름 (base_link, link_1, ...) |
| Visual Mesh | `<mesh filename="...">` | STL 파일 경로 |
| Collision Mesh | `<mesh filename="...">` | 충돌용 메시 |
| Mass | `<mass value="...">` | 질량 (kg) |
| Inertia | `<inertia ixx="...">` | 관성 모멘트 (또는 자동 계산) |
| COM | `<origin xyz="..." rpy="..."/>` | 무게중심 위치 |

#### 조인트 속성 (Bone 선택 시 Phobos → Bone 패널)

| 항목 | URDF 요소 | 설명 |
|---|---|---|
| Joint Name | `<joint name="...">` | 조인트 이름 (joint_1, joint_2, ...) |
| Joint Type | `type="..."` | **revolute** (회전), prismatic, fixed |
| Parent Link | `<parent link="...">` | 부모 링크 (자동 설정) |
| Child Link | `<child link="...">` | 자식 링크 (자동 설정) |
| Axis | `<axis xyz="..."/>` | 회전 축 방향 (RB10: 각 joint별 Z 또는 Y축) |
| Lower Limit | `<limit lower="..."/>` | 최소 각도 (rad) |
| Upper Limit | `<limit upper="..."/>` | 최대 각도 (rad) |
| Effort | `<limit effort="..."/>` | 최대 토크 (Nm) |
| Velocity | `<limit velocity="..."/>` | 최대 속도 (rad/s) |

#### RB10-1300E 조인트 축 참고

협동로봇의 일반적인 축 구성:

| 조인트 | 축 방향 | 회전 범위 (rad) |
|---|---|---|
| joint_1 | Z (0,0,1) | ±2.97 (±170°) |
| joint_2 | Y (0,1,0) | ±2.97 (±170°) |
| joint_3 | Y (0,1,0) | ±2.88 (±165°) |
| joint_4 | Z (0,0,1) | ±3.14 (±180°) |
| joint_5 | Y (0,1,0) | ±2.88 (±165°) |
| joint_6 | Z (0,0,1) | ±3.14 (±180°) |

### 5.6 Collision Mesh 자동 생성

Phobos는 Visual Mesh로부터 Collision Mesh를 자동 생성 가능:

```text
1. 대상 링크 Object 선택
2. Phobos → Tools → "Generate Collision" 버튼
   - "Convex Hull" (볼록 껍질): 충돌 계산에 효율적
   - "Primitive" (박스/구/실린더): 가장 단순
3. Decimation Modifier 로 폴리곤 수 감소 (선택)
```

### 5.7 Inertia 자동 계산

Phobos가 메시 형상과 밀도로 관성 텐서 자동 계산:

```text
1. 대상 링크 Object 선택
2. Phobos → Tools → "Calculate Inertia" 버튼
3. 밀도 값 입력 (예: steel = 7800 kg/m³, aluminum = 2700 kg/m³)
   또는 질량 직접 입력
4. COM(무게중심) 위치 확인
```

### 5.8 URDF 내보내기

```text
1. Phobos → Export 패널
2. Export Format: "URDF" 선택
3. Export Path: 출력 폴더 지정
   (예: C:\Users\user\Desktop\URDFly\phobos_output)
4. Mesh Format: "STL" (권장)
5. 옵션 설정:
   ☑ Export collision meshes
   ☑ Export inertial data
   ☐ Use relative paths
   Precision: 6
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
└── (선택) config/
```

### 5.9 내보낸 URDF 검증

```bash
# URDF XML 구문 검증
python -c "from xml.etree import ElementTree as ET; ET.parse('robot.urdf')"

# URDF 구조 확인
python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('robot.urdf')
root = tree.getroot()
print(f'Robot: {root.get(\"name\")}')
for link in root.findall('link'):
    print(f'  Link: {link.get(\"name\")}')
for joint in root.findall('joint'):
    parent = joint.find('parent').get('link')
    child = joint.find('child').get('link')
    print(f'  Joint: {joint.get(\"name\")} ({parent} → {child})')
"
```

---

## 6. 문제 해결 (Blender 5.x 특화)

### 6.1 "Install from Repository..." 메뉴가 없어요

```
원인: Blender 4.2+ 부터 Extensions 시스템으로 변경됨
해결:
  Edit → Preferences → Add-ons (→ "Get Extensions" 탭 아님)
  → 우측 상단 ▼ 드롭다운 → "Install from Disk..."
  → 다운로드한 ZIP 파일 선택

"Install from Repository..." 라는 메뉴는 Blender에 존재하지 않습니다.
```

### 6.2 ZIP 설치 후 "Phobos 4"가 목록에 안 보여요

```
원인 1: Extension 시스템이 ZIP 구조를 인식하지 못함
해결:
  ZIP 파일 이름을 phobos.zip 으로 단순화하여 재시도

원인 2: Blender 버전이 4.2 미만
해결:
  Blender 5.1.2를 사용 중이면 해당 없음. Blender 버전 확인.
```

### 6.3 활성화했는데 "Requirements installation failed"

```
원인: wheel 파일 추출 실패 또는 Visual C++ 재배포 패키지 누락
해결:
  1. Visual C++ 재배포 가능 패키지 설치:
     https://aka.ms/vs/17/release/vc_redist.x64.exe
  2. Blender 재시작 후 재시도
  3. 그래도 안 되면 수동 설치:
     Blender 내장 Python으로 직접 pip 설치:
     "C:\Program Files\Blender Foundation\Blender 5.1\5.1\python\bin\python.exe" -m pip install numpy scipy pyyaml
  4. 그 다음 ZIP 재설치
```

### 6.4 Phobos 탭이 안 보여요

```
원인 1: Add-on 비활성화 상태
해결:
  Edit → Preferences → Add-ons → "Phobos 4" 검색 → 체크 활성화

원인 2: 설치 실패 (원본 Phobos를 설치한 경우)
해결:
  원본 Phobos(dfki-ric)는 Blender 5.x에서 동작하지 않습니다.
  반드시 포크 버전(marcelizer/phobos-4.0-linux)을 설치해야 합니다.

원인 3: 패널이 접혀 있음
해결:
  3D Viewport에서 N 키를 눌러 우측 패널 열기
  패널 상단에 "Phobos" 탭이 있는지 확인
```

### 6.5 원본 Phobos(dfki-ric)를 실수로 설치했어요

```
해결:
  1. Edit → Preferences → Add-ons → "Phobos" 검색
  2. 체크 해제 (비활성화)
  3. Blender 종료
  4. 아래 폴더에서 Phobos 관련 폴더/파일 삭제:
     C:\Users\user\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\
  5. Blender 재실행
  6. 새로 포크 버전 ZIP 설치 (2.2절 참고)
```

### 6.6 내보낸 URDF의 메시 경로가 깨져요

```
원인: 상대 경로 설정 문제
해결:
  1. Export 옵션에서 "Use relative paths" 체크 해제
  2. URDF 파일을 직접 열어 경로 수정:
     <mesh filename="meshes/base_link.stl"/>
  3. URDF 파일과 meshes/ 폴더가 같은 위치에 있는지 확인
```

### 6.7 모델이 엉뚱한 위치에 떠 있어요

```
원인: STL Import 시 좌표계/스케일 차이
해결:
  1. 모든 STL을 한 번에 선택 (A 키)
  2. S 키 → 0.001 입력 (mm → m 변환, STEP이 mm 단위인 경우)
  3. Apply All Transforms (Ctrl+A → All Transforms)
  4. 각 링크를 Bone 위치에 맞게 G 키로 이동
```

---

## 7. 참고 링크

| 자료 | 링크 |
|---|---|
| Phobos 4.x 포크 | https://github.com/marcelizer/phobos-4.0-linux |
| Phobos 4.x 미러 | https://github.com/elasticdotventures/phobos-4.0 |
| 원본 Phobos (v3.3 전용) | https://github.com/dfki-ric/phobos |
| Blender 5.1 매뉴얼 - Add-ons | https://docs.blender.org/manual/en/latest/editors/preferences/addons.html |
| Blender 5.1 매뉴얼 - Extensions | https://docs.blender.org/manual/en/latest/editors/preferences/extensions.html |
| 원본 Phobos #402 (5.x 미작동 이슈) | https://github.com/dfki-ric/phobos/issues/402 |
| 원본 Phobos Wiki | https://github.com/dfki-ric/phobos/wiki |
| STEPtoURDF 가이드 | `C:\Users\user\Desktop\STEPtoURDF_가이드.md` |
| URDFly (URDF 시각화) | https://github.com/Democratizing-Dexterous/URDFly |
| Visual C++ 재배포 패키지 | https://aka.ms/vs/17/release/vc_redist.x64.exe |

---

> **이전 가이드와의 관계**
> - `Blender_Phobos_URDF_guide.md` → **Blender 3.3 LTS + 원본 Phobos** 용
> - `Blender_Phobos_URDF_v5_가이드.md` (이 파일) → **Blender 4.2+/5.x + 포크 Phobos 4.x** 용
>
> Blender 5.1.2에서는 이 파일의 설치 방법을 따라야 합니다.
