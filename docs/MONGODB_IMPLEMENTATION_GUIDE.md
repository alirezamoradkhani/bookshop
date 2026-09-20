# راهنمای پیاده‌سازی نسخهٔ مونگو در پروژهٔ بوک‌شاپ

شاخهٔ مربوط به این پیاده‌سازی:

```text
mongodb-migration
```

این راهنما مسیر واقعی داده را در همین پروژه توضیح می‌دهد. عبارت‌های فنی و مسیر فایل‌ها در سطرهای جدا آمده‌اند تا جهت فارسی و انگلیسی با هم تداخل نداشته باشد.

## ۱. اتصال برنامه به پایگاه‌داده

فایل‌های اصلی:

```text
app/core/setting.py
app/core/database.py
```

تنظیمات آدرس سرور، نام پایگاه‌داده و فعال‌بودن تراکنش در فایل تنظیمات قرار دارند.

کلاینت ناهمگام برنامه:

```python
AsyncMongoClient
```

این کلاینت یک بار برای کل برنامه ساخته می‌شود. تابع زیر اتصال را بررسی می‌کند و ایندکس‌های کالکشن‌ها را می‌سازد:

```python
init_mongo()
```

پایگاه‌دادهٔ واقعی مونگو مستقیماً به واحد کار و ریپازیتوری‌ها تزریق می‌شود. لایهٔ تقلیدی برای ردیابی آبجکت وجود ندارد.

مسیر ساخت وابستگی‌ها:

```text
Container
  -> AsyncMongoClient
  -> AsyncDatabase
  -> UnitOfWork
  -> Repository
```

فایل‌های این مسیر:

```text
app/dependency_injection/container.py
app/dependency_injection/providers/db.py
app/dependency_injection/providers/uow.py
app/core/unit_of_work.py
```

## ۲. ساختار ریپازیتوری‌ها

کد مشترک ریپازیتوری‌ها در این فایل است:

```text
app/mongo/base.py
```

عملیات مشترک:

```text
_next_id()   -> counters.find_one_and_update()
_insert()    -> insert_one()
_find_one()  -> find_one()
_find()      -> find()
_set_fields() -> update_one() + $set
_increment_fields() -> update_one() + $inc
_delete()    -> delete_one()
```

هر ریپازیتوری داخل دامنهٔ خودش قرار دارد. نمونهٔ دامنهٔ کتاب:

```text
app/book/repo/book.py
app/book/repo/book_author.py
app/book/repo/book_category.py
```

اتصال، تبدیل آبجکت و عملیات تکراری در کلاس پایه هستند. کوئری‌های مخصوص کتاب داخل ریپازیتوری کتاب قرار دارند.

## ۳. مدل داده

مونگو جدول و کلید خارجی ندارد. ارتباط‌ها با شناسه ذخیره می‌شوند و سرویس و ریپازیتوری اعتبار آن‌ها را کنترل می‌کنند.

نمونهٔ سند کاربر:

```json
{
  "_id": 1,
  "username": "ali",
  "email": "ali@example.com",
  "role": "user",
  "plan": "gold",
  "wallet_amount": 100000,
  "is_deleted": false
}
```

کاربر، نویسنده و مدیر همگی در یک کالکشن ذخیره می‌شوند:

```text
users
```

نوع هرکدام با فیلد زیر مشخص می‌شود:

```text
role
```

نمونهٔ سند کتاب:

```json
{
  "_id": 10,
  "title": "Dune",
  "author_ids": [2, 3],
  "categories": ["literature", "science"],
  "is_deleted": false
}
```

شناسه‌های نویسنده و دسته‌بندی‌ها داخل سند کتاب هستند، چون معمولاً همراه کتاب خوانده می‌شوند. کالکشن‌های واسط نیز برای حفظ رابط‌های قبلی پروژه و مدیریت مستقل رابطه‌ها باقی مانده‌اند.

## ۴. مسیر اجرای یک درخواست

مسیر ساخت کتاب:

```text
Route
  -> Service
  -> UnitOfWork
  -> BookRepository
  -> MongoDB
```

فایل‌های نمونه:

```text
app/book/route.py
app/book/services/command/create_book.py
app/core/unit_of_work.py
app/book/repo/book.py
```

شکل استفاده در یوزکیس:

```python
async with uow:
    book = await uow.book.get_by_id(book_id)
```

جزئیات مونگو داخل ریپازیتوری می‌ماند؛ به همین دلیل سرویس‌ها با تغییر کمی حفظ شده‌اند.

## ۵. نوشتن و تراکنش

هر متد تغییردهندهٔ ریپازیتوری همان لحظه عملیات مونگو را اجرا می‌کند:

```python
await collection.update_one(
    {"_id": object_id},
    {"$set": {"title": new_title}},
)
```

خواندن یک سند باعث نوشتن دوبارهٔ آن نمی‌شود. ردیابی آبجکت و متد زیر در این پروژه وجود ندارند:

```text
flush()
```

واحد کار فقط ریپازیتوری‌ها و نشست واقعی مونگو را مدیریت می‌کند:

```text
commit()
rollback()
```

این دو متد فقط وقتی اثر دارند که تراکنش واقعی فعال باشد. در حالت عادی هر نوشتن مستقل و فوری است.

تراکنش چندسندی به مجموعهٔ تکرارشوندهٔ مونگو نیاز دارد. تنظیم فعال‌سازی:

```env
MONGO_TRANSACTIONS=true
```

در حالت پیش‌فرض تراکنش خاموش است. عملیات حساس بهتر است با به‌روزرسانی اتمیک انجام شوند:

```text
$inc
$set
```

## ۶. کوئری‌های ترکیبی

کوئری‌های گزارش در این فایل هستند:

```text
app/query/mongo.py
```

معادل عملگرهای اس‌کیوال:

```text
JOIN      -> $lookup
WHERE     -> $match
GROUP BY  -> $group
SELECT    -> $project
ORDER BY  -> $sort
```

## ۷. آوت‌باکس و ورکر

فایل‌های اصلی:

```text
app/outbox/repo.py
app/outbox/publisher.py
app/workers/outbox_worker.py
app/broker/rabit_broker.py
```

رویداد ابتدا در کالکشن زیر ذخیره می‌شود:

```text
outbox_events
```

ورکر رویدادهای پردازش‌نشده را می‌خواند، آن‌ها را در صف پیام منتشر می‌کند و سپس وضعیت پردازش را تغییر می‌دهد.

## ترتیب پیشنهادی مطالعه

```text
1. app/core/setting.py
2. app/core/database.py
3. app/mongo/serialization.py
4. app/mongo/base.py
5. app/book/models/model.py
6. app/book/repo/book.py
7. app/core/unit_of_work.py
8. app/dependency_injection/providers/db.py
9. app/dependency_injection/providers/uow.py
10. app/dependency_injection/container.py
11. app/book/services/command/create_book.py
12. app/book/route.py
13. app/query/mongo.py
14. app/outbox/repo.py
15. app/workers/outbox_worker.py
```

ابتدا مسیر کتاب را کامل بخوان. سپس دامنه‌های کاربر، ویرایش، سفارش و امانت را با همین الگو بررسی کن.
