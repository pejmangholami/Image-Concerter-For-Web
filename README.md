# Image-Concerter-For-Web
تبدیل تصاویر به فرمتهای webp  و avif و بهینه برای استفاده در وبسایت ها  و Seo Friendly تمامی پارامترها

# راهنمای استفاده از Image Converter Web

## معرفی

**Image Converter Web** یک ابزار قدرتمند و هوشمند برای تبدیل تصاویر به فرمت‌های بهینه وب است. این ابزار به صورت خودکار بهترین فرمت موجود را تشخیص داده و تصاویر را با کیفیت بالا و حجم کمتر برای استفاده در وب‌سایت‌ها بهینه‌سازی می‌کند.

## ویژگی‌های کلیدی

### 🚀 تشخیص خودکار فرمت
- **AVIF**: اولویت اول (بهترین فشرده‌سازی و کیفیت)
- **WebP**: اولویت دوم (پشتیبانی وسیع مرورگرها)
- **JPEG**: فرمت پایه (پشتیبانی کامل)

### 🎯 بهینه‌سازی هوشمند
- تغییر اندازه خودکار تصاویر
- حفظ نسبت اصلی تصویر
- حذف اطلاعات اضافی (EXIF)
- فشرده‌سازی بدون افت کیفیت قابل توجه

### 🏷️ مدیریت EXIF سفارشی
- اضافه کردن اطلاعات کپی‌رایت
- درج اطلاعات نویسنده
- تنظیم توضیحات و کلمات کلیدی
- پشتیبانی از آدرس وب‌سایت

### 📱 SEO-Friendly
- تبدیل نام‌های فایل به فرمت SEO
- پشتیبانی از حروف فارسی/عربی
- حذف کاراکترهای نامناسب

## نصب و پیش‌نیازها

### نصب کتابخانه‌های مورد نیاز

```bash
pip install Pillow pillow-heif
```

### پیش‌نیازهای اضافی برای AVIF
```bash
# برای Ubuntu/Debian
sudo apt-get install libheif-dev

# برای macOS
brew install libheif

# برای Windows
# دانلود از: https://github.com/strukturag/libheif/releases
```

## نحوه استفاده

### استفاده ساده
```bash
python image_converter_v2.py مسیر_مبدا مسیر_مقصد
```

### استفاده پیشرفته
```bash
python image_converter_v2.py input_folder output_folder \
    --webp-dir webp_folder \
    --quality 90 \
    --webp-quality 85 \
    --max-width 1920 \
    --max-height 1080 \
    --thumbnails
```

## پارامترهای کلیدی

### پارامترهای اصلی
- `source`: مسیر فولدر حاوی تصاویر اصلی
- `output`: مسیر فولدر خروجی اصلی
- `--webp-dir`: مسیر جداگانه برای فایل‌های WebP

### تنظیمات کیفیت
- `--quality`: کیفیت فرمت اصلی (1-100، پیش‌فرض: 85)
- `--webp-quality`: کیفیت WebP (1-100، پیش‌فرض: 85)
- `--lossless`: استفاده از فشرده‌سازی بدون افت کیفیت
- `--webp-lossless`: WebP بدون افت کیفیت

### تنظیمات اندازه
- `--max-width`: حداکثر عرض (پیش‌فرض: 1920)
- `--max-height`: حداکثر ارتفاع (پیش‌فرض: 1080)
- `--thumbnails`: ایجاد تصاویر کوچک
- `--thumb-sizes`: اندازه‌های thumbnail (پیش‌فرض: 150 300 600)

### تنظیمات EXIF
- `--artist`: نام صاحب عکس
- `--copyright`: اطلاعات کپی‌رایت
- `--website`: آدرس وب‌سایت
- `--software`: نام نرم‌افزار
- `--description`: توضیحات تصویر
- `--keywords`: کلمات کلیدی
- `--comment`: کامنت تصویر
- `--subject`: موضوع تصویر
- `--make`: شرکت سازنده دوربین
- `--model`: مدل دوربین

### تنظیمات اضافی
- `--no-exif`: حذف کامل اطلاعات EXIF
- `--no-seo`: عدم استفاده از نام‌های SEO-friendly
- `--no-transparency`: عدم حفظ شفافیت
- `--no-progressive`: عدم استفاده از بارگذاری تدریجی
- `--method`: روش فشرده‌سازی (0-6، پیش‌فرض: 6)
- `--webp-method`: روش فشرده‌سازی WebP (0-6، پیش‌فرض: 6)

## مثال‌های کاربردی

### مثال 1: تبدیل ساده
```bash
python image_converter_v2.py ./photos ./optimized
```

### مثال 2: تبدیل با WebP جداگانه
```bash
python image_converter_v2.py ./photos ./avif_images --webp-dir ./webp_images
```

