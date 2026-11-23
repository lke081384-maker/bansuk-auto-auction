# -*- coding: utf-8 -*-
"""반석자동차경매 홈페이지 빌드 스크립트.

실행:  python build.py
만드는 파일: index.html, process.html, promise.html, cases.html, faq.html, about.html,
            robots.txt, sitemap.xml, llms.txt
페이지 파일은 직접 고치지 말고 이 파일의 내용을 고친 뒤 다시 실행한다.
"""
import json
import html
from datetime import date
from pathlib import Path

# ── 한 곳에서 관리하는 값 ─────────────────────────────────────────────
BASE = "https://lke081384-maker.github.io/bansuk-auto-auction"  # 실제 주소가 정해지면 이 한 줄만 바꾼다 (끝에 / 없이)
NAME = "반석자동차경매"
OWNER = "이희철"
PHONE = "010-3351-8208"
PHONE_RAW = "01033518208"
KAKAO = "https://open.kakao.com/o/swZVu5h"
BLOG = "https://blog.naver.com/heechul5"
ADDRESS = "경기도 화성시 팔탄면 서해로1121번길 3 503동 301호"
CHECKED = "2026-11-24"  # 블로그 내용을 확인한 날
TODAY = date.today().isoformat()
OUT = Path(__file__).parent

NAV = [
    ("index.html", "홈"),
    ("process.html", "경매 절차"),
    ("promise.html", "비용·반품 약속"),
    ("cases.html", "낙찰 사례"),
    ("faq.html", "자주 묻는 질문"),
    ("about.html", "소개·연락처"),
]

# ── 내용 데이터 (모두 블로그 heechul5에 대표가 올린 글에서 가져옴) ──────
STEPS = [
    ("원하는 조건 알려 주기", "차종, 연식, 주행거리, 색상, 옵션을 카카오톡으로 알려 주세요."),
    ("출품 자료 받기", "조건에 맞는 출품 차량 자료를 경매 전날 밤이나 당일 아침 일찍 보내 드립니다."),
    ("점검 요청", "마음에 드는 차가 있으면 점검을 요청하세요. 몇 번을 요청해도 점검비는 없습니다."),
    ("사진·설명 보고 결정", "대표가 경매장에서 시동을 걸어 점검한 뒤 사진과 설명을 보내 드립니다. 그걸 보고 입찰할지 정합니다."),
    ("계약금 입금", "입찰을 원할 때 계약금 100만 원을 받습니다. 낙찰받지 못하면 전액 바로 돌려 드립니다."),
    ("낙찰 후 대금·보험", "낙찰되면 차량 대금을 고객 이름으로 경매장 계좌에 직접 입금하고, 자동차 보험에 가입합니다."),
    ("출고와 상품화", "광택, 판금·도색, 내비게이션, 블랙박스, 썬팅 같은 작업을 원하면 출고 뒤에 진행합니다."),
    ("타 보고 등록", "차를 먼저 받아 7~10일 타 본 뒤 이상이 없으면 이전 등록을 하고, 등록증은 등기로 보내 드립니다."),
]

WEEK = [
    ("월", "롯데 경매장", "안성"),
    ("화", "현대글로비스", "분당"),
    ("수", "오토허브옥션", "안성"),
    ("목", "현대글로비스 · 케이카옥션", "양산 · 오산"),
    ("금", "현대글로비스", "시화"),
]

PROMISES = [
    ("먼저 타 보고, 그다음에 등록합니다",
     "낙찰받은 차를 먼저 보내 드립니다. 7~10일 동안 평소처럼 타 보고 이상이 없을 때 등록을 요청하시면 됩니다."),
    ("고지와 다르면 환불합니다",
     "엔진·미션에 중대한 결함이 있거나, 사고·침수 여부가 알려 드린 내용과 다르면 책임지고 환불해 드립니다."),
    ("차량 대금은 경매장 계좌로 직접",
     "반석자동차경매는 차량 대금을 받지 않습니다. 고객 이름으로 경매장 계좌에 입금하므로 입금 기록이 그대로 남습니다."),
    ("낙찰 전에는 비용이 없습니다",
     "출품 자료와 점검은 무료입니다. 계약금 100만 원은 입찰을 정한 뒤에 받고, 낙찰이 안 되면 전액 돌려 드립니다."),
    ("수수료 표를 먼저 공개합니다",
     "상담을 시작할 때 수수료 표를 10원 단위까지 보내 드립니다. 처음 알려 드린 수수료 말고 다른 명목의 추가 비용은 없습니다."),
    ("대표가 처음부터 끝까지 합니다",
     "상담, 점검, 입찰, 상품화 진행을 대표 한 사람이 맡습니다. 담당자가 바뀌지 않으니 책임질 사람도 분명합니다."),
]

COMPARE = [
    ("더 뉴 그랜저 IG (2020~2022년식)", "약 1,900만~2,300만 원", "약 2,200만~2,600만 원", "약 150만~200만 원"),
    ("디 올 뉴 그랜저 GN7 (2023~2025년식)", "약 2,500만~3,300만 원", "약 3,000만~3,700만 원", "약 200만~300만 원"),
]

SALES = [(2015, 150), (2016, 210), (2017, 210), (2018, 190), (2019, 190), (2020, 220),
         (2021, 160), (2022, 160), (2023, 160), (2024, 160), (2025, 160)]

