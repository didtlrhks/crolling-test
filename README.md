# K-Startup 신규 사업 공고 크롤링

이 프로젝트는 Playwright를 사용하여 K-Startup 웹사이트의 신규 사업 공고 데이터를 크롤링합니다.

## 가상환경 설정

### 1. 가상환경 생성 (이미 생성됨)
```bash
python3 -m venv venv
```

### 2. 가상환경 활성화
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Cursor/VS Code에서 인터프리터 선택하기

**방법 1: 명령 팔레트 사용**
1. `Cmd + Shift + P` (macOS) 또는 `Ctrl + Shift + P` (Windows/Linux)를 누릅니다
2. "Python: Select Interpreter"를 입력하고 선택합니다
3. 목록에서 다음 경로를 선택합니다:
   ```
   ./venv/bin/python
   ```
   또는 전체 경로:
   ```
   /Users/yangsigwan/크롤링테스트/venv/bin/python
   ```

**방법 2: 상태바에서 선택**
1. VS Code/Cursor 하단 상태바의 Python 버전을 클릭합니다
2. "Select Python Interpreter"를 선택합니다
3. `./venv/bin/python` 또는 `venv/bin/python`을 선택합니다

**방법 3: 직접 경로 입력**
인터프리터 선택 창에서 "Enter interpreter path..."를 선택하고:
```
/Users/yangsigwan/크롤링테스트/venv/bin/python
```

## 설치 방법

1. 가상환경 활성화 (위 참조)

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

## 필터링 기능 사용하기

`scrape_kstartup_filtered.py` 스크립트는 회사 조건에 맞는 공고를 자동으로 필터링합니다.

### 현재 설정된 조건
- **규모**: 10명 남짓
- **지원분야**: 헬스케어, 건강, 임상, AI 관련
- **업력**: 5-7년

### 조건 변경하기

`scrape_kstartup_filtered.py` 파일의 `main()` 함수에서 조건을 수정할 수 있습니다:

```python
company_filter = CompanyFilter(
    company_size="10명",
    support_fields=["헬스케어", "건강", "임상", "AI", "의료", "의약", "바이오", "헬스"],
    business_years="5-7년"
)
```

### 출력 파일

- `kstartup_filtered.json`: 조건에 맞는 공고만 필터링된 JSON 파일
- `kstartup_filtered.csv`: 조건에 맞는 공고만 필터링된 CSV 파일
- `kstartup_all.json`: 필터링 전 전체 공고 JSON 파일
- `kstartup_all.csv`: 필터링 전 전체 공고 CSV 파일

## 주의사항

- 웹사이트의 구조가 변경되면 스크립트 수정이 필요할 수 있습니다.
- 과도한 요청은 서버에 부하를 줄 수 있으므로 적절한 딜레이를 두고 사용하세요.
- 웹사이트의 이용약관을 확인하고 준수하세요.
- 페이지가 JavaScript로 동적 로드되므로 크롤링에 시간이 걸릴 수 있습니다.

