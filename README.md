# RGT_LibraryServer

## 프로젝트 개요
RGT_LibraryServer는 도서 관리 시스템을 위한 백엔드 서버입니다. 이 프로젝트는 FastAPI를 기반으로 구축되었으며, 도서 대출, 사용자 관리, 대출 기록 관리 등의 기능을 제공합니다.

## 주요 기능
- **사용자 관리**: 사용자 등록, 조회, 수정, 삭제 기능 제공.
- **도서 관리**: 도서 등록, 조회, 수정, 삭제 기능 제공.
- **대출 관리**: 
  - 도서 대출 요청 처리 (`/loans/borrow`)
  - 도서 반납 요청 처리 (`/loans/return`)
  - 사용자별 대출 기록 조회 (`/loans`)
- **JWT 인증**: JSON Web Token을 사용한 인증 및 권한 부여.
- **환경 변수 관리**: `python-decouple`을 사용하여 민감한 정보를 `.env` 파일에서 관리.
- **API 문서화**: Swagger UI 및 ReDoc을 통해 자동으로 생성된 API 문서 제공.

## 기술 스택
- **프레임워크**: FastAPI
- **데이터베이스**: SQLite (기본 설정, 다른 데이터베이스로 확장 가능)
- **ORM**: SQLAlchemy
- **환경 변수 관리**: python-decouple
- **HTTP 클라이언트**: requests

## 설치 및 실행 방법
1. 저장소를 클론합니다:
   ```bash
   git clone https://github.com/dongfan/RGT_LibraryServer.git
   ```
2. 프로젝트 디렉토리로 이동합니다:
   ```bash
   cd RGT_LibraryServer
   ```
3. 가상 환경을 생성하고 활성화합니다:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
4. 필요한 패키지를 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```
5. 서버를 실행합니다:
   ```bash
   uvicorn main:app --reload
   ```
6. 브라우저에서 API 문서를 확인합니다:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 디렉토리 구조
```
RGT_LibraryServer/
├── routers/
│   ├── books.py       # 도서 관련 라우터
│   ├── loans.py       # 대출 관련 라우터
│   └── users.py       # 사용자 관련 라우터
├── utils/
│   └── validation.py  # 데이터 검증 유틸리티
├── main.py            # FastAPI 애플리케이션 진입점
├── client.py          # API 테스트 클라이언트
├── database.py        # 데이터베이스 초기화 및 세션 관리
├── models.py          # SQLAlchemy 모델 정의
├── requirements.txt   # 프로젝트 의존성 목록
├── .env               # 환경 변수 파일
└── README.md          # 프로젝트 설명 파일
```

## 기여 방법
1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다:
   ```bash
   git checkout -b feature/새로운기능
   ```
3. 변경 사항을 커밋합니다:
   ```bash
   git commit -m "새로운 기능 추가"
   ```
4. 브랜치에 푸시합니다:
   ```bash
   git push origin feature/새로운기능
   ```
5. Pull Request를 생성합니다.