# (날짜, 연료, 차종, 한 줄 설명, 블로그 글 번호)
CASES = [
    ("2026-11-14", "디젤", "올 뉴 K7 디젤", "낙찰가 490만 원. 예전 고객의 소개로 이어진 거래입니다.", "224477145122"),
    ("2026-11-13", "하이브리드", "쏘렌토 하이브리드 2023년식", "카카오톡으로 자료를 보내고, 입찰부터 상품화까지 통화로 진행했습니다.", "224474710904"),
    ("2026-11-13", "LPG", "쏘나타 DN8 LPI", "옵션이 좋은 가스차를 낙찰받은 사례입니다.", "224475306916"),
    ("2026-11-13", "하이브리드", "디 올 뉴 니로 하이브리드", "원하는 그린 색상이 나올 때까지 기다려 낙찰받았습니다. 재구매 고객입니다.", "224474490375"),
    ("2026-11-12", "LPG", "올 뉴 K7 LPI", "가스차를 찾는 고객의 낙찰 사례입니다.", "224474322729"),
    ("2026-11-12", "하이브리드", "디 올 뉴 투싼 하이브리드", "원하는 조건의 차가 출품될 때까지 기다려 낙찰받았습니다.", "224474292354"),
    ("2026-08-31", "가솔린", "아반떼 AD", "조건에 맞는 차가 나오기까지 석 달이 걸린 사례입니다.", "224395923328"),
    ("2026-08-31", "디젤", "올 뉴 카니발 7인승 리무진 2018년식", "7인승 리무진 디젤 낙찰 사례입니다.", "224395887981"),
    ("2026-08-31", "가솔린", "K8 2.5 가솔린", "K8 2.5 가솔린 낙찰 사례입니다.", "224395851401"),
    ("2026-08-17", "전기", "니로 EV", "전기차 낙찰 사례입니다.", "224381465360"),
    ("2026-07-24", "수소", "넥쏘", "수소차 낙찰 사례입니다.", "224356380700"),
    ("2026-07-24", "전기", "EV6", "전기차 낙찰 사례입니다.", "224356341977"),
    ("2026-07-08", "가솔린", "더 올 뉴 G80", "낙찰가 4,420만 원.", "224340401499"),
]

# (작성자 표시, 날짜, 발췌) — 블로그 '솔직한 고객 후기 모음' 글에 실린 고객 댓글
REVIEWS = [
    ("조세비***", "2022.3.15.", "친절한 안내와, 고객의 입장에서 차량을 알아 봐 주고, 또 꼼꼼히 살펴주고, 마지막 탁송까지 친절하게 잘 해주셔서 너무 기분 좋게 차를 잘 전달 받았습니다."),
    ("소희소율***", "2021.2.16.", "처음에는 중고차에 대한 걱정이 있었는데, 받아보니 차량내부에 비닐도 안띤 거의 새차였습니다."),
    ("pixi***", "2021.3.10.", "이번 계기로 아버지께서 생각하시던 경매차량에 대한 인식이 완전히 바뀌셨습니다."),
    ("S** ***", "2026.7.15.", "여러번 귀찮게 해서 이 차량까지 4대를 반석님께 구매했네요."),
]
REVIEW_URL = BLOG + "/220728853054"
FAQ_SRC = BLOG + "/222062383436"

# (묶음, 질문, 답)
FAQS = [
    ("경매로 사는 방법", "일반인도 자동차경매장에서 직접 입찰할 수 있나요?",
     "아니요, 일반인은 직접 입찰할 수 없습니다. 경매장에 보증금과 연회비를 내고 계약한 매매상사만 입찰할 수 있어서, 반석자동차경매가 고객 대신 점검하고 입찰합니다."),
    ("경매로 사는 방법", "경매는 어떤 순서로 진행되나요?",
     "원하는 조건을 알려 주시면 출품 자료를 보내 드리고, 점검 → 입찰 결정 → 계약금 → 낙찰 → 대금 입금과 보험 가입 → 출고·상품화 → 타 본 뒤 등록 순서로 진행합니다. 자세한 내용은 경매 절차 페이지에 있습니다."),
    ("경매로 사는 방법", "경매는 언제 열리나요?",
     "월요일부터 금요일까지 열립니다. 월요일 롯데(안성), 화요일 현대글로비스(분당), 수요일 오토허브옥션(안성), 목요일 현대글로비스(양산)와 케이카옥션(오산), 금요일 현대글로비스(시화)입니다. 일정은 경매장 사정에 따라 바뀔 수 있습니다."),
    ("경매로 사는 방법", "출품 자료는 언제 받을 수 있나요?",
     "경매 전날 밤이나 경매 당일 아침 일찍 보내 드립니다."),
    ("경매로 사는 방법", "경매장에 직접 가서 차를 봐도 되나요?",
     "네, 언제든 경매장에 오셔서 차를 보실 수 있습니다. 시동을 걸어 보고 점검할 수 있습니다."),
    ("경매로 사는 방법", "시작가에서 얼마나 오르나요?",
     "시작가가 1,000만 원인 차는 버튼을 한 번 누를 때마다 5만 원씩 오릅니다. 블로그 안내 기준으로 시작가에서 100만~300만 원 오른 가격에 낙찰되는 경우가 많고, 많이 오를 때는 500만~1,000만 원까지 오르기도 합니다."),
    ("경매로 사는 방법", "법원 경매와는 무엇이 다른가요?",
     "자동차경매장에서는 시동을 걸고 엔진과 미션 상태를 점검할 수 있습니다. 법원 경매 차량은 시동을 걸어 볼 수 없습니다."),
    ("비용", "점검만 요청해도 비용이 드나요?",
     "아니요, 들지 않습니다. 낙찰 전까지는 비용이 없고, 점검을 여러 번 요청해도 점검비는 무료입니다."),
    ("비용", "계약금은 언제, 얼마를 내나요?",
     "점검 내용과 사진을 보고 입찰을 원하실 때 계약금 100만 원을 받습니다. 낙찰받지 못하면 전액 바로 돌려 드립니다."),
    ("비용", "수수료는 얼마인가요?",
     "수수료 표는 카카오톡으로 요청하시면 10원 단위까지 정리해 바로 보내 드립니다. 블로그 안내에 따르면 대행료와 매도비는 받지 않고 기본 상사매입비는 받습니다. 처음 알려 드린 수수료 외에 추가 비용은 없습니다."),
    ("비용", "더 싼 곳을 찾으면 어떻게 하나요?",
     "대표가 블로그에 밝힌 최저가 보장제에 따라, 더 낮은 수수료를 제시하는 곳이 있으면 그 업체의 정산 방식을 적용하고 20만 원을 더 할인해 드립니다."),
    ("비용", "차량 대금은 어디로 입금하나요?",
     "경매장 계좌에 고객 이름으로 직접 입금합니다. 반석자동차경매는 차량 대금을 받지 않습니다. 입금 기한은 낙찰 후 3일 이내입니다."),
    ("비용", "현금영수증이나 세금계산서를 발행해 주나요?",
     "네, 추가금 없이 발행해 드립니다."),
    ("비용", "광택이나 도색 같은 상품화 비용은 얼마나 드나요?",
     "광택, 판금·도색, 블랙박스, 내비게이션, 썬팅, 언더코팅을 협력 업체에서 업자 가격으로 해 드립니다. 금액은 차 상태와 작업 범위에 따라 달라 상담 때 안내합니다."),
    ("비용", "할부나 대출로도 살 수 있나요?",
     "네, 은행 자동차 대출이나 캐피탈을 이용할 수 있습니다. 대표는 블로그에서 캐피탈사로부터 수수료를 받지 않는다고 밝히고 있습니다. 금리는 시기와 신용에 따라 달라 상담 때 확인해 드립니다."),
    ("낙찰 뒤", "낙찰 후 차를 받기까지 얼마나 걸리나요?",
     "상품화 작업을 하면 보통 3~5일 걸립니다. 광택은 하루, 판금·도색은 이틀 정도 필요합니다. 아무 작업도 하지 않으면 경매 당일 탁송으로 받을 수도 있습니다."),
    ("낙찰 뒤", "차를 받을 때 등록증도 같이 받나요?",
     "아니요, 등록은 차를 타 본 뒤에 합니다. 차를 먼저 받아 7~10일 운행해 보고 이상이 없으면 등록하고, 등록증은 등기로 보내 드립니다. 보험에 가입되어 있으면 등록 전에도 운행할 수 있습니다."),
    ("낙찰 뒤", "낙찰받은 뒤에 취소할 수 있나요?",
     "아니요, 취소할 수 없습니다. 취소하면 낙찰가의 10%를 경매장에 내야 합니다."),
    ("낙찰 뒤", "차가 마음에 안 들면 반품할 수 있나요?",
     "엔진·미션에 중대한 결함이 있거나 사고·침수 여부가 알려 드린 내용과 다르면 환불해 드립니다. 타이어, 라이닝, 배터리, 오일류 같은 소모품이나 흠집을 이유로 한 반품은 되지 않습니다."),
    ("낙찰 뒤", "엔진·미션 보증이 있나요?",
     "네, 블로그 안내 기준으로 1개월 또는 2,000km까지 엔진·미션을 보증합니다."),
    ("낙찰 뒤", "타던 차도 매입해 주나요?",
     "네, 매입해 드립니다. 타던 차의 차종과 상태를 상담 때 알려 주세요."),
    ("반석자동차경매", "상담부터 낙찰까지 누가 진행하나요?",
     "대표 이희철이 상담, 점검, 입찰, 상품화 진행을 직접 맡습니다. 차량 등록 서류는 담당 직원이 돕습니다."),
    ("반석자동차경매", "지방에 살아도 이용할 수 있나요?",
     "네, 이용할 수 있습니다. 상담은 카카오톡과 전화로 진행하고 차는 탁송으로 보내 드립니다."),
    ("반석자동차경매", "상담은 어떻게 신청하나요?",
     "카카오톡 오픈채팅이나 문자(" + PHONE + ")로 원하는 차종, 연식, 주행거리, 색상, 옵션을 알려 주시면 됩니다."),
]

