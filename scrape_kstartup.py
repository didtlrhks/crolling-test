"""
K-Startup 신규 사업 공고 크롤링 스크립트
Playwright를 사용하여 https://www.k-startup.go.kr/ 의 신규 사업 공고 데이터를 수집합니다.
"""

from playwright.sync_api import sync_playwright
import json
import csv
from datetime import datetime
from typing import List, Dict


def scrape_new_announcements() -> List[Dict]:
    """
    K-Startup 메인 페이지에서 신규 사업 공고 데이터를 크롤링합니다.
    
    Returns:
        List[Dict]: 공고 정보 리스트 (제목, URL, 상세 정보 등)
    """
    announcements = []
    
    with sync_playwright() as p:
        # 브라우저 실행 (headless=False로 설정하면 브라우저 창이 보입니다)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        try:
            # 메인 페이지 접속
            print("K-Startup 메인 페이지 접속 중...")
            page.goto('https://www.k-startup.go.kr/', wait_until='networkidle')
            page.wait_for_timeout(2000)  # 페이지 로딩 대기
            
            # "신규 사업 공고" 섹션 찾기
            print("신규 사업 공고 섹션 찾는 중...")
            
            # 방법 1: 제목으로 섹션 찾기
            section_heading = page.locator('h3:has-text("신규 사업 공고")')
            
            if section_heading.count() > 0:
                # 섹션 내의 공고 링크들 찾기
                # 섹션 내부의 리스트에서 링크 추출
                section = section_heading.locator('xpath=following-sibling::*[1]')
                
                # 공고 링크 선택자 (href에 pbancSn이 포함된 링크)
                # 섹션 내부의 링크만 선택
                announcement_links = section.locator('a[href*="pbancSn="]')
                
                link_count = announcement_links.count()
                print(f"메인 페이지에서 발견된 공고 링크 수: {link_count}")
                
                # 각 공고 정보 추출
                for i in range(link_count):
                    try:
                        link = announcement_links.nth(i)
                        title = link.inner_text().strip()
                        href = link.get_attribute('href')
                        
                        if href and title and len(title) > 5:
                            # 상대 경로를 절대 경로로 변환
                            if href.startswith('/'):
                                full_url = f'https://www.k-startup.go.kr{href}'
                            elif href.startswith('http'):
                                full_url = href
                            else:
                                full_url = f'https://www.k-startup.go.kr/{href}'
                            
                            # pbancSn 추출
                            pbanc_sn = None
                            if 'pbancSn=' in href:
                                pbanc_sn = href.split('pbancSn=')[1].split('&')[0]
                            
                            announcement = {
                                'title': title,
                                'url': full_url,
                                'pbanc_sn': pbanc_sn,
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            announcements.append(announcement)
                            print(f"  - {title}")
                    except Exception as e:
                        print(f"공고 {i+1} 처리 중 오류: {e}")
                        continue
            
            # 방법 2: JavaScript를 사용하여 메인 페이지에서 직접 추출
            print("\nJavaScript를 사용하여 추가 데이터 수집 중...")
            js_result = page.evaluate("""
                () => {
                    const announcements = [];
                    // "신규 사업 공고" 제목 찾기
                    const headings = Array.from(document.querySelectorAll('h3'));
                    const newAnnouncementHeading = headings.find(h => h.textContent.includes('신규 사업 공고'));
                    
                    if (newAnnouncementHeading) {
                        // 제목 다음 요소들에서 링크 찾기
                        let current = newAnnouncementHeading.nextElementSibling;
                        let depth = 0;
                        
                        while (current && depth < 10) {
                            const links = current.querySelectorAll('a[href*="pbancSn="]');
                            links.forEach(link => {
                                const href = link.getAttribute('href');
                                const title = link.textContent.trim();
                                
                                if (href && title && title.length > 5) {
                                    let fullUrl = href;
                                    if (href.startsWith('/')) {
                                        fullUrl = 'https://www.k-startup.go.kr' + href;
                                    } else if (!href.startsWith('http')) {
                                        fullUrl = 'https://www.k-startup.go.kr/' + href;
                                    }
                                    
                                    let pbancSn = null;
                                    if (href.includes('pbancSn=')) {
                                        pbancSn = href.split('pbancSn=')[1].split('&')[0];
                                    }
                                    
                                    announcements.push({
                                        title: title,
                                        url: fullUrl,
                                        pbanc_sn: pbancSn
                                    });
                                }
                            });
                            
                            if (links.length > 0) break;
                            current = current.nextElementSibling;
                            depth++;
                        }
                    }
                    
                    return announcements;
                }
            """)
            
            # 중복 제거를 위한 기존 URL 집합
            existing_urls = {ann['url'] for ann in announcements}
            
            for item in js_result:
                if item['url'] not in existing_urls:
                    item['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    announcements.append(item)
                    existing_urls.add(item['url'])
                    print(f"  - {item['title']}")
            
            # 방법 3: 전체 목록 페이지에서 추가 데이터 수집
            print("\n전체 목록 페이지에서 추가 데이터 수집 중...")
            page.goto('https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do', 
                     wait_until='networkidle')
            page.wait_for_timeout(3000)
            
            # 목록 페이지에서 공고 링크 찾기
            list_links = page.locator('a[href*="pbancSn="]')
            list_count = list_links.count()
            print(f"목록 페이지에서 발견된 공고 링크 수: {list_count}")
            
            for i in range(min(list_count, 50)):  # 최대 50개
                try:
                    link = list_links.nth(i)
                    title = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if not href or not title or len(title) < 5:
                        continue
                    
                    # 상대 경로를 절대 경로로 변환
                    if href.startswith('/'):
                        full_url = f'https://www.k-startup.go.kr{href}'
                    elif href.startswith('http'):
                        full_url = href
                    else:
                        full_url = f'https://www.k-startup.go.kr/{href}'
                    
                    # 중복 체크
                    if full_url in existing_urls:
                        continue
                    
                    # pbancSn 추출
                    pbanc_sn = None
                    if 'pbancSn=' in href:
                        pbanc_sn = href.split('pbancSn=')[1].split('&')[0]
                    
                    announcement = {
                        'title': title,
                        'url': full_url,
                        'pbanc_sn': pbanc_sn,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    announcements.append(announcement)
                    existing_urls.add(full_url)
                    print(f"  - {title}")
                except Exception as e:
                    print(f"목록 공고 {i+1} 처리 중 오류: {e}")
                    continue
            
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")
        finally:
            browser.close()
    
    return announcements


def save_to_json(data: List[Dict], filename: str = 'kstartup_announcements.json'):
    """데이터를 JSON 파일로 저장"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n데이터가 {filename}에 저장되었습니다.")


def save_to_csv(data: List[Dict], filename: str = 'kstartup_announcements.csv'):
    """데이터를 CSV 파일로 저장"""
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    fieldnames = ['title', 'url', 'pbanc_sn', 'scraped_at']
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"데이터가 {filename}에 저장되었습니다.")


def main():
    """메인 함수"""
    print("=" * 50)
    print("K-Startup 신규 사업 공고 크롤링 시작")
    print("=" * 50)
    
    # 크롤링 실행
    announcements = scrape_new_announcements()
    
    print(f"\n총 {len(announcements)}개의 공고를 수집했습니다.")
    
    # 데이터 저장
    if announcements:
        save_to_json(announcements)
        save_to_csv(announcements)
        
        # 결과 미리보기
        print("\n수집된 공고 목록:")
        print("-" * 50)
        for i, ann in enumerate(announcements[:10], 1):
            print(f"{i}. {ann['title']}")
            print(f"   URL: {ann['url']}")
        if len(announcements) > 10:
            print(f"\n... 외 {len(announcements) - 10}개")
    else:
        print("수집된 공고가 없습니다.")


if __name__ == '__main__':
    main()