### مثال 3: بهینه‌سازی برای وب‌سایت
```bash
python image_converter_v2.py ./original ./web_optimized \
    --quality 80 \
    --max-width 1200 \
    --max-height 800 \
    --thumbnails \
    --thumb-sizes 150 300 600 \
    --artist "نام شما" \
    --copyright "© 2024 وب‌سایت شما" \
    --website "https://example.com"
```

### مثال 4: تنظیمات حرفه‌ای
```bash
python image_converter_v2.py ./photos ./optimized \
    --webp-dir ./webp \
    --quality 90 \
    --webp-quality 85 \
    --max-width 1920 \
    --max-height 1080 \
    --thumbnails \
    --method 6 \
    --artist "عکاس حرفه‌ای" \
    --copyright "© 2024 استودیو عکاسی" \
    --website "https://photography-studio.com" \
    --keywords "عکاسی، طبیعت، هنری" \
    --description "مجموعه عکس‌های طبیعت"
```

## مدیریت فایل تنظیمات

### ذخیره تنظیمات
```bash
python image_converter_v2.py ./photos ./optimized --save-config my_config.json
```

### استفاده از تنظیمات ذخیره شده
```bash
python image_converter_v2.py ./photos ./optimized --config my_config.json
```

### نمونه فایل تنظیمات (config.json)
```json
{
  "quality": 90,
  "webp_quality": 85,
  "max_width": 1920,
  "max_height": 1080,
  "remove_exif": false,
  "optimize_for_web": true,
  "seo_friendly_names": true,
  "preserve_transparency": true,
  "thumbnail_sizes": [150, 300, 600],
  "create_thumbnails": true,
  "progressive": true,
  "lossless": false,
  "method": 6,
  "create_webp": true,
  "webp_lossless": false,
  "webp_method": 6,
  "custom_exif": {
    "Artist": "نام شما",
    "Copyright": "© 2024 وب‌سایت شما",
    "Software": "Image Converter Web",
    "Website": "https://example.com",
    "ImageDescription": "توضیحات تصویر",
    "XPKeywords": "کلمات کلیدی",
    "XPComment": "کامنت تصویر",
    "XPSubject": "موضوع تصویر",
    "Make": "Canon",
    "Model": "EOS R5"
  }
}
```

## فرمت‌های پشتیبانی شده

### فرمت‌های ورودی
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)
- GIF (.gif)

### فرمت‌های خروجی
- **AVIF**: بهترین فشرده‌سازی (نیاز به pillow-heif)
- **WebP**: پشتیبانی وسیع مرورگرها
- **JPEG**: پشتیبانی کامل

## نکات مهم

### بهینه‌سازی عملکرد
- برای تصاویر حجیم از `--max-width` و `--max-height` استفاده کنید
- برای وب‌سایت‌ها کیفیت 80-90 کافی است
- استفاده از `--thumbnails` برای بارگذاری سریع‌تر

### پیشنهادات SEO
- از `--artist` و `--copyright` برای اعتبارسازی استفاده کنید
- `--keywords` و `--description` برای SEO تصاویر مفید است
- `--website` برای linking به سایت اصلی

### مدیریت حافظه
- برای پردازش تصاویر بسیار بزرگ حافظه کافی داشته باشید
- استفاده از `--method 6` برای بهترین نتیجه (کندتر)
- برای سرعت بیشتر از `--method 0` استفاده کنید

## آمار و گزارش‌ها

اسکریپت به صورت خودکار آمار زیر را نمایش می‌دهد:

- تعداد کل فایل‌ها
- تعداد تبدیل‌های موفق
- تعداد تبدیل‌های ناموفق
- درصد کاهش حجم
- حجم کل قبل و بعد از تبدیل
- فهرست فایل‌های ناموفق

## عیب‌یابی

### خطاهای رایج
1. **ModuleNotFoundError**: نصب کتابخانه‌های مورد نیاز
2. **AVIF not supported**: نصب pillow-heif
3. **Permission denied**: بررسی دسترسی‌های فولدر
4. **Out of memory**: کاهش `max_width` و `max_height`

### بهبود عملکرد
- استفاده از SSD برای سرعت بیشتر
- بستن برنامه‌های غیرضروری
- استفاده از `--method` کمتر برای سرعت بیشتر

## نتیجه‌گیری

Image Converter Web ابزاری قدرتمند و کامل برای بهینه‌سازی تصاویر وب است که با قابلیت‌های پیشرفته و سهولت استفاده، نیازهای مختلف کاربران را برآورده می‌کند. استفاده از این ابزار منجر به بهبود سرعت بارگذاری وب‌سایت و تجربه کاربری بهتر می‌شود.
