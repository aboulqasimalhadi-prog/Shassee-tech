import streamlit as st
import requests
import json
import base64
import os
import re
import random
import hashlib
from bs4 import BeautifulSoup
import cloudscraper
from PIL import Image
import time

# ==============================================
# 1. إعدادات الصفحة (مبسطة وسريعة)
# ==============================================
st.set_page_config(
    page_title="شاصي تك | SHASSEE TECH v38",
    page_icon="⚙️",
    layout="wide"
)

# CSS مبسط (نفس السابق ولكن أقل حجماً)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }
    .stApp { background: #0B0F19; }
    .stButton>button { width: 100%; background: #1E3A8A; color: white; border-radius: 10px; padding: 10px; font-weight: bold; }
    .stButton>button:hover { background: #10B981; color: black; }
    .premium-card { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-bottom: 20px; border-right: 4px solid #3B82F6; }
    .badge-copart { background: #1E3A8A; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
    .badge-iaai { background: #7C2D12; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ==============================================
# 2. دوال جلب البيانات (محاولة حقيقية + احتياطي)
# ==============================================

def get_platform(lot):
    return lot.get("platform", "Copart")

def extract_clean_url(url):
    match = re.search(r'(https?://[^\s\)"\'<>]+)', url)
    return match.group(1).strip() if match else url.strip()

def detect_platform(url):
    return "Copart" if "copart" in url.lower() else "IAAI" if "iaai" in url.lower() else "Copart"

def extract_lot_id(url):
    patterns = [r'/lot/(\d+)', r'id=(\d+)', r'lotId=(\d+)']
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return str(random.randint(1000000, 9999999))

def fetch_from_scrapingbee(url, api_key):
    if not api_key:
        return None, "مفتاح ScrapingBee غير موجود"
    try:
        response = requests.get(
            "https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": api_key,
                "url": url,
                "render_js": "true",
                "premium_proxy": "true",
                "wait_for": "5000",
                "retry": "true",
                "country_code": "us"
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.text, None
        else:
            return None, f"خطأ في ScrapingBee: {response.status_code}"
    except Exception as e:
        return None, str(e)

def fetch_from_cloudscraper(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def universal_extract_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    if "cloudflare" in html.lower() or "captcha" in html.lower():
        return None
        
    data = {
        "year": 2022,
        "make": "Toyota",
        "model": "Unknown",
        "vin": "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17)),
        "location": "Texas (Houston)",
        "title": "Salvage Title",
        "impact": "خلفية (Rear Impact)",
        "current_bid": 3000,
        "images": []
    }
    
    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schema = json.loads(script.string)
            if isinstance(schema, list):
                schema = schema[0]
            if schema.get("@type") in ["Car", "Vehicle", "Product"]:
                name = schema.get("name", "")
                if name:
                    yr = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', name)
                    if yr:
                        data["year"] = int(yr.group(1))
                    words = name.split()
                    if len(words) >= 2:
                        data["make"] = words[0]
                        data["model"] = name
                img = schema.get("image")
                if img:
                    data["images"] = [img] if isinstance(img, str) else [i for i in img if isinstance(i, str)]
                break
        except:
            pass
    
    # Open Graph
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        title_text = og_title.get("content")
        yr = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', title_text)
        if yr:
            data["year"] = int(yr.group(1))
        cleaned = re.sub(r'for sale.*$', '', title_text, flags=re.IGNORECASE).strip()
        words = cleaned.split()
        if len(words) >= 2:
            data["make"] = words[1] if words[0].isdigit() else words[0]
            data["model"] = cleaned
    
    og_image = soup.find("meta", attrs={"property": "og:image"})
    if og_image and og_image.get("content") and og_image.get("content") not in data["images"]:
        data["images"].append(og_image.get("content"))
    
    # CSS
    title_tag = soup.select_one("h1[data-uname='lotDetailHeader']") or soup.select_one("h1.lot-title")
    if title_tag:
        title_text = title_tag.text.strip()
        yr = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', title_text)
        if yr:
            data["year"] = int(yr.group(1))
        words = title_text.split()
        if len(words) >= 2:
            data["make"] = words[0]
            data["model"] = title_text
    
    loc_tag = soup.select_one("div[data-uname='locationValue']") or soup.select_one(".location-value")
    if loc_tag:
        data["location"] = loc_tag.text.strip()
    
    title_tag2 = soup.select_one("div[data-uname='titleValue']") or soup.select_one(".title-value")
    if title_tag2:
        data["title"] = title_tag2.text.strip()
    
    bid_tag = soup.select_one("span[data-uname='bidPrice']") or soup.select_one(".current-bid")
    if bid_tag:
        bid_text = re.sub(r'[^\d.]', '', bid_tag.text.strip())
        if bid_text:
            try:
                data["current_bid"] = float(bid_text)
            except:
                pass
    
    vin_tag = soup.select_one("div[data-uname='vinValue']") or soup.select_one(".vin-value")
    if vin_tag:
        data["vin"] = vin_tag.text.strip()
    
    if not data["images"]:
        model_lower = data["model"].lower()
        if "tacoma" in model_lower:
            data["images"] = ["https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600"]
        elif "4runner" in model_lower:
            data["images"] = ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
        else:
            data["images"] = ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
    
    return data

def generate_smart_guess(url, platform, lot_id):
    seed = int(hashlib.md5(lot_id.encode()).hexdigest(), 16) % 10000000
    r_gen = random.Random(seed)
    url_lower = url.lower()
    year_match = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', url)
    year = int(year_match.group(1)) if year_match else 2022
    make = "Toyota"
    model = "Tacoma"
    if "4runner" in url_lower:
        model = "4Runner"
    elif "tundra" in url_lower:
        model = "Tundra"
    elif "t100" in url_lower:
        model = "T100"
    
    vin = "".join(r_gen.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17))
    location = r_gen.choice(["Texas (Houston)", "California (Sacramento)", "New York (Long Island)"])
    title = r_gen.choice(["Salvage Title", "Clean Title", "Bill of Sale"])
    current_bid = r_gen.choice([3200, 4500, 5800, 2900, 6400])
    impact = r_gen.choice(["أمامية يسار (Front-Left)", "خلفية (Rear Impact)", "جانبية (Side Impact)"])
    
    ground_cost = 450 if "texas" in location.lower() else 850 if "california" in location.lower() else 350
    
    if "tacoma" in model.lower():
        market_val = 95000
        oem = [{"part": "مصد خلفي", "oem": "52159-04020"}, {"part": "مصباح خلفي", "oem": "81560-04180"}]
    elif "4runner" in model.lower():
        market_val = 110000
        oem = [{"part": "باب أمامي أيسر", "oem": "67002-35110"}, {"part": "رفرف جانبي", "oem": "53812-35220"}]
    else:
        market_val = 72000
        oem = [{"part": "رادياتير", "oem": "16400-0C210"}]
    
    return {
        "id": f"LOT-{lot_id}",
        "vin": vin,
        "make": make,
        "model": model,
        "year": year,
        "platform": platform,
        "location": location,
        "ground_cost": ground_cost,
        "title": title,
        "impact": impact,
        "current_bid": current_bid,
        "market_val_lyd": market_val,
        "oem_parts": oem,
        "scraped": False,
        "url": url,
        "images": ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
    }

def smart_parse_auction_url(url):
    clean_url = extract_clean_url(url)
    platform = detect_platform(clean_url)
    lot_id = extract_lot_id(clean_url)
    
    # 1. ScrapingBee
    api_key = st.session_state.get("scrapingbee_key", "")
    if api_key:
        html, err = fetch_from_scrapingbee(clean_url, api_key)
        if html:
            data = universal_extract_from_html(html)
            if data:
                data["id"] = f"LOT-{lot_id}"
                data["platform"] = platform
                data["url"] = clean_url
                data["scraped"] = True
                data["ground_cost"] = 450
                data["market_val_lyd"] = 95000
                data["oem_parts"] = [{"part": "غير محدد", "oem": "N/A"}]
                return data
        else:
            st.session_state["last_error"] = f"ScrapingBee: {err}"
    
    # 2. Cloudscraper
    html = fetch_from_cloudscraper(clean_url)
    if html:
        data = universal_extract_from_html(html)
        if data:
            data["id"] = f"LOT-{lot_id}"
            data["platform"] = platform
            data["url"] = clean_url
            data["scraped"] = True
            data["ground_cost"] = 450
            data["market_val_lyd"] = 95000
            data["oem_parts"] = [{"part": "غير محدد", "oem": "N/A"}]
            return data
    
    # 3. محاكاة
    st.session_state["last_error"] = "تعذر جلب البيانات، تم تنشيط المحاكاة"
    return generate_smart_guess(clean_url, platform, lot_id)

# ==============================================
# 3. دوال تحليل الصور بالذكاء الاصطناعي (مبسطة)
# ==============================================

def analyze_image_with_openai(image_bytes, api_key):
    if not api_key:
        return "❌ مفتاح OpenAI غير موجود. يرجى إدخاله في الشريط الجانبي."
    try:
        import openai
        openai.api_key = api_key
        img_b64 = base64.b64encode(image_bytes).decode()
        data_url = f"data:image/jpeg;base64,{img_b64}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "قم بتحليل هذه الصورة لسيارة متضررة. حدد المناطق المتضررة (مصد، رفرف، باب، إطار، صدام) ووصف الضرر، واكتشاف الصدأ إن وجد. أعطِ قائمة بالقطع المتضررة مع شدتها."},
                        {"type": "image_url", "image_url": data_url}
                    ]
                }
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ فشل التحليل: {str(e)}"

# ==============================================
# 4. تهيئة البيانات
# ==============================================
if "selected_car_id" not in st.session_state:
    st.session_state["selected_car_id"] = "LOT-3849102"

if "lots_db" not in st.session_state:
    st.session_state.lots_db = [
        {
            "id": "LOT-3849102",
            "vin": "5YFEPRAU6GP102834",
            "make": "Toyota",
            "model": "Toyota Tacoma",
            "year": 2022,
            "platform": "Copart",
            "location": "Texas (Austin)",
            "ground_cost": 450,
            "title": "Salvage Title",
            "impact": "خلفية (Rear Impact)",
            "current_bid": 3800,
            "market_val_lyd": 95000,
            "oem_parts": [{"part": "مصد خلفي", "oem": "52159-04020"}, {"part": "مصباح خلفي", "oem": "81560-04180"}],
            "scraped": True,
            "url": "",
            "images": ["https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600"]
        },
        {
            "id": "LOT-5928103",
            "vin": "5YFEPRAU6GP291034",
            "make": "Toyota",
            "model": "Toyota 4Runner",
            "year": 2021,
            "platform": "IAAI",
            "location": "California (Los Angeles)",
            "ground_cost": 850,
            "title": "Clean Title",
            "impact": "جانبية (Side Impact)",
            "current_bid": 4800,
            "market_val_lyd": 110000,
            "oem_parts": [{"part": "باب أمامي", "oem": "67002-35110"}, {"part": "رفرف جانبي", "oem": "53812-35220"}],
            "scraped": True,
            "url": "",
            "images": ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
        }
    ]

# تأمين البيانات
for lot in st.session_state.lots_db:
    if "platform" not in lot:
        lot["platform"] = "Copart"

# ==============================================
# 5. الشريط الجانبي (الإعدادات)
# ==============================================
st.sidebar.image("https://via.placeholder.com/300x80/0B0F19/10B981?text=SHASSEE+TECH", use_container_width=True)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ مفاتيح API")
scrapingbee_key = st.sidebar.text_input("🔑 مفتاح ScrapingBee (للجلب)", type="password", value=st.session_state.get("scrapingbee_key", ""))
st.session_state["scrapingbee_key"] = scrapingbee_key

openai_key = st.sidebar.text_input("🧠 مفتاح OpenAI (للتحليل)", type="password", value=st.session_state.get("openai_key", ""))
st.session_state["openai_key"] = openai_key

if openai_key:
    st.sidebar.success("✅ OpenAI مفعل")
else:
    st.sidebar.warning("⚠️ أدخل مفتاح OpenAI لتفعيل تحليل الصور")

st.sidebar.markdown("---")
st.sidebar.subheader("👤 تفضيلات المستورد")
pref_make = st.sidebar.multiselect("الماركات المفضلة", ["Toyota", "Lexus", "Honda"], default=["Toyota"])
pref_impact = st.sidebar.multiselect("زوايا الصدمة المقبولة", ["خلفية", "جانبية", "أمامية يسار"], default=["خلفية", "جانبية"])
pref_budget = st.sidebar.number_input("الميزانية ($)", min_value=1000, max_value=30000, value=5000)

# ==============================================
# 6. واجهة التطبيق (تبويبات)
# ==============================================
tab1, tab2, tab3 = st.tabs(["🔍 بحث وجلب", "🧠 تحليل الصور", "📊 جدوى"])

# ==============================================
# TAB 1: البحث والجلب
# ==============================================
with tab1:
    st.markdown("""
    <div class="premium-card">
        <h3>🔍 جلب بيانات السيارة</h3>
        الصق رابط السيارة من Copart أو IAAI، وسيحاول النظام جلب البيانات (إن توفر مفتاح ScrapingBee).
    </div>
    """, unsafe_allow_html=True)
    
    col_url, col_btn = st.columns([3, 1])
    with col_url:
        url_input = st.text_input("رابط السيارة:", placeholder="https://www.copart.com/lot/12345678")
    with col_btn:
        st.write("")
        fetch_btn = st.button("⚡ جلب", use_container_width=True)
    
    if fetch_btn and url_input:
        with st.spinner("⏳ جاري جلب البيانات..."):
            new_lot = smart_parse_auction_url(url_input)
            exists = any(l.get("id") == new_lot.get("id") for l in st.session_state.lots_db)
            if not exists:
                st.session_state.lots_db.insert(0, new_lot)
            st.session_state["selected_car_id"] = new_lot.get("id")
            st.rerun()
    
    # عرض اللوتات
    st.markdown("---")
    st.subheader("📋 اللوتات المحفوظة")
    
    # تصفية
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        search_platform = st.selectbox("المنصة", ["الكل", "Copart", "IAAI"])
    with col_f2:
        search_text = st.text_input("بحث في VIN أو اللوت", placeholder="اكتب...")
    
    filtered = []
    for lot in st.session_state.lots_db:
        if search_platform != "الكل" and get_platform(lot) != search_platform:
            continue
        if search_text and search_text.lower() not in lot.get("vin", "").lower() and search_text.lower() not in lot.get("id", "").lower():
            continue
        filtered.append(lot)
    
    for lot in filtered:
        col1, col2 = st.columns([3, 1])
        platform = get_platform(lot)
        badge = "badge-copart" if platform == "Copart" else "badge-iaai"
        source = "🟢 حقيقي" if lot.get("scraped") else "🟡 محاكاة"
        
        with col1:
            st.markdown(f"""
            <div class="premium-card" style="border-right-color: {'#10B981' if lot.get('scraped') else '#F59E0B'};">
                <span class="{badge}">{platform}</span> {source}
                <b>{lot.get('year')} {lot.get('model')}</b>
                <span style="color:#9CA3AF; font-size:13px;">({lot.get('id')} | VIN: {lot.get('vin')})</span><br>
                <span style="font-size:13px;">📍 {lot.get('location')} | 💰 ${lot.get('current_bid'):,.0f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write("")
            if st.button("🔍 فتح", key=f"open_{lot.get('id')}"):
                st.session_state["selected_car_id"] = lot.get("id")
                st.rerun()
    
    # تفاصيل السيارة المختارة
    selected = None
    for lot in st.session_state.lots_db:
        if lot.get("id") == st.session_state.get("selected_car_id"):
            selected = lot
            break
    
    if selected:
        st.markdown("---")
        st.subheader(f"🔧 تفاصيل: {selected.get('year')} {selected.get('model')}")
        
        # عرض الصورة
        img = selected.get("images", [])
        if img:
            st.image(img[0], use_container_width=True)
        
        # تعديل يدوي
        with st.expander("✏️ تعديل البيانات يدوياً"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                new_model = st.text_input("الموديل", selected.get("model"))
                new_year = st.number_input("السنة", 1990, 2027, int(selected.get("year", 2022)))
                new_bid = st.number_input("السعر ($)", 500, 50000, int(selected.get("current_bid", 3000)))
            with col_e2:
                new_impact = st.selectbox("الصدمة", ["أمامية يسار", "خلفية", "جانبية", "سليمة"], index=0)
                new_title = st.selectbox("نوع السند", ["Salvage Title", "Clean Title", "Bill of Sale"], index=0)
                new_location = st.selectbox("الموقع", ["Texas (Houston)", "California (Sacramento)", "New York (Long Island)"], index=0)
            
            if st.button("💾 حفظ التعديلات"):
                for idx, l in enumerate(st.session_state.lots_db):
                    if l.get("id") == selected.get("id"):
                        st.session_state.lots_db[idx]["model"] = new_model
                        st.session_state.lots_db[idx]["year"] = new_year
                        st.session_state.lots_db[idx]["current_bid"] = new_bid
                        st.session_state.lots_db[idx]["impact"] = new_impact
                        st.session_state.lots_db[idx]["title"] = new_title
                        st.session_state.lots_db[idx]["location"] = new_location
                        st.success("✅ تم التحديث")
                        st.rerun()

# ==============================================
# TAB 2: تحليل الصور بالذكاء الاصطناعي
# ==============================================
with tab2:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #8B5CF6;">
        <h3>🧠 تحليل الصور بالذكاء الاصطناعي</h3>
        ارفع صورة السيارة أو استخدم صور المزاد لتحليل الأضرار واكتشاف الصدأ وتحديد قطع الغيار.
    </div>
    """, unsafe_allow_html=True)
    
    # اختيار مصدر الصورة
    src_option = st.radio("مصدر الصورة:", ["رفع صورة", "استخدام صورة المزاد"])
    
    image_data = None
    if src_option == "رفع صورة":
        uploaded = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])
        if uploaded:
            image_data = uploaded.read()
            st.image(image_data, use_container_width=True)
    else:
        # استخدام صورة السيارة المختارة
        selected = None
        for lot in st.session_state.lots_db:
            if lot.get("id") == st.session_state.get("selected_car_id"):
                selected = lot
                break
        if selected and selected.get("images"):
            try:
                img_url = selected["images"][0]
                resp = requests.get(img_url, timeout=10)
                if resp.status_code == 200:
                    image_data = resp.content
                    st.image(image_data, use_container_width=True)
                else:
                    st.warning("تعذر جلب الصورة")
            except:
                st.warning("خطأ في جلب الصورة")
        else:
            st.info("اختر سيارة في تبويب البحث أولاً، أو استخدم رفع صورة")
    
    if image_data:
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            if st.button("🔍 تحليل بالذكاء الاصطناعي", use_container_width=True):
                result = analyze_image_with_openai(image_data, st.session_state.get("openai_key", ""))
                st.markdown("### 📝 نتيجة التحليل:")
                st.write(result)
                
                # استخراج OEM (مبسط)
                model = st.session_state.get("active_type", "Tacoma")
                oem_parts = []
                if "tacoma" in model.lower():
                    oem_parts = [{"part": "مصد خلفي", "oem": "52159-04020"}, {"part": "مصباح خلفي", "oem": "81560-04180"}]
                elif "4runner" in model.lower():
                    oem_parts = [{"part": "باب أمامي", "oem": "67002-35110"}, {"part": "رفرف جانبي", "oem": "53812-35220"}]
                
                if oem_parts:
                    st.markdown("### 🔩 قطع الغيار المقترحة (OEM)")
                    for p in oem_parts:
                        st.markdown(f"- **{p['part']}**: `{p['oem']}`")
        
        with col_a2:
            if st.button("🦀 كشف الصدأ", use_container_width=True):
                try:
                    import cv2
                    import numpy as np
                    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    lower = np.array([0, 50, 50])
                    upper = np.array([30, 255, 255])
                    mask = cv2.inRange(hsv, lower, upper)
                    rust_percent = (np.sum(mask > 0) / mask.size) * 100
                    st.metric("نسبة الصدأ المقدرة", f"{rust_percent:.1f}%")
                    if rust_percent > 10:
                        st.warning("⚠️ نسبة صدأ مرتفعة")
                    else:
                        st.success("✅ نسبة صدأ منخفضة")
                except Exception as e:
                    st.error(f"تعذر تحليل الصدأ: {e}")

# ==============================================
# TAB 3: الجدوى اللوجستية
# ==============================================
with tab3:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3>📊 الجدوى اللوجستية والتكلفة</h3>
    </div>
    """, unsafe_allow_html=True)
    
    active = None
    for lot in st.session_state.lots_db:
        if lot.get("id") == st.session_state.get("selected_car_id"):
            active = lot
            break
    
    if active:
        bid = active.get("current_bid", 0)
        ground = active.get("ground_cost", 450)
        market = active.get("market_val_lyd", 95000)
        exchange = 9.4
        shipping = 2250
        
        total_usd = bid + ground + shipping
        total_lyd = total_usd * exchange
        profit_lyd = market - total_lyd
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🚛 الشحن البري", f"${ground:,.0f}")
        col2.metric("🚢 الشحن البحري", f"${shipping:,.0f}")
        col3.metric("💰 التكلفة الإجمالية", f"${total_usd:,.0f}\n{total_lyd:,.0f} د.ل")
        
        st.markdown(f"""
        <div class="premium-card">
            سعر السوق في ليبيا: <b>{market:,.0f} د.ل</b><br>
            هامش الربح المتوقع: <b style="color:{'#10B981' if profit_lyd > 0 else '#EF4444'};">{profit_lyd:,.0f} د.ل</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("اختر سيارة أولاً في تبويب البحث.")

# ==============================================
# 7. تذييل
# ==============================================
st.markdown("""
---
<div style="text-align:center; color:#9CA3AF; font-size:12px; padding:10px;">
    ⚠️ جميع التقييمات تنبؤية، يجب مطابقتها بالفحص العيني.
</div>
""", unsafe_allow_html=True)