# ── 도우미 ────────────────────────────────────────────────────────────
def e(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def business_ld(full=False):
    d = {
        "@context": "https://schema.org",
        "@type": "AutoDealer",
        "@id": BASE + "/#business",
        "name": NAME,
        "url": BASE + "/",
        "telephone": "+82-10-3351-8208",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "KR",
            "addressRegion": "경기도",
            "addressLocality": "화성시",
            "streetAddress": "팔탄면 서해로1121번길 3 503동 301호",
        },
        "sameAs": [BLOG, KAKAO],
    }
    if full:
        d["founder"] = {"@type": "Person", "name": OWNER, "jobTitle": "대표"}
        d["description"] = "대기업 자동차경매장에서 대표가 직접 점검하고 입찰하는 중고차 경매 대행. 먼저 타 본 뒤 등록하는 반품 제도를 운영합니다."
        d["areaServed"] = {"@type": "Country", "name": "대한민국"}
        d["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": "자동차경매 대행 서비스",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
                for n in ["자동차경매 입찰 대행", "경매 출품 차량 점검", "출고 차량 상품화(광택·판금·도색)", "타던 차 매입"]
            ],
        }
    return d


def crumbs_ld(title, page):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + "/" + page},
        ],
    }


MARK = ('<svg class="brand-mark" viewBox="0 0 30 30" aria-hidden="true">'
        '<rect width="30" height="30" rx="4" fill="#0e4b3a"/>'
        '<path d="M5 22 11 10l5 7 3-4 6 9z" fill="#f4c20d"/></svg>')


def layout(page, title, desc, body, extra_ld=None, full_ld=False):
    url = BASE + "/" + ("" if page == "index.html" else page)
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == page else "", e(t)) for h, t in NAV
    )
    lds = [ld(business_ld(full_ld))] + [ld(x) for x in (extra_ld or [])]
    return """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="theme-color" content="#08301f">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@700;800&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/style.css">
{lds}
</head>
<body>
<a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="index.html">{mark}{name}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">메뉴</button>
    <nav class="nav" id="nav" aria-label="주요 메뉴">{nav}<a class="nav-cta" href="{kakao}" target="_blank" rel="noopener">카카오톡 상담</a></nav>
  </div>
</header>
<main id="main">
{body}
<section class="cta" aria-labelledby="cta-h">
  <div class="wrap">
    <h2 id="cta-h">찾는 차의 조건만 알려 주세요</h2>
    <p>차종, 연식, 주행거리, 색상, 옵션을 보내 주시면 조건에 맞는 출품 차량 자료와 수수료 표를 보내 드립니다. 낙찰 전까지는 비용이 없습니다.</p>
    <div class="btn-row">
      <a class="btn btn-kakao" href="{kakao}" target="_blank" rel="noopener">카카오톡으로 상담하기</a>
      <a class="btn btn-line" href="sms:{phone_raw}">문자 보내기 {phone}</a>
    </div>
  </div>
</section>
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <strong>{name}</strong>
      <p>대표 {owner} · {address}</p>
      <p>문자·전화 <a href="tel:{phone_raw}">{phone}</a> · <a href="{blog}" target="_blank" rel="noopener">네이버 블로그</a></p>
      <p>이 홈페이지의 내용은 대표가 네이버 블로그에 올린 글을 {checked}에 확인해 정리한 것입니다. 수수료와 경매 일정은 상담 때 다시 확인해 주세요.</p>
    </div>
    <nav aria-label="바닥 메뉴"><ul>{foot_nav}</ul></nav>
  </div>
</footer>
<div class="dock">
  <a href="{kakao}" target="_blank" rel="noopener">카카오톡 상담</a>
  <a href="sms:{phone_raw}">문자</a>
  <a href="tel:{phone_raw}">전화</a>
</div>
<script src="assets/site.js" defer></script>
</body>
</html>
""".format(
        title=e(title), desc=e(desc), url=url, name=NAME, lds="\n".join(lds), mark=MARK, nav=nav,
        kakao=KAKAO, phone=PHONE, phone_raw=PHONE_RAW, owner=OWNER, address=ADDRESS, blog=BLOG,
        checked=CHECKED.replace("-", "."), body=body,
        foot_nav="".join('<li><a href="%s">%s</a></li>' % (h, e(t)) for h, t in NAV),
    )


