import streamlit as st
import time

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم المتجاوب مع الهواتف
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة البث المباشر والماسنجر التفاعلي",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. إدارة الجلسات وقاعدة البيانات الحقيقية
# ---------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin2026", "name": "مدير النظام العام", "role": "أدمن"}
    }

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'global_feed' not in st.session_state:
    st.session_state.global_feed = [
        {"user": "مدير النظام العام", "action": "أنشأ الغرفة وبدأ البث الرئيسي", "time": "الآن"}
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"sender": "مدير النظام العام", "msg": "أهلاً بالجميع في استوديو البث الحي والدردشة المباشرة.", "time": "الآن"}
    ]

if 'active_users_list' not in st.session_state:
    st.session_state.active_users_list = ["مدير النظام العام"]

# ---------------------------------------------------------
# 3. تخصيص التصميم والأنماط (CSS) لمنع تداخل الحروف على الجوال
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');

    html, body, [class*="stApp"] {
        font-family: 'Tajawal', sans-serif !important;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        color: #f8fafc !important;
        direction: rtl !important;
        text-align: right !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }

    *, p, span, div, h1, h2, h3, h4, h5, h6, button, input, textarea {
        letter-spacing: normal !important;
        word-spacing: normal !important;
        writing-mode: horizontal-tb !important;
        box-sizing: border-box !important;
        -webkit-text-size-adjust: 100%;
    }

    .stMainBlockContainer {
        padding: 0.5rem !important;
        max-width: 100% !important;
    }

    .zoom-container {
        position: relative;
        background-color: #000000;
        border: 2px solid #3b82f6;
        border-radius: 14px;
        overflow: hidden;
        width: 100%;
        min-height: 340px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.25);
    }

    .pip-box {
        position: absolute;
        bottom: 12px;
        left: 12px;
        width: 110px;
        height: 80px;
        background: #1e293b;
        border: 2px solid #60a5fa;
        border-radius: 8px;
        z-index: 99;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        color: #93c5fd;
        text-align: center;
        box-shadow: 0 0 12px rgba(0,0,0,0.8);
    }

    .card-box {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .title-blue {
        color: #60a5fa;
        font-weight: 700;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. بوابات التسجيل والدخول
# ---------------------------------------------------------
if not st.session_state.current_user:
    st.markdown("<h2 class='title-blue' style='text-align:center; margin-top:20px;'>بوابة التسجيل والدخول إلى منصة البث</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.85rem; color:#94a3b8;'>قم بالتسجيل أو الدخول للانضمام للغرفة واستخدام البث والمراسلة:</p>", unsafe_allow_html=True)
    
    col_auth1, col_auth2, col_auth3 = st.columns([1, 3, 1])
    with col_auth2:
        auth_mode = st.radio("اختر العملية:", ["تسجيل دخول لحساب مسجل", "إنشاء حساب جديد"])
        
        if auth_mode == "إنشاء حساب جديد":
            new_user = st.text_input("اسم المستخدم الجديد:")
            new_pass = st.text_input("كلمة المرور:", type="password")
            role_choice = st.selectbox("نوع الحساب:", ["عضو / مشارك", "مدير النظام (Admin)"])
            
            if st.button("إتمام التسجيل والدخول فوراً", use_container_width=True):
                if new_user.strip() and new_pass.strip():
                    if new_user in st.session_state.users_db:
                        st.error("اسم المستخدم مسجل مسبقاً!")
                    else:
                        is_admin = "مدير" in role_choice
                        st.session_state.users_db[new_user] = {
                            "pass": new_pass, 
                            "name": new_user, 
                            "role": "أدمن" if is_admin else "عضو"
                        }
                        st.session_state.current_user = st.session_state.users_db[new_user]
                        if new_user not in st.session_state.active_users_list:
                            st.session_state.active_users_list.append(new_user)
                        st.session_state.global_feed.insert(0, {"user": new_user, "action": "انضم إلى الغرفة واستوديو البث", "time": "الآن"})
                        st.success("تم التسجيل والدخول بنجاح!")
                        st.rerun()
                else:
                    st.warning("يرجى ملء كافة الحقول.")
        else:
            login_user = st.text_input("اسم المستخدم:")
            login_pass = st.text_input("كلمة المرور:", type="password")
            
            if st.button("تسجيل الدخول", use_container_width=True):
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user]["pass"] == login_pass:
                    st.session_state.current_user = st.session_state.users_db[login_user]
                    if login_user not in st.session_state.active_users_list:
                        st.session_state.active_users_list.append(login_user)
                    st.session_state.global_feed.insert(0, {"user": login_user, "action": "سجل دخوله وانضم إلى استوديو البث", "time": "الآن"})
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة.")
    st.stop()

# ---------------------------------------------------------
# 5. الشريط الجانبي ومعلومات المستخدم الحالي
# ---------------------------------------------------------
st.sidebar.markdown(f"<h4 class='title-blue'>مرحباً: {st.session_state.current_user['name']}</h4>", unsafe_allow_html=True)
st.sidebar.write(f"الصلاحية: **{st.session_state.current_user['role']}**")
st.sidebar.write(f"المستخدمون المتواجدون: **{len(st.session_state.active_users_list)}**")

if st.sidebar.button("🚪 تسجيل الخروج"):
    if st.session_state.current_user['name'] in st.session_state.active_users_list:
        st.session_state.active_users_list.remove(st.session_state.current_user['name'])
    st.session_state.current_user = None
    st.rerun()

st.markdown("<h2 class='title-blue' style='text-align:center; margin-bottom:5px;'>منصة استوديو البث المباشر والماسنجر التفاعلي</h2>", unsafe_allow_html=True)

# شريط التفاعلات والنشاط الحي
st.markdown(f"""
<div style='background: rgba(59,130,246,0.15); border: 1px solid #3b82f6; padding: 10px; border-radius: 10px; font-size: 11px; margin-bottom: 10px;'>
    <b>🔴 شريط النشاط الفوري:</b> {st.session_state.global_feed[0]['user']} ({st.session_state.global_feed[0]['action']})
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. التبويبات الرئيسية (البث والماسنجر والإدارة)
# ---------------------------------------------------------
tabs_list = [
    "📡 استوديو البث الحي (Zoom / Meet)",
    "💬 الماسنجر والدردشة الحية"
]

if st.session_state.current_user['role'] == "أدمن":
    tabs_list.append("🛡️ لوحة تحكم الأدمن")

main_tabs = st.tabs(tabs_list)

# ---------------------------------------------------------
# التبويب 1: استوديو البث الحي
# ---------------------------------------------------------
with main_tabs[0]:
    st.markdown("### 📡 استوديو البث المباشر والتفاعلي")
    st.markdown("<p style='font-size:0.8rem; color:#94a3b8;'>شاشة بث مرئي وصوتي مباشر تتيح لك مشاركة الفيديو والصوت مع جميع الحاضرين في الغرفة.</p>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns([2, 1])
    
    with col_b1:
        st.markdown("""
        <div class="zoom-container">
            <div style="text-align: center; color: #60a5fa;">
                <p style="font-size: 14px; font-weight: bold; margin-bottom: 5px;">غرفة البث المباشر نشطة</p>
                <span style="font-size: 10px; background: #ef4444; padding: 3px 10px; border-radius: 6px; color: white; font-weight: bold;">LIVE ON AIR</span>
            </div>
            <div class="pip-box">
                <span>صورة الشاشة المصغرة<br>(المتحدث النشط)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        start_broadcast = st.toggle("🔴 تفعيل الكاميرا والميكروفون للبث في الغرفة", value=False)
        if start_broadcast:
            st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": "بدأ البث المرئي والصوتي للغرفة", "time": "الآن"})
            cam_vid = st.camera_input("التقاط وبث الفيديو المباشر")
            mic_aud = st.audio_input("تسجيل وبث الصوت المباشر")
            if mic_aud:
                st.audio(mic_aud)
                st.success("تم بث التسجيل الصوتي للحاضرين!")
        else:
            st.info("⚪ البث متوقف. اضغط على المفتاح أعلاه لتشغيل الكاميرا والميكروفون فوراً.")

    with col_b2:
        st.markdown("#### 👥 المتصلون بالغرفة")
        active_html = "".join([f"<p style='font-size:12px; margin:5px 0;'>🟢 {usr}</p>" for usr in st.session_state.active_users_list])
        st.markdown(f"<div class='card-box'>{active_html}</div>", unsafe_allow_html=True)
        
        st.markdown("#### ✋ طلب مداخلة من الأدمن")
        call_req = st.text_input("اكتب طلب المداخلة هنا:")
        if st.button("إرسال طلب المداخلة", use_container_width=True):
            if call_req.strip():
                st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": f"طلب مداخلة: {call_req}", "time": "الآن"})
                st.success("تم إرسال طلب المداخلة للإدارة بنجاح!")

# ---------------------------------------------------------
# التبويب 2: الماسنجر والدردشة الحية
# ---------------------------------------------------------
with main_tabs[1]:
    st.markdown("### 💬 الماسنجر والدردشة المباشرة")
    st.markdown("<p style='font-size:0.8rem; color:#94a3b8;'>مراسلة كتابية مباشرة بين الأعضاء والمدراء في الغرفة.</p>", unsafe_allow_html=True)
    
    chat_container = st.container(height=320)
    with chat_container:
        for msg in st.session_state.chat_messages:
            st.markdown(f"""
            <div class='card-box'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#60a5fa;'>
                    <b>{msg['sender']}</b>
                    <span>{msg['time']}</span>
                </div>
                <p style='margin-top:5px; font-size:0.9rem;'>{msg['msg']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    col_m1, col_m2 = st.columns([4, 1])
    with col_m1:
        new_msg = st.text_input("اكتب رسالتك للجميع هنا...", key="chat_input_field")
    with col_m2:
        st.write("")
        if st.button("إرسال", use_container_width=True):
            if new_msg.strip():
                st.session_state.chat_messages.append({
                    "sender": st.session_state.current_user['name'],
                    "msg": new_msg,
                    "time": "الآن"
                })
                st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": "أرسل رسالة جديدة في الماسنجر", "time": "الآن"})
                st.rerun()

# ---------------------------------------------------------
# التبويب 3: لوحة تحكم الأدمن
# ---------------------------------------------------------
if len(main_tabs) > 2:
    with main_tabs[2]:
        st.markdown("### 🛡️ لوحة تحكم الأدمن")
        if st.session_state.current_user['role'] != "أدمن":
            st.warning("هذه اللوحة مخصصة لمدير النظام فقط.")
        else:
            st.success("مرحباً بك في لوحة تحكم الإدارة. يمكنك نشر تنبيهات وإعلانات عامة للحاضرين.")
            
            announcement_text = st.text_input("إرسال إعلان عام للمتواجدين:")
            if st.button("نشر الإعلان فوراً", use_container_width=True):
                if announcement_text.strip():
                    st.session_state.global_feed.insert(0, {"user": "المدير العام", "action": f"نشر إعلان: {announcement_text}", "time": "الآن"})
                    st.success("تم نشر الإعلان بنجاح!")

st.write("---")
st.markdown("<p style='text-align:center; color:#60a5fa; font-size:0.75rem;'>منصة استوديو البث الحي والدردشة © 2026</p>", unsafe_allow_html=True)
