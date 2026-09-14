SUPPORTED_LANGUAGES = {"fa", "en"}
DEFAULT_LANGUAGE = "fa"

# Each key maps to a dict with language codes as values.
# Use {name}, {username}, {id}, {chat}, {members}, etc. as placeholders.
TRANSLATIONS = {
    # ===================== GENERAL =====================
    "group_activated": {
        "fa": "گروه فعال شد و بات آماده مدیریت است!",
        "en": "Group activated and bot is ready to manage!",
    },
    "group_already_active": {
        "fa": "گروه از قبل فعال شده بود",
        "en": "Group was already active",
    },
    "group_already_active_rude": {
        "fa": "گروه که از قبل فعال بود کصخل",
        "en": "Group was already active, idiot",
    },
    "no_admin_permission": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_rude": {
        "fa": "اخه تو ادمینی؟",
        "en": "Are you even an admin?",
    },
    "bot_leave": {
        "fa": "ناراحت شدم، میرم سیکتیر کنم",
        "en": "I'm sad, I'm leaving now",
    },
    "reset_done": {
        "fa": "خب، تموم شد، همه چی ریست شد",
        "en": "Done, everything has been reset",
    },
    "reset_start": {
        "fa": "حله، الان کل رکورد گروه (بجز فیلتر ها) رو پاک و بازنویسی از صفر میکنم، انگار که هیچ اتفاقی نیوفتاده",
        "en": "OK, I'll wipe all group records (except filters) and start from scratch, as if nothing happened",
    },

    # ===================== LOCKS =====================
    "swear_lock_on_already": {
        "fa": "ضدفحش در حال حاضر نیز فعال است",
        "en": "Anti-swear is already active",
    },
    "swear_lock_on_already_rude": {
        "fa": "همینطوریشم فعال هست ستونم",
        "en": "It was already active, idiot",
    },
    "swear_lock_on": {
        "fa": "قفل فعال شد",
        "en": "Swear lock activated",
    },
    "swear_lock_off_already": {
        "fa": "ضدفحش در حال حاضر نیز غیرفعال است",
        "en": "Anti-swear is already inactive",
    },
    "swear_lock_off_already_rude": {
        "fa": "همینطوریشم غیرفعال هست ستونم",
        "en": "It was already inactive, idiot",
    },
    "swear_lock_off": {
        "fa": "قفل غیرفعال شد",
        "en": "Swear lock deactivated",
    },
    "group_lock_on": {
        "fa": "گروه با موفقیت قفل شد",
        "en": "Group has been locked",
    },
    "group_lock_on_rude": {
        "fa": "کسی خایه داره پیام بده",
        "en": "Nobody dares to send a message now",
    },
    "group_lock_on_already": {
        "fa": "گروه از قبل نیز قفل بود",
        "en": "Group was already locked",
    },
    "group_lock_on_already_rude": {
        "fa": "گروه که از قبل قفل بود کصخل",
        "en": "Group was already locked, idiot",
    },
    "group_lock_off": {
        "fa": "گروه با موفقیت باز شد",
        "en": "Group has been unlocked",
    },
    "group_lock_off_rude": {
        "fa": "راحت گوه بخورید",
        "en": "Go enjoy yourselves",
    },
    "group_lock_off_already": {
        "fa": "گروه از قبل نیز باز بود",
        "en": "Group was already unlocked",
    },
    "group_lock_off_already_rude": {
        "fa": "گروه که از قبل باز بود کصخل",
        "en": "Group was already unlocked, idiot",
    },
    "link_lock_on": {
        "fa": "ضدلینک فعال شد",
        "en": "Anti-link activated",
    },
    "link_lock_on_already": {
        "fa": "ضدلینک در حال حاضر نیز فعال است",
        "en": "Anti-link is already active",
    },
    "link_lock_on_already_rude": {
        "fa": "خیالت راحت باشه نمیگفتی هم لینکارو پاک میکردم",
        "en": "Don't worry, I was already deleting links",
    },
    "link_lock_off": {
        "fa": "ضدلینک غیرفعال شد",
        "en": "Anti-link deactivated",
    },
    "link_lock_off_already": {
        "fa": "ضدلینک از قبل نیز غیرفعال بود",
        "en": "Anti-link was already inactive",
    },
    "link_lock_off_already_rude": {
        "fa": "باع، قفل که قبلشم باز بود",
        "en": "Dude, the lock was already open",
    },
    "forward_lock_on": {
        "fa": "ضدفوروارد فعال شد",
        "en": "Anti-forward activated",
    },
    "forward_lock_on_already": {
        "fa": "ضدفوروارد در حال حاضر نیز فعال است",
        "en": "Anti-forward is already active",
    },
    "forward_lock_on_already_rude": {
        "fa": "خیالت راحت باشه نمیگفتی هم فورواردارو پاک میکردم",
        "en": "Don't worry, I was already deleting forwards",
    },
    "forward_lock_off": {
        "fa": "ضدفوروارد غیرفعال شد",
        "en": "Anti-forward deactivated",
    },
    "forward_lock_off_already": {
        "fa": "ضدفوروارد از قبل نیز غیرفعال بود",
        "en": "Anti-forward was already inactive",
    },
    "forward_lock_off_already_rude": {
        "fa": "باع، قفل که قبلشم باز بود",
        "en": "Dude, the lock was already open",
    },
    "gif_lock_on": {
        "fa": "ضدگیف فعال شد",
        "en": "Anti-GIF activated",
    },
    "gif_lock_on_already": {
        "fa": "ضدگیف در حال حاضر نیز فعال است",
        "en": "Anti-GIF is already active",
    },
    "gif_lock_on_already_rude": {
        "fa": "خیالت راحت باشه نمیگفتی هم گیفارو پاک میکردم",
        "en": "Don't worry, I was already deleting GIFs",
    },
    "gif_lock_off": {
        "fa": "ضدگیف غیرفعال شد",
        "en": "Anti-GIF deactivated",
    },
    "gif_lock_off_already": {
        "fa": "ضدگیف از قبل نیز غیرفعال بود",
        "en": "Anti-GIF was already inactive",
    },
    "gif_lock_off_already_rude": {
        "fa": "باع، قفل که قبلشم باز بود",
        "en": "Dude, the lock was already open",
    },
    "raid_lock_on": {
        "fa": "ضد حمله فعال شد، ورود انبوه اعضا کنترل می‌شود",
        "en": "Anti-raid activated, mass joins will be controlled",
    },
    "raid_lock_on_already": {
        "fa": "ضد حمله در حال حاضر نیز فعال است",
        "en": "Anti-raid is already active",
    },
    "raid_lock_on_already_rude": {
        "fa": "حله دیگه، همونطوریشم فعاله",
        "en": "It was already active, duh",
    },
    "raid_lock_off": {
        "fa": "ضد حمله غیرفعال شد",
        "en": "Anti-raid deactivated",
    },
    "raid_lock_off_already": {
        "fa": "ضد حمله از قبل نیز غیرفعال بود",
        "en": "Anti-raid was already inactive",
    },
    "raid_lock_off_already_rude": {
        "fa": "باع، که قبلشم باز بود",
        "en": "Dude, it was already open",
    },
    "raid_threshold_set": {
        "fa": "سقف ورود انبوه به {val} عضو تنظیم شد",
        "en": "Raid threshold set to {val} members",
    },
    "raid_window_set": {
        "fa": "بازه تشخیص حمله به {val} ثانیه تنظیم شد",
        "en": "Raid window set to {val} seconds",
    },
    "invalid_number": {
        "fa": "عدد معتبر وارد کن",
        "en": "Enter a valid number",
    },
    "captcha_lock_on": {
        "fa": "کپچا فعال شد؛ اعضای جدید باید برای ورود کپچا حل کنند",
        "en": "Captcha activated; new members must solve a captcha to join",
    },
    "captcha_lock_on_already": {
        "fa": "کپچا در حال حاضر نیز فعال است",
        "en": "Captcha is already active",
    },
    "captcha_lock_on_already_rude": {
        "fa": "همینطوریشم فعاله کصخل",
        "en": "It was already active, idiot",
    },
    "captcha_lock_off": {
        "fa": "کپچا غیرفعال شد",
        "en": "Captcha deactivated",
    },
    "captcha_lock_off_already": {
        "fa": "کپچا از قبل نیز غیرفعال بود",
        "en": "Captcha was already inactive",
    },
    "captcha_lock_off_already_rude": {
        "fa": "باع، که قبلشم باز بود",
        "en": "Dude, it was already open",
    },
    "spam_lock_on": {
        "fa": "✅ قفل اسپم فعال شد",
        "en": "✅ Anti-spam activated",
    },
    "spam_lock_on_already": {
        "fa": "ضد اسپم از قبل فعال است",
        "en": "Anti-spam is already active",
    },
    "spam_lock_on_already_rude": {
        "fa": "قفل اسپم که قبلاً روشنه کصخل",
        "en": "Anti-spam was already on, idiot",
    },
    "spam_lock_off": {
        "fa": "✅ قفل اسپم غیرفعال شد",
        "en": "✅ Anti-spam deactivated",
    },
    "spam_lock_off_already": {
        "fa": "ضد اسپم از قبل غیرفعال است",
        "en": "Anti-spam is already inactive",
    },
    "spam_lock_off_already_rude": {
        "fa": "قفل اسپم که قبلاً باز بود",
        "en": "Anti-spam was already off",
    },
    "flood_lock_on": {
        "fa": "✅ قفل فلود فعال شد",
        "en": "✅ Anti-flood activated",
    },
    "flood_lock_on_already": {
        "fa": "ضد فلود از قبل فعال است",
        "en": "Anti-flood is already active",
    },
    "flood_lock_on_already_rude": {
        "fa": "قفل فلود که قبلاً روشنه کصخل",
        "en": "Anti-flood was already on, idiot",
    },
    "flood_lock_off": {
        "fa": "✅ قفل فلود غیرفعال شد",
        "en": "✅ Anti-flood deactivated",
    },
    "flood_lock_off_already": {
        "fa": "ضد فلود از قبل غیرفعال است",
        "en": "Anti-flood is already inactive",
    },
    "flood_lock_off_already_rude": {
        "fa": "قفل فلود که قبلاً باز بود",
        "en": "Anti-flood was already off",
    },
    "inline_lock_on": {
        "fa": "قفل اینلاین فعال شد ✅",
        "en": "Inline lock activated ✅",
    },
    "inline_lock_on_already": {
        "fa": "قفل اینلاین از قبل فعال بوده",
        "en": "Inline lock was already active",
    },
    "inline_lock_on_already_rude": {
        "fa": "قفل اینلاین رو که قبلا روشن کرده بودی کصخل الزایمری",
        "en": "You already turned on the inline lock, you forgetful idiot",
    },
    "inline_lock_off": {
        "fa": "قفل اینلاین غیرفعال شد ✅",
        "en": "Inline lock deactivated ✅",
    },
    "inline_lock_off_already": {
        "fa": "قفل اینلاین از قبل غیرفعال بوده",
        "en": "Inline lock was already inactive",
    },
    "inline_lock_off_already_rude": {
        "fa": "اقا من بعنوان برنامه نویس ناموسا خسته شدم دیگه مغزم نمیکشه چی بنویسم کصخل نباشید دیگه غیرفعال بوده از قبل",
        "en": "Dude as a programmer I'm tired, I can't think of what to write anymore, don't be an idiot, it was already inactive",
    },

    # ===================== POLITE / RUDE MODE =====================
    "polite_already": {
        "fa": "بنده از قبل باادب بوده‌ام",
        "en": "I was already polite",
    },
    "polite_changed": {
        "fa": "ادب کیری مهمه، من باادب میشم",
        "en": "Politeness matters, I'll be polite",
    },
    "rude_changed": {
        "fa": "وقتشه کیری حرف بزنم",
        "en": "Time to talk dirty",
    },
    "rude_already": {
        "fa": "کصمغز منکه از قبلشم بی ادب بودم",
        "en": "I was already rude, dumbass",
    },

    # ===================== PUBLIC COMMANDS =====================
    "public_commands_on": {
        "fa": "دستورات عمومی روشن شد",
        "en": "Public commands enabled",
    },
    "public_commands_on_already": {
        "fa": "دستورات عمومی از قبل نیز برای همه قابل استفاده بود",
        "en": "Public commands were already enabled for everyone",
    },
    "public_commands_on_already_rude": {
        "fa": "همینطوریشم روشنه ستونم",
        "en": "It was already on, idiot",
    },
    "public_commands_off": {
        "fa": "دستورات عمومی خاموش شد",
        "en": "Public commands disabled",
    },
    "public_commands_off_already": {
        "fa": "دستورات عمومی از قبل نیز غیرفعال بود",
        "en": "Public commands were already disabled",
    },
    "public_commands_off_already_rude": {
        "fa": "همینطوریشم خاموشه ستونم",
        "en": "It was already off, idiot",
    },

    # ===================== BLOCKED WORDS =====================
    "word_blocked": {
        "fa": "کلمه ‌ی \"{word}‌\" با موفقیت مسدود شد",
        'en': 'Word "{word}" has been blocked',
    },
    "word_unblocked": {
        "fa": "کلمه ‌ی \"{word}‌\" با موفقیت از مسدودی خارج شد و کاربران میتوانند آنرا در گروه ارسال کنند",
        'en': 'Word "{word}" has been unblocked and users can now send it in the group',
    },

    # ===================== BOT BLOCKS =====================
    "bot_blocked": {
        "fa": "بات {username} بلاک شد",
        "en": "Bot @{username} has been blocked",
    },
    "bot_unblocked": {
        "fa": "بات {username} آن‌بلاک شد",
        "en": "Bot @{username} has been unblocked",
    },
    "no_blocked_bots": {
        "fa": "هیچ باتی بلاک نشده",
        "en": "No bots are blocked",
    },
    "blocked_bots_list": {
        "fa": "بات های بلاک شده :",
        "en": "Blocked bots:",
    },

    # ===================== INVITE LINK =====================
    "invite_link_created": {
        "fa": "🔗 لینک دعوت مخصوص شما:\n{link}\n📌 ساخته شده توسط کمک‌ی‌ـــار",
        "en": "🔗 Your personal invite link:\n{link}\n📌 Created by KomakYaar",
    },
    "invite_link_no_permission": {
        "fa": "ربات دسترسی ساخت لینک ندارد",
        "en": "Bot doesn't have permission to create invite links",
    },
    "invite_max_set": {
        "fa": "حداکثر تعداد دعوت به {maximum} دعوت تغییر پیدا کرد",
        "en": "Maximum invite limit changed to {maximum}",
    },
    "invite_max_invalid": {
        "fa": "کصخل اشتباه نوشتی",
        "en": "You wrote it wrong, idiot",
    },

    # ===================== FILTERS =====================
    "filters_list_header": {
        "fa": "تمامی فیلترها :",
        "en": "All filters:",
    },
    "filter_added": {
        "fa": "✅ فیلتر اضافه شد!\nکلیدواژه: {keyword}\nپاسخ: {response}",
        "en": "✅ Filter added!\nKeyword: {keyword}\nResponse: {response}",
    },
    "filter_add_format": {
        "fa": "⚠️ فرمت درست: ریپلای روی پیام و نوشتن: فیلتر پاسخ",
        "en": "⚠️ Correct format: reply to a message and write: filter <response>",
    },
    "filter_removed": {
        "fa": "❌ فیلتر '{keyword}' حذف شد",
        "en": "❌ Filter '{keyword}' has been removed",
    },
    "filter_remove_format": {
        "fa": "⚠️ فرمت درست: حذف فیلتر روی ریپلای یا با نوشتن کلیدواژه",
        "en": "⚠️ Correct format: reply with 'delete filter' or write: delete filter <keyword>",
    },

    # ===================== WARN PUNISHMENT =====================
    "warn_punish_select": {
        "fa": "از دکمه‌های زیر برای انتخاب نوع مجازات استفاده کنید",
        "en": "Use the buttons below to select punishment type",
    },
    "warn_punish_changed": {
        "fa": "نوع مجازات اخطار با موفقیت به {type} تغییر کرد",
        "en": "Warning punishment changed to {type}",
    },
    "warn_punish_changed_rude": {
        "fa": "ردیفه اخطار رو گذاشتم رو {type}",
        "en": "Set warning punishment to {type}",
    },

    # ===================== WARN MAX =====================
    "warn_max_set": {
        "fa": "سقف اخطارها با موفقیت تنظیم شد",
        "en": "Warning limit set successfully",
    },
    "warn_max_invalid": {
        "fa": "{word} خودتی",
        "en": "{word} is yourself",
    },

    # ===================== ECHO =====================
    "echo_sent": {
        "fa": "{name}: \n {text}",
        "en": "{name}: \n {text}",
    },

    # ===================== RULES =====================
    "no_rules": {
        "fa": "قانونی برای این گروه ثبت نشده!",
        "en": "No rules have been set for this group!",
    },

    # ===================== HELP =====================
    "help_sent_pv": {
        "fa": "📎 پنل راهنما به پیوی شما ارسال شد!",
        "en": "📎 Help panel sent to your DM!",
    },
    "help_pv_blocked": {
        "fa": "⚠️ نم‌تونم پیوی شما پیام بفرستم، لطفا دایرکت ربات رو باز کنید.",
        "en": "⚠️ I can't DM you, please open the bot's private chat.",
    },

    # ===================== CAPTCHA =====================
    "captcha_correct": {
        "fa": "✅ پاسخ درست بود، خوش اومدی!",
        "en": "✅ Correct answer, welcome!",
    },
    "captcha_correct_welcome": {
        "fa": "[{name}](tg://user?id={id}) تایید شد! خوش اومدی",
        "en": "[{name}](tg://user?id={id}) verified! Welcome",
    },
    "captcha_wrong": {
        "fa": "پاسخ غلط بود! {remaining} تلاش دیگر باقی مانده",
        "en": "Wrong answer! {remaining} attempts remaining",
    },
    "captcha_wrong_ban": {
        "fa": "پاسخ غلط بود؛ شما از گروه حذف شدید",
        "en": "Wrong answer; you've been removed from the group",
    },
    "captcha_expired": {
        "fa": "کپچا منقضی شده است",
        "en": "Captcha has expired",
    },

    # ===================== WELCOME =====================
    "welcome_bot_added": {
        "fa": """سلام رفقا
من کمک‌ی‌ـــارم، یه دستیار مدیریت گروه و یه رفیق باحال برای شما
از طریق من میتونین به راحتی کاربرا، مدیرا، محتوا و... گروهتون رو مدیریت کنید
فقط کافیه برای شروع بهم دسترسی های کامل بدید و یه ادمین بگه `فعال شو` تا کارمونو شروع کنیم
برای دیدن طرز کار با من کلمه ی `راهنما` رو ارسال کنید

پیشنهاد میکنیم برای باخبر شدن از قابلیت های جدید ربات و همچنین گزارش باگ و پیشنهادات، در کانال و گروه کمک یار هم عضو شید :
کانال : {channel}
گروه : {group}
همچنین، من یه ربات متن‌بازم پس میتونید کد منو ببینید و تغییر بدید و استفاده کنید در صورت نام بردن از کمک یار
لینک پروژه :
https://github.com/Code-Wizaard/KomakYaar""",
        "en": """Hey everyone!
I'm KomakYaar, a group management assistant and a cool friend for you.
Through me, you can easily manage users, admins, content, and more in your group.
Just give me full permissions and have an admin send `activate` to get started.
To see how to use me, send the word `help`.

I recommend joining KomakYaar's channel and group to stay updated on new features, report bugs, and share suggestions:
Channel: {channel}
Group: {group}
Also, I'm open-source so you can view my code and modify it, as long as you credit KomakYaar.
Source link:
https://github.com/Code-Wizaard/KomakYaar""",
    },
    "welcome_group_start": {
        "fa": """درود و مهر ❤️👋
من کمک یارم، یه ربات خودمونی همه کاره برای مدیریت انواع گروه ها، از گروه های دوستانه و رفاقتی تا گروه های رسمی و پرجمعیت و همچنین گروه های کامنت
خیلی خوشحالم که اینجام، اگر دسترسی های ادمین رو بهم دادی، با فرستادن دستور فعال شو من میتونم کارمو شروع کنم
اگرم تا الان من فعال هستم که چه بهتر، گوش به زنگم
پیشنهاد میکنم برای باخبر شدن از قابلیت های جدید ربات و همچنین گزارش باگ و پیشنهادات، در کانال و گروه کمک یار هم عضو شید :
کانال : {channel}
گروه : {group}
همچنین اگر دلتون میخواد که یه کمک‌ی‌ـــار برای خودتون داشته باشید یا روی امنیت چیزایی که استفاده میکنید حساسید، بهتره که بگم کمک‌ی‌ـــار یه ربات کاملا اوپن سورسه و میتونید کدش رو ببینید و اگر تونستید و ایده ای داشتید روش مشارکت کنید
لینک سورس :
https://github.com/Code-Wizaard/KomakYaar""",
        "en": """Hello and peace ❤️👋
I'm KomakYaar, an all-in-one bot for managing all kinds of groups, from friendly ones to formal and high-traffic groups, as well as comment groups.
I'm happy to be here. If you've given me admin permissions, send the command `activate` to get me started.
If I'm already active, even better, I'm all ears.
I recommend joining KomakYaar's channel and group for new features, bug reports, and suggestions:
Channel: {channel}
Group: {group}
Also, if you want your own KomakYaar or care about the security of what you use, KomakYaar is fully open-source and you can view and contribute to the code.
Source link:
https://github.com/Code-Wizaard/KomakYaar""",
    },

    # ===================== RAID =====================
    "raid_detected": {
        "fa": "🚨 ورود انبوه اعضا (حمله) تشخیص داده شد!\nاعضای جدید به مدت {minutes} دقیقه سکوت م‌شوند.",
        "en": "🚨 Mass member join (raid) detected!\nNew members will be muted for {minutes} minutes.",
    },

    # ===================== SPAM / FLOOD =====================
    "spam_punished": {
        "fa": "[{name}](tg://user?id={id}) {violation} نکن! ۵ دقیقه سکوت داده شدی 🔇",
        "en": "[{name}](tg://user?id={id}) Don't {violation}! You've been muted for 5 minutes 🔇",
    },
    "spam_punished_admin": {
        "fa": "[{name}](tg://user?id={id}) {violation} کردی، حیف که ادمینی وگرنه میوتت میکردم",
        "en": "[{name}](tg://user?id={id}) You {violation}ed, good thing you're an admin or I'd mute you",
    },

    # ===================== SWEAR =====================
    "swear_warning": {
        "fa": "[{name}](tg://user?id={id}) عزیزم قرار شد دیگه فحش ندیم باید باهم دوست باشیم",
        "en": "[{name}](tg://user?id={id}) sweetheart, we agreed no more swearing, we should be friends",
    },

    # ===================== INLINE / WHISPER =====================
    "whisper_help_title": {
        "fa": "راهنمای ارسال نجوا با کمک یار",
        "en": "Whisper guide with KomakYaar",
    },
    "whisper_help_text": {
        "fa": "پیام خود را به صورت زیر بنویسید تا پیام خصوصی شما به فرد مورد نظر ارسال شود:\n\n@{bot} <متن پیام> @username",
        "en": "Write your message as follows to send a private message to the desired person:\n\n@{bot} <message text> @username",
    },
    "whisper_cannot_pv": {
        "fa": "نمیتوانید در پیوی نجوا ارسال کنید",
        "en": "You can't send whispers in DM",
    },
    "whisper_cannot_self": {
        "fa": "شما نمی‌توانید به خودتان پیام دهید",
        "en": "You can't send a message to yourself",
    },
    "whisper_cannot_bot": {
        "fa": "شما نمی‌توانید به خود ربات پیام دهید",
        "en": "You can't send a message to the bot itself",
    },
    "whisper_too_long": {
        "fa": "پیام بسیار طولانی است! محدودیت کاراکتر ارسال نجوا ۲۰۰ کاراکتر",
        "en": "Message is too long! Whisper character limit is 200 characters",
    },

    # ===================== REPORT =====================
    "report_sent": {
        "fa": "گزارش با موفقیت ثبت و به ادمین ها اطلاع رسانی شد، به زودی گزارش بررسی میشود",
        "en": "Report submitted successfully and admins have been notified, it will be reviewed soon",
    },

    # ===================== MUTE / KICK / BAN =====================
    "muted_temp": {
        "fa": "🔇 کاربر سکوت داده شد برای {minutes} دقیقه.",
        "en": "🔇 User muted for {minutes} minutes.",
    },
    "muted_permanent": {
        "fa": "🔇 کاربر سکوت داده شد.",
        "en": "🔇 User muted.",
    },
    "warned": {
        "fa": "کاربر با موفقیت اخطار داده شد! ⚠️\n اخطار های کاربر : {warns}/{max}",
        "en": "User warned successfully! ⚠️\n User warnings: {warns}/{max}",
    },
    "warn_kick": {
        "fa": "👢 کاربر کیک شد!",
        "en": "👢 User kicked!",
    },
    "warn_ban": {
        "fa": "⛔ کاربر بن شد!",
        "en": "⛔ User banned!",
    },
    "warn_mute": {
        "fa": "کاربر میوت شد! 🤑",
        "en": "User muted! 🤑",
    },
    "warns_cleared": {
        "fa": "شتر دیدی ندیدی! ✅",
        "en": "What warnings? ✅",
    },
    "kicked": {
        "fa": "👢 کاربر کیک شد!",
        "en": "👢 User kicked!",
    },
    "banned": {
        "fa": "⛔ کاربر بن شد!",
        "en": "⛔ User banned!",
    },
    "unbanned": {
        "fa": "✅ کاربر آن‌بن شد!",
        "en": "✅ User unbanned!",
    },
    "unmuted": {
        "fa": "✅ کاربر آن‌میوت شد!",
        "en": "✅ User unmuted!",
    },
    "cannot_self_punish": {
        "fa": "❌ نم‌توانم خودم را {action} کنم!",
        "en": "❌ I can't {action} myself!",
    },
    "target_is_admin": {
        "fa": "دوست عزیز، فرد انتخاب شده ادمین است",
        "en": "Sorry, the selected user is an admin",
    },
    "target_is_admin_rude": {
        "fa": "حاجی بی شوخی خیلی کصخلی طرف ادمینه من اینو چیکارش کنم",
        "en": "Dude, the person is an admin, what do you want me to do",
    },

    # ===================== ALIAS / ASL =====================
    "alias_set": {
        "fa": "لقب {alias} با موفقیت برای این کاربر ثبت شد",
        "en": "Nickname '{alias}' has been set for this user",
    },
    "alias_get": {
        "fa": "لقب ثبت شده برای این کاربر :\n {alias}",
        "en": "Registered nickname for this user:\n {alias}",
    },
    "asl_set": {
        "fa": "اصل {asl} با موفقیت برای این کاربر ثبت شد",
        "en": "Origin '{asl}' has been set for this user",
    },
    "asl_get": {
        "fa": "اصل ثبت شده برای این کاربر :\n {asl}",
        "en": "Registered origin for this user:\n {asl}",
    },

    # ===================== SETTINGS =====================
    "welcome_set": {
        "fa": "متن خوشامد گویی ربات با موفقیت تنظیم شد",
        "en": "Welcome message set successfully",
    },
    "rules_set": {
        "fa": "قوانین گروه با موفقیت تنظیم شد",
        "en": "Group rules set successfully",
    },
    "rules_reply_needed": {
        "fa": "روی پیام قوانین ریپلای کنید",
        "en": "Reply to the rules message",
    },
    "comment_set": {
        "fa": "متن کامنت زیر پست ها تغییر پیدا کرد",
        "en": "Comment text under posts has been changed",
    },
    "comment_set_empty": {
        "fa": "خب دقیقا متن رو به چی تغییر باید بدم :\\",
        "en": "What exactly should I change the text to :\\",
    },
    "help_request_sent": {
        "fa": "این دستور، درخواستی حاوی لینک گروه به اونر برای ورود و حل مشکل شما ارسال میکند، درصورتی که مشکل شما فوری و بدون جواب داخل راهنماها باشد کمک یار به دستور اونر در گروه از کار خواهد افتاد",
        "en": "This command sends a request with the group link to the owner for help. If your issue is urgent and not solved by the guides, KomakYaar will be disabled in the group at the owner's command",
    },
    "help_request_confirmed": {
        "fa": "درخواست به اونر ارسال شد! در صورت تایید به گروه عضو خواهد شد",
        "en": "Request sent to the owner! They will join the group if approved",
    },
    "help_request_cancelled": {
        "fa": "این درخواست لغو شده است!",
        "en": "This request has been cancelled!",
    },
    "help_request_received": {
        "fa": "درخواست کمک از گروهی ارسال شده\nنام گروه : {title}\nآیدی گروه : {id}",
        "en": "Help request received from a group\nGroup name: {title}\nGroup ID: {id}",
    },

    # ===================== POST LOCK =====================
    "post_locked": {
        "fa": "این پست قفل شده است 🔒\n دیگر اعضای عادی دسترسی ارسال کامنت زیر این پست را ندارد",
        "en": "This post is locked 🔒\nRegular members can no longer comment under this post",
    },
    "post_locked_rude": {
        "fa": "کیر کردم تو این پست حالا خایه داری کامنت بذار این زیر",
        "en": "I locked this post, try commenting now if you dare",
    },
    "post_unlocked": {
        "fa": "پست باز شد 🔓\n دیگر تمامی اعضا قادر به ارسال کامنت زیر این پست خواهند بود",
        "en": "Post unlocked 🔓\nAll members can now comment under this post",
    },
    "post_unlocked_rude": {
        "fa": "تا کی تبعیض، قفل رو جر دادم برید کامنتارو بگایید",
        "en": "No more discrimination, I unlocked it, go comment away",
    },
    "post_lock_not_comment": {
        "fa": "پیام شما به هیچ پستی اشاره نمیکند، لطفا زیر پستی که میخواهید قفل شود این دستور را کامنت کنید",
        "en": "Your message doesn't reference any post, please comment this command under the post you want to lock",
    },

    # ===================== DELETE =====================
    "msg_deleted": {
        "fa": "پیام پاک شد 🗑️",
        "en": "Message deleted 🗑️",
    },
    "bulk_deleted": {
        "fa": "{count} پیام با موفقیت حذف شد 🗑️",
        "en": "{count} messages successfully deleted 🗑️",
    },

    # ===================== ID =====================
    "owner_not_allowed": {
        "fa": "تو اونر بات نیستی",
        "en": "You're not the bot owner",
    },
    "not_owner_tag": {
        "fa": "دوست عزیز، شما اونر نیستید",
        "en": "Sorry, you're not the owner",
    },
    "not_owner_tag_rude": {
        "fa": "گوه نخور بابا این گوزا به تو نیومده",
        "en": "Don't be arrogant, this isn't for you",
    },

    # ===================== CALLBACK =====================
    "callback_no_admin": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "callback_no_admin_rude": {
        "fa": "انگشت نکن بیشرف",
        "en": "Don't touch, scum",
    },
    "panel_closed": {
        "fa": "پنل به دستور مدیر بسته شد!",
        "en": "Panel closed by admin!",
    },
    "settings_updated": {
        "fa": "تنظیمات به‌روزرسانی شد ✅",
        "en": "Settings updated ✅",
    },
    "already_in_this_state": {
        "fa": "این ویژگی از قبل نیز در همین وضعیت بود",
        "en": "This feature was already in this state",
    },
    "already_in_this_state_rude": {
        "fa": "همینطوریشم همینه ستونم",
        "en": "It was already like this, idiot",
    },

    # ===================== LOCK PANEL =====================
    "lock_panel_title": {
        "fa": "🔒 **پنل قفل‌ها**\n\nبرای تغییر وضعیت هر قفل روی دکمه‌های زیر بزنید:",
        "en": "🔒 **Lock Panel**\n\nTap the buttons below to toggle each lock:",
    },
    "lock_panel_desc": {
        "fa": "از دکمه‌های زیر برای قفل و باز کردن ویژگی‌های مختلف گروه استفاده کنید:",
        "en": "Use the buttons below to lock and unlock various group features:",
    },

    # ===================== REQUEST =====================
    "request_status": {
        "fa": "از دکمه ی زیر برای تغییر وضعیت درخواست دعوت استفاده کنید \n وضعیت فعلی : {status}",
        "en": "Use the button below to change the invite request status\nCurrent status: {status}",
    },
    "request_on": {
        "fa": "درخواست برای دعوت با موفقیت روشن شد",
        "en": "Invite request has been enabled",
    },
    "request_off": {
        "fa": "درخواست برای دعوت با موفقیت خاموش شد",
        "en": "Invite request has been disabled",
    },

    # ===================== OWNER BANGROUP =====================
    "group_banned_msg": {
        "fa": "درود، متاسفانه، این گروه از کمک‌ی‌ــار بن شده و اعضا و ادمین های آن دیگر قادر به کار با ربات نیستند",
        "en": "Hello, unfortunately, this group has been banned from KomakYaar and its members and admins can no longer use the bot",
    },

    # ===================== UPDATE =====================
    "update_broadcast_start": {
        "fa": "✅ در حال پخش آپدیت {version} به همه گروه‌ها...",
        "en": "✅ Broadcasting update {version} to all groups...",
    },
    "update_broadcast_done": {
        "fa": "✅ پخش آپدیت تموم شد!\n\nارسال موفق: {success} گروه\nخطا یا بلاک شده: {err} گروه",
        "en": "✅ Update broadcast complete!\n\nSent successfully: {success} groups\nErrors or blocked: {err} groups",
    },
    "update_no_updates": {
        "fa": "❌ هیچ آپدیتی نوشته نشده!",
        "en": "❌ No updates written!",
    },
    "update_bad_format": {
        "fa": "❌ فرمت اشتباه!\n\nمثال:\n/update v1.2.5\nیا\n/update 1.2.5\nسپس تغییرات رو در خطوط بعدی بنویس",
        "en": "❌ Wrong format!\n\nExample:\n/update v1.2.5\nor\n/update 1.2.5\nThen write the changes in the following lines",
    },

    # ===================== HELP REQUEST CONFIRM =====================
    "help_request_confirm_title": {
        "fa": "تایید ✅",
        "en": "Confirm ✅",
    },
    "help_request_cancel_title": {
        "fa": "لغو ❌",
        "en": "Cancel ❌",
    },

    # ===================== OWNER HELP BTN =====================
    "go_to_group": {
        "fa": "رفتن به گروه",
        "en": "Go to group",
    },

    # ===================== START PRIVATE =====================
    "start_pv": {
        "fa": """🌟 به **ربات کمک‌یار** خوش اومدی!

من یه دستیار قدرتمند برای مدیریت گروه‌های تلگرامی هستم.

🚀 **برای شروع کافیه:**
1. منو به گروهت اضافه کن
2. بهم دسترسی ادمین بده
3. تو گروه دستور `فعال شو` رو بفرست

📊 **قابلیت‌های من:**
• مدیریت کامل اعضا (اخطار، بن، میوت، کیک)
• فیلترهای هوشمند و پاسخ خودکار
• قفل‌های متنوع (لینک، فحش، فوروارد، گیف)
• سیستم نجوا برای پیام‌های خصوصی
• گزارش‌دهی و لاگ‌گیری
• و ده‌ها قابلیت دیگر...

🔗 **لینک‌های مفید:**
• کد منبع: [گیت‌هاب](https://github.com/aydin-here/KomakYaar)
• کانال آپدیت: {channel}
• گروه پشتیبانی: {group}

📖 برای مشاهده راهنما، دکمه `/help` رو بزن.

🎉 نسخه {version}

Made with ❤️ by Code-Wizaard""",
        "en": """🌟 Welcome to **KomakYaar Bot**!

I'm a powerful assistant for managing Telegram groups.

🚀 **To get started:**
1. Add me to your group
2. Give me admin permissions
3. Send the command `activate` in the group

📊 **My features:**
• Full member management (warn, ban, mute, kick)
• Smart filters and auto-replies
• Various locks (link, swear, forward, GIF)
• Whisper system for private messages
• Reporting and logging
• And many more features...

🔗 **Useful links:**
• Source code: [GitHub](https://github.com/aydin-here/KomakYaar)
• Update channel: {channel}
• Support group: {group}

📖 Press `/help` to see the guide.

🎉 Version {version}

Made with ❤️ by Code-Wizaard""",
    },

    # ===================== @admins =====================
    "admins_mention_header": {
        "fa": "ادمین‌ها:",
        "en": "Admins:",
    },

    # ===================== BOT NAME REPLY =====================
    "bot_name_reply": {
        "fa": "{name}",
        "en": "{name}",
    },

    # ===================== STATS / LEADERBOARD =====================
    "stats_header": {
        "fa": "📊 **آمار فعال‌ترین اعضای گروه**\n",
        "en": "📊 **Group Activity Leaderboard**\n",
    },
    "stats_entry": {
        "fa": "#{rank} {name} — {count} پیام",
        "en": "#{rank} {name} — {count} messages",
    },
    "stats_empty": {
        "fa": "هنوز هیچ آماری ثبت نشده!",
        "en": "No stats recorded yet!",
    },
    "stats_yours": {
        "fa": "📊 **آمار شما:**\nپیام‌ها: {count}\nحذف شده توسط اسپم: {spam_deducted}\nحذف شده توسط فحش: {swear_deducted}\nرتبه: #{rank}",
        "en": "📊 **Your Stats:**\nMessages: {count}\nDeducted by spam: {spam_deducted}\nDeducted by swear: {swear_deducted}\nRank: #{rank}",
    },
    "stats_yours_no_rank": {
        "fa": "📊 **آمار شما:**\nپیام‌ها: {count}\nحذف شده توسط اسپم: {spam_deducted}\nحذف شده توسط فحش: {swear_deducted}\nشما هنوز در لیست نیستید",
        "en": "📊 **Your Stats:**\nMessages: {count}\nDeducted by spam: {spam_deducted}\nDeducted by swear: {swear_deducted}\nYou're not on the leaderboard yet",
    },
    "stats_reset_done": {
        "fa": "✅ آمار گروه با موفقیت ریست شد",
        "en": "✅ Group stats have been reset",
    },

    # ===================== LANGUAGE =====================
    "language_set": {
        "fa": "✅ زبان به {language} تغییر کرد",
        "en": "✅ Language changed to {language}",
    },
    "language_set_group": {
        "fa": "✅ زبان گروه به {language} تغییر کرد",
        "en": "✅ Group language changed to {language}",
    },
    "language_invalid": {
        "fa": "❌ زبان نامعتبر! زبان‌های موجود: fa (فارسی), en (English)",
        "en": "❌ Invalid language! Available languages: fa (Persian), en (English)",
    },
    "language_current": {
        "fa": "زبان فعلی: {lang}",
        "en": "Current language: {lang}",
    },

    # ===================== HELP GUIDE TEXTS =====================
    "guide_members_title": {
        "fa": "👥 مدیریت اعضا",
        "en": "👥 Member Management",
    },
    "guide_locks_title": {
        "fa": "🔒 قفل‌ها و محدودیت‌ها",
        "en": "🔒 Locks & Restrictions",
    },
    "guide_filters_title": {
        "fa": "🏆 فیلترها و پاسخ خودکار",
        "en": "🏆 Filters & Auto-replies",
    },
    "guide_public_title": {
        "fa": "💬 دستورات عمومی",
        "en": "💬 Public Commands",
    },
    "guide_invite_title": {
        "fa": "🔗 لینک و دعوت",
        "en": "🔗 Links & Invites",
    },
    "guide_settings_title": {
        "fa": "⚙️ تنظیمات گروه",
        "en": "⚙️ Group Settings",
    },
    "guide_warnings_title": {
        "fa": "📝 سیستم اخطار و گزارش",
        "en": "📝 Warning & Report System",
    },
    "guide_profile_title": {
        "fa": "🎭 لقب و اصل",
        "en": "🎭 Nickname & Origin",
    },
    "guide_antivirus_title": {
        "fa": "🛡️ ضدویروس فایل",
        "en": "🛡️ File Antivirus",
    },
    "guide_whisper_title": {
        "fa": "🕵️ نجوا (پیام خصوصی)",
        "en": "🕵️ Whisper (Private Message)",
    },
    "guide_bridge_title": {
        "fa": "🌉 بریج بله ↔ تلگرام",
        "en": "🌉 Bale ↔ Telegram Bridge",
    },
    "guide_faq_title": {
        "fa": "❓ سوالات متداول",
        "en": "❓ FAQ",
    },
    "guide_stats_title": {
        "fa": "📊 آمار و رتبه\u200cبندی",
        "en": "📊 Stats & Leaderboard",
    },

    # ===================== MUTE / KICK / BAN (extended) =====================
    "muted_self": {
        "fa": "❌ نمی\u200cتوانم خودم را سکوت کنم!",
        "en": "❌ I can't mute myself!",
    },
    "muted_self_rude": {
        "fa": "چرا انقدر همه با من بد هستند",
        "en": "Why is everyone so mean to me",
    },
    "warned_self": {
        "fa": "❌ نمی\u200cتوانم خودم را اخطار کنم!",
        "en": "❌ I can't warn myself!",
    },
    "warned_self_rude": {
        "fa": "به کدامین گناه؟",
        "en": "For what sin?",
    },
    "kicked_self": {
        "fa": "❌ نمی\u200cتوانم خودم را کیک کنم!",
        "en": "❌ I can't kick myself!",
    },
    "kicked_self_rude": {
        "fa": "حالا باهم یه چندتا شوخی کردیم چرا میخوای منو کیک کنی",
        "en": "We were just joking around, why kick me",
    },
    "banned_self": {
        "fa": "❌ نمی\u200cتوانم خودم را بن کنم!",
        "en": "❌ I can't ban myself!",
    },
    "banned_self_rude": {
        "fa": "عامو تفنگو بگیر اونور به من چیکار داری",
        "en": "Put the gun down, what do you want from me",
    },
    "unmuted_self": {
        "fa": "❌ نمی\u200cتوانم خودم را آن\u200cمیوت کنم!",
        "en": "❌ I can't unmute myself!",
    },
    "unmuted_self_rude": {
        "fa": "مشتی منکه میوت نیستم بخوام ان میوت شم",
        "en": "Dude I'm not muted to begin with",
    },
    "cannot_admin_punish_rude": {
        "fa": "حاجی بی شوخی خیلی کصخلی طرف ادمینه من اینو چیکارش کنم",
        "en": "Dude the person is an admin, what do you want me to do",
    },
    "cannot_self_punish_rude": {
        "fa": "چرا انقدر همه با من بد هستند",
        "en": "Why is everyone so mean to me",
    },
    "kick_admin_rude": {
        "fa": "باشه داداش دوبار الان برات ادمینو کیک میکنم",
        "en": "Sure buddy, let me kick the admin for you",
    },
    "ban_admin_rude": {
        "fa": "پاول دوروفم نمیتونه ادمین بن کنه تو دیگه چه انتظاری داری",
        "en": "Even Pavel Durov can't ban admins, what do you expect",
    },
    "ban_silent_admin": {
        "fa": "دوست عزیز، نمیتوانم ادمین هارا بن یا کیک کنم",
        "en": "Sorry, I can't ban or kick admins",
    },
    "ban_silent_admin_rude": {
        "fa": "سیشتیر بابا همتون همینو میگید",
        "en": "Get lost, you all say the same thing",
    },
    "ban_silent_self_rude": {
        "fa": "اگر انقدر از من بدت میاد بگو سیکتیر کن سیکتیر کنم",
        "en": "If you hate me so much just say leave and I'll leave",
    },

    # ===================== ADMIN PERMISSIONS =====================
    "no_admin_permission_mute": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_mute_rude": {
        "fa": "اخه چی بگم من به تو",
        "en": "What can I even say to you",
    },
    "no_admin_permission_warn": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_warn_rude": {
        "fa": "برنامه نویس : خداوکیلی مغزم گوزید دیگه نمیدونم چی بنویسم",
        "en": " Programmer: I'm out of ideas for rude messages",
    },
    "no_admin_permission_kick": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_kick_rude": {
        "fa": "برو تا سیکتو نزدم",
        "en": "Go away before I kick you",
    },
    "no_admin_permission_ban": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_ban_rude": {
        "fa": "کیر شدی بدبخت ادمین نیستی",
        "en": "You're not an admin, loser",
    },
    "no_admin_permission_ban_silent": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_ban_silent_rude": {
        "fa": "ببین بچه جون تا نبردمت زیرزمین خونمون برو گمشو",
        "en": "Watch it kid, get lost before I take you to our basement",
    },
    "no_admin_permission_alias": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_alias_rude": {
        "fa": "بدو بینم",
        "en": "Get lost",
    },
    "no_admin_permission_origin": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_origin_rude": {
        "fa": "کیرم تو اصلت",
        "en": "Screw your origin",
    },
    "no_admin_permission_delete": {
        "fa": "دوست عزیز، شما دسترسی ادمین ندارید",
        "en": "Sorry, you don't have admin permission",
    },
    "no_admin_permission_delete_rude": {
        "fa": "امیدوارم از زندگی حذف شی",
        "en": "I hope you get deleted from life",
    },
    "no_admin_permission_clear_warns_rude": {
        "fa": "چیزی میزنی؟ اصلا مگه میتونم اخطار بدم که الان میگی حذف اخطار",
        "en": "Are you even writing? I can't even warn, let alone clear warnings",
    },

    # ===================== WARN EXTENDED =====================
    "warn_punish_kick_done": {
        "fa": "👢 کاربر کیک شد!",
        "en": "👢 User kicked!",
    },
    "warn_punish_ban_done": {
        "fa": "⛔ کاربر بن شد!",
        "en": "⛔ User banned!",
    },
    "warn_punish_mute_done": {
        "fa": "کاربر میوت شد! 🤐",
        "en": "User muted! 🤐",
    },
    "clears_warns_rude": {
        "fa": "چیزی میزنی؟ اصلا مگه میتونم اخطار بدم که الان میگی حذف اخطار",
        "en": "Are you even writing? I can't even warn, let alone clear warnings",
    },

    # ===================== CALLBACK PANELS =====================
    "panel_closed_by_admin": {
        "fa": "پنل به دستور مدیر بسته شد!",
        "en": "Panel closed by admin!",
    },
    "lock_panel_title_full": {
        "fa": "🔒 **پنل قفل\u200cها**\n\nبرای تغییر وضعیت هر قفل روی دکمه\u200cهای زیر بزنید:",
        "en": "🔒 **Lock Panel**\n\nTap the buttons below to toggle each lock:",
    },
    "guide_select_topic": {
        "fa": "یک موضوع را انتخاب کنید تا راهنمای دقیق همان دستور را ببینید:",
        "en": "Select a topic to see the detailed guide for that command:",
    },
    "settings_updated_callback": {
        "fa": "تنظیمات به\u200cروزرسانی شد ✅",
        "en": "Settings updated ✅",
    },
    "help_request_confirmed_callback": {
        "fa": "درخواست به اونر ارسال شد! در صورت تایید به گروه عضو خواهد شد",
        "en": "Request sent to the owner! They will join if approved",
    },
    "help_request_cancelled_callback": {
        "fa": "این درخواست لغو شده است!",
        "en": "This request has been cancelled!",
    },
    "report_checked": {
        "fa": "گزارش با موفقیت توسط شما بررسی شد",
        "en": "Report checked successfully",
    },
    "report_not_found": {
        "fa": "این پیام منقضی شده یا وجود ندارد",
        "en": "This message has expired or doesn't exist",
    },
    "whisper_no_permission": {
        "fa": "شما اجازه دیدن این پیام را ندارید",
        "en": "You don't have permission to see this message",
    },
    "lock_status_changed": {
        "fa": "{name} با موفقیت {status} شد",
        "en": "{name} successfully {status}",
    },
    "lock_status_changed_rude": {
        "fa": "ردیفه ستون {name} رو {status} کردم",
        "en": "Done, I {status} the {name}",
    },
    "post_lock_status_changed": {
        "fa": "قفل پست با موفقیت {status} شد ✅",
        "en": "Post lock successfully {status} ✅",
    },

    # ===================== DB RESTORE =====================
    "db_owner_only": {
        "fa": "تو اونر بات نیستی",
        "en": "You're not the bot owner",
    },
    "db_restore_prompt": {
        "fa": "📥 لطفاً فایل بکاپ دیتابیس (با پسوند .db یا .sqlite) را همین\u200cجا در پیوی ارسال کنید.\n\n❌ برای لغو: /cancel_restore",
        "en": "📥 Please send the database backup file (.db or .sqlite) here in DM.\n\n❌ To cancel: /cancel_restore",
    },
    "db_restore_cancelled": {
        "fa": "❌ بازیابی دیتابیس لغو شد.",
        "en": "❌ Database restore cancelled.",
    },
    "db_restore_no_active": {
        "fa": "هیچ درخواست بازیابی فعالی وجود ندارد.",
        "en": "No active restore request.",
    },
    "db_restore_bad_format": {
        "fa": "❌ فرمت فایل معتبر نیست! فقط فایل با پسوند .db یا .sqlite بفرستید.\n\n❌ برای لغو: /cancel_restore",
        "en": "❌ Invalid file format! Send a .db or .sqlite file.\n\n❌ To cancel: /cancel_restore",
    },
    "db_restore_receiving": {
        "fa": "⏳ در حال دریافت و بررسی فایل بکاپ...",
        "en": "⏳ Receiving and checking backup file...",
    },
    "db_restore_not_sqlite": {
        "fa": "❌ فایل ارسال\u200cشده یک دیتابیس SQLite معتبر نیست!",
        "en": "❌ The sent file is not a valid SQLite database!",
    },
    "db_restore_not_komakyaar": {
        "fa": "❌ فایل ارسال\u200cشده بکاپ معتبر کمک\u200cیار نیست (جداول اصلی پیدا نشد)!",
        "en": "❌ The sent file is not a valid KomakYaar backup (core tables not found)!",
    },
    "db_restore_success": {
        "fa": "✅ دیتابیس با موفقیت بازیابی شد و جایگزین دیتابیس فعلی شد!",
        "en": "✅ Database restored successfully and replaced the current one!",
    },
    "db_restore_error": {
        "fa": "❌ خطا در بازیابی دیتابیس:\n{error}",
        "en": "❌ Error restoring database:\n{error}",
    },

    # ===================== BAN/UNBAN GROUP =====================
    "bangroup_format": {
        "fa": "فرمت پیامت اشتباهه",
        "en": "Your message format is wrong",
    },
    "bangroup_done": {
        "fa": "گروه دریافتی با موفقیت بن شد و قادر به کار با ربات نیست",
        "en": "The group has been banned and can no longer use the bot",
    },
    "bangroup_already": {
        "fa": "گروه از قبل هم بن شده بود",
        "en": "The group was already banned",
    },
    "bangroup_msg_to_group": {
        "fa": "درود، متاسفانه، این گروه از کمک\u200cی\u200cــار بن شده و اعضاء و ادمین های آن دیگر قادر به کار با ربات نیستند",
        "en": "Hello, unfortunately, this group has been banned from KomakYaar and its members and admins can no longer use the bot",
    },
    "unbangroup_format": {
        "fa": "فرمت پیام اشتباه است",
        "en": "Wrong message format",
    },
    "unbangroup_done": {
        "fa": "گروه دریافتی با موفقیت از حالت مسدودی درآمد",
        "en": "The group has been successfully unbanned",
    },
    "unbangroup_not_banned": {
        "fa": "گروه که اصلا بن نشده بود بخوای آن\u200cبن کنی",
        "en": "The group wasn't banned in the first place",
    },
    "unbangroup_msg_to_group": {
        "fa": "خبر خوب، گروه شما از حالت مسدودی خارج شده و همگی دوباره قادر به استفاده از ربات هستند",
        "en": "Good news, your group has been unbanned and everyone can use the bot again",
    },
    "unbangroup_owner_only": {
        "fa": "فقط به حرف اونر گوش میدم",
        "en": "I only listen to the owner",
    },

    # ===================== UPDATE =====================
    "update_owner_only": {
        "fa": "فقط اونر می\u200cتونه آپدیت پخش کنه!",
        "en": "Only the owner can broadcast updates!",
    },

    # ===================== WHISPER =====================
    "whisper_expired": {
        "fa": "این پیام منقضی شده یا وجود ندارد",
        "en": "This message has expired or doesn't exist",
    },
    "whisper_no_permission_show": {
        "fa": "شما اجازه دیدن این پیام را ندارید",
        "en": "You don't have permission to see this message",
    },

    # ===================== MISC =====================
    "member_count_unknown": {
        "fa": "نامشخص",
        "en": "unknown",
    },
    "bot_owner_only_tag": {
        "fa": "دوست عزیز، شما اونر نیستید",
        "en": "Sorry, you're not the owner",
    },
    "bot_owner_only_tag_rude": {
        "fa": "گوه نخور بابا این گوزا به تو نیومده",
        "en": "Don't be arrogant, this isn't for you",
    },

    # ===================== PANEL UI =====================
    "panel_main_title": {
        "fa": "📊 **پنل جامع مدیریت گروه**\n",
        "en": "📊 **Group Management Panel**\n",
    },
    "panel_settings_header": {
        "fa": "⚙️ **تنظیمات:**",
        "en": "⚙️ **Settings:**",
    },
    "panel_bot_tone": {
        "fa": "لحن بات",
        "en": "Bot tone",
    },
    "panel_tone_polite": {
        "fa": "باادب 🎩",
        "en": "Polite 🎩",
    },
    "panel_tone_rude": {
        "fa": "بی\u200cادب 😈",
        "en": "Rude 😈",
    },
    "panel_public_cmds": {
        "fa": "دستورات عمومی",
        "en": "Public commands",
    },
    "panel_on": {
        "fa": "روشن ✅",
        "en": "On ✅",
    },
    "panel_off": {
        "fa": "خاموش ❌",
        "en": "Off ❌",
    },
    "panel_raid_info": {
        "fa": "سقف حمله",
        "en": "Raid threshold",
    },
    "panel_raid_window": {
        "fa": "بازه حمله",
        "en": "Raid window",
    },
    "panel_seconds": {
        "fa": "ثانیه",
        "en": "seconds",
    },
    "panel_warn_max": {
        "fa": "سقف اخطار",
        "en": "Warn limit",
    },
    "panel_warn_punish": {
        "fa": "مجازات اخطار",
        "en": "Warn punishment",
    },
    "panel_invite_max": {
        "fa": "حداکثر دعوت",
        "en": "Max invites",
    },
    "panel_unlimited": {
        "fa": "نامحدود",
        "en": "unlimited",
    },
    "panel_locks_btn": {
        "fa": "🔒 قفل\u200cها",
        "en": "🔒 Locks",
    },
    "panel_polite_btn": {
        "fa": "لحن باادب",
        "en": "Polite mode",
    },
    "panel_public_btn": {
        "fa": "دستورات عمومی",
        "en": "Public commands",
    },
    "panel_guide_btn": {
        "fa": "📖 راهنمای گام به گام",
        "en": "📖 Step-by-step guide",
    },
    "panel_close_btn": {
        "fa": "بستن پنل",
        "en": "Close panel",
    },
    "panel_back_to_main": {
        "fa": "🔙 برگشت به پنل جامع",
        "en": "🔙 Back to main panel",
    },
    "panel_close_lock_panel": {
        "fa": "بستن پنل قفل",
        "en": "Close lock panel",
    },
    "panel_post_lock_on": {
        "fa": "قفل پست ✅",
        "en": "Post lock ✅",
    },
    "panel_post_lock_off": {
        "fa": "قفل پست ❌",
        "en": "Post lock ❌",
    },
    "lock_status_locked": {
        "fa": "قفل",
        "en": "locked",
    },
    "lock_status_unlocked": {
        "fa": "باز",
        "en": "unlocked",
    },
    "post_lock_activated": {
        "fa": "فعال",
        "en": "activated",
    },
    "post_lock_deactivated": {
        "fa": "غیرفعال",
        "en": "deactivated",
    },
    "punishment_kick": {
        "fa": "کیک",
        "en": "kick",
    },
    "punishment_ban": {
        "fa": "بن",
        "en": "ban",
    },
    "punishment_mute": {
        "fa": "میوت",
        "en": "mute",
    },
    "back_to_menu": {
        "fa": "🔙 برگشت به منوی اصلی",
        "en": "🔙 Back to main menu",
    },
    "back_to_category": {
        "fa": "🔙 برگشت به دسته",
        "en": "🔙 Back to category",
    },

    # ===================== LOCK NAMES =====================
    "lock_name_link": {
        "fa": "لینک",
        "en": "link",
    },
    "lock_name_forward": {
        "fa": "فوروارد",
        "en": "forward",
    },
    "lock_name_swear": {
        "fa": "فحش",
        "en": "swear",
    },
    "lock_name_group": {
        "fa": "گروه",
        "en": "group",
    },
    "lock_name_gif": {
        "fa": "گیف",
        "en": "GIF",
    },
    "lock_name_spam": {
        "fa": "اسپم",
        "en": "spam",
    },
    "lock_name_flood": {
        "fa": "فلاد",
        "en": "flood",
    },
    "lock_name_inline": {
        "fa": "اینلاین",
        "en": "inline",
    },
    "lock_name_raid": {
        "fa": "حمله",
        "en": "raid",
    },
    "lock_name_captcha": {
        "fa": "کپچا",
        "en": "captcha",
    },
}