def page_head(title, lede):
    return ('<section class="page-head"><div class="wrap"><h1><span class="name">%s</span>%s</h1>'
            '<p>%s</p></div></section>' % (NAME, e(title), lede))


def steps_html(cls="steps"):
    return '<ol class="%s">%s</ol>' % (
        cls, "".join("<li><h3>%s</h3><p>%s</p></li>" % (e(t), e(d)) for t, d in STEPS))


def week_html():
    return '<div class="week">%s</div>' % "".join(
        '<div class="day"><b>%s</b><div><span>%s</span><small>%s</small></div></div>' % (d, e(n), e(p))
        for d, n, p in WEEK)


def promises_html():
    return '<div class="promises">%s</div>' % "".join(
        '<div class="promise"><h3>%s</h3><p>%s</p></div>' % (e(t), e(d)) for t, d in PROMISES)


def compare_html():
    rows = "".join(
        '<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td class="save">%s</td></tr>' % tuple(map(e, r))
        for r in COMPARE)
    return ('<div class="table-wrap"><table><caption>대표가 2026년 6월 블로그에 정리한 그랜저 비교입니다. '
            '차 상태와 시기에 따라 달라지며 절약 금액을 보장하는 표는 아닙니다.</caption>'
            '<thead><tr><th scope="col">차종</th><th scope="col">경매장 평균 낙찰가</th>'
            '<th scope="col">매매상 시세</th><th scope="col">예상 차이</th></tr></thead>'
            '<tbody>%s</tbody></table></div>' % rows)


def ledger_html(items):
    out = []
    for d, fuel, car, note, no in items:
        out.append(
            '<li><time datetime="%s">%s</time><span class="fuel">%s</span>'
            '<h3>%s<small>%s</small></h3>'
            '<a href="%s/%s" target="_blank" rel="noopener" aria-label="%s 낙찰 글 블로그에서 보기">블로그 글 보기</a></li>'
            % (d, d.replace("-", "."), e(fuel), e(car), e(note), BLOG, no, e(car)))
    return '<ul class="ledger">%s</ul>' % "".join(out)


def bars_html():
    top = max(n for _, n in SALES)
    bars = "".join('<div class="bar" style="height:%d%%"><span>%d</span></div>' % (round(n / top * 88), n)
                   for _, n in SALES)
    years = "".join("<span>’%02d</span>" % (y % 100) for y, _ in SALES)
    total = sum(n for _, n in SALES)
    label = ", ".join("%d년 %d대" % (y, n) for y, n in SALES)
    return ('<div class="bars" role="img" aria-label="연도별 판매 대수: %s">%s</div>'
            '<div class="bar-years" aria-hidden="true">%s</div>'
            '<p class="note" style="margin-top:1rem">대표가 블로그에 공개한 2015~2025년 판매 대수입니다(단위: 대). '
            '11년 합계는 %s대입니다.</p>' % (label, bars, years, format(total, ",")))


def reviews_html(items):
    return '<div class="reviews">%s</div>' % "".join(
        '<blockquote><p>“%s”</p><footer>%s · %s 블로그 댓글</footer></blockquote>' % (e(q), e(w), e(d))
        for w, d, q in items)


def faq_html(items, grouped=False):
    out, last = [], None
    for g, q, a in items:
        if grouped and g != last:
            if last is not None:
                out.append("</div>")
            out.append('<h2 class="faq-group">%s</h2><div class="faq">' % e(g))
            last = g
        out.append("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)))
    if grouped:
        return "".join(out) + "</div>"
    return '<div class="faq">%s</div>' % "".join(out)


def faq_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for _, q, a in items
        ],
    }


