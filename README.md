# AI vs Human 플랫폼

AI vs Human 플랫폼은 사용자가 AI가 만든 콘텐츠와 사람이 만든 콘텐츠를 블라인드 테스트 형식으로 맞혀보는 대결형 서비스입니다. Django 기반 REST API와 React 프론트엔드로 구성되어 있으며, 주간 단위의 팀 경쟁 및 포인트 보상 시스템을 제공합니다.

## 주요 기능 개요
- 사용자 회원가입 및 로그인, 팀 선택 (TEAM AI / TEAM HUMAN)
- 작품 업로드 및 블라인드 투표 시스템
- 카테고리별 주간 우승자 및 정답자 포인트 지급
- 진영별 주간 승부(감식안 점수 + 결과 점수) 및 팀 보상

## 백엔드 (Django)

### 환경 준비
1. 가상환경을 생성하고 필요한 패키지를 설치합니다.
   ```bash
   pip install django djangorestframework
   ```
2. 데이터베이스 마이그레이션과 관리자 계정을 생성합니다.
   ```bash
   python backend/manage.py migrate
   python backend/manage.py createsuperuser
   ```
3. 개발 서버를 실행합니다.
   ```bash
   python backend/manage.py runserver
   ```

### 주간 결과 집계 명령어
주간 결과를 계산하고 포인트를 지급하는 커스텀 명령어입니다.
```bash
python backend/manage.py compute_weekly_results
```

## 프론트엔드 (React)

### 환경 준비
1. 의존성을 설치합니다.
   ```bash
   cd frontend
   npm install
   ```
2. 개발 서버를 실행합니다.
   ```bash
   npm start
   ```

프론트엔드 애플리케이션은 Django API가 `/api/` 경로에 노출되어 있다고 가정합니다.
