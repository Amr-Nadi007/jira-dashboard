# Jira Cloud Dashboard

لوحة معلومات متقدمة لمراقبة Jira مع FastAPI + React + Vite + Tailwind + SQLite

## المتطلبات

- Docker و Docker Compose
- Python 3.9+
- Node.js 16+

## التثبيت والتشغيل السريع

### 1. استنساخ المستودع

```bash
git clone https://github.com/Amr-Nadi007/jira-dashboard.git
cd jira-dashboard
```

### 2. إعدادات البيئة

أنشئ ملف `.env` في جذر المشروع:

```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./data/database.db
```

### 3. تشغيل المشروع

```bash
docker-compose up -d
```

الخدمات المتاحة:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## المميزات الرئيسية

✅ **الاتصال المباشر بـ Jira Cloud** - عبر Email + API Token  
✅ **لوحة المعلومات الرئيسية** - عداد فوري لمصر ونيجيريا  
✅ **لوحة الإنتاج** - إحصائيات الوكلاء حسب اليوم  
✅ **التقارير المجدولة** - تقارير تلقائية صباحاً وليلاً  
✅ **صفحة الإدارة** - إدارة بيانات Jira والوكلاء النشطين  
✅ **واجهة استجابية** - تصميم حديث مع Tailwind CSS  
✅ **الرسوم البيانية** - عرض البيانات مع Chart.js  

## الهيكل الأساسي

```
jira-dashboard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── jira_service.py
│   │   ├── scheduler_service.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   ├── production.py
│   │   │   ├── reports.py
│   │   │   └── admin.py
│   │   └── config.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Production.jsx
│   │   │   ├── Reports.jsx
│   │   │   ├── Admin.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── ProductionPage.jsx
│   │   │   ├── ReportsPage.jsx
│   │   │   └── AdminPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

## API Endpoints

| المسار | الطريقة | الوصف |
|--------|--------|-------|
| `/dashboard` | GET | بيانات لوحة المعلومات الرئيسية |
| `/production` | GET | بيانات لوحة الإنتاج |
| `/report/morning` | GET | تقرير الصباح |
| `/report/night` | GET | تقرير الليل |
| `/sync` | POST | مزامنة البيانات من Jira |
| `/admin/settings` | GET/POST | إعدادات Jira والوكلاء |
| `/admin/agents` | GET/POST/PUT/DELETE | إدارة الوكلاء |

## متطلبات Jira

- حساب Jira Cloud
- API Token (من Account Settings)
- الوصول إلى Project مع المفتاح `DHNON`

## قاعات العمل

- ساعات العمل: 8:00 صباحاً - 12:00 منتصف الليل
- التقرير الصباحي: 8:00 صباحاً يومياً
- التقرير الليلي: 12:00 منتصف الليل يومياً

## المتطلبات التقنية

### Backend
- FastAPI
- SQLAlchemy
- APScheduler
- Requests
- Python-dotenv
- Pydantic

### Frontend
- React 18
- Vite
- Tailwind CSS
- Chart.js
- Axios

## التطوير

### تشغيل Backend مباشرة

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### تشغيل Frontend مباشرة

```bash
cd frontend
npm install
npm run dev
```

## الترخيص

MIT License

## الدعم

للمساعدة والأسئلة، يرجى فتح Issue في المستودع.