# ── 페이지 ────────────────────────────────────────────────────────────
def page_index():
    hero_case = CASES[0]
    home_faq = [f for f in FAQS if f[1] in (
        "일반인도 자동차경매장에서 직접 입찰할 수 있나요?",
        "점검만 요청해도 비용이 드나요?",
        "계약금은 언제, 얼마를 내나요?",
        "차량 대금은 어디로 입금하나요?",
        "차가 마음에 안 들면 반품할 수 있나요?",
        "지방에 살아도 이용할 수 있나요?",
    )]
    body = """
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1><span class="name">{name} · 경기 화성</span>대기업 자동차경매장에서 대표가 직접 보고 낙찰받아 드립니다</h1>
      <p class="lede">일반인은 들어갈 수 없는 경매장에서, 2014년부터 경매 대행만 해 온 대표가 시동을 걸어 점검하고 입찰합니다. 차를 먼저 받아 7~10일 타 본 뒤에 등록합니다.</p>
      <div class="btn-row">
        <a class="btn btn-kakao" href="{kakao}" target="_blank" rel="noopener">카카오톡으로 상담하기</a>
        <a class="btn btn-line" href="process.html">경매 절차 보기</a>
      </div>
      <p class="fine">문자 상담 <a href="sms:{phone_raw}">{phone}</a> · 낙찰 전까지 비용 없음</p>
    </div>
    <div class="board" aria-label="낙찰 사례 전광판">
      <div class="board-head"><span>최근 낙찰 사례</span><span class="lamp">경매 진행</span></div>
      <p class="board-car">{car}</p>
      <p class="board-sub">{cdate} 블로그 게시</p>
      <p class="board-price"><b data-price="490">490</b><span>만 원</span></p>
      <p class="board-step">입찰 버튼을 한 번 누르면 5만 원씩 오릅니다</p>
      <div class="stamp" aria-hidden="true">낙찰</div>
      <p class="board-foot">숫자가 오르는 모습은 경매 방식을 보여 주는 연출이고, 490만 원이 실제 낙찰가입니다. <a href="{blog}/{cno}" target="_blank" rel="noopener">이 사례 글 보기</a></p>
    </div>
  </div>
</section>

<section class="sec sec-paper" aria-labelledby="h-promise">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-promise">차를 보지 않고 사는 불안을 줄이는 여섯 가지 약속</h2>
      <p>경매 대행은 고객이 차를 직접 보지 못한 채 진행되는 경우가 많습니다. 그래서 돈이 오가는 길과 책임지는 범위를 먼저 밝혀 둡니다.</p>
    </div>
    {promises}
    <p class="more"><a href="promise.html">비용과 반품 약속 자세히 보기</a></p>
  </div>
</section>

<section class="sec sec-green" aria-labelledby="h-steps">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-steps">조건을 알려 주는 것부터 등록까지 여덟 단계</h2>
      <p>상담은 카카오톡과 전화로 진행하고, 차는 탁송으로 보내 드립니다. 지방에 계셔도 같은 순서로 진행합니다.</p>
    </div>
    {steps}
    <p class="more"><a href="process.html">단계별 설명과 경매 요일 보기</a></p>
  </div>
</section>

<section class="sec" aria-labelledby="h-compare">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-compare">같은 그랜저, 경매장 낙찰가와 매매상 시세</h2>
      <p>매매상은 경매장에서 낙찰받은 차에 마진을 붙여 팝니다. 경매 대행은 그 낙찰가에 수수료를 더해 사는 방식입니다.</p>
    </div>
    {compare}
  </div>
</section>

<section class="sec sec-paper" aria-labelledby="h-cases">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-cases">최근에 낙찰받은 차</h2>
      <p>블로그에는 낙찰 사례 글이 1,282개 있습니다({checked} 기준). 고객과 주고받은 상담 내용과 차량 사진은 각 글에서 볼 수 있습니다.</p>
    </div>
    {ledger}
    <p class="more"><a href="cases.html">낙찰 사례 더 보기</a></p>
  </div>
</section>

<section class="sec" aria-labelledby="h-sales">
  <div class="wrap two">
    <div>
      <h2 id="h-sales">대표 한 사람이 해마다 150대 넘게 낙찰받았습니다</h2>
      <p style="margin-top:1rem;color:var(--ink-soft)">딜러를 여러 명 두지 않고, 서류를 돕는 직원 한 명과 일합니다. 대표는 판매한 차의 70%가 재구매와 지인 소개라고 블로그에 밝히고 있습니다.</p>
      <p><a href="about.html">대표 소개 보기</a></p>
    </div>
    <div>{bars}</div>
  </div>
</section>

<section class="sec sec-paper" aria-labelledby="h-reviews">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-reviews">차를 받은 고객이 블로그에 남긴 글</h2>
    </div>
    {reviews}
    <p class="more"><a href="{review_url}" target="_blank" rel="noopener">블로그에서 후기 모음 전체 보기</a></p>
  </div>
</section>

<section class="sec" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="h-faq">처음 경매로 차를 살 때 많이 묻는 질문</h2>
    </div>
    {faq}
    <p class="more"><a href="faq.html">질문 {nfaq}개 모두 보기</a></p>
  </div>
</section>
""".format(
        name=NAME, kakao=KAKAO, phone=PHONE, phone_raw=PHONE_RAW, blog=BLOG,
        car=e(hero_case[2]), cdate=hero_case[0].replace("-", "."), cno=hero_case[4],
        promises=promises_html(), steps=steps_html(), compare=compare_html(),
        ledger=ledger_html(CASES[:6]), bars=bars_html(), reviews=reviews_html(REVIEWS),
        review_url=REVIEW_URL, faq=faq_html(home_faq), nfaq=len(FAQS), checked=CHECKED.replace("-", "."),
    )
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": BASE + "/", "inLanguage": "ko"}
    return layout("index.html", "반석자동차경매 | 화성 중고차 자동차경매 대행",
                  "대기업 자동차경매장에서 대표가 직접 점검하고 입찰하는 중고차 경매 대행. 낙찰 전 비용 없음, 차량 대금은 경매장 계좌로 직접 입금, 7~10일 타 본 뒤 등록합니다.",
                  body, [site_ld, faq_ld(home_faq)], full_ld=True)


