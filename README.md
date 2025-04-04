![Chatbot](https://raw.githubusercontent.com/ChatbootProjet/chatboot/refs/heads/main/Assets/banner.png)

**Ai-O** هو نموذج ذكاء اصطناعي متقدم تم تطويره بواسطة **AIO** لتقديم المساعدة والإجابة على أسئلة المستخدمين بطريقة منظمة ومختصرة. هذا المستند مخصص لفريق العمل لفهم كيفية التعامل مع المشروع، تعديله، وتطويره.

---

## بنية المشروع

### 1. الملفات الرئيسية
| الملف                     | الوصف                                                                 |
|---------------------------|----------------------------------------------------------------------|
| `main.py`                  | ملف الخادم الرئيسي الذي يدير المنطق والتفاعل مع API.               |
| `config.py`                  | (تخزين مفاتيح API + تعليمات الـ Ai) إدارة الإعدادات العامة           |
| `templates/index.html`    | واجهة المستخدم الأمامية التي تحتوي على التصميم والتفاعل.         |
| `requirements.txt`        | قائمة بالاعتمادات المطلوبة لتشغيل المشروع.                       |
| `README.md`               | هذا الملف، يحتوي على وثائق المشروع الداخلية.                      |

### 2. البنية العامة
- **الواجهة الأمامية**: مكتوبة باستخدام HTML، CSS، وJavaScript مع مكتبات مثل jQuery، Font Awesome، Prism.js، وLottie.
- **الواجهة الخلفية**: مكتوبة باستخدام Python مع Flask لإدارة الطلبات والتعامل مع API الذكاء الاصطناعي.

---

## كيفية التعديل والتطوير

### 1. إضافة ميزات جديدة
- **واجهة المستخدم**:
  - يمكنك تعديل التصميم في ملف `index.html` وإضافة أي ميزات جديدة باستخدام JavaScript أو CSS.
  - إذا كنت بحاجة إلى إضافة مكتبات جديدة، قم بإضافتها في `<head>` أو `<body>` حسب الحاجة.

- **المنطق الخلفي**:
  - يمكنك تعديل ملف `main.py` لإضافة منطق جديد أو تحسين الاستجابات.
  - إذا كنت بحاجة إلى دمج APIs جديدة، قم بتعديل الدالة `send_message_to_gemini`.

### 2. إدارة السياق
- يتم تخزين الرسائل السابقة في قائمة `conversation_history`. يمكنك تعديل هذه القائمة لإدارة السياق بشكل أفضل.
- إذا كنت تريد تقليل عدد الرسائل المخزنة لتحسين الأداء، يمكنك إضافة شرط لحذف الرسائل القديمة.

### 3. التعامل مع الأخطاء
- يتم التعامل مع الأخطاء في الدالة `send_message_to_gemini`. يمكنك إضافة المزيد من الحالات لمعالجة أخطاء API المختلفة.
- إذا كنت بحاجة إلى تسجيل الأخطاء بشكل أفضل، يمكنك استخدام مكتبة مثل `logging`.

### 4. تحسين الأداء
- إذا كنت تواجه مشكلات في الأداء، يمكنك:
  - تقليل عدد الرسائل المرسلة مع كل طلب.
  - استخدام ذاكرة تخزين مؤقت (Cache) لتخزين الردود الشائعة.

---

## كيفية تشغيل المشروع محليًا

### 1. استنساخ المشروع
```bash
git clone https://github.com/ChatbootProjet/chatboot.git
cd chatbot
```

### 2. إنشاء بيئة افتراضية (اختياري)
```bash
python3 -m venv venv
source venv/bin/activate  # لنظام Linux/Mac
venv\Scripts\activate     # لنظام Windows
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. تشغيل التطبيق
```bash
python main.py
```

التطبيق سيكون متاحًا على الرابط التالي:
```
http://127.0.0.1:5000/
```

---

## أدوات التطوير

### 1. Flask
- Flask هو إطار عمل خفيف الوزن يستخدم لإنشاء الخادم.
- يمكنك تعديل المسارات (`routes`) في ملف `main.py` لإضافة صفحات جديدة أو تعديل السلوك الحالي.

### 2. Requests
- تُستخدم مكتبة `requests` للتعامل مع API الخارجية.
- يمكنك تعديل الدالة `send_message_to_gemini` لتغيير طريقة التعامل مع API أو إضافة ميزات جديدة.

### 3. Lottie Animations
- تُستخدم مكتبة Lottie لإضافة رسوم متحركة.
- يمكنك استبدال ملف الرسوم المتحركة الحالي بملف جديد عن طريق تغيير الرابط في ملف `index.html`.

### 4. Prism.js
- تُستخدم مكتبة Prism.js لتسليط الضوء على بناء الجملة في الكود.
- إذا كنت بحاجة إلى تخصيص الألوان أو الأنماط، يمكنك تعديل ملف CSS الخاص بها.

---

## أمثلة على التعديلات

### 1. إضافة زر جديد
إذا كنت تريد إضافة زر جديد في واجهة المستخدم:
- افتح ملف `index.html`.
- أضف الزر داخل `<div class="input-box">` أو في أي مكان آخر حسب الحاجة.
- أضف منطق الزر في ملف JavaScript داخل `<script>`.

مثال:
```html
<button id="new-button">زر جديد</button>
```

```javascript
$("#new-button").click(function () {
    alert("تم النقر على الزر الجديد!");
});
```

### 2. تعديل نظام الرسائل
إذا كنت تريد تحسين نظام الرسائل:
- افتح ملف `main.py` وعدل الدالة `addMessage`.
- يمكنك إضافة ميزات مثل تصنيف الرسائل أو إضافة علامات زمنية.

---
