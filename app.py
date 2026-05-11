import streamlit as st
import joblib
import pandas as pd
import os
import hashlib
import base64
import random
import string
import smtplib
from email.message import EmailMessage
from datetime import datetime

# =========================
# Page Settings
# =========================
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide"
)

# =========================
# Email Settings
# =========================
SENDER_EMAIL = "osama715008285@gmail.com"
SENDER_APP_PASSWORD = "your_app_password"

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fake_news_model.pkl")
USERS_FILE = os.path.join(BASE_DIR, "users_data.csv")
BG_IMAGE = os.path.join(BASE_DIR, "news_bg.jpg")

# =========================
# Languages
# =========================
TEXT = {
    "English": {
        "system": "Fake News System",
        "home": "Home",
        "register_page": "Register Page",
        "login_page": "Login Page",
        "forgot_page": "Forgot Password",
        "detection_page": "Detection Page",
        "logout": "Logout",
        "project_info": "Project Information",
        "prepared_by": "Prepared By:",
        "name": "Osamah Musaed",
        "email_label": "Email:",
        "email_value": "osama715008285@gmail.com",
        "course_label": "Course:",
        "course_value": "Machine Learning Project",

        "title": "Fake News Detection System",
        "home_subtitle": "A Machine Learning project that detects whether news text is Fake or Real.",
        "home_subtitle2": "Please create an account first, then login to use the system.",
        "step1": "Step 1: Register your information including your email.",
        "step2": "Step 2: Login using your phone number and password.",
        "step3": "Step 3: If you forget your password, use Forgot Password.",

        "register": "Register",
        "register_desc": "Create a new account using your name, phone number, email, and password.",
        "create_account": "Create Account",

        "login": "Login",
        "login_desc": "Login using your phone number and password to access the system.",
        "login_now": "Login Now",

        "forgot": "Forgot Password",
        "forgot_desc": "Reset your password using your registered email address.",
        "reset_password": "Reset Password",

        "first_name": "First Name",
        "last_name": "Last Name",
        "age": "Age",
        "phone": "Phone Number",
        "user_email": "Email",
        "password": "Password",

        "register_title": "User Registration",
        "register_subtitle": "Create a new account to use the Fake News Detection System.",
        "login_title": "User Login",
        "login_subtitle": "Login using your phone number and password.",
        "forgot_title": "Forgot Password",
        "forgot_subtitle": "Enter your registered email. A new password will be sent to your email.",

        "enter_first": "Please enter your first name.",
        "enter_last": "Please enter your last name.",
        "enter_phone": "Please enter your phone number.",
        "enter_email": "Please enter your email.",
        "valid_email": "Please enter a valid email.",
        "enter_password": "Please enter your password.",
        "enter_phone_password": "Please enter phone number and password.",
        "phone_registered": "This phone number is already registered.",
        "email_registered": "This email is already registered.",
        "register_success": "Registration completed successfully.",
        "go_login": "Now go to Login page and enter your phone number and password.",
        "login_success": "Login successful.",
        "wrong_login": "Wrong phone number or password.",
        "no_users": "No users registered yet.",
        "email_not_found": "Email not found.",
        "new_password_sent": "A new password has been sent to your email.",
        "email_failed": "Password changed, but email sending failed: ",
        "forgot_button": "Forgot Password?",

        "welcome": "Welcome",
        "detect_subtitle": "Detect whether a news text is Fake or Real using Machine Learning.",
        "detect_info": "Enter the news text below, then click the prediction button.",
        "news_text": "Enter News Text:",
        "predict": "Predict News",
        "empty_news": "Please enter news text first.",
        "fake": "This news is Fake",
        "real": "This news is Real",
        "model_missing": "The model file fake_news_model.pkl was not found.",
        "model_hint": "Make sure fake_news_model.pkl is in the same folder as app.py.",
        "model_error": "Error while loading the model.",
        "prediction_error": "Prediction error.",
        "private": "© 2026 Fake News Detection System - Your data is private and protected.",
        "logged_in_as": "Logged in as "
    },

    "العربي": {
        "system": "نظام كشف الأخبار",
        "home": "الرئيسية",
        "register_page": "صفحة التسجيل",
        "login_page": "صفحة الدخول",
        "forgot_page": "نسيت الشفرة",
        "detection_page": "صفحة الفحص",
        "logout": "تسجيل خروج",
        "project_info": "معلومات المشروع",
        "prepared_by": "إعداد:",
        "name": "Osamah Musaed",
        "email_label": "الإيميل:",
        "email_value": "osama715008285@gmail.com",
        "course_label": "المادة:",
        "course_value": "Machine Learning Project",

        "title": "نظام كشف الأخبار المزيفة",
        "home_subtitle": "مشروع تعلم آلة يقوم بكشف هل الخبر مزيف أو حقيقي.",
        "home_subtitle2": "قم بإنشاء حساب أولًا، ثم سجل الدخول لاستخدام النظام.",
        "step1": "الخطوة 1: سجل بياناتك مع الإيميل.",
        "step2": "الخطوة 2: ادخل برقم الجوال والشفرة.",
        "step3": "الخطوة 3: إذا نسيت الشفرة استخدم صفحة نسيت الشفرة.",

        "register": "تسجيل جديد",
        "register_desc": "أنشئ حسابًا جديدًا باستخدام الاسم، رقم الجوال، الإيميل، والشفرة.",
        "create_account": "إنشاء حساب",

        "login": "تسجيل الدخول",
        "login_desc": "ادخل باستخدام رقم الجوال والشفرة للوصول إلى النظام.",
        "login_now": "دخول الآن",

        "forgot": "نسيت الشفرة",
        "forgot_desc": "استعد الشفرة باستخدام الإيميل المسجل.",
        "reset_password": "استعادة الشفرة",

        "first_name": "الاسم",
        "last_name": "اللقب",
        "age": "العمر",
        "phone": "رقم الجوال",
        "user_email": "الإيميل",
        "password": "الشفرة",

        "register_title": "تسجيل مستخدم جديد",
        "register_subtitle": "أنشئ حسابًا جديدًا لاستخدام نظام كشف الأخبار المزيفة.",
        "login_title": "تسجيل الدخول",
        "login_subtitle": "ادخل باستخدام رقم الجوال والشفرة.",
        "forgot_title": "نسيت الشفرة",
        "forgot_subtitle": "أدخل الإيميل المسجل وسيتم إرسال شفرة جديدة إلى بريدك.",

        "enter_first": "أدخل الاسم.",
        "enter_last": "أدخل اللقب.",
        "enter_phone": "أدخل رقم الجوال.",
        "enter_email": "أدخل الإيميل.",
        "valid_email": "أدخل إيميل صحيح.",
        "enter_password": "أدخل الشفرة.",
        "enter_phone_password": "أدخل رقم الجوال والشفرة.",
        "phone_registered": "رقم الجوال مسجل من قبل.",
        "email_registered": "الإيميل مسجل من قبل.",
        "register_success": "تم إنشاء الحساب بنجاح.",
        "go_login": "انتقل الآن إلى صفحة تسجيل الدخول وأدخل رقم الجوال والشفرة.",
        "login_success": "تم تسجيل الدخول بنجاح.",
        "wrong_login": "رقم الجوال أو الشفرة غير صحيحة.",
        "no_users": "لا يوجد مستخدمون مسجلون حتى الآن.",
        "email_not_found": "الإيميل غير موجود.",
        "new_password_sent": "تم إرسال شفرة جديدة إلى الإيميل.",
        "email_failed": "تم تغيير الشفرة، لكن فشل إرسال الإيميل: ",
        "forgot_button": "نسيت الشفرة؟",

        "welcome": "مرحبًا",
        "detect_subtitle": "اكتشف هل نص الخبر مزيف أو حقيقي باستخدام تعلم الآلة.",
        "detect_info": "أدخل نص الخبر بالأسفل ثم اضغط زر الفحص.",
        "news_text": "أدخل نص الخبر:",
        "predict": "فحص الخبر",
        "empty_news": "يرجى إدخال نص الخبر أولًا.",
        "fake": "هذا الخبر مزيف",
        "real": "هذا الخبر حقيقي",
        "model_missing": "ملف الموديل fake_news_model.pkl غير موجود.",
        "model_hint": "تأكد أن ملف fake_news_model.pkl موجود في نفس مجلد app.py.",
        "model_error": "حدث خطأ أثناء تحميل الموديل.",
        "prediction_error": "حدث خطأ أثناء التنبؤ.",
        "private": "© 2026 نظام كشف الأخبار المزيفة - بيانات المستخدمين خاصة ومحمية.",
        "logged_in_as": "تم الدخول باسم "
    },

    "Türkçe": {
        "system": "Sahte Haber Sistemi",
        "home": "Ana Sayfa",
        "register_page": "Kayıt Sayfası",
        "login_page": "Giriş Sayfası",
        "forgot_page": "Şifremi Unuttum",
        "detection_page": "Analiz Sayfası",
        "logout": "Çıkış Yap",
        "project_info": "Proje Bilgileri",
        "prepared_by": "Hazırlayan:",
        "name": "Osamah Musaed",
        "email_label": "E-posta:",
        "email_value": "osama715008285@gmail.com",
        "course_label": "Ders:",
        "course_value": "Machine Learning Project",

        "title": "Sahte Haber Tespit Sistemi",
        "home_subtitle": "Haber metninin sahte mi gerçek mi olduğunu tespit eden bir Makine Öğrenmesi projesi.",
        "home_subtitle2": "Sistemi kullanmak için önce hesap oluşturun, sonra giriş yapın.",
        "step1": "Adım 1: E-posta dahil bilgilerinizi kaydedin.",
        "step2": "Adım 2: Telefon numarası ve şifre ile giriş yapın.",
        "step3": "Adım 3: Şifrenizi unutursanız Şifremi Unuttum sayfasını kullanın.",

        "register": "Kayıt Ol",
        "register_desc": "Ad, telefon numarası, e-posta ve şifre ile yeni hesap oluşturun.",
        "create_account": "Hesap Oluştur",

        "login": "Giriş Yap",
        "login_desc": "Sisteme erişmek için telefon numarası ve şifre ile giriş yapın.",
        "login_now": "Giriş Yap",

        "forgot": "Şifremi Unuttum",
        "forgot_desc": "Kayıtlı e-posta adresinizi kullanarak şifrenizi sıfırlayın.",
        "reset_password": "Şifreyi Sıfırla",

        "first_name": "Ad",
        "last_name": "Soyad",
        "age": "Yaş",
        "phone": "Telefon Numarası",
        "user_email": "E-posta",
        "password": "Şifre",

        "register_title": "Kullanıcı Kaydı",
        "register_subtitle": "Sahte Haber Tespit Sistemini kullanmak için yeni hesap oluşturun.",
        "login_title": "Kullanıcı Girişi",
        "login_subtitle": "Telefon numaranız ve şifreniz ile giriş yapın.",
        "forgot_title": "Şifremi Unuttum",
        "forgot_subtitle": "Kayıtlı e-postanızı girin. Yeni şifre e-postanıza gönderilecektir.",

        "enter_first": "Lütfen adınızı girin.",
        "enter_last": "Lütfen soyadınızı girin.",
        "enter_phone": "Lütfen telefon numaranızı girin.",
        "enter_email": "Lütfen e-posta adresinizi girin.",
        "valid_email": "Lütfen geçerli bir e-posta adresi girin.",
        "enter_password": "Lütfen şifrenizi girin.",
        "enter_phone_password": "Lütfen telefon numarası ve şifre girin.",
        "phone_registered": "Bu telefon numarası zaten kayıtlı.",
        "email_registered": "Bu e-posta zaten kayıtlı.",
        "register_success": "Kayıt başarıyla tamamlandı.",
        "go_login": "Şimdi giriş sayfasına gidip telefon numaranız ve şifreniz ile giriş yapın.",
        "login_success": "Giriş başarılı.",
        "wrong_login": "Telefon numarası veya şifre hatalı.",
        "no_users": "Henüz kayıtlı kullanıcı yok.",
        "email_not_found": "E-posta bulunamadı.",
        "new_password_sent": "Yeni şifre e-postanıza gönderildi.",
        "email_failed": "Şifre değiştirildi, ancak e-posta gönderilemedi: ",
        "forgot_button": "Şifremi unuttum?",

        "welcome": "Hoş geldiniz",
        "detect_subtitle": "Haber metninin sahte mi gerçek mi olduğunu Makine Öğrenmesi ile tespit edin.",
        "detect_info": "Aşağıya haber metnini girin ve analiz butonuna tıklayın.",
        "news_text": "Haber Metnini Girin:",
        "predict": "Haberi Analiz Et",
        "empty_news": "Lütfen önce haber metnini girin.",
        "fake": "Bu haber sahtedir",
        "real": "Bu haber gerçektir",
        "model_missing": "fake_news_model.pkl model dosyası bulunamadı.",
        "model_hint": "fake_news_model.pkl dosyasının app.py ile aynı klasörde olduğundan emin olun.",
        "model_error": "Model yüklenirken hata oluştu.",
        "prediction_error": "Tahmin sırasında hata oluştu.",
        "private": "© 2026 Sahte Haber Tespit Sistemi - Kullanıcı verileri özel ve korunmaktadır.",
        "logged_in_as": "Giriş yapan kullanıcı: "
    }
}

