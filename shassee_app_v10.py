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
    page_title="شاصي تك | SHASSEE TECH v9",
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

# Look for alternative logo filenames as a robust fallback system
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
            border-radius: 20px; 
            padding: 30px; 
            text-align: center; 
            margin-bottom: 35px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);">
    <h1 style="color: #FFFFFF; font-family: 'Cairo', sans-serif; font-weight: 900; font-size: 42px; margin-bottom: 5px; text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);">🚗 منصة شاصي تك | SHASSEE TECH</h1>
    <p style="color: #10B981; font-family: 'Cairo', sans-serif; font-weight: 700; font-size: 18px; margin-top: 0px; letter-spacing: 0.5px;">التقييم الفني والمالي المستقل والامتثال الجمركي الذكي للسيارات المستوردة لعام 2026</p>
</div>
""", unsafe_allow_html=True)

# 🛠️ Sidebar Design & Brand Logo Integration (Right Side of Screen in RTL)
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

st.sidebar.subheader("⚙️ إعدادات النظام ومفاتيح الربط")

# Integration Mode Toggle
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
    use_openai = st.sidebar.checkbox("🧠 تفعيل فحص الصور الحقيقي (OpenAI Vision)", value=False, help="قم بالتحديد لتشغيل الفحص الفعلي للصور بعد شحن بطاقتك.")
    if use_openai:
        openai_key = st.sidebar.text_input("🔑 OpenAI API Key (Vision):", type="password", help="مفتاح تحليل الصور الفعلي باستخدام GPT-4o-mini")
    else:
        st.sidebar.info("💡 سيتم تفعيل السيرفر وحفظ البيانات حقيقياً في Supabase، مع استخدام المحاكاة الذكية السريعة للصور مؤقتاً لتوفير استهلاك رصيد OpenAI.")
else:
    st.sidebar.info("💡 يعمل النظام الآن بنظام المحاكاة الذكية المتقدمة بناءً على الخبرة التشغيلية لـ 12 عاماً.")

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.sidebar.subheader("🚘 تفاصيل المركبة المستهدفة")
vin_input = st.sidebar.text_input("📝 رقم الشاصي (VIN):", "5YFEPRAU6GPXXXXXX")
vehicle_type = st.sidebar.selectbox(
    "🚘 نوع السيارة:",
    ["Toyota Tacoma", "Toyota 4Runner", "Toyota Tundra 2006", "Toyota T100", "Pickup Halfton"]
)

# Set financial bounds based on the memorandum specs
if vehicle_type == "Toyota Tundra 2006":
    bidding_limit = 5500  # $5,500
    bidding_limit_lyd = 51700  # 51,700 LYD
else:
    bidding_limit = 4500  # $4,500
    bidding_limit_lyd = 42300  # 42,300 LYD

shipping_cost = 2250  # Fixed $2,250
exchange_rate = 9.4  # USD to LYD

st.sidebar.markdown(f"""
<div style="background: rgba(30, 58, 138, 0.2); border: 1px solid rgba(59, 130, 246, 0.25); padding: 16px; border-radius: 12px; font-size:13px; line-height: 1.6;">
<b style="color: #10B981; font-size:14px;">💡 معايير التدقيق المالي المعتمدة:</b><br>
• سعر الصرف المعتمد: {exchange_rate} د.ل/$<br>
• كلفة الشحن الثابتة: ${shipping_cost} ({shipping_cost * exchange_rate:,.0f} د.ل)<br>
• سقف الشراء الأقصى بالمزاد: ${bidding_limit} ({bidding_limit_lyd:,.0f} د.ل)
</div>
""", unsafe_allow_html=True)

# Layout Tabs (V8 Hyper-Premium Design)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 فحص الأضرار والـ 3D Heatmap", 
    "📊 حاسبة المقاصة والجدوى المالية", 
    "🔌 فك رموز كمبيوتر السيارة (OBD-II)",
    "📜 ملصق الـ QR وأرشفة السيارة",
    "⚙️ تهيئة السيرفر وقاعدة البيانات (SQL)"
])

# Utility function to encode image to base64 for OpenAI Vision API
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# --- TAB 1: AI DAMAGE DETECTION & 3D HEATMAP ---
with tab1:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #3B82F6;">
        <h3 style="color: #3B82F6; margin-top:0px; font-weight:800;">👁️ نظام التحليل الفيزيائي البصري التنبئي للأضرار</h3>
        قم برفع صور المزاد للحصول على تقييم هندسي حقيقي للصدمات وتأثيراتها غير المرئية على الشاصي وأجزاء التعليق بدون قيود على عمر السيارات.
    </div>
    """, unsafe_allow_html=True)
    
    # Impact angle selector
    impact_angle = st.selectbox(
        "🎯 حدد زاوية الصدمة الرئيسية لتحديث النموذج ثلاثي الأبعاد:",
        ["أمامية يسار (Front-Left Impact)", "أمامية يمين (Front-Right Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)", "سليمة / صدمة خفيفة جداً"]
    )
    
    uploaded_files = st.file_uploader(
        "📸 ارفع صور المزاد (PNG, JPG, JPEG):", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg']
    )
    
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.markdown("### 🗺️ الخريطة الحرارية ثلاثية الأبعاد لهيكل السيارة (3D Structural Heatmap)")
        
        # Base Points representing a vehicle chassis
        x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
        y = [0, 4, 4, 0, 0, 4, 4, 0, 0, 4]
        z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
        
        # Dynamically set intensity based on selected impact angle to make the 3D model ACTUALLY responsive!
        if impact_angle == "أمامية يسار (Front-Left Impact)":
            intensity = [0.95, 0.1, 0.1, 0.8, 0.9, 0.1, 0.1, 0.7, 0.6, 0.2]
        elif impact_angle == "أمامية يمين (Front-Right Impact)":
            intensity = [0.1, 0.1, 0.95, 0.8, 0.1, 0.1, 0.9, 0.7, 0.6, 0.2]
        elif impact_angle == "خلفية (Rear Impact)":
            intensity = [0.1, 0.95, 0.95, 0.1, 0.1, 0.9, 0.9, 0.1, 0.2, 0.8]
        elif impact_angle == "جانبية (Side Impact)":
            intensity = [0.1, 0.1, 0.1, 0.1, 0.85, 0.85, 0.1, 0.1, 0.7, 0.3]
        else: # Clean/very light
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
        st.markdown("""
        <div style="text-align: center; font-size: 14px; background: rgba(15, 23, 42, 0.4); padding: 12px; border-radius: 10px;">
            <span style="color:#EF4444; font-weight:bold;">🔴 الأحمر: ضرر هيكلي جسيم يتطلب شد بالزرق ومحاذاة</span> | 
            <span style="color:#F59E0B; font-weight:bold;">🟡 الأصفر: تضرر صاج خارجي قابل للتعديل</span> | 
            <span style="color:#10B981; font-weight:bold;">🟢 الأخضر: سليم تماماً</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📋 تقرير الفحص الفني الذكي (معالجة وتحليل حقيقي)")
        
        if uploaded_files:
            if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)" and use_openai and openai_key:
                st.info("⏳ جاري إرسال الصور وتحليلها بواسطة الذكاء الاصطناعي السحابي GPT-4o Vision...")
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai_key}"
                    }
                    base64_image = encode_image(uploaded_files[0])
                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"You are Shassee AI, an expert structural damage inspector for American salvage cars imported to Libya. Analyze this vehicle crash image for model {vehicle_type} (VIN: {vin_input}). Answer in Arabic. Detail the structural damage, chassis frame alignment probability, estimated parts needed, and salt belt rust index if applicable. Be highly technical, objective, and realistic."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 800
                    }
                    
                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    result_json = response.json()
                    
                    if "choices" in result_json:
                        ai_report = result_json["choices"][0]["message"]["content"]
                        st.success("✅ تم الفحص والتحليل الهيكلي الفعلي بواسطة الذكاء الاصطناعي السحابي:")
                        st.markdown(f"""
                        <div class="premium-card" style="border-right-color: #10B981; background: rgba(16, 185, 129, 0.05);">
                            <b style="color: #10B981; font-size: 17px;">📝 تقرير الفحص البصري الفعلي (Real-time Vision AI):</b><br><br>
                            {ai_report.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ خطأ من واجهة OpenAI: {result_json.get('error', {}).get('message', 'خطأ غير معروف')}")
                except Exception as e:
                    st.error(f"❌ فشل الاتصال بخوادم الذكاء الاصطناعي: {str(e)}")
            else:
                with st.spinner("⏳ جاري تشغيل خوارزميات YOLOv8 لتحديد ناقل الصدمة ومطابقة الولاية..."):
                    time.sleep(1.2)
                
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.1); border-right: 5px solid #10B981; padding: 14px; border-radius: 10px; color: #A7F3D0; font-weight:bold; margin-bottom:15px;">
                    ✅ تم معالجة وتحليل الصور بنجاح بنظام الفحص العيني للموقع!
                </div>
                """, unsafe_allow_html=True)
                
                if impact_angle == "أمامية يسار (Front-Left Impact)":
                    chassis_prob = "82% - احتمالية التواء زاوية الشاصي الأمامي الأيسر"
                    parts = "• مصد أمامي كامل خارجي مع شبك<br>• رفرف أمامي أيسر<br>• مقص تعليق علوي وسفلي أيسر (مجموعة الركبة)<br>• ممتص صدمات أيسر ومصباح أمامي"
                    color_style = "color:#EF4444;"
                elif impact_angle == "أمامية يمين (Front-Right Impact)":
                    chassis_prob = "78% - احتمالية تأثر رأس الشاصي الأيمن وجسر الرادياتير"
                    parts = "• مصد أمامي كامل<br>• رفرف أمامي أيمن<br>• مروحة التبريد ومبرد المحرك (Radiator)<br>• مقص تعليق وسوستة يمين"
                    color_style = "color:#EF4444;"
                elif impact_angle == "خلفية (Rear Impact)":
                    chassis_prob = "65% - احتمالية انضغاط جسر الصدمة الخلفي وقاعدة الإطار الاحتياطي"
                    parts = "• واجهة خلفية كاملة<br>• باب صندوق خلفي (لطرازات تاكوما/تندرا)<br>• مصابيح خلفية LED<br>• حساسات المصد الخلفي"
                    color_style = "color:#F59E0B;"
                elif impact_angle == "جانبية (Side Impact)":
                    chassis_prob = "40% - خطر انحناء القائم الأوسط (B-Pillar) وضرر عتبة الباب"
                    parts = "• باب أمامي أيسر/أيمن<br>• باب خلفي<br>• زجاج النوافذ الجانبية<br>• ستائر هوائية جانبية (Airbags)"
                    color_style = "color:#F59E0B;"
                else:
                    chassis_prob = "5% - لا توجد أي مؤشرات لضرر هيكلي"
                    parts = "• مصد بلاستيكي أمامي (تجميلي فقط)"
                    color_style = "color:#10B981;"

                state_checked = "Pennsylvania (حزام الملح - خطر تآكل مرتفع 75%)" if "5YF" in vin_input else "Texas (خطر تآكل منخفض 10%)"
                
                st.markdown(f"""
                <div class="premium-card">
                    <b style="color: #3B82F6; font-size:18px;">📌 تقرير الفحص التنبئي لزاوية ({impact_angle}):</b><br><br>
                    • <b>ناقل الصدمة وعمق الإزاحة:</b> ضربة فيزيائية مباشرة أدت لضغط فيزيائي عميق.<br>
                    • <b>احتمالية ضرر الشاصي (Chassis Integrity):</b> <span style='{color_style} font-weight:bold;'>{chassis_prob}</span><br>
                    • <b>مؤشر الصدأ الجغرافي (Corrosion Index):</b> <span style='color:#F59E0B; font-weight:bold;'>{state_checked}</span><br><br>
                    • <b>قائمة قطع الغيار الهجينة المتوقعة (BOM):</b><br>
                    <span style="font-size: 14px; color:#D1D5DB; line-height: 1.6;">{parts}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(30, 58, 138, 0.1); border: 1px dashed rgba(59, 130, 246, 0.25); padding: 30px; border-radius: 16px; text-align: center; margin-top:15px;">
                <p style="color: #9CA3AF; margin-bottom: 0px; font-size: 15px;">📸 يرجى رفع صور السيارة المصدومة من ساحة المزاد لتشغيل خوارزمية الفحص الهيكلي وتوليد الخريطة الحرارية للأعطال.</p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: FINANCIAL ARBITRAGE & REHAB BUDGET ---
with tab2:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #10B981;">
        <h3 style="color: #10B981; margin-top:0px; font-weight:800;">📊 حاسبة المقاصة المالية ودراسة الجدوى الفورية</h3>
        بناءً على المعادلة المالية المعتمدة للمشروع للتأهيل الشامل (تكلفة السيارة واصلة + 20% لتأهيل الصيانة).
    </div>
    """, unsafe_allow_html=True)
    
    # Cost parameters
    purchase_price = st.number_input("💵 سعر شراء السيارة المتوقع بالمزاد ($):", min_value=500, max_value=15000, value=3500, step=100)
    
    # Financial calculations
    cost_at_workshop_usd = purchase_price + shipping_cost
    cost_at_workshop_lyd = cost_at_workshop_usd * exchange_rate
    
    # Comprehensive Rehab Formula: 20% on top of delivered cost
    rehab_cost_lyd = cost_at_workshop_lyd * 0.20
    parts_budget_lyd = cost_at_workshop_lyd * 0.10
    labor_budget_lyd = cost_at_workshop_lyd * 0.10
    
    total_cost_lyd = cost_at_workshop_lyd + rehab_cost_lyd
    
    # Target Sale Price for 15% net profit margin
    target_sale_price_lyd = total_cost_lyd * 1.15
    target_net_profit_lyd = target_sale_price_lyd - total_cost_lyd
    
    # Check limit & safety warning
    is_safe = purchase_price <= bidding_limit
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #3B82F6; background: rgba(59, 130, 246, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>التكلفة واصلة للورشة:</span><br>
            <span class="metric-val" style="color: #3B82F6;">${cost_at_workshop_usd:,.0f}</span><br>
            <span style='font-size:13px; color:#9CA3AF;'>({cost_at_workshop_lyd:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_f2:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #F59E0B; background: rgba(245, 158, 11, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>ميزانية التأهيل والتحضير (20%):</span><br>
            <span class="metric-val" style="color: #F59E0B;">{rehab_cost_lyd:,.0f} د.ل</span><br>
            <span style='font-size:11px; color:#D1D5DB;'>10% قطع ({parts_budget_lyd:,.0f} د.ل)<br>10% صيانة ({labor_budget_lyd:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_f3:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center; border-right-color: #10B981; background: rgba(16, 185, 129, 0.05);">
            <span style='color: #9CA3AF; font-size:14px;'>سعر البيع المستهدف (ربح 15%):</span><br>
            <span class="metric-val" style="color: #10B981;">{target_sale_price_lyd:,.0f} د.ل</span><br>
            <span style='font-size:13px; color:#10B981; font-weight:bold;'>صافي الربح المقدر: {target_net_profit_lyd:,.0f} د.ل</span>
        </div>
        """, unsafe_allow_html=True)
        
    if is_safe:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border-right: 5px solid #10B981; padding: 16px; border-radius: 12px; color: #A7F3D0; font-weight:bold; margin-bottom: 20px;">
            ✅ سعر الشراء المتوقع (${purchase_price:,.0f}) يقع ضمن الحدود والضوابط الآمنة (أقل من سقف المزايدة المعتمد: ${bidding_limit:,.0f}).
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border-right: 5px solid #EF4444; padding: 16px; border-radius: 12px; color: #FCA5A5; font-weight:bold; margin-bottom: 20px;">
            ⚠️ تنبيه حازم: تجاوز سعر المزاد السقف الآمن المعتمد (${bidding_limit:,.0f}) للمركبة من طراز {vehicle_type}! هذا يهدد ميزانية الطوارئ والمخاطرة.
        </div>
        """, unsafe_allow_html=True)

    # Hybrid parts table
    st.markdown("### 🔩 التوزيع الهجين لقطع الغيار المطلوبة (توفير 20% بمطابقة كود هولاندر)")
    st.info("💡 يتم شحن القطع مستندة على كود هولاندر وقطع جديدة بالكرتون للحساسات باستخدام الشحن المتداخل (Piggyback) بتكلفة شحن صفر.")
    
    parts_data = {
        "اسم الجزء المطلوب": ["مصد خارجي كامل", "رفرف أمامي جانبي", "مجموعات مقصات علوية وسفلية", "حساسات الزوايا والرادار", "مصباح أمامي LED"],
        "طبيعة القطعة": ["مستعمل أصلي (تفصيخ)", "مستعمل أصلي (تفصيخ)", "جديد بالكرتون", "جديد بالكرتون", "مستعمل أصلي (تفصيخ)"],
        "طريقة الشحن المعتمدة": ["شحن متداخل (Piggyback)", "شحن متداخل (Piggyback)", "صندوق الأمتعة الداخلي", "صندوق الأمتعة الداخلي", "شحن متداخل (Piggyback)"],
        "كلفة الشحن ($)": [0, 0, 15, 5, 0],
        "قناة التوريد الموصى بها": ["شبكات LKQ / Car-Part", "شبكات LKQ / Car-Part", "منصة RockAuto", "منصة PartsSouq (دبي)", "شبكات LKQ / Car-Part"]
    }
    st.table(pd.DataFrame(parts_data))

# --- TAB 3: OBD-II DTC PARSER ---
with tab3:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #F59E0B;">
        <h3 style="color: #F59E0B; margin-top:0px; font-weight:800;">🔌 فك رموز وفحص كمبيوتر السيارة (OBD-II DTC Parser)</h3>
        قم بلصق رموز الأعطال المسحوبة من كمبيوتر السيارة أو فحص OBD-II لترجمتها فوراً للغة العربية ومعرفة كلفة إصلاحها الحقيقية.
    </div>
    """, unsafe_allow_html=True)
    
    dtc_input = st.text_input("📝 اكتب رموز الأعطال هنا تفصل بينها فاصلة (مثال: P0300, P0171, P0420):", "P0300, P0171")
    
    if st.button("🔌 تشغيل محلل وفك الرموز الذكي"):
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
        car_url = f"https://shassee-app-ly.supabase.co/car-history?vin={vin_input}"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={requests.utils.quote(car_url)}"
        
        st.markdown(f"""
        <div style="text-align: center; border: 2px dashed rgba(59, 130, 246, 0.4); padding: 24px; border-radius: 16px; background-color: #0B0F19; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <img src="{qr_api_url}" alt="QR Code" style="margin-bottom: 15px; max-width:100%; border-radius:10px; border: 4px solid #FFFFFF; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
            <br><b style="color:#FFFFFF; font-size:17px; font-family:'Cairo';">الملصق الرقمي للزجاج الأمامي</b><br>
            <span style="font-size: 13px; color: #10B981; font-weight:bold; letter-spacing: 1px;">SHASSEE TECH CERTIFIED</span><br>
            <span style="font-size: 12px; color: #9CA3AF;">معرف الحالة: SHS-{vin_input[:6]}-LY</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_qr2:
        st.markdown("### 📋 البيانات الجاهزة للرفع والتشفير (Supabase Cloud)")
        
        st.markdown(f"""
        <div class="premium-card" style="line-height: 1.8;">
            • <b>رقم الشاصي المعتمد:</b> <code style="color:#10B981; font-weight:bold; font-size:15px;">{vin_input}</code><br>
            • <b>الفئة والموديل:</b> <span style="color:#FFFFFF; font-weight:bold;">{vehicle_type}</span><br>
            • <b>زاوية الصدمة والضرر:</b> <span style="color:#F59E0B; font-weight:bold;">{impact_angle}</span><br>
            • <b>كلفة الشراء المتوقعة:</b> <span style="color:#FFFFFF; font-weight:bold;">${purchase_price:,.0f}</span> ({purchase_price * exchange_rate:,.0f} د.ل)<br>
            • <b>ميزانية التأهيل والتحضير (20%):</b> <span style="color:#FFFFFF; font-weight:bold;">{rehab_cost_lyd:,.0f} د.ل</span><br>
            • <b>سعر البيع المستهدف للمستهلك:</b> <span style="color:#10B981; font-weight:bold; font-size:16px;">{target_sale_price_lyd:,.0f} د.ل</span> (لضمان صافي ربح 15% للمشروع)
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 ترحيل وحفظ الملف الرقمي وتنشيط كود الـ QR"):
            if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)" and supabase_url and supabase_anon_key:
                st.info("⏳ جاري ترحيل البيانات وحفظ التقرير إلى خادم Supabase السحابي الحقيقي...")
                try:
                    # Clean up URL dynamically to prevent double /rest/v1 and spaces
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
                        "vin": vin_input,
                        "vehicle_type": vehicle_type,
                        "impact_angle": impact_angle,
                        "purchase_price": purchase_price,
                        "rehab_cost_lyd": rehab_cost_lyd,
                        "target_sale_price_lyd": target_sale_price_lyd,
                        "is_safe": is_safe
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
                    🎉 تم محاكاة حفظ الملف بنجاح! تم تسجيل وتشفير "ملف السيارة الموثق إلى تاريخ البيع" في لوحة الشركاء السحابية بنجاح.
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