def page_process():
    body = page_head("자동차경매 대행 절차", "조건을 알려 주시는 것부터 등록증을 받기까지의 순서입니다. 낙찰 전까지는 비용이 들지 않습니다.") + """
<section class="sec sec-paper"><div class="wrap">
  <div class="sec-head"><h2>여덟 단계로 진행합니다</h2></div>
  {steps}
</div></section>

<section class="sec sec-green"><div class="wrap">
  <div class="sec-head">
    <h2>경매는 월요일부터 금요일까지 열립니다</h2>
    <p>일주일에 약 8천 대가 출품됩니다. 원하는 조건의 차가 바로 없으면 다음 경매를 기다리면 됩니다.</p>
  </div>
  {week}
  <p class="note" style="margin-top:1rem">블로그 안내 기준입니다. 경매장 사정에 따라 요일과 장소가 바뀔 수 있어 상담 때 다시 확인해 드립니다.</p>
</div></section>

<section class="sec"><div class="wrap prose">
  <h2>입찰 가격은 이렇게 오릅니다</h2>
  <p>시작가가 1,000만 원인 차는 입찰 버튼을 한 번 누를 때마다 5만 원씩 오릅니다. 경매장은 딜러의 참여를 늘리려고 시작가를 낮게 잡기 때문에, 블로그 안내 기준으로 시작가보다 100만~300만 원 높은 가격에 낙찰되는 경우가 많습니다. 많이 오를 때는 500만~1,000만 원까지 오르기도 합니다.</p>
  <p>그래서 입찰 전에 얼마까지 따라갈지 상한가를 함께 정합니다.</p>

  <h2>낙찰 뒤에 고객이 할 일</h2>
  <ul>
    <li>낙찰 후 3일 이내에 차량 대금을 경매장 계좌로, 고객 이름으로 입금합니다.</li>
    <li>자동차 보험에 가입합니다. 보험에 가입되어야 경매장에서 차를 출고할 수 있습니다.</li>
    <li>낙찰 뒤에는 취소할 수 없습니다. 취소하면 낙찰가의 10%를 경매장에 내야 합니다.</li>
  </ul>

  <h2>차를 받기까지 걸리는 시간</h2>
  <p>광택은 하루, 판금·도색은 이틀 정도 필요해서 상품화 작업을 하면 보통 3~5일 걸립니다. 아무 작업도 원하지 않으면 경매 당일 탁송으로 집 앞에서 받을 수 있습니다.</p>
  <p>조건이 까다로우면 원하는 차가 출품될 때까지 시간이 걸립니다. 블로그에는 아반떼 AD를 석 달 기다려 낙찰받은 사례도 있습니다.</p>

  <h2>경매장 평가점 읽는 법</h2>
  <p>경매장마다 평가점을 매기는 방식이 다릅니다. 대표가 블로그에 정리한 기준은 다음과 같습니다.</p>
  <ul>
    <li>현대글로비스: A7~A9 정도면 교환이 없는 무사고 차량입니다. B, C, D, F로 시작하면 골격에 사고가 있는 차량입니다.</li>
    <li>롯데: A/B처럼 빗금 앞뒤로 적습니다. 빗금 앞 글자가 A이면 교환 없는 무사고, B이면 펜더나 문짝 같은 단순 교환이 있는 차량입니다.</li>
    <li>오토허브옥션: 롯데와 비슷하지만, 앞 글자가 C여도 무사고인 경우가 있습니다.</li>
  </ul>
  <p>평가점만으로는 엔진·미션 상태를 알 수 없습니다. 그래서 대표가 직접 시동을 걸어 점검하고, 사고 차량은 자료에서 빼고 보내 드립니다.</p>
</div></section>
""".format(steps=steps_html("steps steps-light steps-wide"), week=week_html())
    howto = {
        "@context": "https://schema.org", "@type": "HowTo", "name": "반석자동차경매 자동차경매 대행 절차",
        "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(STEPS)],
    }
    return layout("process.html", "자동차경매 대행 절차와 경매 요일 | 반석자동차경매",
                  "조건 상담, 출품 자료, 무료 점검, 계약금 100만 원, 낙찰, 대금 입금, 상품화, 타 본 뒤 등록까지 자동차경매 대행 여덟 단계와 요일별 경매장을 안내합니다.",
                  body, [crumbs_ld("경매 절차", "process.html"), howto])


def page_promise():
    cost_faq = [f for f in FAQS if f[0] == "비용"]
    body = page_head("비용과 반품 약속", "돈이 언제, 어디로 가는지와 문제가 생겼을 때 책임지는 범위를 먼저 알려 드립니다.") + """
<section class="sec sec-paper"><div class="wrap">
  <div class="sec-head"><h2>여섯 가지 약속</h2></div>
  {promises}
</div></section>

<section class="sec"><div class="wrap two">
  <div class="prose">
    <h2>돈이 오가는 순서</h2>
    <ul>
      <li>상담, 출품 자료, 점검: 비용 없음</li>
      <li>입찰을 정했을 때: 계약금 100만 원 (낙찰이 안 되면 전액 환불)</li>
      <li>낙찰 후 3일 이내: 차량 대금을 고객 이름으로 경매장 계좌에 입금</li>
      <li>수수료: 상담 때 받은 수수료 표대로 정산</li>
      <li>상품화: 원하는 작업만 선택</li>
    </ul>
    <p>현금영수증과 세금계산서는 추가금 없이 발행해 드립니다.</p>
  </div>
  <div class="prose">
    <h2>수수료</h2>
    <p>수수료 표는 카카오톡으로 요청하시면 10원 단위까지 정리해 보내 드립니다. 블로그 안내에 따르면 대행료와 매도비는 받지 않고, 기본 상사매입비는 받습니다.</p>
    <p>대표가 블로그에 밝힌 최저가 보장제도 있습니다. 더 낮은 수수료를 제시하는 곳이 있으면 그 업체의 정산 방식을 적용하고 20만 원을 더 할인해 드립니다.</p>
    <p><a class="btn btn-green" href="{kakao}" target="_blank" rel="noopener">수수료 표 요청하기</a></p>
  </div>
</div></section>

<section class="sec sec-green"><div class="wrap two">
  <div>
    <h2>먼저 타 보고, 그다음에 등록</h2>
    <p style="margin-top:1rem">낙찰받은 차를 먼저 보내 드립니다. 7~10일 동안 평소처럼 운행해 보고, 이상이 없다고 확인한 뒤 등록을 요청하시면 이전 등록을 마치고 등록증을 등기로 보내 드립니다. 더 오래 타 보고 싶으면 기간을 조율할 수 있습니다.</p>
    <p>등록을 먼저 하면 문제가 생겼을 때 되돌리기 어렵기 때문에 순서를 이렇게 잡았습니다. 보험에 가입되어 있으면 등록 전에도 운행할 수 있습니다.</p>
  </div>
  <div>
    <h2>환불하는 경우와 안 되는 경우</h2>
    <p style="margin-top:1rem"><strong>환불합니다.</strong> 경매장에서 점검해 알려 드린 내용과 달리 엔진·미션에 중대한 결함이 있을 때, 사고나 침수 여부가 알려 드린 내용과 다를 때.</p>
    <p><strong>반품이 안 됩니다.</strong> 타이어, 라이닝, 배터리, 오일류 같은 소모품이나 흠집을 이유로 한 경우.</p>
    <p>블로그 안내 기준으로 엔진·미션은 1개월 또는 2,000km까지 보증합니다.</p>
  </div>
</div></section>

<section class="sec sec-paper"><div class="wrap">
  <div class="sec-head">
    <h2>경매장 성능 기록만 믿지 않는 이유</h2>
    <p>대표가 블로그에 쓴 주의사항을 간추렸습니다.</p>
  </div>
  <div class="promises">
    <div class="promise"><h3>외관은 과하게, 엔진은 나쁘게 적힙니다</h3><p>경매장은 딜러의 항의를 피하려고 잔흠집에도 도색이 필요하다고 적고, 엔진·미션은 책임을 지지 않으려고 좋지 않게 적는 경향이 있습니다. 정말 나쁜 차와 구분하려면 직접 봐야 합니다.</p></div>
    <div class="promise"><h3>운행은 못 하고 소리로 판단합니다</h3><p>경매장 차는 시동은 걸 수 있어도 운행해 볼 수는 없습니다. 엔진과 미션 소리를 듣고 판단해야 해서 경험이 필요합니다.</p></div>
    <div class="promise"><h3>침수 의심 차는 건너뜁니다</h3><p>경매장 점검이 침수차를 다 걸러 내지는 못합니다. 조금이라도 의심되는 차는 입찰하지 않습니다.</p></div>
    <div class="promise"><h3>무사고 표기도 다시 확인합니다</h3><p>무사고로 고지된 차에서 사고 부위가 발견되는 경우가 있습니다. 대표는 낙찰받은 차를 경매장에 반품할 수 없기 때문에 더 꼼꼼히 봅니다.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>비용에 관한 질문</h2></div>
  {faq}
</div></section>
""".format(promises=promises_html(), kakao=KAKAO, faq=faq_html(cost_faq))
    return layout("promise.html", "자동차경매 대행 수수료·반품 제도 | 반석자동차경매",
                  "낙찰 전 비용 없음, 계약금 100만 원 환불 조건, 경매장 계좌 직접 입금, 수수료 표 공개, 7~10일 타 본 뒤 등록하는 반품 제도를 안내합니다.",
                  body, [crumbs_ld("비용·반품 약속", "promise.html"), faq_ld(cost_faq)])


