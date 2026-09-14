if __name__ == "__main__":
    from DataBase import DataBase

import asyncio
import base64
import datetime
import hashlib
import json
import logging
import os
import random
import re
import secrets
import shutil
import sqlite3
import time
import traceback
from io import BytesIO

import aiohttp
import aiosqlite
from cryptography.fernet import Fernet
from pyrobale import Client
from pyrobale.objects import InputFile, Message, User
from pyrobale.objects.enums import ChatType
from telebot import ContinueHandling, types
from telebot.async_telebot import AsyncTeleBot

from anti_spam import AntiSpam
from anti_virus import AntiVirus
from i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, cmd_match, cmd_startswith, t
from profanity_checker import ProfanityDetector
from utils import *

logger = logging.getLogger('TeleBot').setLevel(logging.INFO)

class KomakYaar:
    def __init__(self):
        self.bot = AsyncTeleBot(API_TOKEN)
        self.me = asyncio.run(self.bot.get_me())
        self.bale_bot = Client(BALE_TOKEN)
        self.bale_bot_me: User = self.bale_bot.get_me()
        # ============ راهنمای گام‌به‌گام ============
        # ساختار: دسته → زیردسته → راهنمای دقیق همان دستور
        self.guide_categories = {
            "help_members": {
                "title": "👥 مدیریت اعضا",
                "subs": [
                    ("help_members_warn", "⚠️ اخطار و سقف اخطار"),
                    ("help_members_punish", "🔨 مجازات‌ها (میوت / کیک / بن)"),
                    ("help_members_info", "ℹ️ اطلاعات کاربر"),
                ],
            },
            "help_locks": {
                "title": "🔒 قفل‌ها و محدودیت‌ها",
                "subs": [
                    ("help_locks_content", "📝 قفل محتوا (فحش / لینک / فوروارد / گیف / گروه)"),
                    ("help_locks_words", "🔤 مدیریت کلمات مسدود"),
                    ("help_locks_post", "📌 قفل پست‌های کانال"),
                    ("help_locks_antiabuse", "🛑 اسپم / فلاد / حمله"),
                    ("help_locks_captcha", "🤖 کپچای ورود اعضا"),
                    ("help_locks_panel", "💡 پنل مدیریت قفل"),
                ],
            },
            "help_filters": {
                "title": "🎯 فیلترها و پاسخ خودکار",
                "subs": [
                    ("help_filters_add", "➕ افزودن فیلتر"),
                    ("help_filters_remove", "➖ حذف فیلتر"),
                    ("help_filters_list", "📋 مشاهده فیلترها"),
                ],
            },
            "help_public": {
                "title": "💬 دستورات عمومی",
                "subs": [
                    ("help_public_toggle", "⚙️ فعال / غیرفعال کردن"),
                    ("help_public_cmds", "💬 لیست دستورات عمومی"),
                ],
            },
            "help_invite": {
                "title": "🔗 لینک و دعوت",
                "subs": [
                    ("help_invite_make", "🔗 ساخت لینک دعوت"),
                    ("help_invite_limits", "🔢 تنظیم حداکثر دعوت"),
                    ("help_invite_request", "✅ درخواست برای ورود"),
                ],
            },
            "help_settings": {
                "title": "⚙️ تنظیمات گروه",
                "subs": [
                    ("help_settings_texts", "📝 تنظیم متون (خوشامد / قوانین / کامنت)"),
                    ("help_settings_vars", "🔤 متغیرهای متن خوشامد"),
                    ("help_settings_bots", "🤖 مدیریت بات‌ها"),
                    ("help_settings_misc", "🛠️ سایر تنظیمات"),
                ],
            },
            "help_warnings": {
                "title": "📝 سیستم اخطار و گزارش",
                "subs": [
                    ("help_warnings_warn", "⚠️ اخطار و مجازات"),
                    ("help_warnings_report", "📢 گزارش به ادمین"),
                ],
            },
            "help_profile": {
                "title": "🎭 لقب و اصل",
                "subs": [
                    ("help_profile_set", "✏️ ثبت لقب و اصل"),
                    ("help_profile_view", "👀 مشاهده اطلاعات"),
                ],
            },
            "help_antivirus": {
                "title": "🛡️ ضدویروس فایل",
                "direct": True,
            },
            "help_whisper": {
                "title": "🕵️ نجوا (پیام خصوصی)",
                "direct": True,
            },
            "help_bridge": {
                "title": "🌉 بریج بله ↔ تلگرام",
                "direct": True,
            },
            "help_faq": {
                "title": "❓ سوالات متداول",
                "direct": True,
            },
            "help_stats": {
                "title": "📊 آمار و رتبه\u200cبندی",
                "direct": True,
            },
        }

        _size_mb = MAX_ANTIVIRUS_FILE_SIZE / (1024 * 1024)

        self.guide_texts = {
            "help_members_warn": (
                "⚠️ **اخطار و سقف اخطار**\n\n"
                "**ثبت اخطار:**\n"
                "• `اخطار` (ریپلای روی پیام کاربر) - یک اخطار اضافه می‌کند\n"
                "• `حذف اخطارها` (ریپلای) - تمام اخطارهای کاربر را پاک می‌کند\n"
                "• `سقف اخطار <عدد>` - حداکثر اخطار قبل از مجازات (پیش‌فرض: 3)\n\n"
                "**تنظیم مجازات اخطار:**\n"
                "• `تعیین مجازات اخطار` - انتخاب مجازات (کیک/بن/میوت) هنگام رسیدن به سقف\n\n"
                "**مثال:**\n"
                "• `سقف اخطار 5` - بعد از ۵ اخطار کاربر مجازات می‌شود"
            ),
            "help_members_punish": (
                "🔨 **مجازات‌ها**\n\n"
                "**میوت (سکوت):**\n"
                "• `خفه <دقیقه>` - میوت موقت کاربر\n"
                "• `سکوت` (ریپلای) - میوت کاربر\n"
                "• `آن‌میوت` (ریپلای) - برداشتن میوت\n\n"
                "**اخراج و بن:**\n"
                "• `کیک` / `سیک` / `ریم` (ریپلای) - اخراج از گروه\n"
                "• `بن` / `سیکتیر` (ریپلای) - بن دائم\n"
                "• `بن+` / `سیک مخفی` (ریپلای) - بن + حذف پیام فرمان\n"
                "• `آن‌بن` (ریپلای) - برداشتن بن\n\n"
                "**تنظیم مجازات اخطار:**\n"
                "• `تعیین مجازات اخطار` - انتخاب نوع مجازاتی که با رسیدن به سقف اخطار اجرا شود"
            ),
            "help_members_info": (
                "ℹ️ **اطلاعات کاربر**\n\n"
                "• `اطلاعات` (ریپلای روی کاربر) - اطلاعات کامل (آیدی، وضعیت، عکس)\n"
                "• `لقب` (ریپلای) - نمایش لقب کاربر\n"
                "• `اصل` (ریپلای) - نمایش اصل و نسب کاربر"
            ),

            "help_locks_content": (
                "📝 **قفل محتوا**\n\n"
                "• `قفل فحش` / `بازکردن فحش` - مسدود کردن فحش\n"
                "• `قفل لینک` / `بازکردن لینک` - مسدود کردن لینک\n"
                "• `قفل فوروارد` / `بازکردن فوروارد` - مسدود کردن فوروارد\n"
                "• `قفل گیف` / `بازکردن گیف` - مسدود کردن گیف\n"
                "• `قفل گروه` / `بازکردن گروه` - قفل کامل گروه (حذف پیام همه)\n\n"
                "💡 راه ساده‌تر: دستور `پنل` را بفرستید و قفل‌ها را با دکمه روشن/خاموش کنید."
            ),
            "help_locks_words": (
                "🔤 **مدیریت کلمات مسدود**\n\n"
                "• `مسدود کلمه <متن>` - مسدود کردن یک کلمه خاص\n"
                "• `بازکردن کلمه <متن>` - آزاد کردن کلمه مسدود\n\n"
                "**مثال:**\n"
                "• `مسدود کلمه بی‌ادبی` - هر پیامی که شامل «بی‌ادبی» باشد حذف می‌شود\n\n"
                "💡 اگر کلمه چندکلمه‌ای باشد در هر جای متن حذف می‌شود؛ اگر تک‌کلمه‌ای باشد دقیقاً همان کلمه."
            ),
            "help_locks_post": (
                "📌 **قفل پست‌های کانال**\n\n"
                "• `قفل پست` (ریپلای روی پست کانال) - غیرفعال کردن کامنت روی پست\n"
                "• `باز کردن پست` (ریپلای) - فعال کردن دوباره کامنت\n\n"
                "💡 وقتی پست قفل باشد، کامنت‌های ارسال‌شده روی آن حذف می‌شوند."
            ),
            "help_locks_antiabuse": (
                "🛑 **ضد اسپم، فلاد و حمله**\n\n"
                "**اسپم:**\n"
                "• `قفل اسپم` / `بازکردن اسپم` - جلوگیری از پیام‌های تکراری و سریع\n\n"
                "**فلاد:**\n"
                "• `قفل فلاد` / `بازکردن فلاد` - جلوگیری از ارسال پشت‌سرهم خیلی سریع\n\n"
                "**ضد حمله (Anti-Raid):**\n"
                "• `قفل حمله` / `بازکردن حمله` - جلوگیری از ورود انبوه اعضا\n"
                "• `تنظیم سقف حمله <عدد>` - حداکثر ورود عضو در بازه (پیش‌فرض: ۵)\n"
                "• `تنظیم بازه حمله <ثانیه>` - بازه زمانی تشخیص حمله (پیش‌فرض: ۳۰)\n\n"
                "**مثال:**\n"
                "• `تنظیم سقف حمله 10`\n"
                "• `تنظیم بازه حمله 60`"
            ),
            "help_locks_captcha": (
                "🤖 **کپچای ورود اعضا**\n\n"
                "• `قفل کپچا` - فعال کردن کپچا برای اعضای جدید\n"
                "• `بازکردن کپچا` - غیرفعال کردن کپچا\n\n"
                "💡 با فعال بودن کپچا، اعضای جدید باید یک معما را حل کنند؛ این کار از ورود ربات‌ها و اکانت‌های جعلی جلوگیری می‌کند."
            ),
            "help_locks_panel": (
                "💡 **پنل مدیریت قفل**\n\n"
                "• `پنل قفل` - نمایش پنل گرافیکی قفل‌ها با دکمه روشن/خاموش\n"
                "• `پنل` - نمایش پنل جامع (همه قفل‌ها + تنظیمات + دسترسی به راهنما)\n\n"
                "💡 با دکمه‌های پنل می‌توانید قفل‌ها را بدون تایپ کردن روشن/خاموش کنید."
            ),

            "help_filters_add": (
                "➕ **افزودن فیلتر (پاسخ خودکار)**\n\n"
                "روی پیامی که می‌خواهید پاسخ داده شود **ریپلای** کنید و بنویسید:\n"
                "`فیلتر <پاسخ مورد نظر>`\n\n"
                "**مثال:**\n"
                "1. روی پیام «سلام» ریپلای کنید\n"
                "2. بنویسید: `فیلتر علیک سلام`\n"
                "3. از این به بعد هرکس «سلام» بنویسد، جواب «علیک سلام» می‌گیرد\n\n"
                "💡 فیلترها به حروف بزرگ و کوچک حساس نیستند."
            ),
            "help_filters_remove": (
                "➖ **حذف فیلتر**\n\n"
                "**روش اول:**\n"
                "روی پیام فیلتر شده ریپلای کنید و بنویسید:\n"
                "`حذف فیلتر`\n\n"
                "**روش دوم:**\n"
                "`حذف فیلتر <کلمه کلیدی>`\n\n"
                "**مثال:**\n"
                "• `حذف فیلتر سلام` - فیلتر «سلام» را حذف می‌کند"
            ),
            "help_filters_list": (
                "📋 **مشاهده فیلترها**\n\n"
                "• `فیلترها` - نمایش لیست تمام فیلترهای گروه\n\n"
                "💡 این دستور برای همه اعضا (در صورت روشن بودن دستورات عمومی) قابل استفاده است."
            ),

            "help_public_toggle": (
                "⚙️ **فعال / غیرفعال کردن دستورات عمومی**\n\n"
                "• `دستورات عمومی روشن` - همه اعضا می‌توانند از دستورات عمومی استفاده کنند\n"
                "• `دستورات عمومی خاموش` - فقط ادمین‌ها می‌توانند از دستورات استفاده کنند\n\n"
                "💡 پیش‌فرض: روشن"
            ),
            "help_public_cmds": (
                "💬 **لیست دستورات عمومی (برای همه اعضا)**\n\n"
                "• `لینک` - دریافت لینک دعوت اختصاصی\n"
                "• `قوانین` - مشاهده قوانین گروه\n"
                "• `فیلترها` - مشاهده فیلترهای فعال\n"
                "• `اکو <متن>` - تکرار متن\n"
                "• `کمک یار` - منو و راهنما\n"
                "• `@admins` - منشن کردن همه ادمین‌ها\n"
                "• `گزارش` (ریپلای) - گزارش پیام به ادمین‌ها\n"
                "• `اطلاعات` (ریپلای) - اطلاعات کاربر\n"
                "• `لقب` (ریپلای) - لقب کاربر\n"
                "• `اصل` (ریپلای) - اصل و نسب کاربر"
            ),

            "help_invite_make": (
                "🔗 **ساخت لینک دعوت**\n\n"
                "• `لینک` - ساخت لینک دعوت اختصاصی شما\n\n"
                "💡 هر کاربر می‌تواند لینک اختصاصی خودش را بسازد و لینک‌ها با نام سازنده ذخیره می‌شوند."
            ),
            "help_invite_limits": (
                "🔢 **تنظیم حداکثر دعوت**\n\n"
                "• `تنظیم حداکثر دعوت <عدد>` - محدودیت تعداد استفاده از لینک\n\n"
                "**مثال:**\n"
                "• `تنظیم حداکثر دعوت 50` - هر لینک فقط ۵۰ بار قابل استفاده است\n\n"
                "💡 اگر حداکثری تعیین نشده باشد، لینک نامحدود است."
            ),
            "help_invite_request": (
                "✅ **درخواست برای ورود**\n\n"
                "• `درخواست برای ورود` - روشن/خاموش کردن نیاز به تایید ادمین برای ورود\n\n"
                "💡 وقتی روشن باشد، افرادی که با لینک وارد می‌شوند باید توسط ادمین تایید شوند."
            ),

            "help_settings_texts": (
                "📝 **تنظیم متون**\n\n"
                "• `تنظیم خوشامد` (ریپلای روی پیام حاوی متن جدید) - تغییر متن خوشامدگویی\n"
                "• `تنظیم قوانین` (ریپلای) - تغییر قوانین گروه\n"
                "• `تنظیم متن کامنت` (ریپلای) - تغییر متن زیر پست‌های کانال\n\n"
                "**مثال:**\n"
                "1. پیامی بنویسید: `به {name} خوش آمدید!`\n"
                "2. روی همان پیام ریپلای کنید و بنویسید `تنظیم خوشامد`"
            ),
            "help_settings_vars": (
                "🔤 **متغیرهای متن خوشامد**\n\n"
                "• `{name}` - نام کاربر جدید\n"
                "• `{username}` - یوزرنیم کاربر\n"
                "• `{id}` - آیدی عددی کاربر\n"
                "• `{chat}` - نام گروه\n"
                "• `{members}` - تعداد اعضای گروه\n\n"
                "**نمونه متن خوشامد:**\n"
                "`{name} عزیز خوش اومدی به {chat}! الان {members} نفر هستیم 🎉`"
            ),
            "help_settings_bots": (
                "🤖 **مدیریت بات‌ها**\n\n"
                "• `بلاک بات @username` - مسدود کردن یک بات در گروه\n"
                "• `آن‌بلاک بات @username` - آزاد کردن بات\n"
                "• `بات های بلاک شده` - لیست بات‌های مسدود\n\n"
                "**مثال:**\n"
                "• `بلاک بات @somebot`"
            ),
            "help_settings_misc": (
                "🛠️ **سایر تنظیمات**\n\n"
                "• `باادب شو` / `بی ادب شو` - تغییر لحن پاسخ‌های بات\n"
                "• `دستورات عمومی روشن / خاموش` - کنترل دسترسی همه به دستورات عمومی\n"
                "• `ریست` - بازنشانی تنظیمات گروه (فیلترها باقی می‌مانند)\n"
                "• `درخواست کمک` - درخواست ورود اونر بات به گروه برای مشکلات فوری\n"
                "• `پنل` - نمایش پنل جامع مدیریت"
            ),

            "help_warnings_warn": (
                "⚠️ **اخطار و مجازات**\n\n"
                "• `اخطار` (ریپلای) - ثبت اخطار برای کاربر\n"
                "• `حذف اخطارها` (ریپلای) - پاک کردن تمام اخطارهای کاربر\n"
                "• `سقف اخطار <عدد>` - تعیین حداکثر اخطار (پیش‌فرض: 3)\n"
                "• `تعیین مجازات اخطار` - انتخاب مجازات (کیک/بن/میوت) هنگام رسیدن به سقف\n\n"
                "**مثال:**\n"
                "• `سقف اخطار 5` - بعد از ۵ اخطار مجازات اجرا می‌شود"
            ),
            "help_warnings_report": (
                "📢 **گزارش به ادمین**\n\n"
                "• `گزارش` (ریپلای روی پیام) - گزارش یک پیام به همه ادمین‌ها\n\n"
                "💡 ادمین‌ها می‌توانند گزارش را در پیوی خود بررسی کنند. گزارش‌ها شامل لینک مستقیم به پیام هستند."
            ),

            "help_profile_set": (
                "✏️ **ثبت لقب و اصل**\n\n"
                "• `ثبت لقب <متن>` (ریپلای روی خود یا دیگران) - ثبت لقب برای کاربر\n"
                "• `ثبت اصل <متن>` (ریپلای) - ثبت اصل و نسب\n\n"
                "**مثال:**\n"
                "1. روی پیام کاربر ریپلای کنید\n"
                "2. بنویسید: `ثبت لقب دانشمند بزرگ`\n\n"
                "💡 ادمین‌ها می‌توانند برای دیگران ثبت کنند، بقیه فقط برای خودشان."
            ),
            "help_profile_view": (
                "👀 **مشاهده اطلاعات**\n\n"
                "• `لقب` (ریپلای) - مشاهده لقب کاربر\n"
                "• `اصل` (ریپلای) - مشاهده اصل کاربر\n"
                "• `اطلاعات` (ریپلای) - اطلاعات کامل (آیدی، وضعیت، عکس)"
            ),

            "help_antivirus": (
                "🛡️ **ضدویروس فایل**\n\n"
                "**نحوه عملکرد:**\n"
                "با ارسال فایل‌های متنی (مثل `txt`, `py`, `js` و...) در گروه، ربات به صورت خودکار محتوای فایل را بررسی می‌کند و در صورت تشخیص بدافزار هشدار می‌دهد.\n\n"
                "**معنای واکنش‌های ربات روی فایل:**\n"
                "• `🤔` - در حال بررسی فایل\n"
                "• `👍` - فایل سالم است\n"
                "• `💀` - بدافزار تشخیص داده شد!\n"
                "• `❓` - محتوای فایل قابل خواندن نبود\n"
                "• `🥴` - نوع فایل پشتیبانی نمی‌شود یا فایل بزرگ‌تر از سقف مجاز است (بررسی نمی‌شود)\n\n"
                "**فایل‌های قابل بررسی:**\n"
                "`txt`, `py`, `js`, `html`, `css`, `json`, `xml`, `md`, `csv`, `log`, `sh`, `bat`, `ps1`, `php`, `java`, `cs`, `cpp`, `c`, `h`, `hpp`, `rb`, `pl`, `go`, `rs`\n\n"
                f"💡 فایل‌های بزرگ‌تر از حدود `{_size_mb:.1f}MB` بدون دانلود رد می‌شوند تا پهنای باند ربات مصرف نشود."
            ),

            "help_whisper": (
                "🕵️ **نجوا (ارسال پیام خصوصی)**\n\n"
                "از طریق **Inline Mode** می‌توانید به کاربران دیگر پیام خصوصی بفرستید بدون اینکه دیگران ببینند.\n\n"
                "**طریقه استفاده:**\n"
                "1. در باکس پیام، `@username_ربات` را تایپ کنید\n"
                "2. بنویسید: `<متن پیام> @username_مقصد`\n"
                "3. مثال: `@KomakYaarBot سلام چطوری؟ @Ali`\n"
                "4. روی نتیجه کلیک کنید و ارسال کنید\n\n"
                "**نکات مهم:**\n"
                "• فقط فرستنده و گیرنده می‌توانند پیام را بخوانند\n"
                "• پیام‌ها در دیتابیس رمزنگاری می‌شوند\n"
                "• نمی‌توانید به خودتان یا به ربات پیام بفرستید\n"
                "• در پیوی شخصی نمی‌توانید استفاده کنید"
            ),

            "help_bridge": (
                "🌉 **پل ارتباطی (Telegram ↔ Bale)**\n\n"
                "**قابلیت:**\n"
                "ارسال خودکار تمام پیام‌ها، عکس‌ها، ویدیوها و فایل‌ها از یک کانال تلگرام به کانال بله (و بالعکس).\n\n"
                "**تنظیم پل از تلگرام به بله:**\n"
                "1. ربات را به عنوان ادمین در **کانال تلگرام** و **کانال بله** اضافه کنید.\n"
                f"آیدی ربات در بله: [@{self.bale_bot_me.username}](https://ble.ir/{self.bale_bot_me.username})\n"
                "2. در کانال بله دستور `/getid` را ارسال کنید تا آیدی کانال بله را بگیرید.\n"
                "3. در **کانال تلگرام** دستور زیر را ارسال کنید:\n"
                "`/setbridge آیدی_کانال_بله`\n\n"
                "**حذف پل:**\n"
                "در کانال تلگرام:\n"
                "`/removebridge آیدی_کانال_بله`\n\n"
                "**نکات مهم:**\n"
                "• پل فقط روی **کانال‌ها** کار می‌کند (نه گروه).\n"
                "• ربات باید ادمین هر دو کانال باشد.\n"
                "• فورواردها، عکس، ویدیو، گیف، استیکر، صدا و فایل پشتیبانی می‌شوند.\n"
                "• بریج دوطرفه است؛ محتوای تلگرام به بله و بالعکس منتقل می‌شود.\n\n"
                "💡 **مثال:**\n"
                "`/setbridge -1001234567890`"
            ),

            "help_faq": (
                "❓ **سوالات متداول**\n\n"
                "**۱. چرا بات پاسخ نمی‌دهد؟**\n"
                "• مطمئن شوید دستور `فعال شو` را فرستاده باشید\n"
                "• بررسی کنید بات ادمین گروه باشد\n"
                "• گروه ممکن است بن شده باشد\n\n"
                "**۲. چگونه تنظیمات را ریست کنم؟**\n"
                "• از دستور `ریست` استفاده کنید\n"
                "• فیلترها حذف نمی‌شوند، فقط تنظیمات ریست می‌شوند\n\n"
                "**۳. چرا لینک دعوت کار نمی‌کند؟**\n"
                "• بررسی کنید `تنظیم حداکثر دعوت` را تنظیم کرده‌اید\n"
                "• اگر `درخواست برای ورود` فعال است، افراد باید تایید شوند\n\n"
                "**۴. چگونه از شر پیام‌های اسپم خلاص شوم؟**\n"
                "• از قفل‌های لینک، فحش و فوروارد استفاده کنید\n"
                "• کلمات نامناسب را با `مسدود کلمه` اضافه کنید\n\n"
                "**۵. آیا بات اوپن سورس است؟**\n"
                "• بله! کد بات در گیت\u200cهاب موجود است:\n"
                "• https://github.com/Code-Wizaard/KomakYaar"
            ),

            "help_stats": (
                "📊 **آمار و رتبه\u200cبندی**\n\n"
                "این بخش به شما امکان مشاهده فعال\u200cترین اعضای گروه را می\u200cدهد.\n\n"
                "**دستورات:**\n"
                "• `آمار` - نمایش لیست ۱۰ فعال\u200cترین عضو گروه\n"
                "• `آمار من` - مشاهده آمار شخصی شما (تعداد پیام، اخطارها، رتبه)\n"
                "• `ریست آمار` (ادمین) - ریست کردن تمام آمار گروه\n\n"
                "**نکات:**\n"
                "• هر پیامی که ارسال کنید، یک واحد به آمار شما اضافه می\u200cشود\n"
                "• اگر پیام شما به دلیل اسپم یا فحش حذف شود، یک واحد از آمار شما کم می\u200cشود\n"
                "• پیام\u200cهای ادمین\u200cها شمارش نمی\u200cشوند\n\n"
                "**تنظیم زبان:**\n"
                "• `تنظیم زبان fa` - تغییر زبان گروه به فارسی\n"
                "• `تنظیم زبان en` - تغییر زبان گروه به انگلیسی\n\n"
                "💡 در پیوی ربات هم می\u200cتوانید با دستور `/language` یا `زبان` زبان شخصی خود را تنظیم کنید."
            ),
        }

        self.guide_sub_parent = {}
        for parent, cat in self.guide_categories.items():
            for sub_cb, _ in cat.get("subs", []):
                self.guide_sub_parent[sub_cb] = parent

        # Main help keyboard - first & last categories full-width, middle paired
        items = [(cat["title"], cb) for cb, cat in self.guide_categories.items()]
        self.help_keyboard = self.build_pretty_keyboard(items)

        # Start keyboard for private chat
        self.start_keyboard = types.InlineKeyboardMarkup(row_width=2)
        self.start_keyboard.add(
            types.InlineKeyboardButton("➕ اضافه کردن به گروه", url=f"https://t.me/{self.me.username}?startgroup"),
            types.InlineKeyboardButton("📖 راهنمای سریع", callback_data="help_main"),
            types.InlineKeyboardButton("💻 گیت‌هاب پروژه", url="https://github.com/Code-Wizaard/KomakYaar")
        )

        # Back button keyboard
        self.back_keyboard = types.InlineKeyboardMarkup(row_width=1)
        self.back_keyboard.add(
            types.InlineKeyboardButton("🔙 برگشت به منوی اصلی", callback_data="help_main")
        )
        self.db = DataBase(self.bot)
        self.anti_spam = AntiSpam(self.db)
        self.anti_virus = AntiVirus()
        self.profanity_detector = ProfanityDetector()
        self.join_tracker = {}
        self.raid_active = {}
        self.captchas = {}
        self.lock_panel_origin = {}
        self.awaiting_db_restore = False
        self.user_languages = {}  # user_id -> language code (private chat preference)
        self.setup_events()

    async def get_lang(self, chat_id):
        """Get the language code for a group (from group_settings)."""
        lang = await self.db.get_group_setting(chat_id, "LANGUAGE", DEFAULT_LANGUAGE)
        if lang not in SUPPORTED_LANGUAGES:
            lang = DEFAULT_LANGUAGE
        return lang

    def get_user_lang(self, user_id):
        """Get the language preference for a private chat user."""
        return self.user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    async def apply_group_permissions(self, chat_id):
        """Apply full permissions to the group based on its settings"""
        try:
            group_locked = bool(int(await self.db.get_group_setting(chat_id, "GROUP_LOCK", 0)))
            gif_locked = bool(int(await self.db.get_group_setting(chat_id, "GIF_LOCK", 0)))
            inline_locked = bool(int(await self.db.get_group_setting(chat_id, "INLINE_LOCK", 0)))
            
            permissions = types.ChatPermissions(
                can_send_messages=not group_locked,
                can_send_photos=not group_locked,
                can_send_videos=not group_locked,
                can_send_documents=not group_locked,
                can_send_stickers=not group_locked,
                can_send_animations=not (group_locked or gif_locked),
                can_send_audios=not group_locked,
                can_send_voices=not group_locked,
                can_send_video_notes=not group_locked,
                can_send_polls=not group_locked,
                can_send_other_messages=not (group_locked or inline_locked),
            )
            await self.bot.set_chat_permissions(chat_id, permissions)
        except Exception as e:
            print(f"Permission apply error: {e}")

    @staticmethod
    def sender_chat_id(message):
        sender_chat = getattr(message, 'sender_chat', None)
        return sender_chat.id if sender_chat else None

    async def send_welcome(self, message, user):
        template = await self.db.member_template(message.chat.id)
        text = template
        text = text.replace("{name}", user.first_name)
        text = text.replace("{username}", f"@{user.username}" if user.username else user.first_name)
        text = text.replace("{id}", str(user.id))
        text = text.replace("{chat}", message.chat.title)
        try:
            member_count = await self.bot.get_chat_member_count(message.chat.id)
        except Exception:
            member_count = "نامشخص"
        text = text.replace("{members}", str(member_count))
        await self.bot.send_message(message.chat.id, text)

    async def check_raid(self, chat_id):
        now = time.time()
        window = int(await self.db.get_group_setting(chat_id, "RAID_WINDOW", 30))
        threshold = int(await self.db.get_group_setting(chat_id, "RAID_THRESHOLD", 5))
        stamps = self.join_tracker.setdefault(chat_id, [])
        stamps.append(now)
        self.join_tracker[chat_id] = [s for s in stamps if now - s <= window]
        if len(self.join_tracker[chat_id]) >= threshold:
            self.raid_active[chat_id] = now
            return True
        return False

    async def is_raid_active(self, chat_id):
        until = self.raid_active.get(chat_id, 0)
        return time.time() - until < 60

    async def start_captcha(self, message, user):
        chat_id = message.chat.id
        lang = await self.get_lang(chat_id)
        key = (chat_id, user.id)
        timeout = int(await self.db.get_group_setting(chat_id, "CAPTCHA_TIMEOUT", 300))
        try:
            await self.bot.restrict_chat_member(
                chat_id, user.id,
                until_date=int(time.time()) + timeout + 60,
                can_send_messages=False
            )
        except Exception:
            pass
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        answer = a + b
        options = [answer]
        while len(options) < 4:
            o = answer + random.randint(-3, 3)
            if o > 0 and o != answer and o not in options:
                options.append(o)
        random.shuffle(options)
        token = secrets.token_hex(4)
        kb = types.InlineKeyboardMarkup(row_width=2)
        for o in options:
            kb.add(types.InlineKeyboardButton(str(o), callback_data=f"captcha:{chat_id}:{token}:{o}"))
        msg = await self.bot.send_message(
            chat_id,
            f"[{user.first_name}](tg://user?id={user.id}) " + ("برای اثبات انسان بودن، حاصل جمع را انتخاب کن" if lang == "fa" else "Choose the sum to prove you're human") + f":\n\n{a} + {b} = ؟",
            parse_mode="Markdown",
            reply_markup=kb
        )
        task = asyncio.create_task(self.captcha_timeout(chat_id, user.id, token, timeout))
        self.captchas[key] = {"answer": answer, "attempts": 0, "msg_id": msg.message_id, "token": token, "task": task}

    async def captcha_timeout(self, chat_id, user_id, token, timeout):
        await asyncio.sleep(timeout)
        key = (chat_id, user_id)
        entry = self.captchas.get(key)
        if entry and entry.get("token") == token:
            try:
                await self.bot.delete_message(chat_id, entry["msg_id"])
            except Exception:
                pass
            try:
                await self.bot.ban_chat_member(chat_id, user_id)
                await self.bot.unban_chat_member(chat_id, user_id)
            except Exception:
                pass
            self.captchas.pop(key, None)

    async def captcha_success(self, chat_id, user_id, user_name):
        lang = await self.get_lang(chat_id)
        try:
            await self.bot.restrict_chat_member(
                chat_id, user_id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_send_other_messages=True
            )
        except Exception:
            pass
        await self.bot.send_message(chat_id, t("captcha_correct_welcome", lang, name=user_name, id=user_id), parse_mode="Markdown")

    def build_pretty_keyboard(self, items, back_buttons=None):
        """Keyboard with a mixed layout: first and last items get full-width rows,
        the middle items are paired two-per-row. `items` is a list of (text, callback_data).
        `back_buttons` (list of (text, callback_data)) are appended as full-width rows."""
        kb = types.InlineKeyboardMarkup(row_width=2)
        n = len(items)
        if n <= 2:
            rows = [items] if items else []
        else:
            rows = [[items[0]]]
            for i in range(1, n - 1, 2):
                rows.append(items[i:i + 2])
            if (n - 1) % 2 == 1:
                rows.append([items[-1]])
        for row in rows:
            if len(row) == 1:
                kb.row(types.InlineKeyboardButton(row[0][0], callback_data=row[0][1]))
            else:
                kb.add(*[types.InlineKeyboardButton(t, callback_data=c) for t, c in row])
        if back_buttons:
            for t, c in back_buttons:
                kb.row(types.InlineKeyboardButton(t, callback_data=c))
        return kb

    async def build_lock_panel(self, chat_id, row_width=5):
        lang = await self.get_lang(chat_id)
        kb = types.InlineKeyboardMarkup(row_width=row_width)
        lock_keys = ["link", "forward", "swear", "group", "gif", "spam", "flood", "inline", "raid", "captcha"]
        buttons = []
        for latin in lock_keys:
            on = int(await self.db.get_group_setting(chat_id, latin.upper() + "_LOCK", 0)) == 1
            lock_name = t(f"lock_name_{latin}", lang)
            buttons.append(types.InlineKeyboardButton(
                f"{lock_name} {'✅' if on else '❌'}",
                callback_data=f"lock_{latin}:" + ("off" if on else "on")
            ))
        kb.add(*buttons)
        return kb

    async def open_lock_panel(self, chat_id):
        """Build the lock panel with extended row_width and a back button to the global panel.
        The origin is remembered so toggles re-render in place."""
        self.lock_panel_origin[chat_id] = "global"
        lang = await self.get_lang(chat_id)
        lock_kb = await self.build_lock_panel(chat_id, row_width=5)
        lock_kb.add(types.InlineKeyboardButton(t("panel_back_to_main", lang), callback_data="panel_main"))
        return lock_kb

    async def build_global_panel(self, chat_id):
        lang = await self.get_lang(chat_id)
        punishment_map = {"kick": t("punishment_kick", lang), "ban": t("punishment_ban", lang), "mute": t("punishment_mute", lang)}

        lines = [t("panel_main_title", lang)]
        lines.append(t("panel_settings_header", lang))
        polite = int(await self.db.get_group_setting(chat_id, "POLITE_MODE", 1)) == 1
        public = int(await self.db.get_group_setting(chat_id, "PUBLIC_COMMANDS", 1)) == 1
        raid_threshold = await self.db.get_group_setting(chat_id, "RAID_THRESHOLD", 5)
        raid_window = await self.db.get_group_setting(chat_id, "RAID_WINDOW", 30)
        warn_max = await self.db.get_group_setting(chat_id, "WARN_MAXIMUM", 3)
        warn_punishment = punishment_map.get(await self.db.get_group_setting(chat_id, "WARN_PUNISHMENT", "kick"), t("punishment_kick", lang))
        invite_max = await self.db.get_group_setting(chat_id, "invite_maximum", t("panel_unlimited", lang))
        lines.append(f"• {t('panel_bot_tone', lang)}: {t('panel_tone_polite', lang) if polite else t('panel_tone_rude', lang)}")
        lines.append(f"• {t('panel_public_cmds', lang)}: {t('panel_on', lang) if public else t('panel_off', lang)}")
        lines.append(f"• {t('panel_raid_info', lang)}: {raid_threshold} | {t('panel_raid_window', lang)}: {raid_window} {t('panel_seconds', lang)}")
        lines.append(f"• {t('panel_warn_max', lang)}: {warn_max} | {t('panel_warn_punish', lang)}: {warn_punishment}")
        lines.append(f"• {t('panel_invite_max', lang)}: {invite_max}")
        text = "\n".join(lines)

        kb = self.build_pretty_keyboard([
            (t("panel_locks_btn", lang), "panel_locks"),
            (f"{t('panel_polite_btn', lang)} {'✅' if polite else '❌'}", "panel_polite"),
            (f"{t('panel_public_btn', lang)} {'✅' if public else '❌'}", "panel_public"),
            (t("panel_guide_btn", lang), "help_main"),
            (t("panel_close_btn", lang), "close_panel"),
        ])
        return text, kb

    def setup_events(self):
        check = lambda require_admin=False: handler_check(self.bot, self.db, self.anti_spam, require_admin)

        # ===== Owner-only DB restore (private chat) =====
        # Registered first so document updates reach it before the text-based
        # owner handlers below (whose `m.text.startswith(...)` filters would
        # raise AttributeError on document messages and abort handler dispatch).
        @self.bot.message_handler(commands=['restore_db'], func=lambda m: m.chat.type == "private")
        async def ask_db_restore(message: types.Message):
            if message.from_user.id != OWNER_ID:
                await self.bot.reply_to(message, "تو اونر بات نیستی")
                return
            self.awaiting_db_restore = True
            await self.bot.reply_to(
                message,
                "📥 لطفاً فایل بکاپ دیتابیس (با پسوند .db یا .sqlite) را همین‌جا در پیوی ارسال کنید.\n\n"
                "❌ برای لغو: /cancel_restore"
            )

        @self.bot.message_handler(commands=['cancel_restore'], func=lambda m: m.chat.type == "private")
        async def cancel_db_restore(message: types.Message):
            if message.from_user.id != OWNER_ID:
                return
            if self.awaiting_db_restore:
                self.awaiting_db_restore = False
                await self.bot.reply_to(message, "❌ بازیابی دیتابیس لغو شد.")
            else:
                await self.bot.reply_to(message, "هیچ درخواست بازیابی فعالی وجود ندارد.")

        @self.bot.message_handler(func=lambda m: m.chat.type == "private" and m.from_user and m.from_user.id == OWNER_ID, content_types=['document'])
        async def handle_db_restore_file(message: types.Message):
            if not self.awaiting_db_restore:
                return ContinueHandling()
            file_name = (message.document.file_name or "").lower()
            if not file_name.endswith((".db", ".sqlite", ".sqlite3")):
                await self.bot.reply_to(
                    message,
                    "❌ فرمت فایل معتبر نیست! فقط فایل با پسوند .db یا .sqlite بفرستید.\n\n"
                    "❌ برای لغو: /cancel_restore"
                )
                return
            status_msg = await self.bot.reply_to(message, "⏳ در حال دریافت و بررسی فایل بکاپ...")
            tmp_path = None
            try:
                file_info = await self.bot.get_file(message.document.file_id)
                file_bytes = await self.bot.download_file(file_info.file_path)
                if not file_bytes.startswith(b"SQLite format 3\x00"):
                    await self.bot.edit_message_text(
                        "❌ فایل ارسال‌شده یک دیتابیس SQLite معتبر نیست!",
                        message.chat.id, status_msg.message_id
                    )
                    return
                tmp_path = DB_PATH + ".restore_tmp"
                with open(tmp_path, "wb") as f:
                    f.write(file_bytes)
                # Validate: must open as sqlite and contain the bot's core tables
                try:
                    con = sqlite3.connect(tmp_path)
                    cur = con.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = {row[0] for row in cur.fetchall()}
                    con.close()
                except Exception:
                    tables = set()
                required_tables = {"groups", "group_settings"}
                if not required_tables.issubset(tables):
                    os.remove(tmp_path)
                    tmp_path = None
                    await self.bot.edit_message_text(
                        "❌ فایل ارسال‌شده بکاپ معتبر کمک‌یار نیست (جداول اصلی پیدا نشد)!",
                        message.chat.id, status_msg.message_id
                    )
                    return
                # Backup current db before overwriting
                if os.path.exists(DB_PATH):
                    backup_path = f"{DB_PATH}.bak.{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}"
                    shutil.copy2(DB_PATH, backup_path)
                # Atomic replace
                os.replace(tmp_path, DB_PATH)
                tmp_path = None
                self.awaiting_db_restore = False
                # Ensure any missing tables from newer versions exist
                try:
                    await self.db.init_db()
                except Exception:
                    pass
                await self.bot.edit_message_text(
                    "✅ دیتابیس با موفقیت بازیابی شد و جایگزین دیتابیس فعلی شد!",
                    message.chat.id, status_msg.message_id
                )
            except Exception as e:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
                try:
                    await self.bot.edit_message_text(
                        f"❌ خطا در بازیابی دیتابیس:\n{str(e)[:1000]}",
                        message.chat.id, status_msg.message_id
                    )
                except Exception:
                    await self.bot.reply_to(message, f"❌ خطا در بازیابی دیتابیس: {e}")
                await send_error_to_owner(f"Error in db restore: {e}\n{traceback.format_exc()}", OWNER_ID, self.bot, "DB_RESTORE_ERROR")

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "activate"))
        async def cmd_startgroup(message):
            if await self.db.is_group_blocked(message.chat.id):
                return
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if await self.db.is_group_active(message.chat.id):
                await self.bot.reply_to(message, t("group_already_active" if polite else "group_already_active_rude", lang))
                return
            if not await self.db.is_admin(message.chat.id, message.from_user.id, self.sender_chat_id(message)):
                await self.bot.reply_to(message, t("no_admin_permission" if polite else "no_admin_permission_rude", lang))
                return
            await self.db.ensure_group(message.chat.id)
            await self.db.set_group_active(message.chat.id)
            await self.bot.reply_to(message, t("group_activated", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "leave"))
        @check(require_admin=True)
        async def leaver(message):
            lang = await self.get_lang(message.chat.id)
            await self.bot.reply_to(message, t("bot_leave", lang))
            await self.bot.leave_chat(message.chat.id)


        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "help"))
        @check()
        async def send_help(message):
            lang = await self.get_lang(message.chat.id)
            try:
                await self.bot.send_message(message.from_user.id, HELP_TEXT, parse_mode="Markdown", reply_markup=self.help_keyboard)
                if message.chat.type != "private":
                    await self.bot.reply_to(message, t("help_sent_pv", lang))
            except Exception:
                await self.bot.reply_to(message, t("help_pv_blocked", lang))


        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "reset"))
        @check(require_admin=True)
        async def reset_bot_in_group(message):
            lang = await self.get_lang(message.chat.id)
            msg = await self.bot.reply_to(message, t("reset_start", lang))
            await self.db.reset_group(message.chat.id)
            await self.bot.edit_message_text(t("reset_done", lang), message.chat.id, msg.id)

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "set_max_invite") is not None or m.text.startswith("تنظیم حداکثر دعوت"))
        @check(require_admin=True)
        async def change_maximum(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            remainder = cmd_startswith(message.text, "set_max_invite")
            if remainder is None:
                remainder = message.text[len("تنظیم حداکثر دعوت"):].strip()
            if remainder.isdigit():
                maximum = int(remainder)
                await self.db.set_group_setting(message.chat.id, "invite_maximum", maximum)
                if bool(int(await self.db.get_group_setting(message.chat.id, "creates_request", 0))):
                    await self.db.delete_group_setting(message.chat.id, "creates_request")
                await self.bot.reply_to(message, t("invite_max_set", lang, maximum=maximum))
            else:
                await self.bot.reply_to(message, t("invite_max_invalid", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "swear_lock_on"))
        @check(require_admin=True)
        async def active_swear_strict(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "SWEAR_LOCK", 0)) in [-1, 1]:
                await self.db.set_group_setting(message.chat.id, "SWEAR_LOCK", 1)
                await self.bot.reply_to(message, t("swear_lock_on_already" if polite else "swear_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "SWEAR_LOCK", 1)
                await self.bot.reply_to(message, t("swear_lock_on", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "swear_lock_off"))
        @check(require_admin=True)
        async def deactivate_swear(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "SWEAR_LOCK", 0)) in [-1, 0]:
                await self.db.set_group_setting(message.chat.id, "SWEAR_LOCK", 0)
                await self.bot.reply_to(message, t("swear_lock_off_already" if polite else "swear_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "SWEAR_LOCK", 0)
                await self.bot.reply_to(message, t("swear_lock_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "group_lock_on"))
        @check(require_admin=True)
        async def lock_group(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "GROUP_LOCK", 0)) == 0:
                await self.db.set_group_setting(message.chat.id, "GROUP_LOCK", 1)
                await self.bot.reply_to(message, t("group_lock_on" if polite else "group_lock_on_rude", lang))
                await self.apply_group_permissions(message.chat.id)
            else:
                await self.bot.reply_to(message, t("group_lock_on_already" if polite else "group_lock_on_already_rude", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "group_lock_off"))
        @check(require_admin=True)
        async def unlock_group(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "GROUP_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("group_lock_off_already" if polite else "group_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "GROUP_LOCK", 0)
                await self.bot.reply_to(message, t("group_lock_off" if polite else "group_lock_off_rude", lang))
                await self.apply_group_permissions(message.chat.id)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "be_rude"))
        @check(require_admin=True)
        async def turn_rude(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            if int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1:
                await self.db.set_group_setting(message.chat.id, "POLITE_MODE", 0)
                await self.bot.reply_to(message, t("rude_changed", lang))
            else:
                await self.bot.reply_to(message, t("rude_already", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "be_polite"))
        @check(require_admin=True)
        async def turn_polite(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            if int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1:
                await self.bot.reply_to(message, t("polite_already", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "POLITE_MODE", 1)
                await self.bot.reply_to(message, t("polite_changed", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "link_lock_on"))
        @check(require_admin=True)
        async def link_blocker(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "LINK_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("link_lock_on_already" if polite else "link_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "LINK_LOCK", 1)
                await self.bot.reply_to(message, t("link_lock_on", lang))

        @self.bot.message_handler(func= lambda m: cmd_match(m.text, "link_lock_off"))
        @check(require_admin=True)
        async def link_unblocking(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "LINK_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("link_lock_off_already" if polite else "link_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "LINK_LOCK", 0)
                await self.bot.reply_to(message, t("link_lock_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "forward_lock_on"))
        @check(require_admin=True)
        async def forward_blocker(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "FORWARD_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("forward_lock_on_already" if polite else "forward_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "FORWARD_LOCK", 1)
                await self.bot.reply_to(message, t("forward_lock_on", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "forward_lock_off"))
        @check(require_admin=True)
        async def forward_unblocking(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "FORWARD_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("forward_lock_off_already" if polite else "forward_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "FORWARD_LOCK", 0)
                await self.bot.reply_to(message, t("forward_lock_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "gif_lock_on"))
        @check(require_admin=True)
        async def gif_lock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "GIF_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("gif_lock_on_already" if polite else "gif_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "GIF_LOCK", 1)
                await self.bot.reply_to(message, t("gif_lock_on", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "gif_lock_off"))
        @check(require_admin=True)
        async def gif_unlock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "GIF_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("gif_lock_off_already" if polite else "gif_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "GIF_LOCK", 0)
                await self.bot.reply_to(message, t("gif_lock_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "raid_lock_on"))
        @check(require_admin=True)
        async def raid_lock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "RAID_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("raid_lock_on_already" if polite else "raid_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "RAID_LOCK", 1)
                await self.bot.reply_to(message, t("raid_lock_on", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "raid_lock_off"))
        @check(require_admin=True)
        async def raid_unlock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "RAID_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("raid_lock_off_already" if polite else "raid_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "RAID_LOCK", 0)
                await self.bot.reply_to(message, t("raid_lock_off", lang))

        @self.bot.message_handler(func=lambda m: m.text.startswith("تنظیم سقف حمله ") or m.text.lower().startswith("raid threshold "))
        @check(require_admin=True)
        async def raid_threshold(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            if message.text.startswith("تنظیم سقف حمله "):
                val = message.text[len("تنظیم سقف حمله "):].strip()
            else:
                val = message.text[len("raid threshold "):].strip()
            if val.isdigit():
                await self.db.set_group_setting(message.chat.id, "RAID_THRESHOLD", int(val))
                await self.bot.reply_to(message, t("raid_threshold_set", lang, val=val))
            else:
                await self.bot.reply_to(message, t("invalid_number", lang))

        @self.bot.message_handler(func=lambda m: m.text.startswith("تنظیم بازه حمله ") or m.text.lower().startswith("raid window "))
        @check(require_admin=True)
        async def raid_window(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            if message.text.startswith("تنظیم بازه حمله "):
                val = message.text[len("تنظیم بازه حمله "):].strip()
            else:
                val = message.text[len("raid window "):].strip()
            if val.isdigit():
                await self.db.set_group_setting(message.chat.id, "RAID_WINDOW", int(val))
                await self.bot.reply_to(message, t("raid_window_set", lang, val=val))
            else:
                await self.bot.reply_to(message, t("invalid_number", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "captcha_lock_on"))
        @check(require_admin=True)
        async def captcha_lock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "CAPTCHA_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("captcha_lock_on_already" if polite else "captcha_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "CAPTCHA_LOCK", 1)
                await self.bot.reply_to(message, t("captcha_lock_on", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "captcha_lock_off"))
        @check(require_admin=True)
        async def captcha_unlock(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "CAPTCHA_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("captcha_lock_off_already" if polite else "captcha_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "CAPTCHA_LOCK", 0)
                await self.bot.reply_to(message, t("captcha_lock_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "lock_panel"))
        @check(require_admin=True)
        async def lock_panel(message: types.Message):
            reply_to = message.reply_to_message
            is_comment = False
            self.lock_panel_origin.pop(message.chat.id, None)
            lock_keyboard = await self.build_lock_panel(message.chat.id)
            while reply_to:
                if reply_to.is_automatic_forward:
                    is_comment = True
                    break
                else:
                    if reply_to.reply_to_message:
                        reply_to = reply_to.reply_to_message
                    else:
                        reply_to = None
                        break
            if is_comment:
                post_lock = await self.db.post_lock_status(reply_to.chat.id, reply_to.message_id)
                lock_keyboard.add(
                    types.InlineKeyboardButton("قفل پست ✅" if post_lock else "قفل پست ❌", callback_data="post_" + "lock" if not post_lock else "unlock")
                )
            lock_keyboard.add(
                types.InlineKeyboardButton("بستن پنل قفل", callback_data="close_lock_panel")
            )
            lang = await self.get_lang(message.chat.id)
            await self.bot.reply_to(message, t("lock_panel_desc", lang), reply_markup=lock_keyboard)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "panel"))
        @check(require_admin=True)
        async def global_panel(message: types.Message):
            text, kb = await self.build_global_panel(message.chat.id)
            await self.bot.reply_to(message, text, parse_mode="Markdown", reply_markup=kb)

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "public_cmds") is not None or m.text.startswith("دستورات عمومی"))
        @check(require_admin=True)
        async def public_commands(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            remainder = cmd_startswith(message.text, "public_cmds")
            if remainder is None:
                remainder = message.text.replace("دستورات عمومی", "").strip()
            if remainder in ("روشن", "on"):
                if await self.db.get_group_setting(message.chat.id, "PUBLIC_COMMANDS", 1) == 1:
                    await self.bot.reply_to(message, t("public_commands_on_already" if polite else "public_commands_on_already_rude", lang))
                    return
                else:
                    await self.db.set_group_setting(message.chat.id, "PUBLIC_COMMANDS", 1)
                    await self.bot.reply_to(message, t("public_commands_on", lang))
            elif remainder in ("خاموش", "off"):
                if await self.db.get_group_setting(message.chat.id, "PUBLIC_COMMANDS", 1) == 0:
                    await self.bot.reply_to(message, t("public_commands_off_already" if polite else "public_commands_off_already_rude", lang))
                    return
                else:
                    await self.db.set_group_setting(message.chat.id, "PUBLIC_COMMANDS", 0)
                    await self.bot.reply_to(message, t("public_commands_off", lang))

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "block_word") is not None or m.text.startswith("مسدود کلمه "))
        @check(require_admin=True)
        async def block_word(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            remainder = cmd_startswith(message.text, "block_word")
            if remainder is None:
                remainder = message.text.replace("مسدود کلمه", "").strip()
            await self.db.block_word(message.chat.id, remainder)
            await self.bot.reply_to(message, t("word_blocked", lang, word=remainder))

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "unblock_word") is not None or m.text.startswith("بازکردن کلمه "))
        @check(require_admin=True)
        async def unblock_word(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            remainder = cmd_startswith(message.text, "unblock_word")
            if remainder is None:
                remainder = message.text.replace("بازکردن کلمه", "").strip()
            await self.db.unblock_word(message.chat.id, remainder)
            await self.bot.reply_to(message, t("word_unblocked", lang, word=remainder))

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "block_bot") is not None or m.text.startswith("بلاک بات "))
        @check(require_admin=True)
        async def block_bot_handler(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            remainder = cmd_startswith(message.text, "block_bot")
            if remainder is None:
                remainder = message.text.replace("بلاک بات ", "").strip()
            bot_username = remainder.replace("@", "")
            await self.db.block_bot(message.chat.id, bot_username)
            await self.bot.reply_to(message, t("bot_blocked", lang, username=bot_username))

        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "unblock_bot") is not None or m.text.startswith("آن‌بلاک بات "))
        @check(require_admin=True)
        async def unblock_bot_handler(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            remainder = cmd_startswith(message.text, "unblock_bot")
            if remainder is None:
                remainder = message.text.replace("آن‌بلاک بات ", "").strip()
            bot_username = remainder.replace("@", "")
            await self.db.unblock_bot(message.chat.id, bot_username)
            await self.bot.reply_to(message, t("bot_unblocked", lang, username=bot_username))
        
        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "post_lock"))
        @check(require_admin=True)
        async def lock_comment_post(message: types.Message):
            reply_to = message.reply_to_message
            is_comment = False
            while reply_to:
                if reply_to.is_automatic_forward:
                    is_comment = True
                    break
                else:
                    if reply_to.reply_to_message:
                        reply_to = reply_to.reply_to_message
                    else:
                        reply_to = None
                        break
            if is_comment:
                lang = await self.get_lang(message.chat.id)
                polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE",1)) == 1
                await self.db.lock_post(message.reply_to_message.chat.id, message.reply_to_message.message_id)
                await self.bot.reply_to(message, t("post_locked" if polite else "post_locked_rude", lang))
            else:
                lang = await self.get_lang(message.chat.id)
                await self.bot.reply_to(message, t("post_lock_not_comment", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "post_unlock"))
        @check(require_admin=True)
        async def unlock_comment_post(message: types.Message):
            reply_to = message.reply_to_message
            is_comment = False
            while reply_to:
                if reply_to.is_automatic_forward:
                    is_comment = True
                    break
                else:
                    if reply_to.reply_to_message:
                        reply_to = reply_to.reply_to_message
                    else:
                        reply_to = None
                        break
            if is_comment:
                lang = await self.get_lang(message.chat.id)
                polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE",1)) == 1
                await self.db.unlock_post(message.reply_to_message.chat.id, message.reply_to_message.id)
                await self.bot.reply_to(message, t("post_unlocked" if polite else "post_unlocked_rude", lang))
            else:
                lang = await self.get_lang(message.chat.id)
                await self.bot.reply_to(message, t("post_lock_not_comment", lang))

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "spam_lock_on"))
        @check(require_admin=True)
        async def spam_lock_on(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "SPAM_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("spam_lock_on_already" if polite else "spam_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "SPAM_LOCK", 1)
                await self.bot.reply_to(message, t("spam_lock_on", lang))


        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "spam_lock_off"))
        @check(require_admin=True)
        async def spam_lock_off(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "SPAM_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("spam_lock_off_already" if polite else "spam_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "SPAM_LOCK", 0)
                await self.bot.reply_to(message, t("spam_lock_off", lang))
                
        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "flood_lock_on"))
        @check(require_admin=True)
        async def flood_lock_on(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "FLOOD_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("flood_lock_on_already" if polite else "flood_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "FLOOD_LOCK", 1)
                await self.bot.reply_to(message, t("flood_lock_on", lang))
                
        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "flood_lock_off"))
        @check(require_admin=True)
        async def flood_lock_off(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "FLOOD_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("flood_lock_off_already" if polite else "flood_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "FLOOD_LOCK", 0)
                await self.bot.reply_to(message, t("flood_lock_off", lang))
                
        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "inline_lock_on"))
        @check(require_admin=True)
        async def inline_lock_on(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "INLINE_LOCK", 0)) == 1:
                await self.bot.reply_to(message, t("inline_lock_on_already" if polite else "inline_lock_on_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "INLINE_LOCK", 1)
                await self.bot.reply_to(message, t("inline_lock_on", lang))
        
        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "inline_lock_off"))
        @check(require_admin=True)
        async def inline_lock_off(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
            if int(await self.db.get_group_setting(message.chat.id, "INLINE_LOCK", 0)) == 0:
                await self.bot.reply_to(message, t("inline_lock_off_already" if polite else "inline_lock_off_already_rude", lang))
            else:
                await self.db.set_group_setting(message.chat.id, "INLINE_LOCK", 0)
                await self.bot.reply_to(message, t("inline_lock_off", lang))
                

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "request_help"))
        @check(require_admin=True)
        async def request_help_group(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            confirm_keyboard = types.InlineKeyboardMarkup()
            ok_button = types.InlineKeyboardButton(t("help_request_confirm_title", lang), callback_data="ok_btn")
            cancel_button = types.InlineKeyboardButton(t("help_request_cancel_title", lang), callback_data="cancel_req")
            confirm_keyboard.add(ok_button, cancel_button)
            await self.bot.reply_to(message, t("help_request_sent", lang), reply_markup=confirm_keyboard)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "blocked_bots_list"))
        @check(require_admin=True)
        async def blocked_bots(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            blocked_bots = await self.db.get_botBlocks(message.chat.id)
            if not blocked_bots:
                await self.bot.reply_to(message, t("no_blocked_bots", lang))
                return
            string = t("blocked_bots_list", lang) + "\n"
            for bot_username in blocked_bots:
                string += f" - @{bot_username}\n"
            await self.bot.reply_to(message, string)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "join_request"))
        @check(require_admin=True)
        async def toggle_request(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            await self.bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji('👍')])
            toggle = bool(int(await self.db.get_group_setting(message.chat.id, "creates_request", 0)))
            markup = types.InlineKeyboardMarkup()
            if toggle:
                button_off = types.InlineKeyboardButton("خاموش کردن", callback_data="request:off")
                markup.add(button_off)
            else:
                button_on = types.InlineKeyboardButton("روشن کردن", callback_data="request:on")
                markup.add(button_on)
            await self.bot.reply_to(message, t("request_status", lang, status="روشن" if toggle else "خاموش"), reply_markup=markup)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "get_link"))
        @check(require_admin=False)
        async def create_invite_link(message):
            lang = await self.get_lang(message.chat.id)
            try:
                lnk = await self.bot.create_chat_invite_link(
                    chat_id=message.chat.id,
                    name=f"Link by {message.from_user.first_name}",
                    member_limit=int(await self.db.get_group_setting(message.chat.id, "invite_maximum", 0)),
                    creates_join_request=bool(int(await self.db.get_group_setting(message.chat.id, "creates_request", 0)))
                )
                await self.bot.reply_to(
                    message,
                    t("invite_link_created", lang, link=lnk.invite_link)
                )
            except Exception:
                await self.bot.reply_to(
                    message,
                    t("invite_link_no_permission", lang)
                )

            

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "filters_list"))
        @check(require_admin=False)
        async def all_filters(message:types.Message):
            lang = await self.get_lang(message.chat.id)
            filters = await self.db.get_tags(message.chat.id)
            string = t("filters_list_header", lang) + "\n"
            for filter, response in filters.items():
                string += f"{filter} : {response}\n"
            await self.bot.reply_to(message, string)

        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "set_warn_punish"))
        @check(require_admin=True)
        async def set_warn_punish(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            warn_punish = await self.db.get_group_setting(message.chat.id, "WARN_PUNISHMENT", "kick")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(f'کیک {"✅" if warn_punish == "kick" else "❌"}', callback_data="warn_punish:kick"),
                types.InlineKeyboardButton(f'بن {"✅" if warn_punish == "ban" else "❌"}', callback_data="warn_punish:ban"),
                types.InlineKeyboardButton(f'میوت {"✅" if warn_punish == "mute" else "❌"}', callback_data="warn_punish:mute")
            )
            await self.bot.reply_to(message, t("warn_punish_select", lang), reply_markup=keyboard)


        @self.bot.message_handler(func=lambda m: cmd_startswith(m.text, "echo") is not None or m.text.startswith("اکو "))
        @check(require_admin=False)
        async def echo_word(message:types.Message):
            remainder = cmd_startswith(message.text, "echo")
            if remainder is None:
                remainder = message.text[len("اکو"):].strip()
            if message.reply_to_message:
                await self.bot.reply_to(message.reply_to_message, t("echo_sent", "en", name=message.from_user.first_name, text=remainder))
            else:
                await self.bot.send_message(message.chat.id, t("echo_sent", "en", name=message.from_user.first_name, text=remainder))
            await self.bot.delete_message(message.chat.id, message.message_id)


        @self.bot.message_handler(func=lambda m: cmd_match(m.text, "rules"))
        async def show_group_rules(message):
            lang = await self.get_lang(message.chat.id)
            rules = await self.db.get_group_rules(message.chat.id) or t("no_rules", lang)
            try:
                await self.bot.reply_to(message, rules, parse_mode="HTML")
            except ApiTelegramException:
                await self.bot.reply_to(message, rules)



        @self.bot.message_handler(content_types=["new_chat_members"])
        async def greet(message):
            if not await self.db.is_group_active(message.chat.id) or await self.db.is_group_blocked(message.chat.id):
                return

            if message.new_chat_members[0].id == self.me.id:
                lang = await self.get_lang(message.chat.id)
                await self.bot.send_message(message.chat.id, t("welcome_bot_added", lang, channel=BOT_CHANNEL, group=BOT_GROUP), parse_mode="Markdown", disable_web_page_preview=True)
                return

            for user in message.new_chat_members:
                if user.id == self.me.id:
                    continue

                if int(await self.db.get_group_setting(message.chat.id, "RAID_LOCK", 0)) == 1:
                    triggered = await self.check_raid(message.chat.id)
                    if triggered or await self.is_raid_active(message.chat.id):
                        mute_minutes = int(await self.db.get_group_setting(message.chat.id, "RAID_MUTE_MINUTES", 60))
                        try:
                            await self.bot.restrict_chat_member(
                                message.chat.id, user.id,
                                until_date=int(time.time()) + mute_minutes * 60,
                                can_send_messages=False
                            )
                        except Exception:
                            pass
                        if triggered:
                            lang = await self.get_lang(message.chat.id)
                            await self.bot.send_message(
                                message.chat.id,
                                t("raid_detected", lang, minutes=mute_minutes)
                            )
                        continue

                if int(await self.db.get_group_setting(message.chat.id, "CAPTCHA_LOCK", 0)) == 1 and not await self.db.is_admin(message.chat.id, user.id):
                    key = (message.chat.id, user.id)
                    if key not in self.captchas:
                        await self.start_captcha(message, user)
                    continue

                await self.send_welcome(message, user)


        @self.bot.inline_handler(func=lambda q: True)
        async def send_whisper(inline_query: types.InlineQuery):
            query = inline_query.query.strip()
            results = []

            if not query:
                help_result = types.InlineQueryResultArticle(
                    id="help",
                    title=t("whisper_help_title", "en"),
                    description=t("whisper_help_text", "en", bot=self.me.username),
                    input_message_content=types.InputTextMessageContent(
                        message_text=t("whisper_help_text", "fa", bot=self.me.username)
                    )
                )
                results.append(help_result)
            else:
                parts = query.rsplit("@", 1)

                if len(parts) == 2:
                    message_text = parts[0].strip()
                    target_username = parts[1].strip()


                    
                    if message_text and target_username:

                        if inline_query.chat_type == "private":
                            await self.bot.answer_inline_query(inline_query.id, [], cache_time=0, switch_pm_text=t("whisper_cannot_pv", "en"), switch_pm_parameter="invalid_context")
                            return

                        elif target_username == inline_query.from_user.username:
                            await self.bot.answer_inline_query(inline_query.id, [], cache_time=0, switch_pm_text=t("whisper_cannot_self", "en"), switch_pm_parameter="invalid_target")
                            return
                        elif target_username == self.me.username:
                            await self.bot.answer_inline_query(inline_query.id, [], cache_time=0, switch_pm_text=t("whisper_cannot_bot", "en"), switch_pm_parameter="invalid_target")
                            return
                        elif len(message_text) > 200:
                            await self.bot.answer_inline_query(inline_query.id, [], cache_time=0, switch_pm_text=t("whisper_too_long", "en"))

                        target = "@" + target_username

                        try:
                            await self.bot.get_chat(target)
                        except Exception:
                            pass


                        timestamp = int(time.time())
                        token = f"wh#{inline_query.from_user.id}:{target_username}:{timestamp}"

                        

                        result_send = types.InlineQueryResultArticle(
                            id=f"wh:{token}",
                            title=f"ارسال پیام به {target}",
                            description=f"پیام شما:\n{message_text[:40] if len(message_text) > 40 else message_text}\n\nبرای ارسال این پیام به {target}، روی این پیام کلیک کنید.",
                            input_message_content=types.InputTextMessageContent(
                                message_text=f"💬 نجوا ارسال شده توسط @{inline_query.from_user.username}\n🗣️ برای {target}"
                            ),
                            reply_markup=types.InlineKeyboardMarkup().add(
                                types.InlineKeyboardButton("نمایش پیام", callback_data=f"showmsg:{token}")
                            )
                        )
                        results.append(result_send)
            await self.bot.answer_inline_query(inline_query.id, results, cache_time=0)
        
        @self.bot.chosen_inline_handler(func=lambda ch: True)
        async def chosen_inline(inline_result: types.ChosenInlineResult):
            query = inline_result.query
            result_id = inline_result.result_id

            if result_id.startswith("wh:"):
            
                token = result_id.split(":", 1)[1]
                infos = token.split("#")[1]
                sender_id = int(infos.split(":")[0])
                receiver_username = infos.split(":")[1]
                target_chat = None
                try:
                    target_chat = await self.bot.get_chat("@" + receiver_username)
                except Exception:
                    pass
                parts = query.rsplit("@", 1)
                message_text = parts[0].strip()
                timestamp = infos.split(":")[2]

                key = base64.urlsafe_b64encode(hashlib.sha256(token.encode('utf-8')).digest())
                f = Fernet(key)
                encrypted_text = f.encrypt(message_text.encode('utf-8'))
                encrypted_str = base64.b64encode(encrypted_text).decode('utf-8')

                await self.db.store_whisper(
                    token=token,
                    sender_id=sender_id,
                    receiver_username=receiver_username.lower(),
                    receiver_id=target_chat.id if target_chat else None,
                    whisper=encrypted_str,
                    timestamp=timestamp
                )

        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_handler(call: types.CallbackQuery):
            try:
                data = call.data
                if ((data.startswith(("lock_", "post_", "panel_", "request:", "warn_punish:"))
                        or data in ("close_panel", "close_lock_panel"))
                        and not await self.db.is_admin(call.message.chat.id, call.from_user.id)):
                    cb_lang = await self.get_lang(call.message.chat.id)
                    cb_polite = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                    await self.bot.answer_callback_query(
                        call.id,
                        t("callback_no_admin" if cb_polite else "callback_no_admin_rude", cb_lang),
                        show_alert=True,
                    )
                    return
                if data.startswith("captcha:"):
                    parts = data.split(":")
                    if len(parts) == 4:
                        _, chat_id_s, token, chosen_s = parts
                        chat_id = int(chat_id_s)
                        chosen = int(chosen_s)
                        user_id = call.from_user.id
                        key = (chat_id, user_id)
                        entry = self.captchas.get(key)
                        cap_lang = await self.get_lang(chat_id)
                        if not entry or entry.get("token") != token:
                            await self.bot.answer_callback_query(call.id, t("captcha_expired", cap_lang), show_alert=True)
                            return
                        if chosen == entry["answer"]:
                            if entry.get("task"):
                                entry["task"].cancel()
                            try:
                                await self.bot.delete_message(chat_id, entry["msg_id"])
                            except Exception:
                                pass
                            self.captchas.pop(key, None)
                            await self.captcha_success(chat_id, user_id, call.from_user.first_name)
                            await self.bot.answer_callback_query(call.id, t("captcha_correct", cap_lang))
                        else:
                            entry["attempts"] += 1
                            if entry["attempts"] >= 3:
                                if entry.get("task"):
                                    entry["task"].cancel()
                                try:
                                    await self.bot.delete_message(chat_id, entry["msg_id"])
                                except Exception:
                                    pass
                                self.captchas.pop(key, None)
                                try:
                                    await self.bot.ban_chat_member(chat_id, user_id)
                                    await self.bot.unban_chat_member(chat_id, user_id)
                                except Exception:
                                    pass
                                await self.bot.answer_callback_query(call.id, t("captcha_wrong_ban", cap_lang), show_alert=True)
                            else:
                                await self.bot.answer_callback_query(call.id, t("captcha_wrong", cap_lang, remaining=3 - entry['attempts']), show_alert=True)
                    return

                if data.startswith("showmsg:"):
                    token = data.removeprefix("showmsg:")
                    datab = await self.db.get_whisper(token)
                    if not datab:
                        await self.bot.answer_callback_query(call.id, "این پیام منقضی شده یا وجود ندارد", show_alert=True)
                        return
                    
                    if (call.from_user.id == datab["sender_id"]) or (call.from_user.username.lower() == datab["receiver_username"]) or (call.from_user.id == datab["receiver_id"]):
                        encrypted_str = datab["whisper"]
                        encrypted = base64.b64decode(encrypted_str)
                        key = base64.urlsafe_b64encode(hashlib.sha256(token.encode('utf-8')).digest())
                        f = Fernet(key)
                        message_text = f.decrypt(encrypted).decode('utf-8')
                        text = f"{message_text}"
                        await self.bot.answer_callback_query(call.id, text, show_alert=True)
                    else:
                        await self.bot.answer_callback_query(call.id, "شما اجازه دیدن این پیام را ندارید", show_alert=True)
                        return
                    


                elif data.startswith("lock_"):
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    
                    reply_to = call.message.reply_to_message
                    is_comment = False
                    setting = data.split(":")[0].split("_")[1]
                    toggle = data.split(":")[1]
                    
                    current_value = int(await self.db.get_group_setting(call.message.chat.id, setting.upper() + "_LOCK", 0))
                    if (current_value == 1 and toggle == "on") or (current_value == 0 and toggle == "off"):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("already_in_this_state", lang_cb) if polite_cb else t("already_in_this_state_rude", lang_cb))
                        return
                    
                    await self.db.set_group_setting(call.message.chat.id, setting.upper() + "_LOCK", 1 if toggle == "on" else 0)
                    await self.apply_group_permissions(call.message.chat.id)
                    
                    
                    lang_lock = await self.get_lang(call.message.chat.id)
                    polite_lock = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                    lock_name = t(f"lock_name_{setting}", lang_lock)
                    if polite_lock:
                        status_text = t("lock_status_changed", lang_lock, name=lock_name, status=t("lock_status_locked" if toggle == 'on' else "lock_status_unlocked", lang_lock))
                    else:
                        status_text = t("lock_status_changed_rude", lang_lock, name=lock_name, status=t("lock_status_locked" if toggle == 'on' else "lock_status_unlocked", lang_lock))
                    await self.bot.answer_callback_query(call.id, status_text)
                    
                    
                    origin = self.lock_panel_origin.get(call.message.chat.id)
                    if origin == "global":
                        lock_keyboard = await self.open_lock_panel(call.message.chat.id)
                        await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=lock_keyboard)
                        return

                    lock_keyboard = await self.build_lock_panel(call.message.chat.id)
                    

                    while reply_to:
                        if reply_to.is_automatic_forward:
                            is_comment = True
                            break
                        else:
                            if reply_to.reply_to_message:
                                reply_to = reply_to.reply_to_message
                            else:
                                reply_to = None
                                break
                    if is_comment:
                        post_lock = await self.db.post_lock_status(call.message.chat.id, reply_to.message_id)
                        lock_keyboard.add(
                            types.InlineKeyboardButton(t("panel_post_lock_on", lang_lock) if post_lock else t("panel_post_lock_off", lang_lock), callback_data="post_" + ("lock" if not post_lock else "unlock"))
                        )
                    
                    lock_keyboard.add(types.InlineKeyboardButton(t("panel_close_lock_panel", lang_lock), callback_data="close_lock_panel"))
                    
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=lock_keyboard)

                elif data.startswith("post_"):
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb), show_alert=True)
                        return
                    reply_to = call.message.reply_to_message
                    is_comment = False
                    while reply_to:
                        if reply_to.is_automatic_forward:
                            is_comment = True
                            break
                        else:
                            if reply_to.reply_to_message:
                                reply_to = reply_to.reply_to_message
                            else:
                                reply_to = None
                                break
                    data = call.data
                    status = data.split("_")[1]
                    chat_id = reply_to.chat.id
                    post_id = reply_to.message_id
                    if status == "lock":
                        await self.db.lock_post(chat_id, post_id)
                    else:
                        await self.db.unlock_post(chat_id, post_id)
                    lang_post = await self.get_lang(call.message.chat.id)
                    status_label = t("post_lock_activated", lang_post) if status == "lock" else t("post_lock_deactivated", lang_post)
                    await self.bot.answer_callback_query(call.id, t("post_lock_status_changed", lang_post, status=status_label))
                    lock_keyboard = await self.build_lock_panel(call.message.chat.id)

                    if is_comment:
                        post_lock = await self.db.post_lock_status(chat_id, post_id)
                        lock_keyboard.add(
                            types.InlineKeyboardButton(t("panel_post_lock_on", lang_post) if post_lock else t("panel_post_lock_off", lang_post), callback_data="post_" + ("lock" if not post_lock else "unlock"))
                        )
                    lock_keyboard.add(
                        types.InlineKeyboardButton(t("panel_close_lock_panel", lang_post), callback_data="close_lock_panel")
                    )
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=lock_keyboard)


                elif data == "close_lock_panel":
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    lang_cp = await self.get_lang(call.message.chat.id)
                    await self.bot.edit_message_text(t("panel_closed_by_admin", lang_cp), call.message.chat.id, call.message.message_id)
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

                elif data == "panel_locks":
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    lang_pl = await self.get_lang(call.message.chat.id)
                    lock_kb = await self.open_lock_panel(call.message.chat.id)
                    await self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=t("lock_panel_title_full", lang_pl),
                        parse_mode="Markdown",
                        reply_markup=lock_kb
                    )

                elif data == "panel_main":
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    self.lock_panel_origin.pop(call.message.chat.id, None)
                    text, kb = await self.build_global_panel(call.message.chat.id)
                    await self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=kb)

                elif data.startswith("panel_"):
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    setting = data.split("_")[1]
                    key = "POLITE_MODE" if setting == "polite" else "PUBLIC_COMMANDS"
                    current = int(await self.db.get_group_setting(call.message.chat.id, key, 1))
                    await self.db.set_group_setting(call.message.chat.id, key, 0 if current == 1 else 1)
                    text, kb = await self.build_global_panel(call.message.chat.id)
                    await self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=kb)
                    lang_su = await self.get_lang(call.message.chat.id)
                    await self.bot.answer_callback_query(call.id, t("settings_updated_callback", lang_su))

                elif data == "close_panel":
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    lang_cp = await self.get_lang(call.message.chat.id)
                    await self.bot.edit_message_text(t("panel_closed_by_admin", lang_cp), call.message.chat.id, call.message.message_id)
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

                elif data.startswith("warn_punish:"):
                    punish_type = data.split(":")[1]
                    if not await self.db.is_admin(call.message.chat.id, call.from_user.id):
                        polite_cb = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                        lang_cb = await self.get_lang(call.message.chat.id)
                        await self.bot.answer_callback_query(call.id, t("callback_no_admin", lang_cb) if polite_cb else t("callback_no_admin_rude", lang_cb), show_alert=True)
                        return
                    await self.db.set_group_setting(call.message.chat.id, "WARN_PUNISHMENT", punish_type)
                    lang_wp = await self.get_lang(call.message.chat.id)
                    polite_wp = int(await self.db.get_group_setting(call.message.chat.id, "POLITE_MODE", 1)) == 1
                    punish_map = {
                        "kick": t("punishment_kick", lang_wp),
                        "ban": t("punishment_ban", lang_wp),
                        "mute": t("punishment_mute", lang_wp),
                    }
                    punish_label = punish_map.get(punish_type, punish_type)
                    if polite_wp:
                        await self.bot.answer_callback_query(call.id, t("warn_punish_changed", lang_wp, type=punish_label), show_alert=True)
                    else:
                        await self.bot.answer_callback_query(call.id, t("warn_punish_changed_rude", lang_wp, type=punish_label), show_alert=True)
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(
                        types.InlineKeyboardButton(f"{t('punishment_kick', lang_wp)} {'✅' if punish_type == 'kick' else '❌'}", callback_data="warn_punish:kick"),
                        types.InlineKeyboardButton(f"{t('punishment_ban', lang_wp)} {'✅' if punish_type == 'ban' else '❌'}", callback_data="warn_punish:ban"),
                        types.InlineKeyboardButton(f"{t('punishment_mute', lang_wp)} {'✅' if punish_type == 'mute' else '❌'}", callback_data="warn_punish:mute")
                    )
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

                elif data == "ok_btn":
                    lang_ok = await self.get_lang(call.message.chat.id)
                    link = await self.bot.create_chat_invite_link(call.message.chat.id, "CREATED FOR OWNER HELP REQUEST", member_limit=1)
                    markup = types.InlineKeyboardMarkup()
                    goGroup_btn = types.InlineKeyboardButton(t("go_to_group", lang_ok), link.invite_link)
                    markup.add(goGroup_btn)
                    await self.bot.send_message(OWNER_ID, t("help_request_received", lang_ok, title=call.message.chat.title, id=call.message.chat.id),
                                     reply_markup=markup)
                    await self.bot.edit_message_text(t("help_request_confirmed_callback", lang_ok), call.message.chat.id, call.message.message_id)

                elif data == "cancel_req":
                    lang_cr = await self.get_lang(call.message.chat.id)
                    await self.bot.edit_message_text(t("help_request_cancelled_callback", lang_cr), call.message.chat.id, call.message.message_id)

                elif data.startswith("request:"):
                    toggle = data.split(":")[1]
                    if toggle == "on":
                        await self.db.delete_group_setting(call.message.chat.id, "invite_maximum")
                    await self.db.set_group_setting(call.message.chat.id, "creates_request", "1" if toggle == "on" else "0")
                    lang_rq = await self.get_lang(call.message.chat.id)
                    await self.bot.answer_callback_query(call.id, t("request_off", lang_rq) if toggle == "off" else t("request_on", lang_rq))
                    await self.bot.delete_message(call.message.chat.id, call.message.message_id)

                elif data.startswith("swear:"):
                    array = data.split(":")[1]
                    await self.bot.answer_callback_query(call.id, f'لیست فحش های :\n {" - ".join(eval(array))}')

                elif data.startswith("check:"):
                    rep_id = data.split(":")[1]
                    await self.db.check_report(rep_id)
                    lang_ch = await self.get_lang(call.message.chat.id)
                    await self.bot.answer_callback_query(call.id, t("report_checked", lang_ch))
                    await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

                elif data.startswith("setlang:"):
                    lang = data.split(":")[1]
                    if lang in SUPPORTED_LANGUAGES:
                        self.user_languages[call.from_user.id] = lang
                        await self.bot.answer_callback_query(call.id, t("language_set", lang, language=lang))
                        await self.bot.edit_message_text(t("language_set", lang, language=lang), call.message.chat.id, call.message.message_id)
                    else:
                        await self.bot.answer_callback_query(call.id, t("language_invalid", self.get_user_lang(call.from_user.id)), show_alert=True)

                elif data.startswith("help_"):
                    lang_h = await self.get_lang(call.message.chat.id)
                    if data == "help_main":
                        self.lock_panel_origin.pop(call.message.chat.id, None)
                        await self.bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=HELP_TEXT,
                            parse_mode="Markdown",
                            reply_markup=self.help_keyboard
                        )
                    elif data in self.guide_categories:
                        cat = self.guide_categories[data]
                        if cat.get("direct"):
                            await self.bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=self.guide_texts[data],
                                parse_mode="Markdown",
                                reply_markup=self.back_keyboard
                            )
                        else:
                            items = [(sub_title, sub_cb) for sub_cb, sub_title in cat["subs"]]
                            kb = self.build_pretty_keyboard(items, back_buttons=[(t("back_to_menu", lang_h), "help_main")])
                            await self.bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f"📂 **{cat['title']}**\n\n{t('guide_select_topic', lang_h)}",
                                parse_mode="Markdown",
                                reply_markup=kb
                            )
                    elif data in self.guide_texts:
                        parent = self.guide_sub_parent.get(data, "help_main")
                        kb = self.build_pretty_keyboard([], back_buttons=[(t("back_to_category", lang_h), parent), (t("back_to_menu", lang_h), "help_main")])
                        await self.bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=self.guide_texts[data],
                            parse_mode="Markdown",
                            reply_markup=kb
                        )
                    await self.bot.answer_callback_query(call.id)
            except Exception as e:
                error_text = f"callback_handler: {e!s}\n{traceback.format_exc()}"
                await send_error_to_owner(error_text, OWNER_ID, self.bot, "CALLBACK_ERROR")

        @self.bot.message_handler(commands=['bangroup'])
        async def ban_group(message: types.Message):
            if message.from_user.id != OWNER_ID:
                await self.bot.reply_to(message, "تو اونر بات نیستی")
                return
            if not message.text.startswith("/bangroup "):
                await self.bot.reply_to(message, "فرمت پیامت اشتباهه")
                return
            group_id = message.text.replace("/bangroup ", "")
            if not await self.db.is_group_blocked(group_id):
                await self.db.ban_group(group_id)
                await self.bot.reply_to(message, "گروه دریافتی با موفقیت بن شد و قادر به کار با ربات نیست")
                await self.bot.send_message(group_id, "درود، متاسفانه، این گروه از کمک‌یــار بن شده و اعضا و ادمین های آن دیگر قادر به کار با ربات نیستند")
            else:
                await self.bot.reply_to(message, "گروه از قبل هم بن شده بود")

        @self.bot.message_handler(commands=['unbangroup'])
        async def unban_group(message: types.Message):
            if message.from_user.id != OWNER_ID:
                await self.bot.reply_to(message, "فقط به حرف اونر گوش میدم")
                return
            if not message.text.startswith("/unbangroup "):
                await self.bot.reply_to(message, "فرمت پیام اشتباه است")
                return
            group_id = message.text.replace("/unbangroup ", "")
            if await self.db.is_group_blocked(group_id):
                await self.db.unban_group(group_id)
                await self.bot.reply_to(message, "گروه دریافتی با موفقیت از حالت مسدودی درآمد")
                await self.bot.send_message(group_id, "خبر خوب، گروه شما از حالت مسدودی خارج شده و همگی دوباره قادر به استفاده از ربات هستند")
            else:
                await self.bot.reply_to(message, "گروه که اصلا بن نشده بود بخوای آن‌بن کنی")

        @self.bot.message_handler(commands=['update'])
        async def handle_update_command(message):
            if message.from_user.id != OWNER_ID:
                await self.bot.reply_to(message, "فقط اونر می‌تونه آپدیت پخش کنه!")
                return

            text = message.text.strip()
            lines = text.splitlines()

            if len(lines) < 1:
                return

            first_line = lines[0].strip()

            version_match = re.search(r'/update\s+([vV]?\d+\.\d+(\.\d+)?)', first_line, re.IGNORECASE)

            if not version_match:
                await self.bot.reply_to(message, 
                    "❌ فرمت اشتباه!\n\n"
                    "مثال:\n"
                    "/update v1.2.5\n"
                    "یا\n"
                    "/update 1.2.5\n"
                    "سپس تغییرات رو در خطوط بعدی بنویس")
                return

            full_version = version_match.group(1)       
            display_version = full_version if full_version.lower().startswith('v') else f"v{full_version}"


            updates = []
            for line in lines[1:]:
                stripped = line.strip()
                if stripped and not stripped.startswith('/'):
                    if not stripped.startswith('•'):
                        stripped = '• ' + stripped
                    updates.append(stripped)

            if not updates:
                await self.bot.reply_to(message, "❌ هیچ آپدیتی نوشته نشده!")
                return

            preview = f"*نسخه جدید ربات کمک‌یار (***{display_version}***) منتشر شد!*\n\n"
            for upd in updates:
                preview += f"{upd}\n"

            await self.bot.reply_to(message, 
                        f"✅ در حال پخش آپدیت {display_version} به همه گروه‌ها...\n\n"
                        f"پیش‌نمایش:\n{preview}", 
                        parse_mode="Markdown")

            try:
                success, err = await self.db.update_message(updates, full_version.lstrip('vV'))
                
                await self.bot.reply_to(message, 
                            f"✅ پخش آپدیت تموم شد!\n\n"
                            f"ارسال موفق: {success} گروه\n"
                            f"خطا یا بلاک شده: {err} گروه")
            except Exception as e:
                await self.bot.reply_to(message, f"❌ خطا در پخش آپدیت: {e!s}")
                

        @self.bot.message_handler(func=lambda m: m.chat.type == "private")
        async def pv_chats(message:types.Message):
            if message.text == "/start":
                user_lang = self.get_user_lang(message.from_user.id)
                await self.bot.send_message(
                    message.chat.id,
                    t("start_pv", user_lang, channel=BOT_CHANNEL, group=BOT_GROUP, version=VERSION),
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=self.start_keyboard
                )
            elif message.text == "/help":
                await self.bot.send_message(
                    message.from_user.id, 
                    HELP_TEXT, 
                    parse_mode="Markdown", 
                    reply_markup=self.help_keyboard
                )
            elif message.text in ("/language", "/lang", "زبان"):
                user_lang = self.get_user_lang(message.from_user.id)
                current = "فارسی (fa)" if user_lang == "fa" else "English (en)"
                await self.bot.send_message(
                    message.chat.id,
                    f"🌐 Current language: {current}\n\n"
                    f"Choose your language / زبان خود را انتخاب کنید:",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="setlang:fa"),
                        types.InlineKeyboardButton("🇬🇧 English", callback_data="setlang:en"),
                    )
                )
            elif message.text and message.text.startswith("/language ") or (message.text and message.text.startswith("/lang ")):
                parts = message.text.split()
                if len(parts) >= 2:
                    new_lang = parts[1].strip().lower()
                    if new_lang in SUPPORTED_LANGUAGES:
                        self.user_languages[message.from_user.id] = new_lang
                        await self.bot.send_message(message.chat.id, t("language_set", new_lang, language=new_lang))
                    else:
                        await self.bot.send_message(message.chat.id, t("language_invalid", self.get_user_lang(message.from_user.id)))

        @self.bot.message_handler(commands=['start'], func=lambda m: m.chat.type in ["group", "supergroup"])
        async def group_starts(message: types.Message):
            lang = await self.get_lang(message.chat.id)
            await self.bot.reply_to(message, t("welcome_group_start", lang, channel=BOT_CHANNEL, group=BOT_GROUP), disable_web_page_preview=True)

        @self.bot.message_handler(func= lambda m: m.from_user and m.from_user.id == OWNER_ID and (m.text or "").startswith("db:"))
        async def execute_to_db(message):
            try:
                query = message.text.split(":", 1)[1]
                async with aiosqlite.connect(DB_PATH) as con:
                    cur = await con.execute(query)
                    rows = await cur.fetchall()
                    if rows:
                        await self.bot.reply_to(message, f"Hello Master, These are the responses : \n {json.dumps(rows, ensure_ascii=False)}")
                    else:
                        await con.commit()
                        await self.bot.reply_to(message, "Hello Master, query executed successfully ✅")
            except Exception as e:
                await self.bot.reply_to(message, f"ریدی ارور گرفتم \n {e}")

        @self.bot.message_handler(func= lambda m: m.from_user.id == OWNER_ID and m.text == ";id;")
        async def id_informations_owner(message: types.Message):
            if message.reply_to_message:
                await self.bot.reply_to(message, f"اطلاعات فرد مشخص شده : \n"
                f"آیدی فرد : {message.reply_to_message.from_user.id}\n"
                f"آیدی پیام : {message.reply_to_message.id}\n")
            else:
                await self.bot.reply_to(message, f"آیدی گروه : {message.chat.id}\n")

        @self.bot.message_handler(func= lambda m: m.from_user.id == OWNER_ID and m.text.startswith("(tag): "))
        async def make_id_into_tag(message: types.Message):
            user_id = message.text.replace("(tag): ", "").strip()
            await self.bot.reply_to(message, f"[HereYouGo](tg://user?id={user_id})", parse_mode="Markdown")

        @self.bot.channel_post_handler(func=lambda m: m.text.startswith("/setbridge "))
        async def set_bridge(message: types.Message):
            if not message.text.startswith("/setbridge "):
                await self.bot.reply_to(message, "فرمت دستور اشتباه است")
                return
            target_chat_id = message.text.replace("/setbridge ", "").strip()
            if not target_chat_id:
                await self.bot.reply_to(message, "لطفا آیدی گروه مقصد را وارد کنید\n برای انجام این کار میتوانید در کانال مقصد خود که کمک‌یـــــار را عضو ان کرده اید و بعنوان ادمین انتخاب کرده اید از دستور /getid استفاده کنید و آیدی گروه را دریافت کنید")
                return
            try:
                chat = await self.bale_bot.get_chat(target_chat_id)
            except Exception as e:
                await self.bot.reply_to(message, "چنین کانالی ای وجود ندارد یا من به آن دسترسی ندارم")
                await send_error_to_owner(f"Error in set_bridge: {e!s}\n{traceback.format_exc()}", OWNER_ID, self.bot, "SET_BRIDGE_ERROR")
                return
            await self.db.set_bridge(message.chat.id, target_chat_id)
            await self.bot.reply_to(message, f"پل ارتباطی با کانال {chat.title} با موفقیت تنظیم شد")

        @self.bot.channel_post_handler(func=lambda m: m.text.startswith("/removebridge "))
        async def remove_bridge(message: types.Message):
            if not message.text.startswith("/removebridge "):
                await self.bot.reply_to(message, "فرمت دستور اشتباه است")
                return
            target_chat_id = message.text.replace("/removebridge ", "").strip()
            if not target_chat_id:
                await self.bot.reply_to(message, "لطفا آیدی کانال مقصد را وارد کنید\n برای انجام این کار میتوانید در کانال مقصد خود که کمک‌یـــــار را عضو ان کرده اید و بعنوان ادمین انتخاب کرده اید از دستور /getid استفاده کنید و آیدی کانال را دریافت کنید")
                return
            await self.db.remove_bridge(message.chat.id)
            await self.bot.reply_to(message, f"پل ارتباطی با کانال {target_chat_id} با موفقیت حذف شد")

        @self.bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'animation', 'video_note'])
        async def handle_telegram_bridge(message: types.Message):
            if (message.from_user and message.from_user.id == self.me.id) or \
                (message.sender_chat and message.sender_chat.id == self.me.id):
                return
            
            bale_chat_id = await self.db.get_bale_bridge_channel(message.chat.id)
            if not bale_chat_id:
                return

            try:
                text = ""
                if message.forward_origin:
                    text = f"فوروارد شده از [{message.forward_origin.chat.title}](https://t.me/{message.forward_origin.chat.username})\n\n"
                text = text + ((message.text or message.caption) or "")

                if message.text:
                    await self.bale_bot.send_message(bale_chat_id, text)

                elif message.photo:
                    photo = message.photo[-1]
                    file_info = await self.bot.get_file(photo.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    
                    input_file = InputFile(downloaded, file_name="photo.jpg")
                    await self.bale_bot.send_photo(bale_chat_id, input_file, caption=text)

                elif message.video:
                    file_info = await self.bot.get_file(message.video.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    input_file = InputFile(downloaded, file_name="video.mp4")
                    await self.bale_bot.send_video(bale_chat_id, input_file, caption=text)

                elif message.document:
                    file_info = await self.bot.get_file(message.document.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    file_name = message.document.file_name or "document"
                    input_file = InputFile(downloaded, file_name=file_name)
                    await self.bale_bot.send_document(bale_chat_id, input_file, caption=text)

                elif message.animation:
                    file_info = await self.bot.get_file(message.animation.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    input_file = InputFile(downloaded, file_name="animation.gif")
                    await self.bale_bot.send_animation(bale_chat_id, input_file, caption=text)

                elif message.sticker:
                    file_info = await self.bot.get_file(message.sticker.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    input_file = InputFile(downloaded, file_name="sticker.webp")
                    await self.bale_bot.send_sticker(bale_chat_id, input_file)

                elif message.voice:
                    file_info = await self.bot.get_file(message.voice.file_id)
                    downloaded = await self.bot.download_file(file_info.file_path)
                    input_file = InputFile(downloaded, file_name="voice.ogg")
                    await self.bale_bot.send_voice(bale_chat_id, input_file)

            except Exception:
                error_text = f"Telegram → Bale Bridge Error:\n{traceback.format_exc()}"
                print(error_text)
                await send_error_to_owner(error_text, OWNER_ID, self.bot, "BRIDGE_TG_TO_BALE")

        @self.bale_bot.on_message()
        async def get_id(message: Message):
            if message.text and message.text == "/getid" and message.chat.type == ChatType.CHANNEL:
                await self.bale_bot.send_message(message.chat.id, f"آیدی کانال : {message.chat.id}")

        @self.bale_bot.on_message()
        async def handle_bale_bridge(message: Message):
            if message.chat.type == ChatType.CHANNEL:
                if (message.sender_chat and message.sender_chat.id == self.me.id):
                    return
                bridge = await self.db.get_telegram_bridge_channel(message.chat.id)
                if not bridge:
                    return
                telegram_chat_id = bridge
                try:
                    text = ""
                    if message.forward_from_chat:
                        text = f"فوروارد شده از [{message.forward_from_chat['title']}](https://ble.ir/{message.forward_from_chat['username']})\n\n"
                    text = text + ((message.text or message.caption) or "")
                    text = parse_strip(text)

                    if message.text:
                        await self.bot.send_message(telegram_chat_id, text, parse_mode="Markdown")

                    elif message.photo:
                        photo = message.photo[-1]
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{photo['file_id']}") as resp:
                                data = await resp.read()
                        photo_file = BytesIO(data)
                        photo_file.name = "photo.jpg"
                        await self.bot.send_photo(telegram_chat_id, photo_file, caption=text, parse_mode="Markdown")

                    elif message.video:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{message.video['file_id']}") as resp:
                                data = await resp.read()
                        video_file = BytesIO(data)
                        video_file.name = message.video.get("file_name", "video.mp4")
                        await self.bot.send_video(telegram_chat_id, video_file, caption=text, parse_mode="Markdown")

                    elif message.animation:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{message.animation.file_id}") as resp:
                                data = await resp.read()
                        animation_file = BytesIO(data)
                        animation_file.name = message.animation.file_name or "animation.gif"
                        await self.bot.send_animation(telegram_chat_id, animation_file, caption=text, parse_mode="Markdown")

                    elif message.sticker:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{message.sticker.file_id}") as resp:
                                data = await resp.read()
                        sticker_file = BytesIO(data)
                        sticker_file.name = "sticker.webp"
                        await self.bot.send_sticker(telegram_chat_id, sticker_file, parse_mode="Markdown")

                    elif message.voice:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{message.voice.file_id}") as resp:
                                data = await resp.read()
                        voice_file = BytesIO(data)
                        voice_file.name = "voice.ogg"
                        await self.bot.send_voice(telegram_chat_id, voice_file, caption=text, parse_mode="Markdown")

                    elif message.document:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"https://tapi.bale.ai/file/bot{BALE_TOKEN}/{message.document.file_id}") as resp:
                                data = await resp.read()
                        document_file = BytesIO(data)
                        document_file.name = message.document.file_name or"document.pdf"
                        await self.bot.send_document(telegram_chat_id, document_file, caption=text, parse_mode="Markdown")

                    else:
                        await self.bot.send_message(telegram_chat_id, "نوع محتوا ناشناخته")
                except Exception as e:
                    error_text = f"Error in Bale Bridge: {e!s}\n{traceback.format_exc()}"
                    await send_error_to_owner(error_text, OWNER_ID, self.bot, "BALE_BRIDGE_ERROR")


        @self.bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'animation', 'video_note'])
        async def handle_messages(message:types.Message):
            try:
                chat_id = message.chat.id
                user_id = message.from_user.id if message.from_user else (self.sender_chat_id(message) or None)
                sender_chat_id = self.sender_chat_id(message)
                text = (message.text or message.caption) or ""
                message.text = text
                is_comment = False
                reply_to = message.reply_to_message
                comment_channel = message.reply_to_message
                swears: list[str] = []
                is_swear = False

                
                if await self.db.is_group_blocked(chat_id):
                    return

                if not await self.db.is_group_active(chat_id):
                    return

                # Track message count for stats
                if user_id and not sender_chat_id and not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                    await self.db.increment_msg_count(chat_id, user_id)
                
                if (int(await self.db.get_group_setting(chat_id, "SPAM_LOCK", 0)) == 1 or
                    int(await self.db.get_group_setting(chat_id, "FLOOD_LOCK", 0)) == 1):
                    
                    if not text:
                        if message.sticker:
                            text = f"sticker:{message.sticker.file_unique_id}"
                        elif message.animation:
                            text = f"animation:{message.animation.file_unique_id}"
                        elif message.document:
                            text = f"document:{message.document.file_unique_id}"
                        else:
                            text = f"{message.content_type}:{message.message_id}"
                    spam_result = await self.anti_spam.check(chat_id, user_id, text)
                    if spam_result[0] is not None:
                        violation, count = spam_result
                        try:
                            await self.bot.delete_message(chat_id, message.message_id)
                        except ApiTelegramException:
                            pass
                        try:
                            await self.bot.restrict_chat_member(
                                chat_id, 
                                user_id, 
                                until_date=int(time.time()) + 300,
                                can_send_messages=False
                            )
                        except ApiTelegramException:
                            pass
                        self.anti_spam.reset_user(chat_id, user_id)
                        # Deduct from stats on spam/flood
                        if user_id and not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.db.deduct_msg_count(chat_id, user_id, "spam")
                        user_name = message.from_user.first_name if message.from_user else "کاربر"
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.send_message(
                                chat_id,
                                f'[{user_name}](tg://user?id={user_id}) {"اسپم" if violation == "spam" else "فلاد"} نکن! ۵ دقیقه سکوت داده شدی 🔇',
                                parse_mode="Markdown"
                            )
                            return
                        else:
                            await self.bot.send_message(
                                chat_id,
                                f'[{user_name}](tg://user?id={user_id}) {"اسپم" if violation == "spam" else "فلاد"} کردی، حیف که ادمینی وگرنه میوتت میکردم',
                                parse_mode="Markdown"
                            )

                if message.document and not message.animation:
                    file_name = message.document.file_name or ""
                    ext = file_name.split('.')[-1].lower() if '.' in file_name else ""
                    file_size = message.document.file_size or 0

                    if ext != "gif":
                        supported_exts = {
                            'txt', 'py', 'js', 'html', 'css', 'json', 'xml', 
                            'md', 'csv', 'log', 'sh', 'bat', 'ps1', 'php', 'java',
                            'cs', 'cpp', 'c', 'h', 'hpp', 'rb', 'pl', 'go', 'rs',
                        }

                        if ext not in supported_exts:
                            await self.bot.set_message_reaction(
                                chat_id, 
                                message.message_id, 
                                [types.ReactionTypeEmoji('🥴')]  # Unsupported type
                            )
                        elif file_size > MAX_ANTIVIRUS_FILE_SIZE:
                            await self.bot.set_message_reaction(
                                chat_id, 
                                message.message_id, 
                                [types.ReactionTypeEmoji('🥴')]  # Too large to download & scan
                            )
                        else:
                            await self.bot.set_message_reaction(
                                chat_id, 
                                message.message_id, 
                                [types.ReactionTypeEmoji('🤔')]  # Scanning
                            )
                            try:
                                # Download file
                                file_info = await self.bot.get_file(message.document.file_id)
                                downloaded = await self.bot.download_file(file_info.file_path)
                                
                                # Try to read as text (fallback to empty if binary)
                                try:
                                    content = downloaded.decode('utf-8', errors='ignore')
                                except Exception:
                                    content = str(downloaded)[:10000]  # fallback

                                if content.strip():
                                    is_malware, _prob = self.anti_virus.is_malware(content)
                                    
                                    if is_malware:
                                        await self.bot.set_message_reaction(
                                            chat_id, 
                                            message.message_id, 
                                            [types.ReactionTypeEmoji('👾')]  # Malware detected
                                        )
                                    else:
                                        await self.bot.set_message_reaction(
                                            chat_id, 
                                            message.message_id, 
                                            [types.ReactionTypeEmoji('👍')]  # Clean
                                        )
                                else:
                                    await self.bot.set_message_reaction(
                                        chat_id, 
                                        message.message_id, 
                                        [types.ReactionTypeEmoji('❓')] # Not Sure
                                    )
                            except Exception as e:
                                error_text = f"handle_malwares: {e!s}\n{traceback.format_exc()}"
                                await send_error_to_owner(error_text, OWNER_ID, self.bot, "MAIN_ERROR")
                                await self.bot.set_message_reaction(
                                    chat_id, 
                                    message.message_id, 
                                    [types.ReactionTypeEmoji('🤯')] # ERR
                                )

                
                while reply_to:
                    if reply_to.is_automatic_forward:
                        is_comment = True
                        break
                    else:
                        if reply_to.reply_to_message:
                            reply_to = reply_to.reply_to_message
                        else:
                            reply_to = None
                            break

                if int(await self.db.get_group_setting(chat_id, "GROUP_LOCK", 0)) == 1 and not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                    await self.bot.delete_message(chat_id, message.message_id)

                if (int(await self.db.get_group_setting(chat_id, "GIF_LOCK", 0)) == 1
                        and message.content_type == "animation"
                        and not await self.db.is_admin(chat_id, user_id, sender_chat_id)):
                    await self.bot.delete_message(chat_id, message.message_id)

                if message.via_bot:
                    lock = await self.db.get_group_setting(chat_id, "INLINE_LOCK", 0)
                    if int(lock) == 1 and not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        await self.bot.delete_message(chat_id, message.message_id)
                        return
                    bot_username = message.via_bot.username
                    blocked_bots = await self.db.get_botBlocks(message.chat.id)
                    if bot_username in blocked_bots:
                        await self.bot.delete_message(message.chat.id, message.message_id)
                        return
                    
                if message.is_automatic_forward:
                    msg = await self.db.get_comment_message(chat_id)
                    await self.bot.reply_to(message, msg)

                if is_comment:
                    post = await self.db.post_lock_status(message.reply_to_message.chat.id, message.reply_to_message.id)
                    if post:
                        await self.bot.delete_message(message.chat.id, message.message_id)
                    
                if await self.db.get_group_setting(chat_id, "LINK_LOCK", 0) and re.search(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", text):
                    await self.bot.delete_message(chat_id, message.message_id)
                    return

                text_lower = text.lower()
                tokens_lower = [t.lower() for t in text.split()]
                for blocked in await self.db.blocked_words(chat_id):
                    blocked = blocked.strip()
                    if not blocked:
                        continue
                    if len(blocked.split()) > 1:
                        if blocked.lower() in text_lower:
                            swears.append(blocked)
                    elif blocked.lower() in tokens_lower:
                        swears.append(blocked)

                if int(await self.db.get_group_setting(chat_id, "SWEAR_LOCK", 0)) == 1:
                    is_swear_flag, accuracy = self.profanity_detector.is_swear(text)

                    if is_swear_flag and accuracy >= 0.75:
                        is_swear = True
                        swears.append("swear detected by model")


                if (len(swears) != 0) or is_swear:
                    # Deduct from stats on swear
                    if user_id and not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        await self.db.deduct_msg_count(chat_id, user_id, "swear")
                    lang = await self.get_lang(chat_id)
                    user_name = message.from_user.first_name if message.from_user else ("کاربر" if lang == "fa" else "user")
                    await self.bot.reply_to(comment_channel if is_comment else message, t("swear_warning", lang, name=user_name, id=user_id), parse_mode="Markdown")
                    await self.bot.delete_message(chat_id, message.message_id)

                toggle = await self.db.get_group_setting(message.chat.id, "PUBLIC_COMMANDS", 1)
                if not await self.db.is_admin(message.chat.id, user_id, sender_chat_id) and int(toggle) == 0:
                    return

                if text.startswith("db:"):
                    lang = await self.get_lang(chat_id)
                    polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                    await self.bot.reply_to(message, t("bot_owner_only_tag" if polite else "bot_owner_only_tag_rude", lang))

                if text in ("کمک یار", "کمک\u200cیار", "komakyaar", "about"):
                    lang = await self.get_lang(chat_id)
                    await self.bot.reply_to(message, t("bot_name_reply", lang, name=message.from_user.first_name if message.from_user else ("کاربر" if lang == "fa" else "user")))

                # ===================== LANGUAGE SET (GROUP) =====================
                if text.startswith(("تنظیم زبان", "set language")):
                    if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(chat_id, "POLITE_MODE", 1)) == 1
                        await self.bot.reply_to(message, t("no_admin_permission" if polite else "no_admin_permission_rude", lang))
                        return
                    parts = text.split()
                    if len(parts) >= 3:
                        new_lang = parts[2].strip().lower()
                        if new_lang in SUPPORTED_LANGUAGES:
                            await self.db.set_group_setting(chat_id, "LANGUAGE", new_lang)
                            await self.bot.reply_to(message, t("language_set_group", new_lang, language=new_lang))
                        else:
                            await self.bot.reply_to(message, t("language_invalid", await self.get_lang(chat_id)))
                    else:
                        await self.bot.reply_to(message, t("language_invalid", await self.get_lang(chat_id)))
                    return

                tags = await self.db.get_tags(chat_id)
                for k, r in tags.items():
                    if text == k:
                        await self.bot.reply_to(message, r)
                        break

                if text.startswith(("سقف اخطار", "set warn max", "warn max")):
                    lang = await self.get_lang(chat_id)
                    polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                    if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        await self.bot.reply_to(message, t("no_admin_permission" if polite else "no_admin_permission_rude", lang))
                        return
                    words = text.split()
                    num_str = words[-1] if words else ""
                    if num_str.isdigit():
                        digit = convert_digit(num_str)
                        await self.db.set_warn_maximum(chat_id, digit)
                        await self.bot.reply_to(message, t("warn_max_set", lang))
                    else:
                        await self.bot.reply_to(message, t("warn_max_invalid", lang, word=num_str))

                if text.startswith(("حذف فیلتر", "delete filter", "remove filter")):
                    lang = await self.get_lang(chat_id)
                    polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                    if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        await self.bot.reply_to(message, t("callback_no_admin" if polite else "callback_no_admin_rude", lang))
                        return
                    # اگر ریپلای شده روی پیام کلیدواژه
                    if message.reply_to_message:
                        keyword = message.reply_to_message.text.strip()
                    else:
                        # جدا کردن کلیدواژه از متن
                        keyword = text
                        for prefix in ("حذف فیلتر", "delete filter", "remove filter"):
                            if keyword.lower().startswith(prefix):
                                keyword = keyword[len(prefix):].strip()
                                break

                    if keyword:
                        await self.db.del_tag(chat_id, keyword)
                        await self.bot.reply_to(message, t("filter_removed", lang, keyword=keyword))
                    else:
                        await self.bot.reply_to(message, t("filter_remove_format", lang))
                    return

                is_bulk_delete = (
                    (text.startswith("حذف") and text != "حذف اخطارها")
                    or text.lower() in ("delete",)
                    or (text.lower().startswith("delete ") and not text.lower().startswith("delete filter")
                        and text.lower() not in ("clear warns", "clear warnings"))
                )
                if is_bulk_delete:
                    lang = await self.get_lang(chat_id)
                    polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                    if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        await self.bot.reply_to(message, t("no_admin_permission_delete" if polite else "no_admin_permission_delete_rude", lang))
                        return
                    try:
                        cleaned = text
                        for prefix in ("حذف", "delete"):
                            if cleaned.lower().startswith(prefix):
                                cleaned = cleaned[len(prefix):].strip()
                                break
                        n = int(cleaned) if cleaned else 1
                    except Exception:
                        n = 1

                    chat_id = message.chat.id
                    start_id = message.message_id   # id دستور "حذف ۵"
                    err = 0
                    for i in range(n+1):  # +1 یعنی خود دستور هم پاک بشه
                        try:
                            await self.bot.delete_message(chat_id, start_id - i)
                        except Exception:
                            err += 1
                    msg = await self.bot.send_message(chat_id, t("bulk_deleted", lang, count=n-err))
                    await asyncio.sleep(4)
                    await self.bot.delete_message(msg.chat.id, msg.message_id)

                if message.reply_to_message:
                    reply_target = message.reply_to_message.from_user
                    if not reply_target:
                        reply_target = getattr(message.reply_to_message, 'sender_chat', None)
                    target_id = reply_target.id if reply_target else None

                    # ADD TAG (فیلتر)
                    if text.startswith(("فیلتر", "filter")) and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        keyword = message.reply_to_message.text.strip()
                        response = text
                        for prefix in ("فیلتر", "filter"):
                            if response.lower().startswith(prefix):
                                response = response[len(prefix):].strip()
                                break
                        if keyword and response:
                            await self.db.add_tag(chat_id, keyword, response)
                            await self.bot.reply_to(message, t("filter_added", lang, keyword=keyword, response=response))
                        else:
                            await self.bot.reply_to(message, t("filter_add_format", lang))
                        return

                    if text in ("حذف", "delete") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        await self.bot.delete_message(chat_id, message.reply_to_message.message_id)
                        msg = await self.bot.reply_to(message, t("msg_deleted", lang))
                        await asyncio.sleep(4)
                        await self.bot.delete_message(msg.chat.id, msg.message_id)

                    if text in ("گزارش", "report"):
                        lang = await self.get_lang(chat_id)
                        admins = await self.bot.get_chat_administrators(chat_id)
                        msg = await self.bot.reply_to(message, t("report_sent", lang))
                        id = await self.db.file_report(chat_id, user_id, target_id, msg.message_id)
                        target = await self.bot.get_chat(target_id)
                        markup = types.InlineKeyboardMarkup()
                        check_button = types.InlineKeyboardButton(t("help_request_confirm_title", lang), callback_data=f"check:{id}")
                        message_btn = types.InlineKeyboardButton("رفتن به پیام", url=f"https://t.me/c/{str(chat_id)[4:]}/{message.reply_to_message.message_id}")

                        markup.add(check_button)
                        markup.add(message_btn)
                        for admin in admins:
                            if not admin.user.is_bot and admin.user.id != self.me.id:
                                try:
                                    await self.bot.send_message(admin.user.id, f"گزارش دریافتی از کاربر [{message.from_user.first_name if message.from_user else 'کاربر'}](tg://user?id={user_id}) در گروه با ایدی {chat_id}\n فرد گزارش شده : [{target.first_name}](tg://user?id={target_id})\n متن پیام ارسالی :\n > {message.reply_to_message.text}", reply_markup=markup, parse_mode="Markdown")
                                except Exception:
                                    pass

                    if text.startswith(("ثبت لقب", "set nickname", "set alias")):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not (await self.db.is_admin(chat_id, user_id, sender_chat_id) or target_id == user_id):
                            await self.bot.reply_to(message, t("no_admin_permission_alias" if polite else "no_admin_permission_alias_rude", lang))
                            return
                        alias = text
                        for prefix in ("ثبت لقب", "set nickname", "set alias"):
                            if alias.lower().startswith(prefix):
                                alias = alias[len(prefix):].strip()
                                break
                        await self.db.set_alias(chat_id, target_id, alias)
                        await self.bot.reply_to(message, t("alias_set", lang, alias=alias))

                    if text in ("لقب", "nickname", "alias"):
                        lang = await self.get_lang(chat_id)
                        alias = await self.db.get_alias(chat_id, target_id).strip()
                        await self.bot.reply_to(message, t("alias_get", lang, alias=alias))

                    if text.startswith(("ثبت اصل", "set origin")):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not (await self.db.is_admin(chat_id, user_id, sender_chat_id) or target_id == user_id):
                            await self.bot.reply_to(message, t("no_admin_permission_origin" if polite else "no_admin_permission_origin_rude", lang))
                            return
                        asl = text
                        for prefix in ("ثبت اصل", "set origin"):
                            if asl.lower().startswith(prefix):
                                asl = asl[len(prefix):].strip()
                                break
                        await self.db.set_asl(chat_id, target_id, asl)
                        await self.bot.reply_to(message, t("asl_set", lang, asl=asl))

                    if text in ("اصل", "origin"):
                        lang = await self.get_lang(chat_id)
                        asl = await self.db.get_asl(chat_id, target_id).strip()
                        await self.bot.reply_to(message, t("asl_get", lang, asl=asl))

                    if text in ("تنظیم خوشامد", "set welcome") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        await self.db.set_group_welcome(chat_id, message.reply_to_message.text)
                        await self.bot.reply_to(message, t("welcome_set", lang))

                    if text in ("تنظیم قوانین", "set rules") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        if message.reply_to_message:
                            rules_html = message.reply_to_message.html_text or message.reply_to_message.text
                            await self.db.set_group_rules(chat_id, rules_html)
                            await self.bot.reply_to(message, t("rules_set", lang))
                        else:
                            await self.bot.reply_to(message, t("rules_reply_needed", lang))

                    if text in ("تنظیم متن کامنت", "set comment") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        if message.reply_to_message:
                            await self.db.set_comment_message(chat_id, message.reply_to_message.text)
                            await self.bot.reply_to(message, t("comment_set", lang))
                        else:
                            await self.bot.reply_to(message, t("comment_set_empty", lang))

                    if text in ("اطلاعات", "info"):
                        try:
                            # گرفتن اطلاعات پایه کاربر
                            user = await self.bot.get_chat_member(chat_id, target_id).user
                            user_id = user.id
                            first_name = user.first_name or ""
                            last_name = user.last_name or ""
                            username = f"@{user.username}" if user.username else "❌ ندارد"
                            is_bot = "🤖 بله" if user.is_bot else "👤 خیر"

                            # وضعیت کاربر توی گروه
                            member = await self.bot.get_chat_member(chat_id, target_id)
                            status_map = {
                                "creator": "👑 مالک گروه",
                                "administrator": "🛡️ ادمین",
                                "member": "👤 عضو عادی",
                                "restricted": "🚫 محدودشده",
                                "left": "⬅️ ترک کرده",
                                "kicked": "⛔ بن شده"
                            }
                            status = status_map.get(member.status, member.status)

                            caption = (
                                f"🆔 آیدی عددی: <code>{user_id}</code>\n"
                                f"👤 اسم: {first_name} {last_name}\n"
                                f"🔗 یوزرنیم: {username}\n"
                                f"🤖 بات هست؟ {is_bot}\n"
                                f"📌 وضعیت در گروه: {status}\n"
                            )

                            # عکس پروفایل
                            photos = await self.bot.get_user_profile_photos(user_id, limit=1)
                            if photos.total_count > 0:
                                file_id = photos.photos[0][0].file_id
                                await self.bot.send_photo(chat_id, file_id, caption, parse_mode="HTML")
                            else:
                                await self.bot.send_message(chat_id, caption, parse_mode="HTML")

                        except Exception as e:
                            await self.bot.send_message(chat_id, f"❌ خطا در گرفتن اطلاعات کاربر:\n<code>{e}</code>", parse_mode="HTML")

                    # MUTE
                    if (text.startswith(("خفه", "سکوت", "mute"))):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.reply_to(message, t("no_admin_permission_mute" if polite else "no_admin_permission_mute_rude", lang))
                            return
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("target_is_admin" if polite else "target_is_admin_rude", lang))
                            return
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("muted_self" if polite else "muted_self_rude", lang))
                            return
                        parts = text.split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            mins = int(parts[1])
                            await self.bot.restrict_chat_member(chat_id, target_id,
                                                until_date=int(time.time()+mins*60),
                                                can_send_messages=False)
                            await self.db.add_punishment(chat_id, target_id, "mute", int(time.time()+mins*60))
                            await self.bot.reply_to(message, t("muted_temp", lang, minutes=mins))
                        else:
                            # Permanent mute: covers bare "سکوت", "خفه" and "خفه شو"
                            await self.bot.restrict_chat_member(chat_id, target_id, can_send_messages=False)
                            await self.db.add_punishment(chat_id, target_id, "mute", "0")
                            await self.bot.reply_to(message, t("muted_permanent", lang))

                    elif (text.startswith(("اخطار", "warn"))):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.reply_to(message, t("no_admin_permission_warn" if polite else "no_admin_permission_warn_rude", lang))
                            return
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("target_is_admin" if polite else "target_is_admin_rude", lang))
                            return
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("warned_self" if polite else "warned_self_rude", lang))
                            return
                        await self.db.warn_user(chat_id, target_id)
                        warns = await self.db.get_user_warnings(chat_id, target_id)
                        warn_max = await self.db.get_group_setting(chat_id, "WARN_MAXIMUM", 3)
                        await self.bot.reply_to(message, t("warned", lang, warns=warns, max=warn_max))
                        if int(warns) >= int(warn_max):
                            punish = await self.db.get_group_setting(chat_id, "WARN_PUNISHMENT", "kick")
                            if punish == "kick":
                                await self.bot.ban_chat_member(chat_id, target_id)
                                await self.bot.unban_chat_member(chat_id, target_id)
                                await self.db.add_punishment(chat_id, target_id, "kick")
                                await self.bot.reply_to(message, t("warn_punish_kick_done", lang))
                            elif punish == "ban":
                                await self.bot.ban_chat_member(chat_id, target_id)
                                await self.db.add_punishment(chat_id, target_id, "ban")
                                await self.bot.reply_to(message, t("warn_punish_ban_done", lang))
                            elif punish == "mute":
                                await self.bot.restrict_chat_member(chat_id, target_id, can_send_messages=False)
                                await self.bot.reply_to(message, t("warn_punish_mute_done", lang))
                            await self.db.remove_all_warns(chat_id, target_id)

                    elif text in ("حذف اخطارها", "clear warns", "clear warnings") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("target_is_admin" if polite else "target_is_admin_rude", lang))
                            return
                        await self.db.remove_all_warns(chat_id, target_id)
                        await self.bot.reply_to(message, t("warns_cleared", lang))



                    # KICK
                    elif text in ("ریم", "کیک", "سیک", "kick"):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.reply_to(message, t("no_admin_permission_kick" if polite else "no_admin_permission_kick_rude", lang))
                            return
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("target_is_admin" if polite else "kick_admin_rude", lang))
                            return
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("kicked_self" if polite else "kicked_self_rude", lang))
                            return
                        await self.bot.ban_chat_member(chat_id, target_id)
                        await self.bot.unban_chat_member(chat_id, target_id)
                        await self.db.add_punishment(chat_id, target_id, "kick")
                        await self.bot.reply_to(message, t("kicked", lang))

                    # BAN
                    elif text in ("بن", "سیکتیر", "ban"):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.reply_to(message, t("no_admin_permission_ban" if polite else "no_admin_permission_ban_rude", lang))
                            return
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("target_is_admin" if polite else "ban_admin_rude", lang))
                            return
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("banned_self" if polite else "banned_self_rude", lang))
                            return
                        await self.bot.ban_chat_member(chat_id, target_id)
                        await self.db.add_punishment(chat_id, target_id, "ban")
                        await self.bot.reply_to(message, t("banned", lang))

                    elif text in ("مخفی کاری", "بن+", "silent ban", "ban+") or text.startswith("سیک مخفی"):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                            await self.bot.reply_to(message, t("no_admin_permission_ban_silent" if polite else "no_admin_permission_ban_silent_rude", lang))
                            return
                        if await self.db.is_admin(chat_id, target_id):
                            await self.bot.reply_to(message, t("ban_silent_admin" if polite else "ban_silent_admin_rude", lang))
                            return
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("banned_self" if polite else "ban_silent_self_rude", lang))
                            return
                        await self.bot.delete_message(chat_id, message.message_id)
                        await self.bot.ban_chat_member(chat_id, target_id)

                    # UNBAN
                    elif text in ("آن‌بن", "آن بن", "ان بن", "unban") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        await self.bot.unban_chat_member(chat_id, target_id)
                        await self.db.remove_punishment(chat_id, target_id, "ban")
                        await self.bot.reply_to(message, t("unbanned", lang))

                    # UNMUTE
                    elif text in ("آن‌میوت", "آن میوت", "ان میوت", "unmute") and await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        polite = int(await self.db.get_group_setting(message.chat.id, "POLITE_MODE", 1)) == 1
                        if target_id == self.me.id:
                            await self.bot.reply_to(message, t("unmuted_self" if polite else "unmuted_self_rude", lang))
                            return
                        await self.bot.restrict_chat_member(
                            chat_id, 
                            target_id,
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_add_web_page_previews=True,
                            can_send_polls=True,
                            can_send_other_messages=True
                        )
                        await self.db.remove_punishment(chat_id, target_id, "mute")
                        await self.bot.reply_to(message, t("unmuted", lang))


                if text == "@admins":
                    admins = await self.bot.get_chat_administrators(chat_id)
                    mentions = [f"[{a.user.first_name}](tg://user?id={a.user.id})" for a in admins]
                    await self.bot.send_message(chat_id, " ".join(mentions), parse_mode="Markdown")

                # ===================== STATS =====================
                if text in ("آمار", "stats"):
                    lang = await self.get_lang(chat_id)
                    leaderboard = await self.db.get_leaderboard(chat_id, limit=10)
                    if not leaderboard:
                        await self.bot.reply_to(message, t("stats_empty", lang))
                    else:
                        header = t("stats_header", lang)
                        lines = []
                        for rank, (uid, count) in enumerate(leaderboard, 1):
                            try:
                                member = await self.bot.get_chat_member(chat_id, uid)
                                name = member.user.first_name or str(uid)
                            except Exception:
                                name = str(uid)
                            lines.append(t("stats_entry", lang, rank=rank, name=name, count=count))
                        await self.bot.reply_to(message, header + "\n".join(lines), parse_mode="Markdown")
                    return

                if text in ("آمار من", "mystats"):
                    lang = await self.get_lang(chat_id)
                    stats = await self.db.get_user_stat(chat_id, user_id)
                    rank = await self.db.get_user_rank(chat_id, user_id)
                    if stats["message_count"] > 0 and rank:
                        await self.bot.reply_to(
                            message,
                            t("stats_yours", lang, count=stats["message_count"],
                              spam_deducted=stats["spam_deducted"],
                              swear_deducted=stats["swear_deducted"], rank=rank),
                            parse_mode="Markdown"
                        )
                    else:
                        await self.bot.reply_to(
                            message,
                            t("stats_yours_no_rank", lang, count=stats["message_count"],
                              spam_deducted=stats["spam_deducted"],
                              swear_deducted=stats["swear_deducted"]),
                            parse_mode="Markdown"
                        )
                    return

                if text in ("ریست آمار", "reset stats"):
                    if not await self.db.is_admin(chat_id, user_id, sender_chat_id):
                        lang = await self.get_lang(chat_id)
                        await self.bot.reply_to(message, t("no_admin_permission", lang))
                        return
                    await self.db.reset_stats(chat_id)
                    lang = await self.get_lang(chat_id)
                    await self.bot.reply_to(message, t("stats_reset_done", lang))
                    return
                
            except Exception as e:
                error_text = f"handle_messages: {e!s}\n{traceback.format_exc()}"
                await send_error_to_owner(error_text, OWNER_ID, self.bot, "MAIN_ERROR")

    async def run(self):
        print(f"{self.me.username} Group Helper running...")
        try:
            await self.db.init_db()
            print("✅ Database initialized")

                
            telegram_task = asyncio.create_task(
                self.bot.infinity_polling(skip_pending=False, timeout=40)
            )
                
            bale_task = None
            if hasattr(self, 'bale_bot') and self.bale_bot:
                print("✅ Starting Bale Bot...")
                bale_task = asyncio.create_task(self.bale_bot.start_polling(timeout=40))
                
            if bale_task:
                await asyncio.gather(telegram_task, bale_task)
            else:
                await telegram_task

        except Exception as e:
            error_text = f"Polling crashed: {e!s}\n{traceback.format_exc()}"
            print(error_text)
            try:
                await send_error_to_owner(error_text, OWNER_ID, self.bot, "POLLING_CRASH")
            except Exception:
                pass
    
    async def stop(self):
        print(f"Shutting down {self.me.username}...")
        await self.bot.stop_polling()

if __name__ == "__main__":
    komak = KomakYaar()
    asyncio.run(komak.run())