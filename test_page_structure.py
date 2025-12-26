"""페이지 구조 확인용 테스트 스크립트"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 브라우저 창 보이기
    page = browser.new_page()
    
    url = 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?page=1&pbancClssCd=PBC010'
    page.goto(url, wait_until='networkidle')
    page.wait_for_timeout(5000)
    
    # 페이지 구조 확인
    result = page.evaluate("""
        () => {
            const info = {
                basicItems: document.querySelectorAll('.basic_item').length,
                listItems: document.querySelectorAll('.list_item').length,
                allItems: document.querySelectorAll('[class*="item"]').length,
                pbancLinks: document.querySelectorAll('a[href*="pbancSn"]').length,
                allLinks: document.querySelectorAll('a').length,
                linkBoxList: document.querySelectorAll('.link_box-list').length,
                sampleHTML: ''
            };
            
            // 샘플 HTML
            const firstItem = document.querySelector('.basic_item, .list_item');
            if (firstItem) {
                info.sampleHTML = firstItem.outerHTML.substring(0, 1000);
            }
            
            // 모든 링크에서 pbancSn 찾기
            const allLinks = Array.from(document.querySelectorAll('a'));
            const pbancLinks = allLinks.filter(a => {
                const href = a.getAttribute('href') || '';
                return href.includes('pbancSn');
            });
            
            info.pbancLinksFound = pbancLinks.length;
            info.samplePbancLinks = pbancLinks.slice(0, 3).map(link => ({
                text: link.textContent.trim().substring(0, 50),
                href: link.getAttribute('href')
            }));
            
            return info;
        }
    """)
    
    print("페이지 구조 분석 결과:")
    print(f"  - basic_item 개수: {result['basicItems']}")
    print(f"  - list_item 개수: {result['listItems']}")
    print(f"  - [class*='item'] 개수: {result['allItems']}")
    print(f"  - a[href*='pbancSn'] 개수: {result['pbancLinks']}")
    print(f"  - 전체 링크 개수: {result['allLinks']}")
    print(f"  - link_box-list 개수: {result['linkBoxList']}")
    print(f"  - 실제 pbancSn 링크: {result['pbancLinksFound']}개")
    
    if result['samplePbancLinks']:
        print("\n샘플 링크:")
        for link in result['samplePbancLinks']:
            print(f"  - {link['text']}")
            print(f"    {link['href']}")
    
    if result['sampleHTML']:
        print(f"\n샘플 HTML (처음 1000자):\n{result['sampleHTML']}")
    
    input("\n브라우저를 확인하고 Enter를 누르세요...")
    browser.close()