def page_cases():
    body = page_head("자동차경매 낙찰 사례", "최근 블로그에 올린 낙찰 사례입니다. 고객과 주고받은 상담 내용과 차량 사진은 각 글에서 볼 수 있습니다.") + """
<section class="sec sec-paper"><div class="wrap">
  <div class="sec-head">
    <h2>2026년 하반기 낙찰 사례</h2>
    <p>하이브리드, LPG, 전기, 수소, 디젤, 가솔린까지 연료 종류를 가리지 않고 대행합니다.</p>
  </div>
  {ledger}
  <p class="note" style="margin-top:1.25rem">낙찰가는 블로그 글에 적힌 경우에만 옮겼습니다. 같은 차종이라도 연식, 주행거리, 상태, 시기에 따라 낙찰가가 달라집니다.</p>
</div></section>

<section class="sec"><div class="wrap two">
  <div>
    <h2>블로그에 쌓인 낙찰 기록</h2>
    <p style="margin-top:1rem;color:var(--ink-soft)">낙찰 사례 글은 두 개의 모음에 나뉘어 있습니다. 찾는 차종 이름으로 블로그 안에서 검색하면 비슷한 사례를 볼 수 있습니다.</p>
    <dl class="facts">
      <div><dt>낙찰 모음 1</dt><dd>824개</dd></div>
      <div><dt>낙찰 모음 2</dt><dd>458개</dd></div>
      <div><dt>블로그 전체 글</dt><dd>1,398개</dd></div>
      <div><dt>기준일</dt><dd>{checked}</dd></div>
    </dl>
    <p style="margin-top:1.5rem"><a class="btn btn-green" href="{blog}" target="_blank" rel="noopener">네이버 블로그에서 전체 보기</a></p>
  </div>
  <div>
    <h2>연도별 판매 대수</h2>
    <div style="margin-top:3rem">{bars}</div>
  </div>
</div></section>

<section class="sec sec-paper"><div class="wrap">
  <div class="sec-head"><h2>차를 받은 고객이 블로그에 남긴 글</h2></div>
  {reviews}
  <p class="more"><a href="{review_url}" target="_blank" rel="noopener">블로그에서 후기 모음 전체 보기</a></p>
</div></section>
""".format(ledger=ledger_html(CASES), bars=bars_html(), reviews=reviews_html(REVIEWS),
           review_url=REVIEW_URL, blog=BLOG, checked=CHECKED.replace("-", "."))
    return layout("cases.html", "자동차경매 낙찰 사례 | 반석자동차경매",
                  "올 뉴 K7, 쏘렌토 하이브리드, 쏘나타 LPI, 니로 EV, G80 등 반석자동차경매가 최근 낙찰받은 차량 사례와 고객 후기를 모았습니다.",
                  body, [crumbs_ld("낙찰 사례", "cases.html")])


def page_faq():
    body = page_head("자동차경매 자주 묻는 질문", "처음 경매로 차를 사려는 분들이 많이 묻는 질문을 모았습니다. 답은 대표가 블로그에 올린 내용을 기준으로 정리했습니다.") + """
<section class="sec sec-paper"><div class="wrap">
  {faq}
  <p class="note" style="margin-top:2rem">출처: <a href="{src}" target="_blank" rel="noopener">블로그 ‘자동차경매에 관한 궁금한 질문들’</a>과 최근 낙찰 글. 수수료, 금리, 경매 일정처럼 바뀔 수 있는 내용은 상담 때 다시 확인해 주세요.</p>
</div></section>
""".format(faq=faq_html(FAQS, grouped=True), src=FAQ_SRC)
    return layout("faq.html", "자동차경매 자주 묻는 질문 %d가지 | 반석자동차경매" % len(FAQS),
                  "일반인 입찰 가능 여부, 계약금과 수수료, 차량 대금 입금, 낙찰 후 취소, 반품과 보증까지 자동차경매 대행에 관한 질문에 답합니다.",
                  body, [crumbs_ld("자주 묻는 질문", "faq.html"), faq_ld(FAQS)])


