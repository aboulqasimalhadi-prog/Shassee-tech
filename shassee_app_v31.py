import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import json
import base64
import os
import re
import random
import hashlib
from PIL import Image
from io import BytesIO
import time

# ==============================================
# 1. إعدادات الصفحة (نفس السابق)
# ==============================================
st.set_page_config(page_title="شاصي تك | SHASSEE TECH v33", page_icon="⚙️", layout="wide")
# ... (ضع نفس الـ CSS السابق لتوفير المساحة، أو استخدمه من الكود السابق)

# ==============================================
# 2. دوال جلب البيانات (محسنة)
# ==============================================
def fetch_from_scrapingbee_premium(url, api_key):
    """جلب صفحة المزاد باستخدام إعدادات متقدمة"""
    if not api_key:
        return None
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
            return response.text
        else:
            st.warning(f"ScrapingBee error: {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"ScrapingBee exception: {e}")
        return None

def extract_real_data_from_html(html):
    """استخراج البيانات الحقيقية من HTML باستخدام JSON-LD و Open Graph"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    data = {
        "year": 2022,
        "make": "Toyota",
        "model": "Unknown",
        "vin": "",
        "location": "Unknown",
        "title": "Salvage Title",
        "current_bid": 3000,
        "images": []
    }
    # ... (نفس الكود السابق للاستخراج)
    # نعيد البيانات المستخرجة
    return data

def get_car_data_from_url(url):
    """الدالة الرئيسية لجلب البيانات الحقيقية"""
    clean_url = re.search(r'(https?://[^\s\)"\'<>]+)', url).group(1) if re.search(r'(https?://[^\s\)"\'<>]+)', url) else url
    platform = "Copart" if "copart" in clean_url.lower() else "IAAI"
    lot_id = re.search(r'/lot/(\d+)', clean_url)
    lot_id = lot_id.group(1) if lot_id else str(random.randint(1000000, 9999999))
    
    # جرب ScrapingBee إذا وجد مفتاح
    api_key = st.session_state.get("scrapingbee_key", "")
    if api_key:
        html = fetch_from_scrapingbee_premium(clean_url, api_key)
        if html:
            data = extract_real_data_from_html(html)
            data["id"] = f"LOT-{lot_id}"
            data["platform"] = platform
            data["url"] = clean_url
            data["scraped"] = True
            return data
    
    # فشل: استخدم المحاكاة الذكية
    return generate_simulated_data(clean_url, platform, lot_id)

def generate_simulated_data(url, platform, lot_id):
    """بيانات محاكاة (احتياطي)"""
    seed = int(hashlib.md5(lot_id.encode()).hexdigest(), 16) % 10000000
    r_gen = random.Random(seed)
    return {
        "id": f"LOT-{lot_id}",
        "vin": "".join(r_gen.choices("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789", k=17)),
        "make": "Toyota",
        "model": r_gen.choice(["Tacoma", "4Runner", "Tundra"]),
        "year": r_gen.choice([2020, 2021, 2022]),
        "platform": platform,
        "location": r_gen.choice(["Texas (Houston)", "California (Sacramento)"]),
        "title": r_gen.choice(["Salvage Title", "Clean Title"]),
        "current_bid": r_gen.choice([3200, 4500, 5800]),
        "images": [
            "https://images.unsplash.com/photo-1617469767053-d3b508a0d825?auto=format&fit=crop&q=80&w=600",
            "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=300"
        ],
        "scraped": False,
        "url": url
    }

# ==============================================
# 3. دوال تحليل الصور بالذكاء الاصطناعي
# ==============================================
def analyze_car_image_with_openai(image_url, api_key):
    """تحليل صورة السيارة باستخدام OpenAI Vision API"""
    if not api_key:
        return "يرجى تفعيل OpenAI Vision من الإعدادات."
    try:
        import openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "قم بتحليل هذه الصورة لسيارة متضررة. حدد المناطق المتضررة (مصد أمامي، رفرف، باب، إطار، إلخ) ووصف الضرر، واكتشاف الصدأ إن وجد. أعطِ قائمة بالقطع المتضررة مع تقدير لشدتها (بسيط، متوسط، شديد)."},
                        {"type": "image_url", "image_url": image_url}
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
# 4. قاعدة بيانات قطع الغيار (OEM)
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

def get_oem_parts(model, damage_description):
    """استخراج أرقام OEM بناءً على الموديل ووصف الضرر"""
    model_key = model.lower()
    if model_key not in OEM_DB:
        return []
    # بحث بسيط عن الكلمات المفتاحية في وصف الضرر
    found = []
    for part_name, oem_code in OEM_DB[model_key].items():
        if any(word in damage_description.lower() for word in part_name.split()):
            found.append({"part": part_name, "oem": oem_code})
    return found

# ==============================================
# 5. نموذج 3D تفاعلي مع تمييز الأضرار
# ==============================================
def create_3d_chassis_with_damage(damage_levels):
    """إنشاء نموذج 3D مع تلوين حسب شدة الضرر"""
    x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
    y = [0, 4, 4, 0, 0, 4, 4, 0, 0, 4]
    z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
    intensity = damage_levels  # قائمة من 10 قيم بين 0 و 1
    fig = go.Figure(data=[go.Mesh3d(
        x=x, y=y, z=z,
        intensity=intensity,
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
# 6. واجهة المستخدم (Tabs)
# ==============================================
# ... (نفس التبويبات السابقة مع تعديلات)
# سأكتب تبويباً جديداً للتحليل الذكي

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 بحث موحد", "📊 جدوى لوجستية", "🔌 OBD-II", "📜 QR", "⚙️ SQL", "🧠 تحليل ذكي (AI)"
])

with tab6:
    st.markdown("""
    <div class="premium-card" style="border-right-color: #8B5CF6;">
        <h3 style="color: #8B5CF6; margin-top:0px;">🧠 التحليل الذكي بالذكاء الاصطناعي</h3>
        قم برفع صور السيارة أو الصق رابط الصورة لتحليل الأضرار واكتشاف الصدأ وتحديد قطع الغيار بأرقامها المصنعية.
    </div>
    """, unsafe_allow_html=True)
    
    # اختيار طريقة التحليل
    analysis_method = st.radio("طريقة التحليل:", ["رفع صورة", "رابط صورة", "استخدام صور المزاد المسحوبة"])
    
    image_input = None
    if analysis_method == "رفع صورة":
        uploaded_file = st.file_uploader("اختر صورة السيارة", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_input = uploaded_file.read()
    elif analysis_method == "رابط صورة":
        image_url = st.text_input("ألصق رابط الصورة:", placeholder="https://example.com/car.jpg")
        if image_url:
            try:
                response = requests.get(image_url)
                image_input = response.content
            except:
                st.error("رابط غير صالح")
    else:
        # استخدام أول صورة من السيارة المختارة
        selected_lot = st.session_state.get("selected_lot", {})
        images = selected_lot.get("images", [])
        if images:
            try:
                response = requests.get(images[0])
                image_input = response.content
            except:
                st.warning("تعذر جلب الصورة من المزاد")
        else:
            st.info("لا توجد صور محفوظة للسيارة المختارة، اختر سيارة أولاً في تبويب البحث.")
    
    if image_input:
        # عرض الصورة
        st.image(image_input, caption="الصورة المختارة للتحليل", use_container_width=True)
        
        # أزرار التحليل
        col1, col2 = st.columns(2)
        with col1:
            analyze_btn = st.button("🔍 تحليل الصورة بالذكاء الاصطناعي", use_container_width=True)
        with col2:
            rust_btn = st.button("🦀 كشف الصدأ", use_container_width=True)
        
        if analyze_btn:
            with st.spinner("جاري تحليل الصورة..."):
                # تحويل الصورة إلى base64 لإرسالها إلى OpenAI
                img_b64 = base64.b64encode(image_input).decode()
                data_url = f"data:image/jpeg;base64,{img_b64}"
                openai_key = st.session_state.get("openai_key", "")
                if openai_key:
                    result = analyze_car_image_with_openai(data_url, openai_key)
                    st.markdown("### 📝 نتائج التحليل:")
                    st.write(result)
                    
                    # استخراج أرقام OEM
                    model = st.session_state.get("active_type", "Tacoma")
                    oem_parts = get_oem_parts(model, result)
                    if oem_parts:
                        st.markdown("### 🔩 قطع الغيار المتضررة (مع الأرقام المصنعية):")
                        for part in oem_parts:
                            st.markdown(f"- **{part['part']}**: `{part['oem']}`")
                    else:
                        st.info("لم يتم التعرف على قطع غيار محددة من هذا التحليل.")
                else:
                    st.warning("يرجى تفعيل مفتاح OpenAI من الإعدادات الجانبية.")
        
        if rust_btn:
            with st.spinner("جاري تحليل الصدأ..."):
                rust_percent = detect_rust_with_opencv(image_input)
                if rust_percent > 0:
                    st.metric("نسبة الصدأ المقدرة", f"{rust_percent:.1f}%")
                    if rust_percent > 10:
                        st.warning("⚠️ نسبة صدأ مرتفعة، يوصى بفحص دقيق.")
                    else:
                        st.success("✅ نسبة صدأ منخفضة، السيارة بحالة جيدة.")
                else:
                    st.info("لم يتمكن النظام من تقدير نسبة الصدأ (تأكد من وضوح الصورة).")

# ==============================================
# 7. تحديث الإعدادات الجانبية لإضافة مفاتيح OpenAI
# ==============================================
# (أضف في الشريط الجانبي)
st.sidebar.markdown("---")
openai_key = st.sidebar.text_input("🔑 مفتاح OpenAI (لتحليل الصور):", type="password", value=st.session_state.get("openai_key", ""))
st.session_state["openai_key"] = openai_key
if openai_key:
    st.sidebar.success("✅ تفعيل OpenAI Vision")

# ==============================================
# 8. عرض النموذج 3D مع الأضرار (في تبويب البحث)
# ==============================================
# (أضف في تبويب البحث بعد اختيار السيارة)
# يمكنك إضافة هذا القسم في تفاصيل السيارة المختارة:
with st.expander("🗺️ عرض الهيكل 3D مع تمييز الأضرار"):
    # افترض أن لدينا قائمة intensities (من 0 إلى 1) بناءً على تحليل الصور أو التخمين
    # هنا سنضع قيم افتراضية (يمكن تحديثها من تحليل الصور)
    intensities = [0.1, 0.9, 0.9, 0.1, 0.1, 0.9, 0.9, 0.1, 0.2, 0.8]  # مثال
    fig = create_3d_chassis_with_damage(intensities)
    st.plotly_chart(fig, use_container_width=True)
