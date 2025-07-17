import os
import shutil
from pathlib import Path
from PIL import Image
import argparse
from typing import Dict, List, Tuple
import json
from datetime import datetime

class ImageConverterWeb:
    """
    مبدل تصاویر به فرمت‌های بهینه برای وب (AVIF, WebP, JPEG)
    """
    
    def __init__(self, source_dir: str, output_dir: str, config: Dict = None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.config = config or self.get_default_config()
        self.stats = {
            'total_files': 0,
            'converted_files': 0,
            'failed_files': 0,
            'total_size_before': 0,
            'total_size_after': 0,
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
            'max_width': 1920,  # حداکثر عرض تصویر
            'max_height': 1080,  # حداکثر ارتفاع تصویر
            'remove_exif': True,  # حذف اطلاعات EXIF
            'optimize_for_web': True,  # بهینه‌سازی برای وب
            'thumbnail_sizes': [150, 300, 600],  # اندازه‌های thumbnail
            'create_thumbnails': False,  # ایجاد thumbnail ها
            'preserve_transparency': True,  # حفظ شفافیت
            'seo_friendly_names': True,  # نام‌های SEO-friendly
            'progressive': True,  # بارگذاری تدریجی (برای JPEG)
            'lossless': False,  # فشرده‌سازی بدون افت کیفیت (برای WebP)
            'method': 6,  # روش فشرده‌سازی WebP (0-6)
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
            'ه': 'h', 'ی': 'i', 'ئ': 'i', 'ء': 'a'
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
    
    def optimize_image(self, image: Image.Image) -> Image.Image:
        """بهینه‌سازی تصویر برای وب"""
        # تبدیل به RGB اگر RGBA است (برای فرمت‌هایی که شفافیت ندارند)
        if image.mode in ('RGBA', 'LA'):
            if self.output_format == 'JPEG' or not self.config['preserve_transparency']:
                # ایجاد پس‌زمینه سفید
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
        
        # تغییر اندازه
        image = self.resize_image(image)
        
        return image
    
    def get_output_extension(self) -> str:
        """تعیین پسوند فایل خروجی"""
        extensions = {
            'AVIF': '.avif',
            'WebP': '.webp',
            'JPEG': '.jpg'
        }
        return extensions.get(self.output_format, '.jpg')
    
    def convert_image(self, input_path: Path, output_path: Path) -> bool:
        """تبدیل تصویر به فرمت بهینه"""
        try:
            # باز کردن تصویر
            with Image.open(input_path) as img:
                # بهینه‌سازی
                optimized_img = self.optimize_image(img)
                
                # حذف اطلاعات EXIF
                if self.config['remove_exif']:
                    optimized_img.info = {}
                
                # تنظیمات ذخیره بر اساس فرمت
                save_params = self.get_save_params()
                
                # ذخیره تصویر
                optimized_img.save(output_path, self.output_format, **save_params)
                
            return True
        except Exception as e:
            print(f"خطا در تبدیل {input_path}: {str(e)}")
            self.stats['failed_list'].append(str(input_path))
            return False
    
    def get_save_params(self) -> Dict:
        """تنظیمات ذخیره بر اساس فرمت خروجی"""
        base_params = {
            'quality': self.config['quality'],
            'optimize': True,
        }
        
        if self.output_format == 'AVIF':
            return {
                **base_params,
                'speed': 8,  # سرعت انکود
            }
        
        elif self.output_format == 'WebP':
            return {
                **base_params,
                'method': self.config['method'],
                'lossless': self.config['lossless'],
            }
        
        elif self.output_format == 'JPEG':
            return {
                **base_params,
                'progressive': self.config['progressive'],
            }
        
        return base_params
    
    def create_thumbnail(self, image_path: Path, output_dir: Path, size: int):
        """ایجاد thumbnail با اندازه مشخص"""
        try:
            with Image.open(image_path) as img:
                # محاسبه اندازه جدید با حفظ نسبت
                img.thumbnail((size, size), Image.Resampling.LANCZOS)
                
                # نام فایل thumbnail
                stem = image_path.stem
                ext = self.get_output_extension()
                thumb_name = f"{stem}_thumb_{size}x{size}{ext}"
                thumb_path = output_dir / thumb_name
                
                # ذخیره thumbnail
                save_params = self.get_save_params()
                save_params['quality'] = min(self.config['quality'], 80)  # کیفیت کمتر برای thumbnail
                
                img.save(thumb_path, self.output_format, **save_params)
                
        except Exception as e:
            print(f"خطا در ایجاد thumbnail برای {image_path}: {str(e)}")
    
    def process_directory(self):
        """پردازش کل دایرکتوری"""
        if not self.source_dir.exists():
            print(f"دایرکتوری مبدا یافت نشد: {self.source_dir}")
            return
        
        # ایجاد دایرکتوری مقصد
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"شروع تبدیل تصاویر از {self.source_dir} به {self.output_dir}")
        print(f"فرمت خروجی: {self.output_format}")
        print(f"تنظیمات: کیفیت={self.config['quality']}, حداکثر اندازه={self.config['max_width']}x{self.config['max_height']}")
        print("-" * 50)
        
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
            
            # ایجاد ساختار دایرکتوری در مقصد
            output_subdir = self.output_dir / relative_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            # تعیین نام فایل خروجی
            output_filename = self.sanitize_filename(relative_path.stem) + self.get_output_extension()
            output_path = output_subdir / output_filename
            
            # اندازه فایل قبل از تبدیل
            original_size = image_path.stat().st_size
            self.stats['total_size_before'] += original_size
            
            print(f"[{i}/{self.stats['total_files']}] {relative_path} -> {output_filename}")
            
            # تبدیل فایل
            if self.convert_image(image_path, output_path):
                self.stats['converted_files'] += 1
                
                # اندازه فایل بعد از تبدیل
                if output_path.exists():
                    new_size = output_path.stat().st_size
                    self.stats['total_size_after'] += new_size
                    
                    # نمایش درصد کاهش حجم
                    reduction = ((original_size - new_size) / original_size) * 100
                    print(f"  ✓ کاهش حجم: {reduction:.1f}% ({original_size:,} -> {new_size:,} بایت)")
                    
                    # ایجاد thumbnail ها
                    if self.config['create_thumbnails']:
                        for size in self.config['thumbnail_sizes']:
                            self.create_thumbnail(image_path, output_subdir, size)
                
            else:
                self.stats['failed_files'] += 1
                print(f"  ✗ تبدیل ناموفق")
        
        # نمایش آمار نهایی
        self.show_final_stats()
    
    def show_final_stats(self):
        """نمایش آمار نهایی"""
        print("\n" + "=" * 50)
        print("آمار نهایی:")
        print(f"کل فایل‌ها: {self.stats['total_files']}")
        print(f"تبدیل موفق: {self.stats['converted_files']}")
        print(f"تبدیل ناموفق: {self.stats['failed_files']}")
        print(f"فرمت خروجی: {self.output_format}")
        
        if self.stats['total_size_before'] > 0:
            total_reduction = ((self.stats['total_size_before'] - self.stats['total_size_after']) / 
                             self.stats['total_size_before']) * 100
            print(f"کاهش کل حجم: {total_reduction:.1f}%")
            print(f"حجم قبل: {self.stats['total_size_before'] / (1024*1024):.2f} MB")
            print(f"حجم بعد: {self.stats['total_size_after'] / (1024*1024):.2f} MB")
        
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
    parser.add_argument('output', help='مسیر فولدر مقصد')
    parser.add_argument('--quality', type=int, default=85, help='کیفیت فشرده‌سازی (1-100)')
    parser.add_argument('--max-width', type=int, default=1920, help='حداکثر عرض')
    parser.add_argument('--max-height', type=int, default=1080, help='حداکثر ارتفاع')
    parser.add_argument('--thumbnails', action='store_true', help='ایجاد thumbnail ها')
    parser.add_argument('--config', help='مسیر فایل تنظیمات JSON')
    parser.add_argument('--save-config', help='ذخیره تنظیمات فعلی در فایل JSON')
    
    args = parser.parse_args()
    
    # ایجاد تنظیمات
    config = {
        'quality': args.quality,
        'max_width': args.max_width,
        'max_height': args.max_height,
        'create_thumbnails': args.thumbnails,
        'remove_exif': True,
        'optimize_for_web': True,
        'seo_friendly_names': True,
        'preserve_transparency': True,
        'thumbnail_sizes': [150, 300, 600],
        'progressive': True,
        'lossless': False,
        'method': 6,
    }
    
    # ایجاد مبدل
    converter = ImageConverterWeb(args.source, args.output, config)
    
    # بارگذاری تنظیمات از فایل در صورت وجود
    if args.config:
        converter.load_config(args.config)
    
    # ذخیره تنظیمات در صورت درخواست
    if args.save_config:
        converter.save_config(args.save_config)
    
    # شروع پردازش
    converter.process_directory()

if __name__ == "__main__":
    main()