LANGUAGES = ["English", "العربي", "Türkçe"]

# =========================
# Helper Functions
# =========================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_new_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def load_users():
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE)

        if "Email" not in df.columns:
            df["Email"] = ""

        return df

    return pd.DataFrame(columns=[
        "First Name",
        "Last Name",
        "Age",
        "Phone Number",
        "Email",
        "Password",
        "Registration Time"
    ])


def save_users(df):
    df.to_csv(USERS_FILE, index=False)


def save_user(first_name, last_name, age, phone, email, password, t):
    df = load_users()

    phone = phone.strip()
    email = email.strip().lower()

    if not df.empty and phone in df["Phone Number"].astype(str).values:
        return False, t["phone_registered"]

    if not df.empty and email in df["Email"].astype(str).str.lower().values:
        return False, t["email_registered"]

    user_data = {
        "First Name": first_name.strip(),
        "Last Name": last_name.strip(),
        "Age": age,
        "Phone Number": phone,
        "Email": email,
        "Password": hash_password(password),
        "Registration Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    save_users(df)

    return True, t["register_success"]


def login_user(phone, password, t):
    df = load_users()

    if df.empty:
        return False, t["no_users"], ""

    phone = phone.strip()
    hashed_password = hash_password(password)

    user = df[
        (df["Phone Number"].astype(str) == phone) &
        (df["Password"].astype(str) == hashed_password)
    ]

    if user.empty:
        return False, t["wrong_login"], ""

    first_name = str(user.iloc[0]["First Name"])
    return True, t["login_success"], first_name


def send_password_email(receiver_email, new_password):
    try:
        if SENDER_APP_PASSWORD == "your_app_password":
            return False, "You must add Gmail App Password first."

        msg = EmailMessage()
        msg["Subject"] = "Fake News Detection System - New Password"
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        msg.set_content(
            "Hello,\n\n"
            "Your new password for Fake News Detection System is:\n\n"
            + new_password +
            "\n\nPlease login using this new password.\n\n"
            "Regards,\nFake News Detection System"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            smtp.send_message(msg)

        return True, "Email sent successfully."

    except Exception as e:
        return False, str(e)


def reset_password_by_email(email, t):
    df = load_users()

    if df.empty:
        return False, t["no_users"]

    email = email.strip().lower()
    user_index = df[df["Email"].astype(str).str.lower() == email].index

    if len(user_index) == 0:
        return False, t["email_not_found"]

    new_password = generate_new_password()
    df.loc[user_index[0], "Password"] = hash_password(new_password)
    save_users(df)

    sent, message = send_password_email(email, new_password)

    if sent:
        return True, t["new_password_sent"]
    else:
        return False, t["email_failed"] + message


# =========================
# Session State
# =========================
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

if "language" not in st.session_state:
    st.session_state["language"] = "English"

if st.session_state["language"] not in LANGUAGES:
    st.session_state["language"] = "English"

# =========================
# Background
# =========================
bg_base64 = get_base64_image(BG_IMAGE)

if bg_base64:
    page_bg = """
    <style>
    .stApp {
        background-image:
            linear-gradient(rgba(5, 20, 45, 0.55), rgba(5, 20, 45, 0.55)),
            url("data:image/jpg;base64,""" + bg_base64 + """");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """
else:
    page_bg = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b3d91, #b8d2f0);
    }
    </style>
    """

st.markdown(page_bg, unsafe_allow_html=True)

# =========================
# CSS Design
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 25px;
    max-width: 1180px;
}

header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071f4f, #063b8c);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: white !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: white !important;
    color: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
}

div[data-testid="stSelectbox"] {
    background: rgba(255,255,255,0.95);
    border-radius: 14px;
    padding: 4px 8px;
}

.stButton button {
    background-color: #0b3d91 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 8px 14px !important;
    font-weight: bold !important;
    font-size: 13px !important;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.16);
}

.stButton button:hover {
    background-color: #06245c !important;
    color: white !important;
}

.page-card {
    background: rgba(255, 255, 255, 0.96);
    padding: 34px 34px;
    border-radius: 24px;
    box-shadow: 0px 12px 35px rgba(0,0,0,0.28);
    margin-top: 5px;
    margin-bottom: 20px;
}

.page-title {
    text-align: center;
    color: #0b3d91;
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 14px;
}

.page-subtitle {
    text-align: center;
    color: #1f2937;
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 20px;
}

.info-box {
    background-color: #e8f1ff;
    color: #1f2937;
    padding: 18px;
    border-radius: 16px;
    border-left: 7px solid #0b3d91;
    font-size: 16px;
    line-height: 1.8;
    margin-top: 15px;
}

.home-card {
    background: rgba(255, 255, 255, 0.97);
    padding: 14px 14px;
    border-radius: 18px;
    box-shadow: 0px 7px 18px rgba(0,0,0,0.20);
    text-align: center;
    width: 210px;
    height: 210px;
    margin: 12px auto 0 auto;
    border-top: 5px solid #0b3d91;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.home-card-green {
    border-top: 5px solid #16a34a;
}
.home-card-orange {
    border-top: 5px solid #f59e0b;
}
.home-icon {
    font-size: 34px;
    margin-bottom: 6px;
}
.home-title {
    color: #0b3d91;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 6px;
}
.home-text {
    color: #1f2937;
    font-size: 12px;
    line-height: 1.5;
    min-height: 50px;
    margin-bottom: 4px;
    text-align: center;
}

.stAlert p {
    color: #111827 !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Top Right Language Selector
# =========================
top_left, top_right = st.columns([8, 2])

with top_right:
    language = st.selectbox(
        "🌐",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state["language"]),
        label_visibility="collapsed"
    )

st.session_state["language"] = language
t = TEXT[language]

# =========================
# Sidebar
# =========================
st.sidebar.markdown("## 📰 Fake News<br>System", unsafe_allow_html=True)
st.sidebar.markdown("---")

if not st.session_state["logged_in"]:
    if st.sidebar.button("🏠 " + t["home"], use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()

    if st.sidebar.button("📝 " + t["register_page"], use_container_width=True):
        st.session_state["page"] = "register"
        st.rerun()

    if st.sidebar.button("🔐 " + t["login_page"], use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()

    if st.sidebar.button("🔑 " + t["forgot_page"], use_container_width=True):
        st.session_state["page"] = "forgot"
        st.rerun()
else:
    st.sidebar.success(t["logged_in_as"] + st.session_state["user_name"])

    if st.sidebar.button("🏠 " + t["home"], use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()

    if st.sidebar.button("📰 " + t["detection_page"], use_container_width=True):
        st.session_state["page"] = "app"
        st.rerun()

    if st.sidebar.button("🚪 " + t["logout"], use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_name"] = ""
        st.session_state["page"] = "login"
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ " + t["project_info"])
st.sidebar.write("👤 **" + t["prepared_by"] + "**")
st.sidebar.write(t["name"])
st.sidebar.write("✉️ **" + t["email_label"] + "**")
st.sidebar.write(t["email_value"])
st.sidebar.write("📖 **" + t["course_label"] + "**")
st.sidebar.write(t["course_value"])

# =========================
# Home Page
# =========================
if st.session_state["page"] == "home":
    st.markdown("""
    <div class="page-card">
        <div class="page-title">📰 """ + t["title"] + """</div>
        <div class="page-subtitle">
            """ + t["home_subtitle"] + """
            <br>
            """ + t["home_subtitle2"] + """
        </div>
        <div class="info-box">
            👤 <b>""" + t["step1"] + """</b><br>
            🔐 <b>""" + t["step2"] + """</b><br>
            🔑 <b>""" + t["step3"] + """</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, col1, col2, col3, right = st.columns([0.8, 1, 1, 1, 0.8], gap="large")

    with col1:
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">📝</div>
            <div class="home-title">""" + t["register"] + """</div>
            <div class="home-text">""" + t["register_desc"] + """</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📝 " + t["create_account"], use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="home-card home-card-green">
            <div class="home-icon">🔐</div>
            <div class="home-title">""" + t["login"] + """</div>
            <div class="home-text">""" + t["login_desc"] + """</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔐 " + t["login_now"], use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="home-card home-card-orange">
            <div class="home-icon">🔑</div>
            <div class="home-title">""" + t["forgot"] + """</div>
            <div class="home-text">""" + t["forgot_desc"] + """</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔑 " + t["reset_password"], use_container_width=True):
            st.session_state["page"] = "forgot"
            st.rerun()

# =========================
# Register Page
# =========================
elif st.session_state["page"] == "register":
    st.markdown("""
    <div class="page-card">
        <div class="page-title">📝 """ + t["register_title"] + """</div>
        <div class="page-subtitle">""" + t["register_subtitle"] + """</div>
    </div>
    """, unsafe_allow_html=True)

    first_name = st.text_input(t["first_name"])
    last_name = st.text_input(t["last_name"])
    age = st.number_input(t["age"], min_value=1, max_value=100, value=16, step=1)
    phone = st.text_input(t["phone"])
    email = st.text_input(t["user_email"])
    password = st.text_input(t["password"], type="password")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        create_btn = st.button("📝 " + t["create_account"], use_container_width=True)

    with col_b:
        if st.button("🔐 " + t["login_now"], use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    with col_c:
        if st.button("🏠 " + t["home"], use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    if create_btn:
        if first_name.strip() == "":
            st.error("❌ " + t["enter_first"])
            st.stop()

        if last_name.strip() == "":
            st.error("❌ " + t["enter_last"])
            st.stop()

        if phone.strip() == "":
            st.error("❌ " + t["enter_phone"])
            st.stop()

        if email.strip() == "":
            st.error("❌ " + t["enter_email"])
            st.stop()

        if "@" not in email or "." not in email:
            st.error("❌ " + t["valid_email"])
            st.stop()

        if password.strip() == "":
            st.error("❌ " + t["enter_password"])
            st.stop()

        success, message = save_user(first_name, last_name, age, phone, email, password, t)

        if success:
            st.success("✅ " + message)
            st.info(t["go_login"])
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error("❌ " + message)

# =========================
# Login Page
# =========================
elif st.session_state["page"] == "login":
    st.markdown("""
    <div class="page-card">
        <div class="page-title">🔐 """ + t["login_title"] + """</div>
        <div class="page-subtitle">""" + t["login_subtitle"] + """</div>
    </div>
    """, unsafe_allow_html=True)

    login_phone = st.text_input(t["phone"])
    login_password = st.text_input(t["password"], type="password")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        login_btn = st.button("🔐 " + t["login_now"], use_container_width=True)

    with col_b:
        if st.button("🔑 " + t["forgot_button"], use_container_width=True):
            st.session_state["page"] = "forgot"
            st.rerun()

    with col_c:
        if st.button("🏠 " + t["home"], use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    if login_btn:
        if login_phone.strip() == "" or login_password.strip() == "":
            st.error("❌ " + t["enter_phone_password"])
            st.stop()

        success, message, user_name = login_user(login_phone, login_password, t)

        if success:
            st.session_state["logged_in"] = True
            st.session_state["user_name"] = user_name
            st.session_state["page"] = "app"
            st.success("✅ " + message)
            st.rerun()
        else:
            st.error("❌ " + message)

# =========================
# Forgot Password Page
# =========================
elif st.session_state["page"] == "forgot":
    st.markdown("""
    <div class="page-card">
        <div class="page-title">🔑 """ + t["forgot_title"] + """</div>
        <div class="page-subtitle">""" + t["forgot_subtitle"] + """</div>
    </div>
    """, unsafe_allow_html=True)

    reset_email = st.text_input(t["user_email"])

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        reset_btn = st.button("🔑 " + t["reset_password"], use_container_width=True)

    with col_b:
        if st.button("🔐 " + t["login_now"], use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    with col_c:
        if st.button("🏠 " + t["home"], use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    if reset_btn:
        if reset_email.strip() == "":
            st.error("❌ " + t["enter_email"])
            st.stop()

        success, message = reset_password_by_email(reset_email, t)

        if success:
            st.success("✅ " + message)
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error("❌ " + message)

# =========================
# Detection Page
# =========================
elif st.session_state["page"] == "app":
    if not st.session_state["logged_in"]:
        st.warning("⚠️ " + t["login_page"])
        st.session_state["page"] = "login"
        st.rerun()

    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        st.error("❌ " + t["model_missing"])
        st.info(t["model_hint"])
        st.stop()
    except Exception as e:
        st.error("❌ " + t["model_error"])
        st.write(e)
        st.stop()

    st.markdown("""
    <div class="page-card">
        <div class="page-title">📰 """ + t["title"] + """</div>
        <div class="page-subtitle">""" + t["detect_subtitle"] + """</div>
        <div class="info-box">""" + t["detect_info"] + """</div>
    </div>
    """, unsafe_allow_html=True)

    st.success(t["welcome"] + " " + st.session_state["user_name"] + " 👋")

    news_text = st.text_area(t["news_text"], height=220)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        predict_btn = st.button("🔍 " + t["predict"], use_container_width=True)

    with col_b:
        if st.button("🏠 " + t["home"], use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    with col_c:
        if st.button("🚪 " + t["logout"], use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user_name"] = ""
            st.session_state["page"] = "login"
            st.rerun()

    if predict_btn:
        if news_text.strip() == "":
            st.warning("⚠️ " + t["empty_news"])
        else:
            try:
                prediction = model.predict([news_text])

                if prediction[0] == "fake" or prediction[0] == 0:
                    st.error("🚨 " + t["fake"])
                else:
                    st.success("✅ " + t["real"])

            except Exception as e:
                st.error("❌ " + t["prediction_error"])
                st.write(e)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption(t["private"])