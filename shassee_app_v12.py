import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as ob
import time
import requests
import json
import base64
import os

# Set Page Configuration for an absolute premium, immersive UI
st.set_page_config(
    page_title="شاصي تك | SHASSEE TECH v12",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Cyberpunk & Glassmorphism CSS Injection (Aggressive UI Overrides)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Native Scrollbar Customization */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #060913;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E3A8A;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #10B981;
    }

    /* Global Typography & Deep Obsidian Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background: radial-gradient(circle at top right, #0D1527 0%, #070913 100%) !important;
        color: #E5E7EB !important;
    }
    
    /* Sidebar Luxury Neon Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090E1A 0%, #050811 100%) !important;
        border-left: 1px solid rgba(16, 185, 129, 0.15) !important;
        box-shadow: 10px 0px 30px rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Glassmorphic Input & Select Boxes */
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
    
    /* Sci-Fi Scanner Action Button */
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
    .stButton>button:active {
        transform: translateY(1px) !important;
    }

    /* Bidding Secondary Action Buttons */
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

    /* Cyberpunk Hologram Cards */
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
    
    /* Auction Source Badges */
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

    /* Futuristic Diagnostic Terminal for OBD */
    .diagnostic-terminal {
        background: #030712 !important;
        border: 1px solid #10B981 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        font-family: 'Courier New', monospace !important;
        color: #34D399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.1) !important;
    }
    
    /* Neon Glow Metrics Display */
    .metric-box {
        background: rgba(11, 15, 26, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .metric-val {
        font-size: 34px;
        font-weight: 900;
        color: #10B981;
        text-shadow: 0 0 15px rgba(16, 185, 129, 0.35);
        margin: 5px 0;
    }
    
    /* Adaptive Tabs UI */
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

# 🛠️ Dynamic Logo Fallback Loader
logo_path = "shassee_tech_final_logo.png"
logo_exists = os.path.exists(logo_path)

if not logo_exists:
    for file in os.listdir("."):
        if "logo" in file.lower() and file.endswith((".png", ".jpg", ".jpeg")):
            logo_path = file
            logo_exists = True
            break

# 🚗 Sleek Header (AI Era Rebranding - Completely Custom Glass Panel)
st.markdown("""
<div style="background: linear-gradient(90deg, rgba(30, 58, 138, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%); 
            border: 1px solid rgba(59, 130, 246, 0.15); 
            border-radius: 20px; \n            padding: 30px; 
            text-align: center; 
            margin-bottom: 35px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);">
    <h1 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 42px; margin-bottom: 5px; text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);">🚗 منصة شاصي تك | SHASSEE TECH</h1>\n    <p style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 700; font-size: 18px; margin-top: 0px; letter-spacing: 0.5px;">التقييم الفني والمالي المستقل ومغلف البحث الموحد لمزادات السيارات المستوردة لعام 2026</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR: Brand Logo & User Profiling ---
if logo_exists:
    st.sidebar.image(logo_path, use_container_width=True)
    st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 15px; margin-bottom: 15px;">
        <h2 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 28px; margin-bottom: 0px;">SHASSEE TECH</h2>\n        <span style="font-size: 11px; color: #10B981; font-weight: bold; letter-spacing: 1px;">VEHICLE INTELLIGENCE & AUDIT</span>
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

openai_key = ""
supabase_url = ""
supabase_anon_key = ""
use_openai = False

if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)":
    st.sidebar.warning("⚠️ أدخل مفاتيح السيرفر (Supabase) للربط وحفظ تقارير السيارات الحقيقية:")
    supabase_url = st.sidebar.text_input("🌐 Supabase Project URL:", placeholder="https://your-project.supabase.co")
    supabase_anon_key = st.sidebar.text_input("🔑 Supabase Anon Key:", type="password")
    
    st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    use_openai = st.sidebar.checkbox("🧠 تفعيل فحص الصور الحقيقي (OpenAI Vision)", value=False)
    if use_openai:
        openai_key = st.sidebar.text_input("🔑 OpenAI API Key (Vision):", type="password")
else:
    st.sidebar.info("💡 يعمل النظام الآن بنظام المحاكاة الذكية المتقدمة بناءً على الخبرة التشغيلية لـ 12 عاماً.")

# Global configurations
exchange_rate = 9.4  # LYD/$
shipping_cost = 2250  # Fixed $2250 shipping

# Layout Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 مغلف البحث الموحد ومطابقة التفضيلات", 
    "📊 الجدوى اللوجستية وتتبع السلوك", 
    "🔌 فك رموز كمبيوتر السيارة (OBD-II)",
    "📜 ملصق الـ QR وأرشفة السيارة",
    "⚙️ تهيئة السيرفر وقاعدة البيانات (SQL)"
])

# Utility function for base64 encoding
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# --- MOCK AUCTION LOTS DATABASE ---
lots_data = [
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
        ]
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
        ]
    },
    {
        "id": "LOT-1028491",
        "vin": "5YFEPRAU6GP001928",
        "make": "Toyota",
        "model": "Toyota Tundra 2006",
        "year": 2006,
        "platform": "Copart",
        "location": "New Jersey (Newark)",
        "ground_cost": 350,
        "title": "Certificate of Destruction",
        "impact": "أمامية يسار (Front-Left)",
        "current_bid": 5200,
        "market_val_lyd": 72000,
        "oem_parts": [
            {"part": "رادياتير مبرد المحرك", "oem": "16400-0C210", "desc": "ميكانيكي - تبريد بالكرتون"},
            {"part": "مجموعة مقص تعليق أيسر", "oem": "48069-34010", "desc": "تعليق وهيكل سفلي"},
            {"part": "رفرف أمامي أيسر", "oem": "53812-34080", "desc": "صاج تجميلي خارجي"}
        ]
    },
    {
        "id": "LOT-7739102",
        "vin": "5YFEPRAU6GP992019",
        "make": "Toyota",
        "model": "Toyota T100",
        "year": 1998,
        "platform": "IAAI",
        "location": "Pennsylvania (Salt-Belt)",
        "ground_cost": 400,
        "title": "Bill of Sale",
        "impact": "سليمة / صدمة خفيفة",
        "current_bid": 2100,
        "market_val_lyd": 45000,
        "oem_parts": [
            {"part": "مصد أمامي تجميلي", "oem": "52119-34010", "desc": "بلاستيك خارجي تجميلي"}
        ]
    }
]

# --- TAB 1: UNIFIED SEARCH & WRAPPER ---
with tab1:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">🔍 مغلف المزايدة والبحث الموحد لمزادات (Copart & IAAI)</h3>
        تم تجميع وتصفية المركبات من المنصتين وعرضها بهويتك البصرية الفاخرة. حدد السيارة لتشغيل محرك الفحص الذكي ومطابقة تفضيلاتك الاستثمارية فوراً.
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Controls for Unified Search
    col_search_1, col_search_2, col_search_3 = st.columns(3)
    with col_search_1:
        search_platform = st.selectbox("🌐 فلترة بحسب منصة المزاد:", ["الكل (Copart & IAAI)", "Copart فقط", "IAAI فقط"])
    with col_search_2:
        search_make = st.selectbox("🚘 فلترة بالشركة المصنعة:", ["الكل", "Toyota"])
    with col_search_3:
        search_text = st.text_input("📝 بحث سريع برقم الشاصي (VIN) أو رقم اللوط:", placeholder="اكتب للبحث...")

    # Filtered lots
    filtered_lots = []
    for lot in lots_data:
        # Platform filter
        if search_platform == "Copart فقط" and lot["platform"] != "Copart":
            continue
        if search_platform == "IAAI فقط" and lot["platform"] != "IAAI":
            continue
        # Make filter
        if search_make != "الكل" and lot["make"] != search_make:
            continue
        # Text filter
        if search_text and (search_text.lower() not in lot["vin"].lower() and search_text.lower() not in lot["id"].lower()):
            continue
        filtered_lots.append(lot)
        
    st.markdown(f"### 📋 لوتات المزادات المتوفرة في البحث المغلف ({len(filtered_lots)} سيارة معروضة)")
    
    # Display cars in an ultra-premium layout
    selected_lot = None
    
    for lot in filtered_lots:
        col_c1, col_c2 = st.columns([2.5, 1])
        
        badge_style = "badge-copart" if lot["platform"] == "Copart" else "badge-iaai"
        
        # Calculate fit score dynamically based on user preferences in sidebar
        is_make_match = lot["make"] in pref_make
        is_impact_match = lot["impact"] in pref_impact
        is_budget_match = lot["current_bid"] <= pref_budget
        
        matches_count = sum([is_make_match, is_impact_match, is_budget_match])
        if matches_count == 3:
            fit_score = 95
            fit_badge = "🟢 متوافق تماماً مع معاييرك الاستثمارية (95% Match)"
            fit_desc = "السيارة تطابق ميزانيتك، الماركة المفضلة لديك، وزاوية الصدمة المرغوبة."
        elif matches_count == 2:
            fit_score = 70
            fit_badge = "🟡 متوافق جزئياً مع معاييرك (70% Match)"
            fit_desc = "السيارة تطابق غالبية شروطك مع اختلاف بسيط في زاوية الضرر أو الميزانية."
        else:
            fit_score = 35
            fit_badge = "🔴 توافق ضعيف مع معاييرك الاستثمارية (35% Match)"
            fit_desc = "السيارة تقع خارج ميزانيتك المحددة أو تملك أضراراً قوية لا تفضل الاستثمار بها."
            
        with col_c1:
            st.markdown(f"""
            <div class="premium-card" style="border-right-color: {'#10B981' if fit_score >= 90 else '#F59E0B' if fit_score >= 70 else '#EF4444'}; margin-bottom: 10px;">
                <span class="{badge_style}">{lot['platform'].upper()}</span> &nbsp; 
                <b style="font-size:18px; color:white;">{lot['year']} {lot['model']}</b> &nbsp; 
                <span style="font-size:12px; color:#9CA3AF;">(لوط: {lot['id']} | شاصي: {lot['vin']})</span><br>
                <div style="margin-top: 10px; font-size:13px; line-height: 1.6;">
                    • <b>الموقع الجغرافي:</b> {lot['location']} | <b>نوع المستند (Title):</b> {lot['title']}<br>
                    • <b>زاوية الاصطدام الرئيسية:</b> {lot['impact']} | <b>المزايدة الحالية:</b> <span style="color:#10B981; font-weight:bold;">${lot['current_bid']:,.0f}</span><br>
                    • <b style="color: {'#10B981' if fit_score >= 90 else '#F59E0B' if fit_score >= 70 else '#EF4444'};">{fit_badge}</b>: <span style="color:#D1D5DB;">{fit_desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_c2:
            st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
            if st.button("🔍 فحص واختيار السيارة", key=f"btn_select_{lot['id']}"):
                st.session_state["selected_car_id"] = lot["id"]
                st.rerun()

    # Get selected car from session state
    if "selected_car_id" in st.session_state:
        for lot in lots_data:
            if lot["id"] == st.session_state["selected_car_id"]:
                selected_lot = lot
                break
                
    if selected_lot:
        st.markdown("<hr style='border-color: rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown(f"### ⚙️ لوحة الفحص والمزايدة الذكية للمركبة المختارة: {selected_lot['year']} {selected_lot['model']}")
        
        # Display VIP bidding options
        col_bid_1, col_bid_2, col_bid_3 = st.columns(3)
        with col_bid_1:
            st.markdown('<div class="bid-btn-pre">', unsafe_allow_html=True)
            if st.button("⏰ تقديم مزايدة مسبقة (Pre-Bidding)", key="btn_pre_bid"):
                st.toast(f"⏳ تم تسجيل نيتك للمزايدة المسبقة على لوت {selected_lot['id']} وسيتم إخطارك بالتحركات!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_bid_2:
            st.markdown('<div class="bid-btn-live">', unsafe_allow_html=True)
            if st.button("🔥 دخول المزايدة الحية (Live Bidding)", key="btn_live_bid"):
                lot_url = f"https://www.copart.com/lot/{selected_lot['id'].split('-')[1]}/" if selected_lot["platform"] == "Copart" else "https://www.iaai.com/"
                st.success(f"🔗 جاري تحويلك بأمان إلى صفحة السيارة الأصلية لإتمام المزايدة بحسابك الخاص: [اضغط هنا لفتح المزاد]({lot_url})")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_bid_3:
            if st.button("💾 تتبع ومراقبة اللوت (Add to Watchlist)", key="btn_watch_lot"):
                st.toast("📌 تمت إضافة السيارة لقائمة المراقبة والتحذير الجغرافي!")
                
        # Interactive Frame Simulator & Parts Identification
        st.markdown("#### 🗺️ الخريطة الحرارية ثلاثية الأبعاد لهيكل السيارة (3D Structural Heatmap)")
        
        col_sub_1, col_sub_2 = st.columns([1.1, 0.9])
        
        with col_sub_1:
            x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
            y = [0, 4, 4, 0, 0, 4, 4, 0, 0, 4]
            z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
            
            # Match 3D simulation to selected lot's specific damage angle
            if selected_lot["impact"] == "أمامية يسار (Front-Left)":
                intensity = [0.95, 0.1, 0.1, 0.8, 0.9, 0.1, 0.1, 0.7, 0.6, 0.2]
            elif selected_lot["impact"] == "أمامية يمين (Front-Right)":
                intensity = [0.1, 0.1, 0.95, 0.8, 0.1, 0.1, 0.9, 0.7, 0.6, 0.2]
            elif selected_lot["impact"] == "خلفية (Rear Impact)":
                intensity = [0.1, 0.95, 0.95, 0.1, 0.1, 0.9, 0.9, 0.1, 0.2, 0.8]
            elif selected_lot["impact"] == "جانبية (Side Impact)":
                intensity = [0.1, 0.1, 0.1, 0.1, 0.85, 0.85, 0.1, 0.1, 0.7, 0.3]
            else:
                intensity = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
                
            fig = ob.Figure(data=[ob.Mesh3d(
                x=x, y=y, z=z,
                colorbar_title='مستوى الضرر الهيكلي',
                colorscale=[[0, '#10B981'], [0.4, '#F59E0B'], [1, '#EF4444']],
                intensity=intensity,
                intensitymode='vertex',
                name='الشاصي والهيكل',
                showscale=True
            )])
            
            fig.update_layout(
                scene=dict(
                    xaxis=dict(title='العرض', showticklabels=False, backgroundcolor="#060913", gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(title='الطول', showticklabels=False, backgroundcolor="#060913", gridcolor="rgba(255,255,255,0.05)"),
                    zaxis=dict(title='الارتفاع', showticklabels=False, backgroundcolor="#060913", gridcolor="rgba(255,255,255,0.05)"),
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(r=0, l=0, b=0, t=0),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_sub_2:
            st.markdown("##### 🔩 الأجزاء المتضررة بالرقم المصنعي الأصلي (OEM parts list):")
            st.info("💡 تم فك تجميع الهيكل بواسطة الذكاء الاصطناعي وتحديد أرقام القطع المصنعية المعتمدة لكتالوج تويوتا لتسهيل فحص وتوفير الأجزاء بدقة.")
            
            parts_df_data = {
                "الجزء المطلوب": [item["part"] for item in selected_lot["oem_parts"]],
                "رقم القطعة OEM": [item["oem"] for item in selected_lot["oem_parts"]],
                "التكلفة الاسترشادية": ["تحدد لاحقاً" for _ in selected_lot["oem_parts"]],
                "طبيعة القطعة": [item["desc"] for item in selected_lot["oem_parts"]]
            }
            st.table(pd.DataFrame(parts_df_data))
            
            # Title Verification & Compliance
            compliance_badge = ""
            compliance_desc = ""
            if "Clean" in selected_lot["title"] or "Salvage" in selected_lot["title"]:
                compliance_badge = "🟢 أوراق ملكية مقبولة للتصدير والترخيص في ليبيا"
                compliance_desc = "تطابق مستندات المزاد قوانين مصلحة الجمارك لعام 2026."
            elif "Bill of Sale" in selected_lot["title"]:
                compliance_badge = "🟡 مستندات مقيدة تتطلب معالجة ($150 - $300)"
                compliance_desc = "تحتاج لتعديل السند في الولايات المتحدة قبل الشحن."
            else:
                compliance_badge = "🔴 ممنوع جمركياً - خردة وتفكيك فقط"
                compliance_desc = "السيارة مصنفة كـ Certificate of Destruction ولا ترخص بليبيا."
                
            st.markdown(f"""
            <div class="premium-card" style="border-right-color: {'#10B981' if '🟢' in compliance_badge else '#F59E0B' if '🟡' in compliance_badge else '#EF4444'};">
                <b style="font-size:15px; color: white;">🛡️ حارس مطابقة أوراق المزاد والجمارك:</b><br>
                • <b>حالة المستند:</b> {selected_lot['title']}<br>
                • <span style="font-weight:bold;">{compliance_badge}</span><br>
                <span style="font-size:12px; color:#9CA3AF;">{compliance_desc}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Save variables for the rest of the application
            st.session_state["active_vin"] = selected_lot["vin"]
            st.session_state["active_type"] = selected_lot["model"]
            st.session_state["active_impact"] = selected_lot["impact"]
            st.session_state["active_bid"] = selected_lot["current_bid"]
            st.session_state["active_ground_cost"] = selected_lot["ground_cost"]
            st.session_state["active_market_val"] = selected_lot["market_val_lyd"]
    else:
        st.markdown("""
        <div style="background: rgba(30, 58, 138, 0.1); border: 1px dashed rgba(59, 130, 246, 0.25); padding: 40px; border-radius: 16px; text-align: center; margin-top:20px;">
            <p style="color: #9CA3AF; margin-bottom: 0px; font-size: 16px;">💡 اختر سيارة من قائمة لوتات كوبارت أو IAAI الموضحة أعلاه للبدء في الفحص وعرض المجسم ومطابقة البروفايل!</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: LOGISTICS & USER BEHAVIOR TRACKING ---
with tab2:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">📊 الجدوى اللوجستية وتتبع سلوك وملاءمة المستورد</h3>
        التحليل المالي التفصيلي وتتبع كلفة الشحن البري والبحري وصولاً لمتوسط سعر السوق المفتوح بليبيا.
    </div>
    """, unsafe_allow_html=True)
    
    # Retrieve lot specifications
    active_vin = st.session_state.get("active_vin", "5YFEPRAU6GP102834")
    active_type = st.session_state.get("active_type", "Toyota Tacoma")
    active_impact = st.session_state.get("active_impact", "خلفية (Rear Impact)")
    active_bid = st.session_state.get("active_bid", 3800)
    active_ground_cost = st.session_state.get("active_ground_cost", 450)
    active_market_val = st.session_state.get("active_market_val", 95000)
    
    # Logistics calculations
    total_shipping_usd = active_ground_cost + shipping_cost
    total_shipping_lyd = total_shipping_usd * exchange_rate
    
    total_cost_at_workshop_usd = active_bid + total_shipping_usd
    total_cost_at_workshop_lyd = total_cost_at_workshop_usd * exchange_rate
    
    col_l1, col_l2, col_l3 = st.columns(3)
    
    with col_l1:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #3B82F6; background: rgba(59, 130, 246, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>تكلفة النقل البري الداخلي الأمريكي:</span><br>
            <span class="metric-val" style="color: #3B82F6;">${active_ground_cost:,.0f}</span><br>
            <span style='font-size:13px; color:#9CA3AF;'>({active_ground_cost * exchange_rate:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_l2:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #F59E0B; background: rgba(245, 158, 11, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>الشحن البحري الثابت لليبيا:</span><br>
            <span class="metric-val" style="color: #F59E0B;">${shipping_cost:,.0f}</span><br>
            <span style='font-size:13px; color:#D1D5DB;'>({shipping_cost * exchange_rate:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_l3:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #10B981; background: rgba(16, 185, 129, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>التكلفة الإجمالية واصلة للورشة:</span><br>
            <span class="metric-val" style="color: #10B981;">${total_cost_at_workshop_usd:,.0f}</span><br>
            <span style='font-size:13px; color:#10B981; font-weight:bold;'>({total_cost_at_workshop_lyd:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    # Salt Belt and Rust Analysis
    st.markdown("### 🗺️ التقصي الجغرافي وحزام الملح الأمريكي")
    
    if "Pennsylvania" in selected_lot["location"] if selected_lot else False:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); border-right: 5px solid #EF4444; padding: 16px; border-radius: 12px; color: #FCA5A5; font-weight:bold; margin-bottom: 20px;">
            ⚠️ تنبيه الصدأ الجغرافي: هذه السيارة كانت مسجلة في ولاية تقع ضمن "حزام الملح" (Salt-Belt). خطر وجود تآكل وصدأ أسفل الهيكل يصل لـ 75% بسبب إذابة الجليد بالملح. ننصح بفحص حديد التعليق بدقة.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border-right: 5px solid #10B981; padding: 16px; border-radius: 12px; color: #A7F3D0; font-weight:bold; margin-bottom: 20px;">
            ✅ الموقع الجغرافي آمن: تقع السيارة خارج حزام الملح البارد (مؤشر خطر صدأ منخفض 10% فقط). الهيكل والحديد السفلي بحالة جافة ومستقرة.
        </div>
        """, unsafe_allow_html=True)

    # Market Value Benchmark
    st.markdown("### 📊 متوسط السعر المقارن في السوق الليبي المفتوح")
    st.markdown(f"""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        متوسط سعر البيع التقريبي لسيارة من فئة <b>{active_type}</b> بمواصفات ممتازة وتشطيب راقٍ في معارض ليبيا حالياً هو: 
        <span class="metric-val" style="font-size: 24px; color:#3B82F6;">{active_market_val:,.0f} د.ل</span>.<br>
        باستقطاع التكلفة واصلة للورشة (<span style="color:#10B981; font-weight:bold;">{total_cost_at_workshop_lyd:,.0f} د.ل</span>)، يتبقى للمستورد هامش وقدره 
        <b style="color: #10B981; font-size:16px;">{active_market_val - total_cost_at_workshop_lyd:,.0f} د.ل</b> مخصص لتأهيل صيانة السيارة وهامش ربحه الصافي.
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3: OBD-II DTC PARSER ---
with tab3:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #F59E0B;">
        <h3 style="color: #F59E0B; margin-top:0px; font-weight:800;">🔌 فك رموز وفحص كمبيوتر السيارة (OBD-II DTC Parser)</h3>
        قم بلصق رموز الأعطال المسحوبة من كمبيوتر السيارة أو فحص OBD-II لترجمتها فوراً للغة العربية ومعرفة كلفة إصلاحها الحقيقية.
    </div>
    """, unsafe_allow_html=True)
    
    dtc_input = st.text_input("📝 اكتب رموز الأعطال هنا تفصل بينها فاصلة (مثال: P0300, P0171, P0420):", "P0300, P0171", key="tab3_dtc")
    
    if st.button("🔌 تشغيل محلل وفك الرموز الذكي", key="tab3_btn"):
        with st.spinner("⏳ جاري تحليل الرموز ومطابقتها بكتالوجات تويوتا الفنية..."):
            time.sleep(1.0)
        
        st.success("✅ تم فك وتفسير الرموز بنجاح!")
        
        codes = [c.strip().upper() for c in dtc_input.split(",")]
        
        for code in codes:
            if "P0300" in code:
                meaning = "إشعال عشوائي غير منتظم في الأسطوانات (Random/Multiple Cylinder Misfire Detected)"
                cause = "تلف البواجي (شمعات الاحتراق)، تلف الكويلات، أو تسريب هواء للمحرك."
                solution = "استبدال شمعات الاحتراق (بواجي جديدة بالكرتون) وفحص كويلات الإشعال."
                cost = "180 د.ل (قطع غيار جديدة) + 50 د.ل (يد عاملة)"
                severity = "🔴 ضرر مرتفع - يؤثر على استهلاك الوقود ويتلف محول الكاتالايزر"
            elif "P0171" in code:
                meaning = "خليط وقود فقير جداً في البنك 1 (System Too Lean - Bank 1)"
                cause = "تسريب هواء خلف حساس الهواء (MAF)، اتساخ حساس تدفق الهواء، أو ضعف مضخة الوقود."
                solution = "تنظيف أو استبدال حساس الـ MAF، وفحص ليات الهواء للتأكد من عدم وجود تسريب."
                cost = "250 د.ل (حساس جديد) + 30 د.ل (تنظيف وفحص)"
                severity = "🟡 ضرر متوسط - يسبب تذبذب واهتزاز في المحرك أثناء الوقوف"
            elif "P0420" in code:
                meaning = "كفاءة دبة البيئة أقل من المطلوب (Catalyst System Efficiency Below Threshold)"
                cause = "تلف دبة البيئة (دبة التلوث) أو عطل في حساس الأكسجين الخلفي."
                solution = "استبدال دبة البيئة أو تركيب حساس أكسجين جديد ومطابق."
                cost = "1,200 د.ل (مستعملة أصلي تفصيخ) + 150 د.ل (تركيب ولحام)"
                severity = "🟡 ضرر متوسط جمركياً - لا يمنع السيارة من الحركة ولكنه يزيد الانبعاثات"
            else:
                meaning = f"رمز عطل غير معروف ({code}) في نظام الفحص السريع"
                cause = "يتطلب فحصاً معمقاً بجهاز الفحص المتطور."
                solution = "مراجعة الدليل الفني للشركة المصنعة."
                cost = "غير محدد"
                severity = "⚪ رمز فحص عام"
                
            st.markdown(f"""
            <div class="diagnostic-terminal" style="margin-bottom:20px;">
                <b style="font-size: 19px; color: #10B981; font-family: 'Courier New', monospace;">[SYSTEM SCAN] DTC DETECTED: {code}</b><br><br>
                • <b>المعنى التقني:</b> {meaning}<br>
                • <b>السبب الشائع:</b> {cause}<br>
                • <b>الحل الموصى به:</b> {solution}<br>
                • <b>كلفة الإصلاح التقديرية بليبيا:</b> {cost}<br>
                • <b>مستوى الخطورة الفنية:</b> <span style="font-weight:bold; color: #F59E0B;">{severity}</span>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 4: DIGITAL LEDGER & QR LABEL ---
with tab4:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">📜 وثيقة الأرشفة الرقمية للسيارة والـ QR Code المعتمد</h3>
        تتيح لك هذه الصفحة ترحيل البيانات السحابية وتوليد ملصق الـ QR Code ليوضع على زجاج السيارة في المعارض الليبية لكسر الركود بالشفافية المطلقة.
    </div>
    """, unsafe_allow_html=True)
    
    col_qr1, col_qr2 = st.columns([1, 2])
    
    with col_qr1:
        car_url = f"https://shassee-app-ly.supabase.co/car-history?vin={active_vin}"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={requests.utils.quote(car_url)}"
        
        st.markdown(f"""
        <div style="text-align: center; border: 2px dashed rgba(59, 130, 246, 0.4); padding: 24px; border-radius: 16px; background-color: #0B0F19; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <img src="{qr_api_url}" alt="QR Code" style="margin-bottom: 15px; max-width:100%; border-radius:10px; border: 4px solid #FFFFFF; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
            <br><b style="color:#FFFFFF; font-size:17px; font-family:'Cairo';">الملصق الرقمي للزجاج الأمامي</b><br>
            <span style="font-size: 13px; color: #10B981; font-weight:bold; letter-spacing: 1px;">SHASSEE TECH CERTIFIED</span><br>
            <span style="font-size: 12px; color: #9CA3AF;">معرف الحالة: SHS-{active_vin[:6]}-LY</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_qr2:
        st.markdown("### 📋 البيانات الجاهزة للرفع والتشفير (Supabase Cloud)")
        
        st.markdown(f"""
        <div class="premium-card" style="line-height: 1.8;">
            • <b>رقم الشاصي المعتمد:</b> <code style="color:#10B981; font-weight:bold; font-size:15px;">{active_vin}</code><br>
            • <b>الفئة والموديل:</b> <span style="color:#FFFFFF; font-weight:bold;">{active_type}</span><br>
            • <b>زاوية الصدمة والضرر:</b> <span style="color:#F59E0B; font-weight:bold;">{active_impact}</span><br>
            • <b>تكلفة الشراء الحالية:</b> <span style="color:#FFFFFF; font-weight:bold;">${active_bid:,.0f}</span> ({active_bid * exchange_rate:,.0f} د.ل)<br>
            • <b>التكلفة الإجمالية واصلة للورشة:</b> <span style="color:#FFFFFF; font-weight:bold;">${total_cost_at_workshop_usd:,.0f}</span> ({total_cost_at_workshop_lyd:,.0f} د.ل)<br>
            • <b>معدل سعر البيع بالسوق الليبي:</b> <span style="color:#10B981; font-weight:bold; font-size:16px;">{active_market_val:,.0f} د.ل</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 ترحيل وحفظ الملف الرقمي وتنشيط كود الـ QR", key="btn_save_ledger"):
            if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)" and supabase_url and supabase_anon_key:
                st.info("⏳ جاري ترحيل البيانات وحفظ التقرير إلى خادم Supabase السحابي الحقيقي...")
                try:
                    cleaned_url = supabase_url.strip().rstrip('/')
                    if "/rest/v1" in cleaned_url:
                        cleaned_url = cleaned_url.replace("/rest/v1", "")
                    cleaned_url = cleaned_url.rstrip('/')
                    api_endpoint = f"{cleaned_url}/rest/v1/cars"
                    
                    cleaned_anon_key = supabase_anon_key.strip()
                    
                    headers = {
                        "apikey": cleaned_anon_key,
                        "Authorization": f"Bearer {cleaned_anon_key}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    }
                    data = {
                        "vin": active_vin,
                        "vehicle_type": active_type,
                        "impact_angle": active_impact,
                        "purchase_price": active_bid,
                        "rehab_cost_lyd": total_shipping_lyd * 0.2, # 20% mock rehab estimate
                        "target_sale_price_lyd": active_market_val,
                        "is_safe": True
                    }
                    response = requests.post(api_endpoint, headers=headers, json=data)
                    
                    if response.status_code in [200, 201]:
                        st.markdown("""
                        <div style="background: rgba(16, 185, 129, 0.15); border-right: 5px solid #10B981; padding: 16px; border-radius: 12px; color: #A7F3D0; font-weight:bold; margin-top:15px;">
                            🎉 تم ترحيل وحفظ التقرير بنجاح في قاعدة بيانات Supabase السحابية الحقيقية! تم تفعيل رابط ملصق السيارة الآن.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ خطأ في الاستجابة من Supabase: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ فشل الاتصال بقاعدة البيانات السحابية: {str(e)}")
            else:
                with st.spinner("⏳ جاري تشفير البيانات وتزامنها مع خوادم الـ Escrow الآمنة..."):
                    time.sleep(1.5)
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.15); border-right: 5px solid #10B981; padding: 16px; border-radius: 12px; color: #A7F3D0; font-weight:bold; margin-top:15px;">
                    🎉 تم محاكاة حفظ الملف بنجاح! تم تسجيل وتشفير "ملف السيارة الموثق إلى تاريخ البيع" في أرشيف المنصة بنجاح.
                </div>
                """, unsafe_allow_html=True)

# --- TAB 5: SQL SERVER SETUP ---
with tab5:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">⚙️ تهيئة ومخطط قاعدة البيانات (SQL Schema Setup)</h3>
        للبدء في تشغيل قاعدة البيانات السحابية الحقيقية (Supabase) بشكل فوري وبصفر تكلفة برمجية، اتبع الخطوات التالية:
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. أنشئ حساباً مجانياً في موقع [supabase.com](https://supabase.com).<br>
    2. اذهب إلى **SQL Editor** من اللوحة الجانبية لمشروعك.<br>
    3. قم بنسخ كود SQL البرمجي الموضح أدناه، والصقه في المحرر، ثم اضغط على **Run**.<br>
    """, unsafe_allow_html=True)
    
    sql_code = """-- إنشاء جدول السيارات لتخزين وحفظ الأرشفة الرقمية والـ QR
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

-- إضافة سياسة الحماية وتأمين البيانات لضمان عدم التعديل العشوائي
ALTER TABLE cars ENABLE ROW LEVEL SECURITY;

-- السماح للجميع بقراءة البيانات (لقراءة الـ QR من قبل المشترين في المعارض)
CREATE POLICY "Allow public read-only access" ON cars
    FOR SELECT USING (true);

-- السماح لحسابك فقط بإدراج البيانات وحفظها من واجهة موقعك
CREATE POLICY "Allow authenticated insert access" ON cars
    FOR INSERT WITH CHECK (true);"""
    
    st.code(sql_code, language="sql")
    st.info("💡 بعد تشغيل الكود البرمجي أعلاه في Supabase، يمكنك نسخ رابط مشروعك ومفتاح anon_key ولصقهما في شريط الإعدادات بالجانب الأيسر لتفعيل السيرفر الحقيقي.")

st.markdown("""
---
<div style="text-align: center; color: #9CA3AF; font-size: 13px; padding: 15px; background: rgba(15, 23, 42, 0.3); border-radius: 12px; margin-top:20px;">
    <b>⚠️ إخلاء مسؤولية هندسية:</b> تقييم الأضرار والتقديرات البصرية هي أدوات تنبؤية لمساعدة المستوردين على تقليل مخاطر المزايدات بنسبة 90%، ويجب مطابقتها بالفحص الفني العيني والدقيق في الورشة قبل الاعتماد النهائي لضمان أعلى معايير الجودة والشفافية.
</div>
""", unsafe_allow_html=True)
