# SolidWorks URDF Exporter (SW2URDF) 중단 배경과 대안 생태계

> 작성일: 2026-05-21

---

## 목차

1. [SW2URDF 현황 요약](#1-sw2urdf-현황-요약)
2. [SW2URDF가 방치된 6가지 이유](#2-sw2urdf가-방치된-6가지-이유)
3. [대안 생태계 지형도](#3-대안-생태계-지형도)
4. [대안 상세 비교](#4-대안-상세-비교)
5. [결론](#5-결론)
6. [참고 링크](#6-참고-링크)

---

## 1. SW2URDF 현황 요약

| 항목 | 내용 |
|---|---|
| **공식 저장소** | [ros/solidworks_urdf_exporter](https://github.com/ros/solidworks_urdf_exporter) |
| **개발자** | Stephen Brawner (PickNik Consulting, Open Robotics, Willow Garage 지원) |
| **최신 릴리즈** | v1.6.1 (2021년 11월) — **SolidWorks 2021 SP5** |
| **라이선스** | MIT (완전 오픈소스, 수정/배포 자유) |
| **마지막 업데이트 이후** | **4년 6개월** 경과 |
| **지원되는 SW 버전** | 2018 SP5 ~ 2021 (그 이후는 **모두 미지원**) |
| **GitHub 이슈** | 2022~2026년까지 지속적으로 "SW 2022/2023/2024/2025/2026 지원 요청" 등록 |
| **Pull Request** | **0개** (커뮤니티에서 아무도 직접 수정하지 않음) |

> ⚠️ 134개 fork 중 어느 것도 실질적으로 유지보수되는 것은 없습니다.

---

## 2. SW2URDF가 방치된 6가지 이유

### 2.1 ROS1의 종말과 ROS2 전환 (가장 큰 요인)

**SW2URDF의 근본적인 문제: ROS1에 종속된 설계**

SW2URDF는 단순히 URDF를 생성하는 것을 넘어, 함께 생성하는 파일들:
- `package.xml` (ROS1 패키지 매니페스트)
- `CMakeLists.txt` (ROS1 빌드 시스템)
- `.launch` 파일 (ROS1 런처)
- ROS1 스타일의 디렉토리 구조

이 모두가 ROS1 전용입니다. 2021년부터 ROS 커뮤니티가 ROS2로 대규모 이주를 시작하면서, maintainer들은 더 이상 ROS1 전용 툴에 리소스를 투입할 이유가 없어졌습니다.

```
타임라인:
2017  ROS1 Kinetic (마지막 주요 ROS1)
2019  ROS2 Foxy 첫 LTS 릴리즈
2020  ROS1 Noetic (마지막 ROS1 릴리즈)
2021  SW2URDF v1.6.1 ← 마지막 릴리즈
2022  ROS2 Humble LTS → ROS2 사실상 표준 확립
2023  ROS1 EOL 발표 (Noetic 2025년 지원종료)
2025  ROS1 Noetic 지원 종료
```

### 2.2 Fusion 360 개인 무료화 + fusion2urdf (가장 강력한 대체재)

| 시기 | 사건 |
|---|---|
| 2018 | Autodesk, Fusion 360 **개인용 무료 라이선스** 발표 |
| 2020 | syuntoku14, fusion2urdf 첫 릴리즈 |
| 2021~ | fusion2urdf 성숙, 로봇 커뮤니티 표준으로 자리잡음 |
| 현재 | **GitHub ⭐704**, 가장 활성화된 URDF 생성 프로젝트 |

Fusion 360 + fusion2urdf는 SW2URDF와 **동등한 기능**을 제공하면서도:
- **완전 무료** (개인 라이선스)
- **지속적으로 업데이트**
- **활발한 커뮤니티**
- **ROS2 호환**

장점이 너무 명확했기 때문에, 사람들이 "SolidWorks에서 해야 하는 이유"를 잃어버렸습니다.

### 2.3 OnShape 무료 티어 + URDF Exporter

- OnShape는 **웹 브라우저 기반 CAD**로 설치가 전혀 필요 없음
- **무료 계정** 제공 (공개 문서 10개 제한)
- OnShape App Store에서 URDF Exporter 설치 가능
- STEP 파일을 업로드한 후 URDF로 바로 내보내기 가능
- CAD 라이선스 자체가 없어도 시작할 수 있는 가장 낮은 진입 장벽

### 2.4 Blender + Phobos — 완전 무료 오픈소스 생태계

[Phobos](https://github.com/dfki-ric/phobos) (⭐886)는 DFKI(독일 인공지능 연구소)가 개발한 Blender 애드온입니다.

```
Blender (무료) + Phobos (무료) = 모든 기능을 갖춘 URDF 스튜디오
```

| 기능 | SW2URDF | Phobos |
|---|---|---|
| URDF 생성 | ✅ | ✅ |
| SDF 생성 | ❌ | ✅ |
| WYSIWYG 편집 | ❌ (SolidWorks에서 수정) | ✅ (Blender에서 실시간) |
| 충돌 메시 자동 생성 | ❌ | ✅ |
| 관성 자동 계산 | ✅ (SW 물성) | ✅ (Blender 물성) |
| 가격 | SolidWorks 라이선스 필요 | 완전 무료 |

### 2.5 순수 웹/온라인 변환기의 등장

2026년 현재, STEP 파일만 있으면 URDF를 바로 얻을 수 있는 웹 서비스가 존재합니다:

- **[step2urdf.top](https://step2urdf.top)** — STEP 업로드 → URDF 다운로드, 설치 0
- 다양한 mesh 변환 서비스들 (STEP → STL → URDF workflow)

"굳이 SolidWorks로 URDF를 뽑을 필요가 없는 세상"이 된 것입니다.

### 2.6 유지보수 비용 대비 수요 부족

**SW2URDF 유지보수가 어려웠던 이유:**

```
매년 SolidWorks 새 버전 출시
    ↓
SolidWorks.Interop.* DLL 버전 변경 (필수)
    ↓
deprecated API 확인 및 교체 (평균 2~5개/년)
    ↓
.NET Framework 버전 호환성 확인
    ↓
WiX Toolset으로 installer 재빌드
    ↓
서명/배포
    ↓
사용자 테스트 피드백 대응
```

이 모든 과정을 **한 명의 개발자(Stephen Brawner)가 무료로 4년간** 해왔습니다.

| 연도 | SW 버전 | 작업량 |
|---|---|---|
| 2018 | SW 2018 SP5 | 최초 포팅 (대규모) |
| 2019 | SW 2019 | API 변경 대응 |
| 2020 | SW 2020 | Interop 업데이트 + 메뉴 위치 변경 |
| 2021 | SW 2021 | SP5 대응 (마지막) |

그런데 정작 유지보수를 요청하던 사용자들은:
- 134개 fork 중 **PR을 보낸 사람은 0명**
- 이슈만 40개 넘게 열고 "SW 202X 지원해주세요"만 반복
- **아무도 직접 코드를 수정하지 않음**

> "유지보수가 어렵다" + "대안이 많다" + "아무도 도와주지 않는다"
> = **SW2URDF의 자연사 (Natural Death)**

---

## 3. 대안 생태계 지형도

```
                      비용 ↑
                        │
    SW2URDF ────────────┤  SolidWorks 라이선스(연 200~500만원) + SW 2021 한계
    (현재: 방치)         │
                        │
    Fusion 360 ─────────┤  개인 무료 / 상업용 유료
    + fusion2urdf        │  ⭐704, 가장 활성화
    (⭐704)              │
                        │
    OnShape ────────────┤  무료 티어 (공개 문서 10개)
    + URDF Exporter      │  웹 기반, 설치 0
                        │
    Blender ────────────┤  완전 무료
    + Phobos (⭐886)     │  WYSIWYG, SDF도 가능
                        │
    FreeCAD ────────────┤  완전 무료
    + Python 스크립트    │  자동화 자유도 1위, 오프라인
                        │
    step2urdf.top ──────┤  무료 (웹)
                        │  3초면 URDF, 설치 불필요
                        │
                      비용 ↓
```

### 접근성 vs 기능 트레이드오프

```
접근성 ↑                  step2urdf.top
  │                        OnShape URDF
  │                        Fusion 360 + fusion2urdf
  │                        Blender + Phobos
  │                        FreeCAD + Python
  │                  SW2URDF (사실상 종료)
  └──────────────────────────────→ 기능/정밀도 ↑
```

---

## 4. 대안 상세 비교

| 방법 | CAD 라이선스 비용 | URDF 도구 비용 | 설치 | 난이도 | URDF 정밀도 | ROS2 호환 | 자동화 |
|---|---|---|---|---|---|---|---|
| **SW2URDF** (SW 2021까지) | 유료 (연 200~500만) | 무료 | 필요 | 중 | ⭐⭐⭐⭐⭐ | 부분적 | ✅ |
| **Fusion 360 + fusion2urdf** | 개인 무료 / 상업 유료 | 무료 | 필요 | 중 | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| **OnShape + URDF Exporter** | 무료 티어 있음 | 무료 | ❌ (웹) | 하 | ⭐⭐⭐⭐ | ✅ | 부분적 |
| **Blender + Phobos** | ❌ (Blender 무료) | 무료 | 필요 | 중상 | ⭐⭐⭐⭐ | ✅ | 부분적 |
| **FreeCAD + Python** | ❌ (FreeCAD 무료) | 직접 개발 | 필요 | 중 | ⭐⭐⭐⭐ | ✅ | ✅ (최고) |
| **step2urdf.top** | ❌ | 무료 | ❌ (웹) | 매우 쉬움 | ⭐⭐⭐ | ✅ | ❌ |
| **ExportURDF** (david-dorf) | Fusion/OnShape 무료 | 무료 | 필요 | 중 | ⭐⭐⭐⭐ | ✅ | ✅ |

### 상황별 추천

| 상황 | 추천 방법 |
|---|---|
| **STEP 파일 하나만 급하게 URDF로** | step2urdf.top (3초) |
| **무료 CAD로 꾸준히 URDF 필요** | Fusion 360 개인용 + fusion2urdf |
| **CAD 설치 자체가 불가능한 환경** | OnShape URDF Exporter (웹) |
| **URDF를 직접 편집/조정해야 함** | Blender + Phobos |
| **파이프라인 자동화 / CI/CD** | FreeCAD + Python 스크립트 |
| **이미 SolidWorks를 보유 중** | SW2URDF 포팅 or STEP → FreeCAD 경유 |

---

## 5. 결론

SW2URDF가 방치된 것은 **단순한 방치가 아닌 생태계의 자연스러운 진화**입니다.

```
2015~2020: "URDF를 만들려면 SolidWorks + SW2URDF가 유일한 선택지였다"
2021~2023: "Fusion 360이 무료화되고, fusion2urdf가 떠올랐다"
2024~현재: "Blender, OnShape, FreeCAD, 웹 서비스... 선택지가 넘쳐난다"
```

**핵심 메시지:**

1. SW2URDF는 죽은 것이 아니라, **더 이상 필요하지 않게 된 것**
2. 지금은 **모든 예산/환경에 맞는 URDF 생성 방법이 존재**함
3. 우리가 FreeCAD로 구축한 파이프라인은 이 흐름의 정확히 가운데에 있음
   - **완전 무료** ✅
   - **완전 자동화 가능** ✅
   - **오프라인 동작** ✅
   - **크로스 플랫폼** ✅

---

## 6. 참고 링크

| 리소스 | URL |
|---|---|
| SolidWorks URDF Exporter | https://github.com/ros/solidworks_urdf_exporter |
| fusion2urdf | https://github.com/syuntoku14/fusion2urdf |
| OnShape URDF Exporter | https://www.onshape.com / App Store 검색 |
| Blender + Phobos | https://github.com/dfki-ric/phobos |
| ExportURDF (통합 라이브러리) | https://github.com/david-dorf/ExportURDF |
| URDFly | https://github.com/Democratizing-Dexterous/URDFly |
| step2urdf.top | https://step2urdf.top |
| FreeCAD | https://www.freecad.org |
| ROS URDF 튜토리얼 | http://wiki.ros.org/urdf/Tutorials |
