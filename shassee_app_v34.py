import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
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
from io import BytesIO

# ==============================================
# 1. إعدادات الصفحة والتصميم
# ==============================================
st.set_page_config(
    page_title="شاصي تك | SHASSEE TECH v36",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #060913; }
    ::-webkit-scrollbar-thumb { background: #1E3A8A; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #10B981; }
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background: radial-gradient(circle at top right, #0D1527 0%, #070913 100%) !important;
        color: #E5E7EB !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090E1A 0%, #050811 100%) !important;
        border-left: 1px solid rgba(16, 185, 129, 0.15) !important;
        box-shadow: 10px 0px 30px rgba(0, 0, 0, 0.6) !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background: rgba(15, 23, 42, 0.6) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.25) !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        padding: 14px 28px !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        border-color: #34D399 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.45) !important;
        transform: translateY(-2px) !important;
        color: #000000 !important;
    }
    .premium-card {
        padding: 24px;
        border-radius: 16px;
        background: rgba(13, 21, 39, 0.55);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.12);
        border-right: 5px solid #3B82F6;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .premium-card:hover {
        transform: translateY(-4px);
        border-color: rgba(16, 185, 129, 0.3);
        border-right-color: #10B981;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);
    }
    .badge-copart {
        background-color: #1E3A8A !important;
        color: white !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 11px;
        border: 1px solid #3B82F6;
    }
    .badge-iaai {
        background-color: #7C2D12 !important;
        color: white !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 11px;
        border: 1px solid #EA580C;
    }
    .data-source-badge {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        margin-right: 6px;
        font-weight: bold;
    }
    .data-source-real {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
    }
    .data-source-sim {
        background-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid #F59E0B;
    }
    .diagnostic-terminal {
        background: #030712 !important;
        border: 1px solid #10B981 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        font-family: 'Courier New', monospace !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.1) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 23, 42, 0.5) !important;
        backdrop-filter: blur(10px);
        padding: 10px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #9CA3AF !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# 2. دوال مساعدة للشعار والهيدر
# ==============================================
def get_silver_car_b64():
    paths_to_try = [
        "/workspace/artifacts/silver_car_side.png",
        "silver_car_side.png",
        "/workspace/scratch/silver_car_side.png",
        "artifacts/silver_car_side.png"
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                pass
    return ""

silver_car_b64 = get_silver_car_b64()
if silver_car_b64:
    silver_car_html = f'<img src="data:image/png;base64,{silver_car_b64}" alt="Silver Car" style="max-width: 480px; width: 100%; height: auto; margin-bottom: 20px; filter: drop-shadow(0 12px 24px rgba(16, 185, 129, 0.3));">'
else:
    silver_car_html = '''
    <div style="background: rgba(16, 185, 129, 0.03); border: 1px dashed rgba(16, 185, 129, 0.25); border-radius: 16px; padding: 20px 40px; margin-bottom: 25px; text-align: center; box-shadow: 0 0 30px rgba(16, 185, 129, 0.05);">
        <span style="font-size: 50px; filter: drop-shadow(0 0 10px #10B981);">🦾</span>
        <h2 style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 800; font-size: 22px; margin-top: 10px; margin-bottom: 0px; letter-spacing: 1px;">SHASSEE TECH | SECURE CHASSIS AUDIT</h2>
        <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0px;">نظام التحقق الفيزيائي العيني والامتثال الجمركي المستقل لسيارات الاستيراد</p>
    </div>
    '''

header_html = """<div style="background: linear-gradient(135deg, rgba(13, 21, 39, 0.65) 0%, rgba(7, 9, 19, 0.85) 100%); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 24px; padding: 35px 20px; text-align: center; margin-bottom: 35px; box-shadow: 0 20px 40px rgba(0,0,0,0.45); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);"><div style="display: flex; flex-direction: column; align-items: center; justify-content: center;"><h1 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 38px; margin-top: 10px; margin-bottom: 5px; text-shadow: 0 0 25px rgba(16, 185, 129, 0.45);">منصة شاصي تك | SHASSEE TECH</h1><p style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 700; font-size: 18px; margin-top: 0px; letter-spacing: 0.5px;">التقييم الفني والمالي المستقل ومغلف البحث الموحد لمزادات السيارات المستوردة لعام 2026</p></div></div>"""
st.markdown(header_html, unsafe_allow_html=True)

# ==============================================
# 3. الشريط الجانبي (الإعدادات)
# ==============================================
logo_path = "shassee_tech_final_logo.png"
logo_exists = os.path.exists(logo_path)
if not logo_exists:
    for file in os.listdir("."):
        if "logo" in file.lower() and file.endswith((".png", ".jpg", ".jpeg")):
            logo_path = file
            logo_exists = True
            break

if logo_exists:
    st.sidebar.image(logo_path, use_container_width=True)
    st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 15px; margin-bottom: 15px;">
        <h2 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 28px; margin-bottom: 0px;">SHASSEE TECH</h2>
        <span style="font-size: 11px; color: #10B981; font-weight: bold; letter-spacing: 1px;">VEHICLE INTELLIGENCE & AUDIT</span>
    </div>
    <hr style="border-color: rgba(255,255,255,0.05);">
    """, unsafe_allow_html=True)

st.sidebar.subheader("👤 بروفايل معايير وتفضيلات المستورد")
pref_make = st.sidebar.multiselect(
    "🚘 ماركات السيارات المفضلة لديك:",
    ["Toyota", "Lexus", "Honda", "Ford", "GMC"],
    default=["Toyota"]
)
pref_impact = st.sidebar.multiselect(
    "🎯 زوايا الصدمة المقبولة لديك بالصيانة:",
    ["خلفية (Rear Impact)", "جانبية (Side Impact)", "أمامية يسار (Front-Left)", "أمامية يمين (Front-Right)", "سليمة / صدمة خفيفة"],
    default=["خلفية (Rear Impact)", "جانبية (Side Impact)", "سليمة / صدمة خفيفة"]
)
pref_budget = st.sidebar.number_input(
    "💵 ميزانيتك القصوى المتوقعة للشراء بالمزاد ($):",
    min_value=1000, max_value=30000, value=5000, step=500
)

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.sidebar.subheader("⚙️ إعدادات النظام ومفاتيح الربط")

# ===== مفاتيح API =====
scrapingbee_key = st.sidebar.text_input(
    "🔑 مفتاح ScrapingBee (لجلب البيانات الحقيقية):", 
    type="password", 
    value=st.session_state.get("scrapingbee_key", ""),
    help="سجل في scrapingbee.com واحصل على 1000 طلب مجاني."
)
st.session_state["scrapingbee_key"] = scrapingbee_key

openai_key = st.sidebar.text_input(
    "🧠 مفتاح OpenAI (لتحليل الصور بالذكاء الاصطناعي):", 
    type="password", 
    value=st.session_state.get("openai_key", ""),
    help="للحصول على مفتاح: سجل في openai.com وأضف رصيداً."
)
st.session_state["openai_key"] = openai_key

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

integration_mode = st.sidebar.selectbox(
    "🔌 نمط تشغيل النظام:",
    ["🎯 وضع المحاكاة الذكي (Demo Mode)", "⚡ الوضع السحابي الحقيقي (Live Cloud)"]
)

supabase_url = ""
supabase_anon_key = ""
if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)":
    supabase_url = st.sidebar.text_input("🌐 Supabase Project URL:", placeholder="https://your-project.supabase.co")
    supabase_anon_key = st.sidebar.text_input("🔑 Supabase Anon Key:", type="password")
    if not supabase_url.strip() or not supabase_anon_key.strip():
        st.sidebar.warning("⚠️ أدخل مفاتيح السيرفر (Supabase) للربط وحفظ تقارير السيارات الحقيقية:")
    else:
        st.sidebar.success("⚡ السيرفر السحابي متصل الآن وجاهز لحفظ البيانات حقيقياً!")
else:
    st.sidebar.info("💡 يعمل النظام الآن بنظام المحاكاة الذكية المتقدمة بناءً على الخبرة التشغيلية لـ 12 عاماً.")

# ثوابت عامة
EXCHANGE_RATE = 9.4
SHIPPING_COST = 2250

# ==============================================
# 4. دوال جلب البيانات
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
        return None, None, "لم يتم إدخال مفتاح ScrapingBee."
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
            return response.text, 200, None
        else:
            return None, response.status_code, f"خطأ {response.status_code}"
    except Exception as e:
        return None, None, str(e)

def fetch_from_cloudscraper(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def universal_extract_from_html(html, platform, lot_id):
    soup = BeautifulSoup(html, 'lxml')
    html_lower = html.lower()
    if "cloudflare" in html_lower or "enable javascript" in html_lower or "captcha" in html_lower:
        return None
        
    data = {
        "year": 2022,
        "make": "Toyota",
        "model": "Unknown",
        "vin": "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17)),
        "location": "Texas (Houston)",
        "title": "Salvage Title",
        "impact": "خلفية (Rear Impact)",
        "current_bid": 3000.0,
        "images": [],
        "scraped": True
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
                    year_match = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', name)
                    if year_match:
                        data["year"] = int(year_match.group(1))
                    words = name.split()
                    if len(words) >= 2:
                        data["make"] = words[0]
                        data["model"] = name
                img = schema.get("image")
                if img:
                    if isinstance(img, list):
                        data["images"] = [i for i in img if isinstance(i, str)]
                    elif isinstance(img, str):
                        data["images"] = [img]
                break
        except:
            pass
    
    # Open Graph
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        title_text = og_title.get("content")
        year_match = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', title_text)
        if year_match:
            data["year"] = int(year_match.group(1))
        cleaned = re.sub(r'for sale.*$', '', title_text, flags=re.IGNORECASE).strip()
        words = cleaned.split()
        if len(words) >= 2:
            data["make"] = words[1] if words[0].isdigit() else words[0]
            data["model"] = cleaned
    
    og_image = soup.find("meta", attrs={"property": "og:image"}) or soup.find("meta", attrs={"name": "twitter:image"})
    if og_image and og_image.get("content"):
        img_url = og_image.get("content")
        if img_url and img_url not in data["images"]:
            data["images"].append(img_url)
    
    # CSS
    title_tag = soup.select_one("h1[data-uname='lotDetailHeader']") or soup.select_one("h1.lot-title")
    if title_tag:
        title_text = title_tag.text.strip()
        year_match = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', title_text)
        if year_match:
            data["year"] = int(year_match.group(1))
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
            data["images"] = [
                "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600",
                "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=300"
            ]
        elif "4runner" in model_lower:
            data["images"] = [
                "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600",
                "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=300"
            ]
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
    elif "pickup" in url_lower:
        model = "Pickup Halfton"
    
    vin_chars = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
    vin = "".join(r_gen.choices(vin_chars, k=17))
    location = r_gen.choice(["Texas (Houston)", "California (Sacramento)", "New York (Long Island)", "Florida (Miami)", "Pennsylvania (Philadelphia)"])
    title = r_gen.choice(["Salvage Title", "Clean Title", "Bill of Sale", "Certificate of Destruction"])
    current_bid = r_gen.choice([3200, 4500, 5800, 2900, 6400])
    impact = r_gen.choice(["أمامية يسار (Front-Left Impact)", "أمامية يمين (Front-Right Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)"])
    
    ground_cost = 450
    if "texas" in location.lower():
        ground_cost = 450
    elif "california" in location.lower():
        ground_cost = 850
    elif "new york" in location.lower() or "jersey" in location.lower() or "pennsylvania" in location.lower():
        ground_cost = 350
    elif "florida" in location.lower():
        ground_cost = 550
    
    if "tacoma" in model.lower():
        market_val_lyd = 95000
    elif "4runner" in model.lower():
        market_val_lyd = 110000
    elif "tundra" in model.lower():
        market_val_lyd = 72000
    else:
        market_val_lyd = 65000
    
    if "tacoma" in model.lower():
        oem_parts = [
            {"part": "مصد خلفي كامل", "oem": "52159-04020", "desc": "هيكل خلفي تجميلي"},
            {"part": "مصباح خلفي LED أيسر", "oem": "81560-04180", "desc": "كهربائي - فك وتركيب سريع"},
            {"part": "باب حوض خلفي", "oem": "65700-04090", "desc": "هيكل خارجي قابل للتبديل"}
        ]
    elif "4runner" in model.lower():
        oem_parts = [
            {"part": "باب أمامي أيسر", "oem": "67002-35110", "desc": "هيكل خارجي"},
            {"part": "رفرف جانبي أيسر", "oem": "53812-35220", "desc": "صاج تجميلي خارجي"},
            {"part": "مجموعة مقصات جانبية أيسر", "oem": "48069-35120", "desc": "تعليق - جديد بالكرتون للمطابقة"}
        ]
    elif "tundra" in model.lower():
        oem_parts = [
            {"part": "رادياتير مبرد المحرك", "oem": "16400-0C210", "desc": "ميكانيكي - تبريد بالكرتون"},
            {"part": "مجموعة مقص تعليق أيسر", "oem": "48069-34010", "desc": "تعليق وهيكل سفلي"},
            {"part": "رفرف أمامي أيسر", "oem": "53812-34080", "desc": "صاج تجميلي خارجي"}
        ]
    else:
        oem_parts = [
            {"part": "مصد أمامي تجميلي", "oem": "52119-34010", "desc": "بلاستيك خارجي تجميلي"}
        ]
    
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
        "market_val_lyd": market_val_lyd,
        "oem_parts": oem_parts,
        "scraped": False,
        "url": url,
        "images": []
    }

def build_lot_from_data(data, clean_url, platform, lot_id, scraped=True):
    return {
        "id": f"LOT-{lot_id}",
        "vin": data.get("vin", ""),
        "make": data.get("make", "Toyota"),
        "model": data.get("model", "Unknown"),
        "year": data.get("year", 2022),
        "platform": platform,
        "location": data.get("location", "Unknown"),
        "ground_cost": 450,
        "title": data.get("title", "Salvage Title"),
        "impact": data.get("impact", "خلفية (Rear Impact)"),
        "current_bid": float(data.get("current_bid", 3000)),
        "market_val_lyd": data.get("market_val_lyd", 95000),
        "oem_parts": data.get("oem_parts", [{"part": "غير محدد", "oem": "N/A", "desc": "سيتم تحديثه"}]),
        "scraped": scraped,
        "url": clean_url,
        "images": data.get("images", [])
    }

def smart_parse_auction_url(url):
    clean_url = extract_clean_url(url)
    platform = detect_platform(clean_url)
    lot_id = extract_lot_id(clean_url)
    
    st.session_state["last_scrape_status"] = ""
    st.session_state["last_scrape_error"] = ""
    
    scrapingbee_key = st.session_state.get("scrapingbee_key", "")
    if scrapingbee_key:
        html, status, err = fetch_from_scrapingbee(clean_url, scrapingbee_key)
        if html:
            data = universal_extract_from_html(html, platform, lot_id)
            if data is not None:
                st.session_state["last_scrape_status"] = "نجاح عبر ScrapingBee"
                return build_lot_from_data(data, clean_url, platform, lot_id, scraped=True)
            else:
                st.session_state["last_scrape_error"] = "حظر حماية المزادات (Cloudflare)."
        else:
            st.session_state["last_scrape_error"] = f"فشل السحب بـ ScrapingBee: {err}"
    
    html = fetch_from_cloudscraper(clean_url)
    if html:
        data = universal_extract_from_html(html, platform, lot_id)
        if data is not None:
            st.session_state["last_scrape_status"] = "نجاح عبر Cloudscraper"
            return build_lot_from_data(data, clean_url, platform, lot_id, scraped=True)
        else:
            if not st.session_state.get("last_scrape_error"):
                st.session_state["last_scrape_error"] = "حظر حماية Cloudflare."
    
    st.session_state["last_scrape_status"] = "محاكاة احتياطية"
    return generate_smart_guess(clean_url, platform, lot_id)

# ==============================================
# 5. دوال تحليل الصور بالذكاء الاصطناعي
# ==============================================

def analyze_car_image_with_openai(image_bytes, api_key):
    """تحليل صورة السيارة باستخدام OpenAI Vision API"""
    if not api_key:
        return "يرجى تفعيل مفتاح OpenAI من الإعدادات الجانبية."
    try:
        import openai
        openai.api_key = api_key
        # تحويل الصورة إلى base64
        img_b64 = base64.b64encode(image_bytes).decode()
        data_url = f"data:image/jpeg;base64,{img_b64}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "قم بتحليل هذه الصورة لسيارة متضررة. حدد المناطق المتضررة (مصد أمامي، رفرف، باب، إطار، إلخ) ووصف الضرر، واكتشاف الصدأ إن وجد. أعطِ قائمة بالقطع المتضررة مع تقدير لشدتها (بسيط، متوسط، شديد)."},
                        {"type": "image_url", "image_url": data_url}
                    ]
                }
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"فشل التحليل: {str(e)}"

def detect_rust_with_opencv(image_bytes):
    """كشف الصدأ باستخدام OpenCV (بديل بسيط)"""
    try:
        import cv2
        import numpy as np
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # مدى اللون البرتقالي/البني (الصدأ)
        lower = np.array([0, 50, 50])
        upper = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        rust_percentage = (np.sum(mask > 0) / mask.size) * 100
        return rust_percentage
    except:
        return 0.0

# ==============================================
# 6. قاعدة بيانات قطع الغيار (OEM)
# ==============================================
OEM_DB = {
    "tacoma": {
        "مصد خلفي": "52159-04020",
        "مصباح خلفي LED أيسر": "81560-04180",
        "باب حوض خلفي": "65700-04090"
    },
    "4runner": {
        "باب أمامي أيسر": "67002-35110",
        "رفرف جانبي أيسر": "53812-35220",
        "مقصات جانبية أيسر": "48069-35120"
    },
    "tundra": {
        "رادياتير": "16400-0C210",
        "مقص تعليق أيسر": "48069-34010",
        "رفرف أمامي أيسر": "53812-34080"
    }
}

def get_oem_parts_from_text(model, damage_text):
    """استخراج أرقام OEM بناءً على الموديل ووصف الضرر"""
    model_key = model.lower()
    if model_key not in OEM_DB:
        return []
    found = []
    for part_name, oem_code in OEM_DB[model_key].items():
        if any(word in damage_text.lower() for word in part_name.split()):
            found.append({"part": part_name, "oem": oem_code})
    return found

# ==============================================
# 7. نموذج 3D تفاعلي
# ==============================================
def create_3d_chassis(damage_levels):
    """إنشاء نموذج 3D مع تلوين حسب شدة الضرر"""
    x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
    y = [0, 4, 4, 0, 0, 4, 4, 0, 0, 4]
    z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
    fig = go.Figure(data=[go.Mesh3d(
        x=x, y=y, z=z,
        intensity=damage_levels,
        colorscale=[[0, '#10B981'], [0.5, '#F59E0B'], [1, '#EF4444']],
        showscale=True,
        colorbar_title="شدة الضرر"
    )])
    fig.update_layout(scene=dict(
        xaxis=dict(showticklabels=False, backgroundcolor="#060913"),
        yaxis=dict(showticklabels=False, backgroundcolor="#060913"),
        zaxis=dict(showticklabels=False, backgroundcolor="#060913")
    ), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    return fig

# ==============================================
# 8. تهيئة قاعدة البيانات المحلية
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
            "oem_parts": [
                {"part": "مصد خلفي كامل", "oem": "52159-04020", "desc": "هيكل خلفي تجميلي"},
                {"part": "مصباح خلفي LED أيسر", "oem": "81560-04180", "desc": "كهربائي - فك وتركيب سريع"},
                {"part": "باب حوض خلفي", "oem": "65700-04090", "desc": "هيكل خارجي قابل للتبديل"}
            ],
            "scraped": True,
            "url": "",
            "images": []
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
            "oem_parts": [
                {"part": "باب أمامي أيسر", "oem": "67002-35110", "desc": "هيكل خارجي"},
                {"part": "رفرف جانبي أيسر", "oem": "53812-35220", "desc": "صاج تجميلي خارجي"},
                {"part": "مجموعة مقصات جانبية أيسر", "oem": "48069-35120", "desc": "تعليق - جديد بالكرتون للمطابقة"}
            ],
            "scraped": True,
            "url": "",
            "images": []
        },
    ]

for lot in st.session_state.lots_db:
    if "platform" not in lot:
        if "iaai" in lot.get("url", "").lower() or "IAAI" in lot.get("id", ""):
            lot["platform"] = "IAAI"
        else:
            lot["platform"] = "Copart"

# ==============================================
# 9. واجهة التطبيق (Tabs)
# ==============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 بحث موحد", 
    "📊 جدوى لوجستية", 
    "🔌 OBD-II",
    "📜 QR",
    "⚙️ SQL",
    "🧠 تحليل ذكي (AI)"
])

# ==============================================
# TAB 1: البحث الموحد (نفس السابق مع استخدام get_platform)
# ==============================================
with tab1:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">🔍 مغلف المزايدة والبحث الموحد لمزادات (Copart & IAAI)</h3>
        أدخل رابط السيارة من كوبارت أو IAAI، أو ابحث في اللوتات المحفوظة.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.08); border-right: 4px solid #10B981; padding: 18px; border-radius: 12px; margin-bottom: 25px;">
        <b style="color: #10B981; font-size:16px;">🔗 ربط ذكي متعدد الطبقات:</b><br>
        الصق رابط السيارة من <b>Copart</b> أو <b>IAAI</b>، وسيحاول النظام جلب البيانات عبر ScrapingBee (إذا كان المفتاح موجوداً)، ثم Cloudscraper، وأخيراً التخمين الذكي.
    </div>
    """, unsafe_allow_html=True)
    
    if "url_input" not in st.session_state:
        st.session_state.url_input = ""
    
    col_scrape_1, col_scrape_btn = st.columns([3, 1])
    with col_scrape_1:
        raw_url_input = st.text_input(
            "🔗 ألصق رابط السيارة:",
            value=st.session_state.url_input,
            placeholder="https://www.copart.com/lot/12345678"
        )
    with col_scrape_btn:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        btn_trigger = st.button("⚡ سحب البيانات", key="btn_smart_fetch")
    
    clean_url_input = ""
    if raw_url_input:
        match = re.search(r'(https?://[^\s\)"\'<>]+)', raw_url_input)
        if match:
            clean_url_input = match.group(1).strip()
        else:
            clean_url_input = raw_url_input.strip()
        if clean_url_input != raw_url_input:
            st.session_state.url_input = clean_url_input
            st.rerun()
    
    if btn_trigger and clean_url_input:
        with st.spinner("⏳ جاري جلب البيانات..."):
            new_lot = smart_parse_auction_url(clean_url_input)
            
            scrape_err = st.session_state.get("last_scrape_error", "")
            scrape_status = st.session_state.get("last_scrape_status", "")
            
            if "نجاح" in scrape_status:
                st.success(f"🎉 {scrape_status}!")
                if new_lot.get("images"):
                    st.toast("📸 تم استخلاص صور ومعاينة السيارة الحقيقية من ساحة المزاد!")
            else:
                if scrape_err:
                    st.error(f"❌ {scrape_err}")
                st.warning("⚠️ حظر حماية المزادات (Cloudflare) اكتشف الطلب. تم تنشيط محاكاة ذكية، يمكنك تعديل البيانات يدوياً.")
            
            exists = any(lot.get("id") == new_lot.get("id") for lot in st.session_state.lots_db)
            if not exists:
                st.session_state.lots_db.insert(0, new_lot)
            st.session_state["selected_car_id"] = new_lot.get("id")
            st.toast(f"🎉 تم جلب وتنشيط السيارة: {new_lot.get('model', 'Unknown')}")
            st.rerun()
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search_platform = st.selectbox("🌐 المنصة:", ["الكل", "Copart", "IAAI"])
    with col_f2:
        search_make = st.selectbox("🚘 الماركة:", ["الكل", "Toyota", "Lexus", "Honda", "Ford", "GMC"])
    with col_f3:
        search_text = st.text_input("📝 بحث في VIN أو رقم اللوت:", placeholder="اكتب للبحث...")
    
    filter_by_prefs = st.checkbox("🎯 تصفية حسب تفضيلاتي الشخصية", value=False)
    
    filtered_lots = []
    for lot in st.session_state.lots_db:
        if search_platform != "الكل" and get_platform(lot) != search_platform:
            continue
        if search_make != "الكل" and lot.get("make", "") != search_make:
            continue
        if search_text and search_text.lower() not in lot.get("vin", "").lower() and search_text.lower() not in lot.get("id", "").lower():
            continue
        if filter_by_prefs:
            if lot.get("make", "") not in pref_make:
                continue
            match_impact = False
            for p_imp in pref_impact:
                if p_imp.split("(")[0].strip().lower() in lot.get("impact", "").lower() or lot.get("impact", "").lower() in p_imp.lower():
                    match_impact = True
                    break
            if not match_impact:
                continue
            if lot.get("current_bid", 0) > pref_budget:
                continue
        filtered_lots.append(lot)
    
    st.markdown(f"### 📋 النتائج ({len(filtered_lots)} سيارة)")
    
    selected_lot = None
    for lot in filtered_lots:
        col_c1, col_c2 = st.columns([2.5, 1])
        
        platform = get_platform(lot)
        badge = "badge-copart" if platform == "Copart" else "badge-iaai"
        
        if lot.get("scraped", False):
            source_badge = '<span class="data-source-badge data-source-real">🟢 حقيقي</span>'
        else:
            source_badge = '<span class="data-source-badge data-source-sim">🟡 محاكاة</span>'
        
        is_make_match = lot.get("make", "") in pref_make
        is_impact_match = any(
            p_imp.split("(")[0].strip().lower() in lot.get("impact", "").lower() or lot.get("impact", "").lower() in p_imp.lower()
            for p_imp in pref_impact
        )
        is_budget_match = lot.get("current_bid", 0) <= pref_budget
        matches = sum([is_make_match, is_impact_match, is_budget_match])
        if matches == 3:
            fit_score, fit_badge, fit_desc = 95, "🟢 متوافق تماماً", "يطابق جميع معاييرك"
        elif matches == 2:
            fit_score, fit_badge, fit_desc = 70, "🟡 متوافق جزئياً", "يطابق معظم المعايير"
        else:
            fit_score, fit_badge, fit_desc = 35, "🔴 توافق ضعيف", "لا يطابق تفضيلاتك"
        
        with col_c1:
            st.markdown(f"""
            <div class="premium-card" style="border-right-color: {'#10B981' if fit_score >= 90 else '#F59E0B' if fit_score >= 70 else '#EF4444'};">
                <span class="{badge}">{platform}</span>
                {source_badge}
                <b style="font-size:18px; color:white;">{lot.get('year', '')} {lot.get('model', '')}</b>
                <span style="font-size:12px; color:#9CA3AF;">(لوط: {lot.get('id', '')} | VIN: {lot.get('vin', '')})</span><br>
                <div style="margin-top: 8px; font-size:13px;">
                    • <b>الموقع:</b> {lot.get('location', 'غير معروف')} | <b>السند:</b> {lot.get('title', 'غير معروف')}<br>
                    • <b>الصدمة:</b> {lot.get('impact', 'غير معروف')} | <b>السعر الحالي:</b> <span style="color:#10B981; font-weight:bold;">${lot.get('current_bid', 0):,.0f}</span><br>
                    • <b style="color: {'#10B981' if fit_score >= 90 else '#F59E0B' if fit_score >= 70 else '#EF4444'};">{fit_badge}</b> ({fit_desc})
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c2:
            st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("🔍 فتح", key=f"btn_select_{lot.get('id', '')}"):
                st.session_state["selected_car_id"] = lot.get("id", "")
                st.rerun()
    
    if "selected_car_id" in st.session_state:
        for lot in st.session_state.lots_db:
            if lot.get("id") == st.session_state["selected_car_id"]:
                selected_lot = lot
                break
    
    if selected_lot:
        st.markdown("<hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown(f"### ⚙️ التفاصيل المتقدمة للسيارة المختارة: {selected_lot.get('year', '')} {selected_lot.get('model', '')}")
        
        images = selected_lot.get("images", [])
        if not images:
            model_lower = selected_lot.get("model", "").lower()
            if "tacoma" in model_lower:
                images = [
                    "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600",
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=300"
                ]
            elif "4runner" in model_lower:
                images = [
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600",
                    "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=300"
                ]
            else:
                images = ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
        
        col_img1, col_img2 = st.columns([1.5, 1])
        with col_img1:
            st.image(images[0], caption=f"{selected_lot.get('model', '')} - صورة المزاد", use_container_width=True)
        with col_img2:
            if len(images) > 1:
                st.image(images[1], caption="زاوية إضافية", use_container_width=True)
            else:
                st.info("لا توجد صور إضافية.")
        
        with st.expander("🛠️ تعديل البيانات يدوياً (لضمان الدقة)"):
            col_ed1, col_ed2, col_ed3 = st.columns(3)
            with col_ed1:
                edit_model = st.text_input("الموديل:", value=selected_lot.get("model", ""))
                edit_year = st.number_input("السنة:", min_value=1990, max_value=2027, value=int(selected_lot.get("year", 2022)))
            with col_ed2:
                impact_list = ["أمامية يسار (Front-Left Impact)", "أمامية يمين (Front-Right Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)", "سليمة / صدمة خفيفة"]
                current_impact_idx = 0
                for i, imp in enumerate(impact_list):
                    if selected_lot.get("impact", "")[:10] in imp:
                        current_impact_idx = i
                        break
                edit_impact = st.selectbox("زاوية الصدمة:", impact_list, index=current_impact_idx)
                edit_title = st.selectbox("نوع السند:", ["Salvage Title", "Clean Title", "Bill of Sale", "Certificate of Destruction"], index=0)
            with col_ed3:
                loc_list = ["Texas (Houston)", "California (Sacramento)", "New York (Long Island)", "Florida (Miami)", "Pennsylvania (Salt-Belt)"]
                current_loc_idx = 0
                for i, loc in enumerate(loc_list):
                    if selected_lot.get("location", "")[:10] in loc:
                        current_loc_idx = i
                        break
                edit_location = st.selectbox("الموقع:", loc_list, index=current_loc_idx)
                edit_bid = st.number_input("السعر الحالي ($):", min_value=500, max_value=30000, value=int(selected_lot.get("current_bid", 3000)))
            
            if st.button("💾 حفظ التعديلات"):
                for idx, lot in enumerate(st.session_state.lots_db):
                    if lot.get("id") == selected_lot.get("id"):
                        st.session_state.lots_db[idx]["model"] = edit_model
                        st.session_state.lots_db[idx]["year"] = edit_year
                        st.session_state.lots_db[idx]["impact"] = edit_impact
                        st.session_state.lots_db[idx]["title"] = edit_title
                        st.session_state.lots_db[idx]["location"] = edit_location
                        st.session_state.lots_db[idx]["current_bid"] = edit_bid
                        if "texas" in edit_location.lower():
                            st.session_state.lots_db[idx]["ground_cost"] = 450
                        elif "california" in edit_location.lower():
                            st.session_state.lots_db[idx]["ground_cost"] = 850
                        else:
                            st.session_state.lots_db[idx]["ground_cost"] = 350
                        st.toast("✅ تم تحديث البيانات")
                        st.rerun()
        
        st.session_state["active_vin"] = selected_lot.get("vin", "")
        st.session_state["active_type"] = selected_lot.get("model", "")
        st.session_state["active_impact"] = selected_lot.get("impact", "")
        st.session_state["active_bid"] = selected_lot.get("current_bid", 0)
        st.session_state["active_ground_cost"] = selected_lot.get("ground_cost", 450)
        st.session_state["active_market_val"] = selected_lot.get("market_val_lyd", 95000)

# ==============================================
# TAB 2: الجدوى اللوجستية (نفس السابق)
# ==============================================
with tab2:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">📊 الجدوى اللوجستية وتتبع سلوك وملاءمة المستورد</h3>
    </div>
    """, unsafe_allow_html=True)
    
    active_vin = st.session_state.get("active_vin", "5YFEPRAU6GP102834")
    active_type = st.session_state.get("active_type", "Toyota Tacoma")
    active_impact = st.session_state.get("active_impact", "خلفية (Rear Impact)")
    active_bid = st.session_state.get("active_bid", 3800)
    active_ground_cost = st.session_state.get("active_ground_cost", 450)
    active_market_val = st.session_state.get("active_market_val", 95000)
    
    total_shipping_usd = active_ground_cost + SHIPPING_COST
    total_shipping_lyd = total_shipping_usd * EXCHANGE_RATE
    total_cost_usd = active_bid + total_shipping_usd
    total_cost_lyd = total_cost_usd * EXCHANGE_RATE
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚛 النقل البري (دولار)", f"${active_ground_cost:,.0f}", f"{active_ground_cost * EXCHANGE_RATE:,.0f} د.ل")
    with col2:
        st.metric("🚢 الشحن البحري", f"${SHIPPING_COST:,.0f}", f"{SHIPPING_COST * EXCHANGE_RATE:,.0f} د.ل")
    with col3:
        st.metric("💰 التكلفة الإجمالية", f"${total_cost_usd:,.0f}", f"{total_cost_lyd:,.0f} د.ل")
    
    st.markdown(f"""
    <div class="premium-card">
        متوسط سعر السوق الليبي لـ {active_type} هو <b>{active_market_val:,.0f} د.ل</b><br>
        هامش الربح المتوقع: <b style="color:#10B981;">{active_market_val - total_cost_lyd:,.0f} د.ل</b>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# TAB 3: OBD-II (نفس السابق)
# ==============================================
with tab3:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #F59E0B;">
        <h3 style="color: #F59E0B; margin-top:0px; font-weight:800;">🔌 فك رموز وفحص كمبيوتر السيارة (OBD-II)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    dtc_input = st.text_input("📝 أدخل رموز الأعطال (مفصولة بفاصلة):", "P0300, P0171")
    if st.button("🔍 تحليل الرموز"):
        codes = [c.strip().upper() for c in dtc_input.split(",")]
        for code in codes:
            if code == "P0300":
                meaning, cause, solution, cost, severity = "إشعال عشوائي", "تلف البواجي", "استبدال البواجي", "180 د.ل", "🔴 مرتفع"
            elif code == "P0171":
                meaning, cause, solution, cost, severity = "خليط فقير", "تسريب هواء", "تنظيف MAF", "250 د.ل", "🟡 متوسط"
            elif code == "P0420":
                meaning, cause, solution, cost, severity = "كفاءة دبة البيئة", "تلف الدبة", "استبدال الدبة", "1200 د.ل", "🟡 متوسط"
            else:
                meaning, cause, solution, cost, severity = "رمز غير معروف", "فحص يدوي", "مراجعة الدليل", "غير محدد", "⚪ عام"
            
            st.markdown(f"""
            <div class="diagnostic-terminal">
                <b>[{code}]</b><br>
                • {meaning}<br>
                • السبب: {cause}<br>
                • الحل: {solution}<br>
                • التكلفة: {cost}<br>
                • الخطورة: {severity}
            </div>
            """, unsafe_allow_html=True)

# ==============================================
# TAB 4: QR Code (نفس السابق)
# ==============================================
with tab4:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">📜 وثيقة الأرشفة الرقمية والـ QR</h3>
    </div>
    """, unsafe_allow_html=True)
    
    active_vin = st.session_state.get("active_vin", "5YFEPRAU6GP102834")
    active_type = st.session_state.get("active_type", "Toyota Tacoma")
    active_impact = st.session_state.get("active_impact", "خلفية (Rear Impact)")
    active_bid = st.session_state.get("active_bid", 3800)
    total_cost_lyd = (active_bid + SHIPPING_COST + 450) * EXCHANGE_RATE
    
    col_q1, col_q2 = st.columns([1, 2])
    with col_q1:
        car_url = f"https://shassee-app-ly.supabase.co/car-history?vin={active_vin}"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={requests.utils.quote(car_url)}"
        st.image(qr_url, caption="QR Code للسيارة")
    
    with col_q2:
        st.markdown(f"""
        <div class="premium-card">
            • VIN: <b>{active_vin}</b><br>
            • الموديل: <b>{active_type}</b><br>
            • الصدمة: <b>{active_impact}</b><br>
            • السعر: <b>${active_bid:,.0f}</b><br>
            • التكلفة الإجمالية: <b>{total_cost_lyd:,.0f} د.ل</b>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("💾 حفظ الملف الرقمي"):
        st.success("✅ تم حفظ الملف بنجاح (محاكاة)")

# ==============================================
# TAB 5: SQL (نفس السابق)
# ==============================================
with tab5:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">⚙️ تهيئة قاعدة البيانات (Supabase SQL)</h3>
    </div>
    """, unsafe_allow_html=True)
    st.code("""
    CREATE TABLE cars (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        vin VARCHAR(17) UNIQUE NOT NULL,
        vehicle_type VARCHAR(50) NOT NULL,
        impact_angle VARCHAR(50) NOT NULL,
        purchase_price NUMERIC NOT NULL,
        rehab_cost_lyd NUMERIC NOT NULL,
        target_sale_price_lyd NUMERIC NOT NULL,
        is_safe BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
    );
    ALTER TABLE cars ENABLE ROW LEVEL SECURITY;
    CREATE POLICY "Allow public read-only access" ON cars FOR SELECT USING (true);
    CREATE POLICY "Allow authenticated insert access" ON cars FOR INSERT WITH CHECK (true);
    """, language="sql")
    st.info("انسخ الكود أعلاه والصقه في SQL Editor في Supabase لتجهيز الجدول.")

# ==============================================
# TAB 6: تحليل ذكي (AI) – مع رفع الصور والتحليل
# ==============================================
with tab6:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #8B5CF6;">
        <h3 style="color: #8B5CF6; margin-top:0px;">🧠 التحليل الذكي بالذكاء الاصطناعي</h3>
        قم برفع صور السيارة أو استخدام صور المزاد لتحليل الأضرار واكتشاف الصدأ وتحديد قطع الغيار بأرقامها المصنعية.
    </div>
    """, unsafe_allow_html=True)
    
    # اختيار مصدر الصورة
    source_option = st.radio(
        "اختر مصدر الصورة:",
        ["رفع صورة من جهازي", "استخدام صورة من المزاد (السيارة المختارة)"]
    )
    
    image_bytes = None
    if source_option == "رفع صورة من جهازي":
        uploaded_file = st.file_uploader("اختر صورة السيارة", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_bytes = uploaded_file.read()
    else:
        # استخدام صورة من السيارة المختارة
        selected_lot = None
        for lot in st.session_state.lots_db:
            if lot.get("id") == st.session_state.get("selected_car_id"):
                selected_lot = lot
                break
        if selected_lot and selected_lot.get("images"):
            try:
                img_url = selected_lot["images"][0]
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    image_bytes = response.content
                else:
                    st.warning("تعذر جلب الصورة من المزاد، حاول رفع صورة يدوياً.")
            except:
                st.warning("تعذر جلب الصورة، حاول رفع صورة يدوياً.")
        else:
            st.info("لم يتم اختيار سيارة أو لا توجد صور لها، يرجى رفع صورة يدوياً.")
    
    if image_bytes:
        # عرض الصورة
        st.image(image_bytes, caption="الصورة المختارة للتحليل", use_container_width=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_btn = st.button("🔍 تحليل الصورة بالذكاء الاصطناعي", use_container_width=True)
        with col_btn2:
            rust_btn = st.button("🦀 كشف الصدأ", use_container_width=True)
        
        if analyze_btn:
            openai_key = st.session_state.get("openai_key", "")
            if not openai_key:
                st.warning("⚠️ يرجى إدخال مفتاح OpenAI في الشريط الجانبي أولاً.")
            else:
                with st.spinner("⏳ جاري تحليل الصورة... قد يستغرق 10-20 ثانية"):
                    result = analyze_car_image_with_openai(image_bytes, openai_key)
                    st.markdown("### 📝 نتائج التحليل:")
                    st.write(result)
                    
                    # استخراج أرقام OEM
                    model = st.session_state.get("active_type", "Tacoma")
                    oem_parts = get_oem_parts_from_text(model, result)
                    if oem_parts:
                        st.markdown("### 🔩 قطع الغيار المتضررة (مع الأرقام المصنعية):")
                        for part in oem_parts:
                            st.markdown(f"- **{part['part']}**: `{part['oem']}`")
                    else:
                        st.info("لم يتم التعرف على قطع غيار محددة من هذا التحليل (يمكنك إضافتها يدوياً).")
        
        if rust_btn:
            with st.spinner("⏳ جاري تحليل الصدأ..."):
                rust_percent = detect_rust_with_opencv(image_bytes)
                if rust_percent > 0:
                    st.metric("نسبة الصدأ المقدرة", f"{rust_percent:.1f}%")
                    if rust_percent > 10:
                        st.warning("⚠️ نسبة صدأ مرتفعة، يوصى بفحص دقيق للهيكل.")
                    else:
                        st.success("✅ نسبة صدأ منخفضة، السيارة بحالة جيدة.")
                else:
                    st.info("لم يتمكن النظام من تقدير نسبة الصدأ (تأكد من وضوح الصورة).")
    
    # نموذج 3D (عرض توضيحي)
    with st.expander("🗺️ عرض الهيكل 3D مع تمييز الأضرار (افتراضي)"):
        # يمكن تحديث هذه القيم بناءً على تحليل الصور
        intensities = [0.1, 0.9, 0.9, 0.1, 0.1, 0.9, 0.9, 0.1, 0.2, 0.8]
        fig = create_3d_chassis(intensities)
        st.plotly_chart(fig, use_container_width=True)

# ==============================================
# 10. تذييل الصفحة
# ==============================================
st.markdown("""
---
<div style="text-align: center; color: #9CA3AF; font-size: 13px; padding: 15px; background: rgba(15, 23, 42, 0.3); border-radius: 12px; margin-top:20px;">
    <b>⚠️ إخلاء مسؤولية:</b> جميع التقييمات هي أدوات تنبؤية للمساعدة في اتخاذ القرار، ويجب مطابقتها بالفحص الفني العيني.
</div>
""", unsafe_allow_html=True)