def t(key, lang=DEFAULT_LANGUAGE, **kwargs):
    """Translate a key to the given language, with optional formatting."""
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or key
    if kwargs:
        text = text.format(**kwargs)
    return text


# ===================== COMMAND MAPPING (Persian + English) =====================
# Each key maps to a tuple of acceptable command strings (case-insensitive for English).
COMMANDS = {
    # === Group activation / deactivation ===
    "activate":           ("فعال شو", "activate", "start bot"),
    "leave":              ("سیکتیر کن", "leave", "get out"),
    "help":               ("راهنما",),
    "reset":              ("ریست", "reset"),
    "about":              ("کمک یار", "komakyaar", "about"),

    # === Locks: swear ===
    "swear_lock_on":      ("قفل فحش", "lock swear", "swear lock"),
    "swear_lock_off":     ("بازکردن فحش", "unlock swear", "swear unlock"),

    # === Locks: link ===
    "link_lock_on":       ("قفل لینک", "lock link", "link lock"),
    "link_lock_off":      ("بازکردن لینک", "unlock link", "link unlock"),

    # === Locks: forward ===
    "forward_lock_on":    ("قفل فوروارد", "lock forward", "forward lock"),
    "forward_lock_off":   ("بازکردن فوروارد", "unlock forward", "forward unlock"),

    # === Locks: gif ===
    "gif_lock_on":        ("قفل گیف", "lock gif", "gif lock"),
    "gif_lock_off":       ("بازکردن گیف", "unlock gif", "gif unlock"),

    # === Locks: group ===
    "group_lock_on":      ("قفل گروه", "lock group", "group lock"),
    "group_lock_off":     ("بازکردن گروه", "unlock group", "group unlock"),

    # === Locks: raid ===
    "raid_lock_on":       ("قفل حمله", "lock raid", "raid lock", "anti-raid on"),
    "raid_lock_off":      ("بازکردن حمله", "unlock raid", "raid unlock", "anti-raid off"),

    # === Locks: captcha ===
    "captcha_lock_on":    ("قفل کپچا", "lock captcha", "captcha lock"),
    "captcha_lock_off":   ("بازکردن کپچا", "unlock captcha", "captcha unlock"),

    # === Locks: spam ===
    "spam_lock_on":       ("قفل اسپم", "lock spam", "spam lock"),
    "spam_lock_off":      ("بازکردن اسپم", "unlock spam", "spam unlock"),

    # === Locks: flood ===
    "flood_lock_on":      ("قفل فلاد", "lock flood", "flood lock"),
    "flood_lock_off":     ("بازکردن فلاد", "unlock flood", "flood unlock"),

    # === Locks: inline ===
    "inline_lock_on":     ("قفل اینلاین", "lock inline", "inline lock"),
    "inline_lock_off":    ("بازکردن اینلاین", "unlock inline", "inline unlock"),

    # === Locks: post ===
    "post_lock":          ("قفل پست", "lock post", "post lock"),
    "post_unlock":        ("باز کردن پست", "unlock post", "post unlock"),

    # === Lock panel ===
    "lock_panel":         ("پنل قفل", "lock panel"),
    "panel":              ("پنل", "panel"),

    # === Polite / rude mode ===
    "be_rude":            ("بی ادب شو", "be rude", "rude mode"),
    "be_polite":          ("باادب شو", "با ادب شو", "be polite", "polite mode"),

    # === Public commands ===
    "public_cmds":        ("دستورات عمومی روشن", "public commands on"),
    "public_no_cmds":     ("دستورات عمومی خاموش", "public commands off"),

    # === Words ===
    "block_word":         ("مسدود کلمه", "block word"),
    "unblock_word":       ("بازکردن کلمه", "unblock word"),

    # === Bot blocks ===
    "block_bot":          ("بلاک بات", "block bot"),
    "unblock_bot":        ("آن‌بلاک بات", "unblock bot"),
    "blocked_bots_list":  ("بات های بلاک شده", "blocked bots"),

    # === Invite link ===
    "get_link":           ("لینک", "link"),
    "set_max_invite":     ("تنظیم حداکثر دعوت", "set max invite", "set invite limit"),

    # === Filters ===
    "filters_list":       ("فیلترها", "filters"),
    "add_filter":         ("فیلتر", "filter"),
    "remove_filter":      ("حذف فیلتر", "delete filter", "remove filter"),
    "delete_msg":         ("حذف", "delete"),

    # === Warn ===
    "warn":               ("اخطار", "warn"),
    "clear_warns":        ("حذف اخطارها", "clear warns", "clear warnings"),
    "warn_max":           ("سقف اخطار", "set warn max", "warn max"),
    "set_warn_punish":    ("تعیین مجازات اخطار", "set warn punishment", "warn punishment"),

    # === Mute / kick / ban ===
    "mute":               ("خفه", "سکوت", "mute"),
    "unmute":             ("آن‌میوت", "آن میوت", "ان میوت", "unmute"),
    "kick":               ("ریم", "کیک", "سیک", "kick"),
    "ban":                ("بن", "سیکتیر", "ban"),
    "ban_silent":         ("بن+", "مخفی کاری", "سیک مخفی", "silent ban", "ban+"),
    "unban":              ("آن‌بن", "آن بن", "ان بن", "unban"),

    # === Report ===
    "report":             ("گزارش", "report"),
    "@admins":            ("@admins",),

    # === Echo ===
    "echo":               ("اکو", "echo"),

    # === Info / alias / origin ===
    "info":               ("اطلاعات", "info"),
    "alias":              ("لقب", "nickname", "alias"),
    "set_alias":          ("ثبت لقب", "set nickname", "set alias"),
    "origin":             ("اصل", "origin"),
    "set_origin":         ("ثبت اصل", "set origin"),

    # === Settings ===
    "set_welcome":        ("تنظیم خوشامد", "set welcome"),
    "set_rules":          ("تنظیم قوانین", "set rules"),
    "set_comment":        ("تنظیم متن کامنت", "set comment"),

    # === Join request ===
    "join_request":       ("درخواست برای ورود", "join request", "request join"),

    # === Request help ===
    "request_help":       ("درخواست کمک", "request help"),

    # === Rules ===
    "rules":              ("قوانین", "rules"),

    # === Stats ===
    "stats":              ("آمار", "stats"),
    "my_stats":           ("آمار من", "mystats", "my stats"),
    "reset_stats":        ("ریست آمار", "reset stats"),

    # === Language ===
    "set_language":       ("تنظیم زبان", "set language"),
}

# Build a fast lookup: key -> set of lowercase acceptable strings
COMMAND_SETS = {k: {s.lower() for s in v} for k, v in COMMANDS.items()}


def cmd_match(text, cmd_key):
    """Check if text matches any of the command variants for cmd_key (case-insensitive)."""
    if not text:
        return False
    return text.lower() in COMMAND_SETS.get(cmd_key, set())


def cmd_startswith(text, cmd_key):
    """Check if text starts with any of the command variants for cmd_key (case-insensitive).
    Returns the stripped remainder after the matched command, or None."""
    if not text:
        return None
    text_lower = text.lower()
    for variant in COMMAND_SETS.get(cmd_key, set()):
        if text_lower.startswith(variant):
            remainder = text[len(variant):].strip()
            return remainder
    return None
