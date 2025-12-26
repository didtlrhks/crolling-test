# K-Startup 신규 사업 공고 크롤링

이 프로젝트는 Playwright를 사용하여 K-Startup 웹사이트의 신규 사업 공고 데이터를 크롤링합니다.

## 설치 방법

1. Python 가상환경 생성 및 활성화 (선택사항)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. Playwright 브라우저 설치
```bash
playwright install chromium
```

## 사용 방법

스크립트 실행:
```bash
python scrape_kstartup.py
```

## 출력 파일

- `kstartup_announcements.json`: JSON 형식으로 저장된 공고 데이터
- `kstartup_announcements.csv`: CSV 형식으로 저장된 공고 데이터

## 데이터 구조

각 공고는 다음 정보를 포함합니다:
- `title`: 공고 제목
- `url`: 공고 상세 페이지 URL
- `pbanc_sn`: 공고 고유 번호
- `scraped_at`: 수집 시간

## 주의사항

- 웹사이트의 구조가 변경되면 스크립트 수정이 필요할 수 있습니다.
- 과도한 요청은 서버에 부하를 줄 수 있으므로 적절한 딜레이를 두고 사용하세요.
- 웹사이트의 이용약관을 확인하고 준수하세요.

