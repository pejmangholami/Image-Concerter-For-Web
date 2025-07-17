import os
import shutil
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import argparse
from typing import Dict, List, Tuple
import json
from datetime import datetime

class ImageConverterWeb:
    """
    مبدل تصاویر به فرمت‌های بهینه برای وب (AVIF, WebP, JPEG)
    """
    
    def __init__(self, source_dir: str, output_dir: str, webp_dir: str = None, config: Dict = None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.webp_dir = Path(webp_dir) if webp_dir else None
        self.config = config or self.get_default_config()
        self.stats = {
            'total_files': 0,
            'converted_files': 0,
            'failed_files': 0,
            'webp_converted': 0,
            'total_size_before': 0,
            'total_size_after': 0,
            'webp_size_after': 0,
            'failed_list': []
        }
        
        # فرمت‌های پشتیبانی شده
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
        
        # تشخیص فرمت خروجی قابل استفاده
        self.output_format = self.detect_best_format()
        
    def detect_best_format(self) -> str:
        """تشخیص بهترین فرمت خروجی بر اساس کتابخانه‌های موجود"""
        
        # تست AVIF
        try:
            # تست با pillow-heif
            import pillow_heif
            pillow_heif.register_heif_opener()
            # تست ساخت تصویر AVIF
            test_img = Image.new('RGB', (10, 10), color='red')
            test_img.save('test_avif.avif', 'AVIF')
            os.remove('test_avif.avif')
            print("✓ AVIF پشتیبانی می‌شود")
            return 'AVIF'
        except:
            pass
            
        try:
            # تست مستقیم AVIF
            test_img = Image.new('RGB', (10, 10), color='red')
            test_img.save('test_avif.avif', 'AVIF')
            os.remove('test_avif.avif')
            print("✓ AVIF پشتیبانی می‌شود")
            return 'AVIF'
        except:
            pass
        
        # تست WebP
        try:
            test_img = Image.new('RGB', (10, 10), color='red')
            test_img.save('test_webp.webp', 'WebP')
            os.remove('test_webp.webp')
            print("✓ WebP استفاده می‌شود (فرمت دوم بهینه)")
            return 'WebP'
        except:
            pass
        
        # در نهایت از JPEG استفاده کن
        print("! از JPEG استفاده می‌شود (فرمت پایه)")
        return 'JPEG'
    
    def get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض بهینه برای وب"""
        return {
            'quality': 85,  # کیفیت فشرده‌سازی (1-100)
            'webp_quality': 85,  # کیفیت WebP جداگانه
            'max_width': 1920,  # حداکثر عرض تصویر
            'max_height': 1080,  # حداکثر ارتفاع تصویر
            'remove_exif': True,  # حذف اطلاعات EXIF موجود
            'optimize_for_web': True,  # بهینه‌سازی برای وب
            'thumbnail_sizes': [150, 300, 600],  # اندازه‌های thumbnail
            'create_thumbnails': False,  # ایجاد thumbnail ها
            'preserve_transparency': True,  # حفظ شفافیت
            'seo_friendly_names': True,  # نام‌های SEO-friendly
            'progressive': True,  # بارگذاری تدریجی (برای JPEG)
            'lossless': False,  # فشرده‌سازی بدون افت کیفیت (برای WebP)
            'method': 6,  # روش فشرده‌سازی WebP (0-6)
            'create_webp': True,  # ایجاد نسخه WebP
            'webp_lossless': False,  # WebP بدون افت کیفیت
            'webp_method': 6,  # روش فشرده‌سازی WebP
            # تنظیمات EXIF سفارشی
            'custom_exif': {
                'Artist': '',  # صاحب عکس
                'Copyright': '',  # کپی‌رایت
                'Software': '',  # نرم‌افزار
                'Make': '',  # شرکت سازنده
                'Model': '',  # مدل دوربین
                'ImageDescription': '',  # توضیحات تصویر
                'XPComment': '',  # کامنت (برای Windows)
                'XPKeywords': '',  # کلمات کلیدی
                'XPSubject': '',  # موضوع
                'Website': '',  # آدرس وب‌سایت (فیلد سفارشی)
            }
        }
    
    def sanitize_filename(self, filename: str) -> str:
        """تبدیل نام فایل به حالت SEO-friendly"""
        if not self.config['seo_friendly_names']:
            return filename
            
        # حذف کاراکترهای غیرمجاز و تبدیل به lowercase
        name = filename.lower()
        
        # تبدیل کاراکترهای فارسی و عربی
        persian_map = {
            'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j',
            'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r',
            'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z',
            'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh',
            'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v',
            'ه': 'h', 'ی': 'i', 'ئ': 'i', 'ء': 'a', 'آ': 'a', 'ة': 'h',
            'ى': 'i', 'ي': 'i', 'ك': 'k', 'ؤ': 'o', 'إ': 'a', 'أ': 'a',
            '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5',
            '٦': '6', '٧': '7', '٨': '8', '٩': '9'
        }
        
        for persian, english in persian_map.items():
            name = name.replace(persian, english)
        
        # جایگزینی فاصله و کاراکترهای خاص با خط تیره
        import re
        name = re.sub(r'[^\w\-_\.]', '-', name)
        # حذف خط تیره‌های متوالی
        name = re.sub(r'-+', '-', name)
        # حذف خط تیره از ابتدا و انتها
        name = name.strip('-')
        
        # اضافه کردن پیشوند برای SEO (اختیاری)
        if not name.startswith(('img-', 'photo-', 'image-')):
            name = f'img-{name}'
            
        return name
    
    def resize_image(self, image: Image.Image) -> Image.Image:
        """تغییر اندازه تصویر در صورت نیاز"""
        if not self.config['optimize_for_web']:
            return image
            
        width, height = image.size
        max_width = self.config['max_width']
        max_height = self.config['max_height']
        
        if width <= max_width and height <= max_height:
            return image
        
        # محاسبه نسبت تصویر
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # استفاده از LANCZOS برای کیفیت بالاتر
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def optimize_image(self, image: Image.Image, for_webp: bool = False) -> Image.Image:
        """بهینه‌سازی تصویر برای وب"""
        # تبدیل به RGB اگر RGBA است (برای فرمت‌هایی که شفافیت ندارند)
        if image.mode in ('RGBA', 'LA'):
            if (self.output_format == 'JPEG' and not for_webp) or (not self.config['preserve_transparency'] and not for_webp):
                # ایجاد پس‌زمینه سفید
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
        
        # تغییر اندازه
        image = self.resize_image(image)
        
        return image
    
    def add_custom_exif(self, image: Image.Image) -> Image.Image:
        """اضافه کردن EXIF سفارشی"""
        if not any(self.config['custom_exif'].values()):
            return image
        
        try:
            # دریافت EXIF موجود یا ایجاد جدید
            exif_dict = image.getexif()
            
            # نقشه‌برداری فیلدهای EXIF
            exif_mapping = {
                'Artist': 315,  # 0x013B
                'Copyright': 33432,  # 0x8298
                'Software': 305,  # 0x0131
                'Make': 271,  # 0x010F
                'Model': 272,  # 0x0110
                'ImageDescription': 270,  # 0x010E
                'XPComment': 40092,  # 0x9C9C
                'XPKeywords': 40094,  # 0x9C9E
                'XPSubject': 40095,  # 0x9C9F
            }
            
            # اضافه کردن اطلاعات سفارشی
            for key, value in self.config['custom_exif'].items():
                if value and key in exif_mapping:
                    if key.startswith('XP'):
                        # برای فیلدهای XP، باید به UTF-16 تبدیل شود
                        exif_dict[exif_mapping[key]] = value.encode('utf-16le') + b'\x00\x00'
                    else:
                        exif_dict[exif_mapping[key]] = value
            
            # اضافه کردن تاریخ تبدیل
            exif_dict[306] = datetime.now().strftime('%Y:%m:%d %H:%M:%S')  # DateTime
            
            # اضافه کردن آدرس وب‌سایت در بخش کامنت اگر مشخص شده
            if self.config['custom_exif'].get('Website'):
                comment = f"Website: {self.config['custom_exif']['Website']}"
                if self.config['custom_exif'].get('XPComment'):
                    comment = f"{self.config['custom_exif']['XPComment']} | {comment}"
                exif_dict[40092] = comment.encode('utf-16le') + b'\x00\x00'
            
            # اعمال EXIF به تصویر
            image.info['exif'] = exif_dict
            
        except Exception as e:
            print(f"خطا در اضافه کردن EXIF: {str(e)}")
        
        return image
    
    def get_output_extension(self, format_name: str = None) -> str:
        """تعیین پسوند فایل خروجی"""
        format_name = format_name or self.output_format
        extensions = {
            'AVIF': '.avif',
            'WebP': '.webp',
            'JPEG': '.jpg'
        }
        return extensions.get(format_name, '.jpg')
    
    def convert_image(self, input_path: Path, output_path: Path, format_name: str = None) -> bool:
        """تبدیل تصویر به فرمت مشخص"""
        target_format = format_name or self.output_format
        
        try:
            # باز کردن تصویر
            with Image.open(input_path) as img:
                # بهینه‌سازی
                is_webp = target_format == 'WebP'
                optimized_img = self.optimize_image(img, for_webp=is_webp)
                
                # حذف اطلاعات EXIF موجود
                if self.config['remove_exif']:
                    optimized_img.info = {}
                
                # اضافه کردن EXIF سفارشی
                if not self.config['remove_exif'] or any(self.config['custom_exif'].values()):
                    optimized_img = self.add_custom_exif(optimized_img)
                
                # تنظیمات ذخیره بر اساس فرمت
                save_params = self.get_save_params(target_format)
                
                # ذخیره تصویر
                optimized_img.save(output_path, target_format, **save_params)
                
            return True
        except Exception as e:
            print(f"خطا در تبدیل {input_path} به {target_format}: {str(e)}")
            self.stats['failed_list'].append(f"{input_path} ({target_format})")
            return False
    
    def get_save_params(self, format_name: str) -> Dict:
        """تنظیمات ذخیره بر اساس فرمت خروجی"""
        base_params = {
            'optimize': True,
        }
        
        if format_name == 'AVIF':
            return {
                **base_params,
                'quality': self.config['quality'],
                'speed': 8,  # سرعت انکود
            }
        
        elif format_name == 'WebP':
            return {
                **base_params,
                'quality': self.config['webp_quality'],
                'method': self.config['webp_method'],
                'lossless': self.config['webp_lossless'],
            }
        
        elif format_name == 'JPEG':
            return {
                **base_params,
                'quality': self.config['quality'],
                'progressive': self.config['progressive'],
            }
        
        return base_params
    
    def create_thumbnail(self, image_path: Path, output_dir: Path, size: int, format_name: str = None):
        """ایجاد thumbnail با اندازه مشخص"""
        target_format = format_name or self.output_format
        
        try:
            with Image.open(image_path) as img:
                # محاسبه اندازه جدید با حفظ نسبت
                img.thumbnail((size, size), Image.Resampling.LANCZOS)
                
                # نام فایل thumbnail
                stem = image_path.stem
                ext = self.get_output_extension(target_format)
                thumb_name = f"{stem}_thumb_{size}x{size}{ext}"
                thumb_path = output_dir / thumb_name
                
                # ذخیره thumbnail
                save_params = self.get_save_params(target_format)
                if target_format == 'WebP':
                    save_params['quality'] = min(self.config['webp_quality'], 80)
                else:
                    save_params['quality'] = min(self.config['quality'], 80)
                
                img.save(thumb_path, target_format, **save_params)
                
        except Exception as e:
            print(f"خطا در ایجاد thumbnail برای {image_path}: {str(e)}")
    
    def process_directory(self):
        """پردازش کل دایرکتوری"""
        if not self.source_dir.exists():
            print(f"دایرکتوری مبدا یافت نشد: {self.source_dir}")
            return
        
        # ایجاد دایرکتوری‌های مقصد
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.webp_dir and self.config['create_webp']:
            self.webp_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"شروع تبدیل تصاویر از {self.source_dir}")
        print(f"فرمت اصلی: {self.output_format} -> {self.output_dir}")
        if self.webp_dir and self.config['create_webp']:
            print(f"فرمت WebP: {self.webp_dir}")
        
        # نمایش تنظیمات EXIF
        if any(self.config['custom_exif'].values()):
            print("\nاطلاعات EXIF سفارشی:")
            for key, value in self.config['custom_exif'].items():
                if value:
                    print(f"  {key}: {value}")
        
        print(f"\nتنظیمات: کیفیت={self.config['quality']}, WebP کیفیت={self.config['webp_quality']}")
        print(f"حداکثر اندازه={self.config['max_width']}x{self.config['max_height']}")
        print("-" * 60)
        
        # پیدا کردن همه فایل‌های تصویری
        image_files = []
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if Path(file).suffix.lower() in self.supported_formats:
                    image_files.append(Path(root) / file)
        
        self.stats['total_files'] = len(image_files)
        print(f"تعداد فایل‌های یافت شده: {self.stats['total_files']}")
        
        # پردازش هر فایل
        for i, image_path in enumerate(image_files, 1):
            # محاسبه مسیر نسبی
            relative_path = image_path.relative_to(self.source_dir)
            
            # ایجاد ساختار دایرکتوری در مقاصد
            output_subdir = self.output_dir / relative_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            webp_subdir = None
            if self.webp_dir and self.config['create_webp']:
                webp_subdir = self.webp_dir / relative_path.parent
                webp_subdir.mkdir(parents=True, exist_ok=True)
            
            # تعیین نام فایل‌های خروجی
            base_name = self.sanitize_filename(relative_path.stem)
            
            # مسیر فایل اصلی
            output_filename = base_name + self.get_output_extension()
            output_path = output_subdir / output_filename
            
            # مسیر فایل WebP
            webp_path = None
            if webp_subdir:
                webp_filename = base_name + '.webp'
                webp_path = webp_subdir / webp_filename
            
            # اندازه فایل قبل از تبدیل
            original_size = image_path.stat().st_size
            self.stats['total_size_before'] += original_size
            
            print(f"\n[{i}/{self.stats['total_files']}] {relative_path}")
            
            # تبدیل به فرمت اصلی
            success_main = self.convert_image(image_path, output_path)
            if success_main:
                self.stats['converted_files'] += 1
                
                # اندازه فایل بعد از تبدیل
                if output_path.exists():
                    new_size = output_path.stat().st_size
                    self.stats['total_size_after'] += new_size
                    
                    # نمایش درصد کاهش حجم
                    reduction = ((original_size - new_size) / original_size) * 100
                    print(f"  ✓ {self.output_format}: {reduction:.1f}% کاهش ({original_size:,} -> {new_size:,} بایت)")
                    
                    # ایجاد thumbnail برای فرمت اصلی
                    if self.config['create_thumbnails']:
                        for size in self.config['thumbnail_sizes']:
                            self.create_thumbnail(image_path, output_subdir, size)
            
            # تبدیل به WebP
            if webp_path and self.config['create_webp']:
                success_webp = self.convert_image(image_path, webp_path, 'WebP')
                if success_webp:
                    self.stats['webp_converted'] += 1
                    
                    if webp_path.exists():
                        webp_size = webp_path.stat().st_size
                        self.stats['webp_size_after'] += webp_size
                        
                        webp_reduction = ((original_size - webp_size) / original_size) * 100
                        print(f"  ✓ WebP: {webp_reduction:.1f}% کاهش ({original_size:,} -> {webp_size:,} بایت)")
                        
                        # ایجاد thumbnail برای WebP
                        if self.config['create_thumbnails']:
                            for size in self.config['thumbnail_sizes']:
                                self.create_thumbnail(image_path, webp_subdir, size, 'WebP')
            
            if not success_main and (not webp_path or not success_webp):
                self.stats['failed_files'] += 1
                print(f"  ✗ تبدیل ناموفق")
        
        # نمایش آمار نهایی
        self.show_final_stats()
    
    def show_final_stats(self):
        """نمایش آمار نهایی"""
        print("\n" + "=" * 60)
        print("آمار نهایی:")
        print(f"کل فایل‌ها: {self.stats['total_files']}")
        print(f"تبدیل موفق ({self.output_format}): {self.stats['converted_files']}")
        if self.config['create_webp']:
            print(f"تبدیل موفق (WebP): {self.stats['webp_converted']}")
        print(f"تبدیل ناموفق: {self.stats['failed_files']}")
        
        if self.stats['total_size_before'] > 0:
            # آمار فرمت اصلی
            if self.stats['total_size_after'] > 0:
                main_reduction = ((self.stats['total_size_before'] - self.stats['total_size_after']) / 
                                self.stats['total_size_before']) * 100
                print(f"\n{self.output_format} - کاهش حجم: {main_reduction:.1f}%")
                print(f"  حجم قبل: {self.stats['total_size_before'] / (1024*1024):.2f} MB")
                print(f"  حجم بعد: {self.stats['total_size_after'] / (1024*1024):.2f} MB")
            
            # آمار WebP
            if self.stats['webp_size_after'] > 0:
                webp_reduction = ((self.stats['total_size_before'] - self.stats['webp_size_after']) / 
                                self.stats['total_size_before']) * 100
                print(f"\nWebP - کاهش حجم: {webp_reduction:.1f}%")
                print(f"  حجم قبل: {self.stats['total_size_before'] / (1024*1024):.2f} MB")
                print(f"  حجم بعد: {self.stats['webp_size_after'] / (1024*1024):.2f} MB")
        
        if self.stats['failed_list']:
            print(f"\nفایل‌های ناموفق:")
            for failed_file in self.stats['failed_list']:
                print(f"  - {failed_file}")
    
    def save_config(self, config_path: str):
        """ذخیره تنظیمات در فایل JSON"""
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"تنظیمات در {config_path} ذخیره شد")
    
    def load_config(self, config_path: str):
        """بارگذاری تنظیمات از فایل JSON"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config.update(json.load(f))
            print(f"تنظیمات از {config_path} بارگذاری شد")
        else:
            print(f"فایل تنظیمات یافت نشد: {config_path}")

def main():
    parser = argparse.ArgumentParser(description='تبدیل تصاویر به فرمت‌های بهینه برای وب')
    parser.add_argument('source', help='مسیر فولدر مبدا')
    parser.add_argument('output', help='مسیر فولدر مقصد اصلی')
    parser.add_argument('--webp-dir', help='مسیر فولدر WebP (اختیاری)')
    parser.add_argument('--quality', type=int, default=85, help='کیفیت فشرده‌سازی اصلی (1-100)')
    parser.add_argument('--webp-quality', type=int, default=85, help='کیفیت WebP (1-100)')
    parser.add_argument('--max-width', type=int, default=1920, help='حداکثر عرض')
    parser.add_argument('--max-height', type=int, default=1080, help='حداکثر ارتفاع')
    parser.add_argument('--thumbnails', action='store_true', help='ایجاد thumbnail ها')
    parser.add_argument('--config', help='مسیر فایل تنظیمات JSON')
    parser.add_argument('--save-config', help='ذخیره تنظیمات فعلی در فایل JSON')
    
    # تنظیمات EXIF
    parser.add_argument('--artist', help='نام صاحب عکس')
    parser.add_argument('--copyright', help='اطلاعات کپی‌رایت')
    parser.add_argument('--website', help='آدرس وب‌سایت')
    parser.add_argument('--software', help='نام نرم‌افزار')
    parser.add_argument('--description', help='توضیحات تصویر')
    parser.add_argument('--keywords', help='کلمات کلیدی')
    parser.add_argument('--comment', help='کامنت تصویر')
    parser.add_argument('--subject', help='موضوع تصویر')
    parser.add_argument('--make', help='شرکت سازنده دوربین')
    parser.add_argument('--model', help='مدل دوربین')
    
    # تنظیمات اضافی
    parser.add_argument('--no-exif', action='store_true', help='حذف کامل اطلاعات EXIF')
    parser.add_argument('--no-seo', action='store_true', help='عدم استفاده از نام‌های SEO-friendly')
    parser.add_argument('--no-transparency', action='store_true', help='عدم حفظ شفافیت')
    parser.add_argument('--no-progressive', action='store_true', help='عدم استفاده از بارگذاری تدریجی')
    parser.add_argument('--lossless', action='store_true', help='استفاده از فشرده‌سازی بدون افت کیفیت')
    parser.add_argument('--webp-lossless', action='store_true', help='استفاده از WebP بدون افت کیفیت')
    parser.add_argument('--method', type=int, default=6, choices=range(7), help='روش فشرده‌سازی (0-6)')
    parser.add_argument('--webp-method', type=int, default=6, choices=range(7), help='روش فشرده‌سازی WebP (0-6)')
    parser.add_argument('--thumb-sizes', nargs='+', type=int, default=[150, 300, 600], help='اندازه‌های thumbnail')
    
    args = parser.parse_args()
    
    # بررسی صحت ورودی‌ها
    if not (1 <= args.quality <= 100):
        print("خطا: کیفیت باید بین 1 تا 100 باشد")
        return
    
    if not (1 <= args.webp_quality <= 100):
        print("خطا: کیفیت WebP باید بین 1 تا 100 باشد")
        return
    
    if args.max_width <= 0 or args.max_height <= 0:
        print("خطا: حداکثر عرض و ارتفاع باید مثبت باشد")
        return
    
    # ایجاد تنظیمات
    config = {
        'quality': args.quality,
        'webp_quality': args.webp_quality,
        'max_width': args.max_width,
        'max_height': args.max_height,
        'create_thumbnails': args.thumbnails,
        'remove_exif': args.no_exif,
        'optimize_for_web': True,
        'seo_friendly_names': not args.no_seo,
        'preserve_transparency': not args.no_transparency,
        'thumbnail_sizes': args.thumb_sizes,
        'progressive': not args.no_progressive,
        'lossless': args.lossless,
        'method': args.method,
        'create_webp': bool(args.webp_dir),
        'webp_lossless': args.webp_lossless,
        'webp_method': args.webp_method,
        'custom_exif': {
            'Artist': args.artist or '',
            'Copyright': args.copyright or '',
            'Software': args.software or 'Image Converter Web',
            'Website': args.website or '',
            'ImageDescription': args.description or '',
            'XPKeywords': args.keywords or '',
            'XPComment': args.comment or '',
            'XPSubject': args.subject or '',
            'Make': args.make or '',
            'Model': args.model or '',
        }
    }
    
    # ایجاد نمونه مبدل
    converter = ImageConverterWeb(
        source_dir=args.source,
        output_dir=args.output,
        webp_dir=args.webp_dir,
        config=config
    )
    
    # بارگذاری تنظیمات از فایل اگر مشخص شده
    if args.config:
        converter.load_config(args.config)
    
    # نمایش اطلاعات شروع
    print("=" * 60)
    print("🖼️  مبدل تصاویر وب (Image Converter Web)")
    print("=" * 60)
    print(f"📁 مسیر مبدا: {args.source}")
    print(f"📁 مسیر مقصد: {args.output}")
    if args.webp_dir:
        print(f"📁 مسیر WebP: {args.webp_dir}")
    print(f"🔧 فرمت خروجی: {converter.output_format}")
    
    try:
        # شروع پردازش
        converter.process_directory()
        
        # ذخیره تنظیمات اگر درخواست شده
        if args.save_config:
            converter.save_config(args.save_config)
        
        print("\n✅ پردازش با موفقیت تکمیل شد!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  پردازش توسط کاربر متوقف شد")
    except Exception as e:
        print(f"\n❌ خطا در پردازش: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()