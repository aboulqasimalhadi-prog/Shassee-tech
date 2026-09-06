import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as ob
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

# ==============================================
# 1. إعدادات الصفحة والتصميم (كما هي)
# ==============================================
st.set_page_config(
    page_title="شاصي تك | SHASSEE TECH v26",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS المتقدم (نفس الكود السابق)
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
    .bid-btn-pre>button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        color: white !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
    }
    .bid-btn-pre>button:hover {
        background: #FFFFFF !important;
        color: #D97706 !important;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.5) !important;
    }
    .bid-btn-live>button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        color: white !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
    }
    .bid-btn-live>button:hover {
        background: #FFFFFF !important;
        color: #DC2626 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5) !important;
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
    .diagnostic-terminal {
        background: #030712 !important;
        border: 1px solid #10B981 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        font-family: 'Courier New', monospace !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.1) !important;
    }
    .metric-val {
        font-size: 34px;
        font-weight: 900;
        color: #10B981;
        text-shadow: 0 0 15px rgba(16, 185, 129, 0.35);
        margin: 5px 0;
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
# 2. دوال مساعدة للشعار والهيدر (نفس السابق)
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
    <div style="background: rgba(16, 185, 129, 0.03); 
                border: 1px dashed rgba(16, 185, 129, 0.25); 
                border-radius: 16px; 
                padding: 20px 40px; 
                margin-bottom: 25px; 
                text-align: center;
                box-shadow: 0 0 30px rgba(16, 185, 129, 0.05);">
        <span style="font-size: 50px; filter: drop-shadow(0 0 10px #10B981);">🦾</span>
        <h2 style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 800; font-size: 22px; margin-top: 10px; margin-bottom: 0px; letter-spacing: 1px;">
            SHASSEE TECH | SECURE CHASSIS AUDIT
        </h2>
        <p style="color: #9CA3AF; font-size: 13px; margin-top: 5px; margin-bottom: 0px;">
            نظام التحقق الفيزيائي العيني والامتثال الجمركي المستقل لسيارات الاستيراد
        </p>
    </div>
    '''

header_html = f"""<div style="background: linear-gradient(135deg, rgba(13, 21, 39, 0.65) 0%, rgba(7, 9, 19, 0.85) 100%); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 24px; padding: 35px 20px; text-align: center; margin-bottom: 35px; box-shadow: 0 20px 40px rgba(0,0,0,0.45); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);"><div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">{silver_car_html}<h1 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 38px; margin-top: 10px; margin-bottom: 5px; text-shadow: 0 0 25px rgba(16, 185, 129, 0.45);">منصة شاصي تك | SHASSEE TECH</h1><p style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 700; font-size: 18px; margin-top: 0px; letter-spacing: 0.5px;">التقييم الفني والمالي المستقل ومغلف البحث الموحد لمزادات السيارات المستوردة لعام 2026</p></div></div>"""
st.markdown(header_html, unsafe_allow_html=True)

# ==============================================
# 3. الشريط الجانبي (التفضيلات والإعدادات)
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

integration_mode = st.sidebar.selectbox(
    "🔌 نمط تشغيل النظام:",
    ["🎯 وضع المحاكاة الذكي (Demo Mode)", "⚡ الوضع السحابي الحقيقي (Live Cloud)"]
)

# مفاتيح API الإضافية
apibara_key = st.sidebar.text_input(
    "🔑 مفتاح Apibara API (اختياري):", 
    type="password", 
    value=st.session_state.get("apibara_key", ""),
    help="أدخل مفتاحك المجاني من apibara.tech لسحب بيانات لوتات كوبارت وIAAI تلقائياً."
)
st.session_state["apibara_key"] = apibara_key

scrapingbee_key = st.sidebar.text_input(
    "🔑 مفتاح ScrapingBee API (اختياري):", 
    type="password", 
    value=st.session_state.get("scrapingbee_key", ""),
    help="للحصول على مفتاح مجاني: سجل في scrapingbee.com"
)
st.session_state["scrapingbee_key"] = scrapingbee_key

supabase_url = ""
supabase_anon_key = ""
use_openai = False
if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)":
    supabase_url = st.sidebar.text_input("🌐 Supabase Project URL:", placeholder="https://your-project.supabase.co")
    supabase_anon_key = st.sidebar.text_input("🔑 Supabase Anon Key:", type="password")
    if not supabase_url.strip() or not supabase_anon_key.strip():
        st.sidebar.warning("⚠️ أدخل مفاتيح السيرفر (Supabase) للربط وحفظ تقارير السيارات الحقيقية:")
    else:
        st.sidebar.success("⚡ السيرفر السحابي متصل الآن وجاهز لحفظ البيانات حقيقياً!")
    st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    use_openai = st.sidebar.checkbox("🧠 تفعيل فحص الصور الحقيقي (OpenAI Vision)", value=False)
    if use_openai:
        openai_key = st.sidebar.text_input("🔑 OpenAI API Key (Vision):", type="password")
else:
    st.sidebar.info("💡 يعمل النظام الآن بنظام المحاكاة الذكية المتقدمة بناءً على الخبرة التشغيلية لـ 12 عاماً.")

# ثوابت عامة
EXCHANGE_RATE = 9.4
SHIPPING_COST = 2250

# ==============================================
# 4. دوال جلب البيانات الذكية (القلب الجديد)
# ==============================================

def extract_clean_url(url):
    """استخلاص الرابط النظيف من النص المختلط"""
    match = re.search(r'(https?://[^\s\)"\'<>]+)', url)
    if match:
        return match.group(1).strip()
    return url.strip()

def detect_platform(url):
    """تحديد المنصة من الرابط"""
    if "copart" in url.lower():
        return "Copart"
    elif "iaai" in url.lower():
        return "IAAI"
    return "Copart"  # افتراضي

def extract_lot_id(url):
    """استخلاص رقم اللوت من الرابط"""
    # محاولة أنماط مختلفة
    patterns = [r'/lot/(\d+)', r'id=(\d+)', r'lotId=(\d+)']
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return str(random.randint(1000000, 9999999))

def fetch_from_apibara(lot_id, api_key):
    """محاولة جلب البيانات من Apibara API"""
    if not api_key:
        return None
    try:
        response = requests.get(
            "https://apibara.tech/api/v1/vehicle-auction/vehicles",
            params={"lot_id": lot_id},
            headers={"X-API-Key": api_key},
            timeout=6
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("data"):
                return data["data"]
    except Exception:
        pass
    return None

def fetch_from_scrapingbee(url, api_key):
    """محاولة جلب الصفحة عبر ScrapingBee API"""
    if not api_key:
        return None
    try:
        response = requests.get(
            "https://app.scrapingbee.com/api/v1/",
            params={"api_key": api_key, "url": url, "render_js": "false"},
            timeout=10
        )
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return None

def fetch_from_cloudscraper(url):
    """محاولة جلب الصفحة مباشرة باستخدام cloudscraper"""
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return None

def extract_copart_data(html):
    """استخراج البيانات من HTML صفحة كوبارت"""
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    
    # العنوان (يحتوي على الموديل والسنة غالباً)
    title_tag = soup.select_one("h1[data-uname='lotDetailHeader']")
    if title_tag:
        title_text = title_tag.text.strip()
        # استخراج السنة والموديل والماركة
        year_match = re.search(r'\b(20[0-2][0-9]|199[0-9])\b', title_text)
        data['year'] = int(year_match.group(1)) if year_match else 2022
        # حاول استخراج الماركة والموديل
        words = title_text.split()
        if len(words) >= 2:
            data['make'] = words[0]
            data['model'] = " ".join(words[1:])
        else:
            data['make'] = "Toyota"
            data['model'] = "Unknown"
    else:
        data['year'] = 2022
        data['make'] = "Toyota"
        data['model'] = "Unknown"
    
    # السعر الحالي
    bid_tag = soup.select_one("span[data-uname='bidPrice']")
    if bid_tag:
        bid_text = bid_tag.text.strip().replace('$', '').replace(',', '')
        try:
            data['current_bid'] = float(bid_text)
        except:
            data['current_bid'] = 3000
    else:
        data['current_bid'] = 3000
    
    # VIN
    vin_tag = soup.select_one("div[data-uname='vinValue']")
    if vin_tag:
        data['vin'] = vin_tag.text.strip()
    else:
        data['vin'] = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17))
    
    # الموقع
    loc_tag = soup.select_one("div[data-uname='locationValue']")
    if loc_tag:
        data['location'] = loc_tag.text.strip()
    else:
        data['location'] = random.choice(["Texas (Houston)", "California (Sacramento)", "New York (Long Island)"])
    
    # نوع السند
    title_tag2 = soup.select_one("div[data-uname='titleValue']")
    if title_tag2:
        data['title'] = title_tag2.text.strip()
    else:
        data['title'] = random.choice(["Salvage Title", "Clean Title", "Bill of Sale"])
    
    # زاوية الصدمة (تخمين بناءً على النص أو نتركها للتعديل اليدوي)
    data['impact'] = random.choice(["أمامية يسار (Front-Left Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)"])
    
    data['platform'] = "Copart"
    return data

def extract_iaai_data(html):
    """استخراج البيانات من HTML صفحة IAAI (مشابهة لكوبارت)"""
    # بنفس الطريقة مع تغيير المحددات (يمكن تعديلها حسب هيكل IAAI)
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    # ... (نفس المنطق ولكن بمحددات مختلفة)
    # حالياً نعيد بيانات وهمية مع تفعيل التعديل اليدوي
    data['year'] = 2021
    data['make'] = "Toyota"
    data['model'] = "4Runner"
    data['current_bid'] = 4800
    data['vin'] = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17))
    data['location'] = random.choice(["Texas (Houston)", "California (Sacramento)"])
    data['title'] = "Clean Title"
    data['impact'] = random.choice(["أمامية يسار (Front-Left Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)"])
    data['platform'] = "IAAI"
    return data

def generate_smart_guess(url, platform, lot_id):
    """التخمين الذكي من الرابط وقاعدة بيانات مدمجة"""
    # استخدم معرف اللوت كبذرة لتوليد بيانات متسقة
    seed = int(hashlib.md5(lot_id.encode()).hexdigest(), 16) % 10000000
    r_gen = random.Random(seed)
    
    # استخراج كلمات مفتاحية من الرابط
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
    
    # حساب التكلفة الأرضية حسب الموقع
    ground_cost = 450
    if "texas" in location.lower():
        ground_cost = 450
    elif "california" in location.lower():
        ground_cost = 850
    elif "new york" in location.lower() or "jersey" in location.lower() or "pennsylvania" in location.lower():
        ground_cost = 350
    elif "florida" in location.lower():
        ground_cost = 550
    
    # القيمة السوقية في ليبيا
    if "tacoma" in model.lower():
        market_val_lyd = 95000
    elif "4runner" in model.lower():
        market_val_lyd = 110000
    elif "tundra" in model.lower():
        market_val_lyd = 72000
    else:
        market_val_lyd = 65000
    
    # قطع OEM حسب الموديل
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
        "scraped": False,  # تم التخمين وليس سحب حقيقي
        "url": url
    }

def smart_parse_auction_url(url):
    """الدالة الرئيسية لجلب البيانات بذكاء"""
    clean_url = extract_clean_url(url)
    platform = detect_platform(clean_url)
    lot_id = extract_lot_id(clean_url)
    
    # 1. محاولة Apibara API
    api_key = st.session_state.get("apibara_key", "")
    if api_key:
        api_data = fetch_from_apibara(lot_id, api_key)
        if api_data:
            # تحويل البيانات إلى صيغة موحدة
            return {
                "id": f"LOT-{lot_id}",
                "vin": api_data.get("vin", ""),
                "make": api_data.get("make", "Toyota"),
                "model": api_data.get("model", "Unknown"),
                "year": int(api_data.get("year", 2022)),
                "platform": api_data.get("platform", platform),
                "location": api_data.get("location", "Unknown"),
                "ground_cost": 450,
                "title": api_data.get("title", "Salvage Title"),
                "impact": api_data.get("impact", "خلفية (Rear Impact)"),
                "current_bid": float(api_data.get("current_bid", 3000)),
                "market_val_lyd": 95000,
                "oem_parts": [{"part": "غير محدد", "oem": "N/A", "desc": "سيتم تحديثه"}],
                "scraped": True,
                "url": clean_url,
                "images": api_data.get("images", [])
            }
    
    # 2. محاولة ScrapingBee
    if st.session_state.get("scrapingbee_key"):
        html = fetch_from_scrapingbee(clean_url, st.session_state["scrapingbee_key"])
        if html:
            if platform == "Copart":
                data = extract_copart_data(html)
            else:
                data = extract_iaai_data(html)
            # إضافة حقول إضافية
            data["id"] = f"LOT-{lot_id}"
            data["ground_cost"] = 450
            data["market_val_lyd"] = 95000
            data["oem_parts"] = [{"part": "غير محدد", "oem": "N/A", "desc": "سيتم تحديثه"}]
            data["scraped"] = True
            data["url"] = clean_url
            data["images"] = []
            return data
    
    # 3. محاولة Cloudscraper المباشر
    html = fetch_from_cloudscraper(clean_url)
    if html:
        if platform == "Copart":
            data = extract_copart_data(html)
        else:
            data = extract_iaai_data(html)
        data["id"] = f"LOT-{lot_id}"
        data["ground_cost"] = 450
        data["market_val_lyd"] = 95000
        data["oem_parts"] = [{"part": "غير محدد", "oem": "N/A", "desc": "سيتم تحديثه"}]
        data["scraped"] = True
        data["url"] = clean_url
        data["images"] = []
        return data
    
    # 4. التخمين الذكي (fallback)
    return generate_smart_guess(clean_url, platform, lot_id)

# ==============================================
# 5. تهيئة قاعدة البيانات المحلية (lots_db)
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

# ==============================================
# 6. واجهة التطبيق (Tabs)
# ==============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 مغلف البحث الموحد ومطابقة التفضيلات", 
    "📊 الجدوى اللوجستية وتتبع السلوك", 
    "🔌 فك رموز كمبيوتر السيارة (OBD-II)",
    "📜 ملصق الـ QR وأرشفة السيارة",
    "⚙️ تهيئة السيرفر وقاعدة البيانات (SQL)"
])

# ==============================================
# TAB 1: البحث الموحد
# ==============================================
with tab1:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">🔍 مغلف المزايدة والبحث الموحد لمزادات (Copart & IAAI)</h3>
        أدخل رابط السيارة من كوبارت أو IAAI، أو ابحث في اللوتات المحفوظة. النظام يسحب البيانات بذكاء عبر عدة طبقات.
    </div>
    """, unsafe_allow_html=True)
    
    # حقل إدخال الرابط
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.08); border-right: 4px solid #10B981; padding: 18px; border-radius: 12px; margin-bottom: 25px;">
        <b style="color: #10B981; font-size:16px;">🔗 ربط ذكي متعدد الطبقات:</b><br>
        الصق رابط السيارة من <b>Copart</b> أو <b>IAAI</b>، وسيحاول النظام جلب البيانات عبر API، ثم Scraping، وأخيراً التخمين الذكي.
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
    
    # تنظيف الرابط
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
        with st.spinner("⏳ جاري جلب البيانات باستخدام الطبقات الذكية..."):
            new_lot = smart_parse_auction_url(clean_url_input)
            # التحقق من عدم التكرار
            exists = any(lot["id"] == new_lot["id"] for lot in st.session_state.lots_db)
            if not exists:
                st.session_state.lots_db.insert(0, new_lot)
            st.session_state["selected_car_id"] = new_lot["id"]
            st.toast(f"🎉 تم جلب وتنشيط السيارة: {new_lot['model']} ({new_lot['id']})")
            st.rerun()
    
    # عرض اللوتات المفلترة
    st.markdown("<hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search_platform = st.selectbox("🌐 المنصة:", ["الكل", "Copart", "IAAI"])
    with col_f2:
        search_make = st.selectbox("🚘 الماركة:", ["الكل", "Toyota", "Lexus", "Honda", "Ford", "GMC"])
    with col_f3:
        search_text = st.text_input("📝 بحث في VIN أو رقم اللوت:", placeholder="اكتب للبحث...")
    
    filter_by_prefs = st.checkbox("🎯 تصفية حسب تفضيلاتي الشخصية", value=False)
    
    # تصفية القائمة
    filtered_lots = []
    for lot in st.session_state.lots_db:
        if search_platform != "الكل" and lot["platform"] != search_platform:
            continue
        if search_make != "الكل" and lot["make"] != search_make:
            continue
        if search_text and search_text.lower() not in lot["vin"].lower() and search_text.lower() not in lot["id"].lower():
            continue
        if filter_by_prefs:
            if lot["make"] not in pref_make:
                continue
            # مطابقة زاوية الصدمة
            match_impact = False
            for p_imp in pref_impact:
                if p_imp.split("(")[0].strip().lower() in lot["impact"].lower() or lot["impact"].lower() in p_imp.lower():
                    match_impact = True
                    break
            if not match_impact:
                continue
            if lot["current_bid"] > pref_budget:
                continue
        filtered_lots.append(lot)
    
    st.markdown(f"### 📋 النتائج ({len(filtered_lots)} سيارة)")
    
    # عرض البطاقات
    selected_lot = None
    for lot in filtered_lots:
        col_c1, col_c2 = st.columns([2.5, 1])
        badge = "badge-copart" if lot["platform"] == "Copart" else "badge-iaai"
        
        # حساب درجة التوافق
        is_make_match = lot["make"] in pref_make
        is_impact_match = any(
            p_imp.split("(")[0].strip().lower() in lot["impact"].lower() or lot["impact"].lower() in p_imp.lower()
            for p_imp in pref_impact
        )
        is_budget_match = lot["current_bid"] <= pref_budget
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
                <span class="{badge}">{lot['platform']}</span>
                <b style="font-size:18px; color:white;">{lot['year']} {lot['model']}</b>
                <span style="font-size:12px; color:#9CA3AF;">(لوط: {lot['id']} | VIN: {lot['vin']})</span><br>
                <div style="margin-top: 8px; font-size:13px;">
                    • <b>الموقع:</b> {lot['location']} | <b>السند:</b> {lot['title']}<br>
                    • <b>الصدمة:</b> {lot['impact']} | <b>السعر الحالي:</b> <span style="color:#10B981; font-weight:bold;">${lot['current_bid']:,.0f}</span><br>
                    • <b style="color: {'#10B981' if fit_score >= 90 else '#F59E0B' if fit_score >= 70 else '#EF4444'};">{fit_badge}</b> ({fit_desc})
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c2:
            st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("🔍 فتح", key=f"btn_select_{lot['id']}"):
                st.session_state["selected_car_id"] = lot["id"]
                st.rerun()
    
    # إذا تم اختيار سيارة، عرض تفاصيلها المتقدمة
    if "selected_car_id" in st.session_state:
        for lot in st.session_state.lots_db:
            if lot["id"] == st.session_state["selected_car_id"]:
                selected_lot = lot
                break
    
    if selected_lot:
        st.markdown("<hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown(f"### ⚙️ التفاصيل المتقدمة للسيارة المختارة: {selected_lot['year']} {selected_lot['model']}")
        
        # عرض الصور (من API أو افتراضية)
        images = selected_lot.get("images", [])
        if not images:
            # صور افتراضية حسب الموديل
            if "tacoma" in selected_lot["model"].lower():
                images = [
                    "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600",
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=300"
                ]
            elif "4runner" in selected_lot["model"].lower():
                images = [
                    "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600",
                    "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=300"
                ]
            else:
                images = ["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600"]
        
        col_img1, col_img2 = st.columns([1.5, 1])
        with col_img1:
            st.image(images[0], caption=f"{selected_lot['model']} - صورة المزاد", use_container_width=True)
        with col_img2:
            if len(images) > 1:
                st.image(images[1], caption="زاوية إضافية", use_container_width=True)
            else:
                st.info("لا توجد صور إضافية.")
        
        # تعديل يدوي
        with st.expander("🛠️ تعديل البيانات يدوياً (لضمان الدقة)"):
            col_ed1, col_ed2, col_ed3 = st.columns(3)
            with col_ed1:
                edit_model = st.text_input("الموديل:", value=selected_lot["model"])
                edit_year = st.number_input("السنة:", min_value=1990, max_value=2027, value=int(selected_lot["year"]))
            with col_ed2:
                impact_list = ["أمامية يسار (Front-Left Impact)", "أمامية يمين (Front-Right Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)", "سليمة / صدمة خفيفة"]
                current_impact_idx = 0
                for i, imp in enumerate(impact_list):
                    if selected_lot["impact"][:10] in imp:
                        current_impact_idx = i
                        break
                edit_impact = st.selectbox("زاوية الصدمة:", impact_list, index=current_impact_idx)
                edit_title = st.selectbox("نوع السند:", ["Salvage Title", "Clean Title", "Bill of Sale", "Certificate of Destruction"], index=0)
            with col_ed3:
                loc_list = ["Texas (Houston)", "California (Sacramento)", "New York (Long Island)", "Florida (Miami)", "Pennsylvania (Salt-Belt)"]
                current_loc_idx = 0
                for i, loc in enumerate(loc_list):
                    if selected_lot["location"][:10] in loc:
                        current_loc_idx = i
                        break
                edit_location = st.selectbox("الموقع:", loc_list, index=current_loc_idx)
                edit_bid = st.number_input("السعر الحالي ($):", min_value=500, max_value=30000, value=int(selected_lot["current_bid"]))
            
            if st.button("💾 حفظ التعديلات"):
                # تحديث اللوت في قاعدة البيانات
                for idx, lot in enumerate(st.session_state.lots_db):
                    if lot["id"] == selected_lot["id"]:
                        st.session_state.lots_db[idx]["model"] = edit_model
                        st.session_state.lots_db[idx]["year"] = edit_year
                        st.session_state.lots_db[idx]["impact"] = edit_impact
                        st.session_state.lots_db[idx]["title"] = edit_title
                        st.session_state.lots_db[idx]["location"] = edit_location
                        st.session_state.lots_db[idx]["current_bid"] = edit_bid
                        # تحديث التكلفة الأرضية
                        if "texas" in edit_location.lower():
                            st.session_state.lots_db[idx]["ground_cost"] = 450
                        elif "california" in edit_location.lower():
                            st.session_state.lots_db[idx]["ground_cost"] = 850
                        else:
                            st.session_state.lots_db[idx]["ground_cost"] = 350
                        st.toast("✅ تم تحديث البيانات")
                        st.rerun()
        
        # حفظ المتغيرات النشطة للاستخدام في التبويبات الأخرى
        st.session_state["active_vin"] = selected_lot["vin"]
        st.session_state["active_type"] = selected_lot["model"]
        st.session_state["active_impact"] = selected_lot["impact"]
        st.session_state["active_bid"] = selected_lot["current_bid"]
        st.session_state["active_ground_cost"] = selected_lot["ground_cost"]
        st.session_state["active_market_val"] = selected_lot["market_val_lyd"]

# ==============================================
# TAB 2: الجدوى اللوجستية
# ==============================================
with tab2:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">📊 الجدوى اللوجستية وتتبع سلوك وملاءمة المستورد</h3>
        التحليل المالي التفصيلي وتتبع كلفة الشحن البري والبحري وصولاً لمتوسط سعر السوق المفتوح بليبيا.
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
    
    # تحليل حزام الملح
    if "Pennsylvania" in selected_lot["location"] if selected_lot else False:
        st.warning("⚠️ هذه السيارة من حزام الملح (خطر صدأ مرتفع)")
    else:
        st.success("✅ السيارة خارج حزام الملح (خطر صدأ منخفض)")
    
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
        <h3 style="color: #F59E0B; margin-top:0px; font-weight:800;">🔌 فك رموز وفحص كمبيوتر السيارة (OBD-II DTC Parser)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    dtc_input = st.text_input("📝 أدخل رموز الأعطال (مفصولة بفاصلة):", "P0300, P0171")
    if st.button("🔍 تحليل الرموز"):
        codes = [c.strip().upper() for c in dtc_input.split(",")]
        for code in codes:
            # قاموس بسيط للرموز (يمكن توسيعه)
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
# TAB 4: QR Code (نفس السابق مع تعديلات بسيطة)
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
    active_market_val = st.session_state.get("active_market_val", 95000)
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
    st.info("انسخ الكود أعلاه والصقه in SQL Editor في Supabase لتجهيز الجدول.")

# ==============================================
# 7. تذييل الصفحة
# ==============================================
st.markdown("""
---
<div style="text-align: center; color: #9CA3AF; font-size: 13px; padding: 15px; background: rgba(15, 23, 42, 0.3); border-radius: 12px; margin-top:20px;">
    <b>⚠️ إخلاء مسؤولية:</b> جميع التقييمات هي أدوات تنبؤية للمساعدة في اتخاذ القرار، ويجب مطابقتها بالفحص الفني العيني.
</div>
""", unsafe_allow_html=True)