def page_about():
    body = page_head("소개와 연락처", "정직하게, 거룩하게, 온유하게. 대표가 블로그 첫머리에 걸어 둔 말입니다.") + """
<section class="sec sec-paper"><div class="wrap two">
  <div class="prose">
    <h2>대표 {owner}</h2>
    <p>2014년부터 자동차경매 대행만 해 왔습니다. 상담, 경매장 점검, 입찰, 상품화 진행을 직접 맡고, 차량 등록 서류는 직원 한 명이 돕습니다.</p>
    <p>딜러를 여러 명 두고 회사를 키우지 않는 이유를 대표는 블로그에 이렇게 적었습니다. 직원의 실수로 회사의 이름이 흐려지는 것보다, 3년이나 5년, 10년 뒤 차를 바꿀 때 다시 찾아 주는 고객을 기대하며 일하겠다는 것입니다.</p>
    <p>대표는 판매한 차의 70%가 재구매와 지인 소개라고 밝히고 있습니다. 블로그에는 한 고객의 소개로 열 대쯤 거래가 이어진 사례, 같은 고객이 다섯 번째 차를 맡긴 사례가 올라와 있습니다.</p>

    <h2>일하는 곳</h2>
    <p>회사는 경기도 화성에 있습니다. 광택, 판금·도색, 내비게이션, 블랙박스 같은 상품화 작업은 군포의 협력 업체에서 합니다. 경매는 안성, 분당, 오산, 시화, 양산의 경매장에서 열립니다.</p>

    <h2>블로그</h2>
    <p>낙찰 사례와 경매 정보를 네이버 블로그에 꾸준히 올리고 있습니다. {checked} 기준으로 글 1,398개, 이웃 6,652명, 누적 방문 246만여 회입니다.</p>
    <p><a href="{blog}" target="_blank" rel="noopener">네이버 블로그 바로 가기</a></p>
  </div>
  <div>
    <h2>연락처</h2>
    <dl class="facts" style="margin-top:1.5rem">
      <div><dt>상호</dt><dd>{name}</dd></div>
      <div><dt>대표</dt><dd>{owner}</dd></div>
      <div><dt>주소</dt><dd>{address}</dd></div>
      <div><dt>문자·전화</dt><dd><a href="tel:{phone_raw}">{phone}</a></dd></div>
      <div><dt>카카오톡</dt><dd><a href="{kakao}" target="_blank" rel="noopener">오픈채팅 상담방</a></dd></div>
      <div><dt>블로그</dt><dd><a href="{blog}" target="_blank" rel="noopener">blog.naver.com/heechul5</a></dd></div>
    </dl>
    <p style="margin:2rem 0 .75rem;color:var(--ink-soft)">문자나 카카오톡으로 연락 주세요.</p>
    <a class="plate" href="sms:{phone_raw}" aria-label="문자 보내기 {phone}">{phone}</a>
    <div class="btn-row" style="margin-top:1.5rem">
      <a class="btn btn-kakao" href="{kakao}" target="_blank" rel="noopener">카카오톡으로 상담하기</a>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div>
    <h2>해마다 판매한 대수</h2>
    <p style="margin-top:1rem;color:var(--ink-soft)">대표 한 사람이 점검하고 낙찰받은 차입니다.</p>
  </div>
  <div style="padding-top:1.5rem">{bars}</div>
</div></section>
""".format(owner=OWNER, name=NAME, address=ADDRESS, phone=PHONE, phone_raw=PHONE_RAW, kakao=KAKAO,
           blog=BLOG, bars=bars_html(), checked=CHECKED.replace("-", "."))
    return layout("about.html", "반석자동차경매 소개·연락처 | 경기 화성 자동차경매 대행",
                  "2014년부터 자동차경매 대행만 해 온 대표 이희철이 상담부터 낙찰까지 직접 진행합니다. 주소, 문자·전화, 카카오톡 상담 안내.",
                  body, [crumbs_ld("소개·연락처", "about.html")], full_ld=True)


# ── 검색용 파일 ───────────────────────────────────────────────────────
ROBOTS = """User-agent: *
Allow: /

User-agent: Yeti
Allow: /
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: %s/sitemap.xml
"""


def sitemap():
    urls = "".join(
        "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (BASE, "" if h == "index.html" else h, TODAY)
        for h, _ in NAV)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls


def llms():
    lines = [
        "# " + NAME,
        "",
        "> 대기업 자동차경매장에서 대표가 직접 점검하고 입찰하는 중고차 경매 대행. 경기도 화성 소재.",
        "",
        "## 기본 정보",
        "- 상호: " + NAME,
        "- 대표: " + OWNER,
        "- 주소: " + ADDRESS,
        "- 문자·전화: " + PHONE,
        "- 카카오톡 상담: " + KAKAO,
        "- 블로그: " + BLOG,
        "- 내용 확인일: " + CHECKED + " (대표가 블로그에 올린 글 기준)",
        "",
        "## 핵심 내용",
    ]
    lines += ["- %s: %s" % (t, d) for t, d in PROMISES]
    lines += ["", "## 절차"]
    lines += ["%d. %s — %s" % (i + 1, t, d) for i, (t, d) in enumerate(STEPS)]
    lines += ["", "## 페이지"]
    lines += ["- [%s](%s/%s)" % (t, BASE, "" if h == "index.html" else h) for h, t in NAV]
    lines += ["", "## 자주 묻는 질문"]
    for _, q, a in FAQS:
        lines += ["### " + q, a, ""]
    return "\n".join(lines)


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><rect width="30" height="30" rx="4" fill="#0e4b3a"/>'
           '<path d="M5 22 11 10l5 7 3-4 6 9z" fill="#f4c20d"/></svg>')


def main():
    pages = {
        "index.html": page_index(), "process.html": page_process(), "promise.html": page_promise(),
        "cases.html": page_cases(), "faq.html": page_faq(), "about.html": page_about(),
    }
    for name, text in pages.items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    (OUT / "robots.txt").write_text(ROBOTS % BASE, encoding="utf-8", newline="\n")
    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8", newline="\n")
    (OUT / "llms.txt").write_text(llms(), encoding="utf-8", newline="\n")
    (OUT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8", newline="\n")
    print("만든 파일:", ", ".join(list(pages) + ["robots.txt", "sitemap.xml", "llms.txt"]))


if __name__ == "__main__":
    main()
