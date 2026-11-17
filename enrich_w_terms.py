# -*- coding: utf-8 -*-
"""
Enrich the final 10 terms of letter W to achieve 100.0% completion for W.
"""

import json
import os
import re

DICT_FILE = "bilingual_dictionary.json"

W_TERMS_DATA = [
    {
        "slug": "w9form",
        "term_en": "W-9 Form",
        "term_fa": "فرم W-9 (درخواست شماره شناسایی مؤدی)",
        "category": "مالیات، حقوق مالی و مقررات",
        "category_fa": "مالیات، حقوق مالی و مقررات",
        "category_en": "Taxation, Financial Law & Regulation",
        "definition_en": "Form W-9 is an official IRS tax document used by businesses to obtain the correct legal name, address, and Taxpayer Identification Number (TIN) or Social Security Number (SSN) of independent contractors, freelance workers, and vendors.",
        "definition_fa": "فرم W-9 یک سند مالیاتی رسمی اداره خدمات درآمد داخلی آمریکا (IRS) است که توسط کسب‌وکارها برای اخذ نام قانونی، آدرس و شماره شناسایی مالیاتی (TIN) یا شماره تأمین اجتماعی (SSN) پیمانکاران مستقل و ارائه‌دهندگان خدمات استفاده می‌شود.",
        "takeaways_en": [
            "Used exclusively for independent contractors and non-employee vendors, not regular employees.",
            "Helps businesses prepare Form 1099-NEC to report non-employee compensation to the IRS.",
            "Does not trigger tax withholding unless the contractor is subject to backup withholding."
        ],
        "takeaways_fa": [
            "منحصراً برای پیمانکاران مستقل و فریلنسرها به کار می‌رود و برای کارمندان دائمی استفاده نمی‌شود.",
            "به کسب‌وکارها کمک می‌کند تا فرم 1099-NEC را جهت گزارش پرداخت‌ها به اداره مالیات آماده کنند.",
            "باعث کسر مالیات در منبع نمی‌شود، مگر اینکه پیمانکار مشمول کسر مالیات علی‌الحساب احتیاطی باشد."
        ],
        "bottom_line_en": "Form W-9 serves as a vital compliance instrument ensuring that entities paying independent contractors properly document recipient tax identities and avoid IRS reporting penalties.",
        "bottom_line_fa": "فرم W-9 به عنوان یک ابزار انطباق حیاتی عمل می‌کند که تضمین می‌نماید پرداخت‌ها به پیمانکاران مستقل با هویت مالیاتی صحیح ثبت شده و از جریمه‌های مالیاتی جلوگیری گردد.",
        "sections": [
            {
                "title_en": "What Is Form W-9?",
                "title_fa": "فرم W-9 چیست؟",
                "paragraphs_en": [
                    "Form W-9, formally known as the Request for Taxpayer Identification Number and Certification, is widely utilized in the United States when a business hires an independent contractor or vendor whose compensation is expected to exceed $600 in a calendar year."
                ],
                "paragraphs_fa": [
                    "فرم W-9 که رسماً به عنوان درخواست شماره شناسایی مؤدی و گواهی مالیاتی شناخته می‌شود، زمانی که یک شرکت پیمانکار یا فریلنسری را استخدام کند که انتظار می‌رود دستمزد او در سال تقویمی از ۶۰۰ دلار بیشتر باشد، به کار گرفته می‌شود."
                ],
                "items_en": [],
                "items_fa": []
            },
            {
                "title_en": "Key Components of the W-9 Form",
                "title_fa": "بخش‌های کلیدی فرم W-9",
                "paragraphs_en": [
                    "When filling out Form W-9, payees must certify under penalties of perjury that their taxpayer information is correct and whether they are exempt from backup withholding."
                ],
                "paragraphs_fa": [
                    "هنگام تکمیل فرم W-9، دریافت‌کننده وجه باید تحت سوگند قانونی گواهی دهد که اطلاعات شناسایی مالیاتی او صحیح بوده و معاف از کسر علی‌الحساب است."
                ],
                "items_en": [
                    "Legal Name of the business or individual",
                    "Federal tax classification (Sole proprietorship, LLC, Corporation)",
                    "Taxpayer Identification Number (SSN or EIN)"
                ],
                "items_fa": [
                    "نام قانونی شخص حقیقی یا شخصیت حقوقی",
                    "طبقه‌بندی ساختار مالیاتی فدرال (انفرادی، با مسئولیت محدود، شرکت سهامی)",
                    "شماره شناسایی مالیاتی (شماره تأمین اجتماعی یا شناسه کارفرمایی)"
                ]
            }
        ]
    },
    {
        "slug": "w-shaped-recovery",
        "term_en": "W-Shaped Recovery",
        "term_fa": "بهبود اقتصادی W شکل (رکود دوگانه)",
        "category": "اقتصاد کلان و سیاست‌های پولی",
        "category_fa": "اقتصاد کلان و سیاست‌های پولی",
        "category_en": "Macroeconomics & Monetary Policy",
        "definition_en": "A W-shaped recovery is an economic cycle pattern characterized by an economy falling into recession, rebounding sharply for a brief period, falling back into a second recession, and finally recovering sustainably—often referred to as a double-dip recession.",
        "definition_fa": "بهبود W شکل الگویی از چرخه اقتصادی است که در آن اقتصاد دچار رکود شده، سپس به سرعت و به طور موقت رونق نسبی می‌گیرد، مجدداً وارد رکود دوم می‌شود و نهایتاً به رشد پایدار می‌رسد که به آن رکود دوگانه نیز می‌گویند.",
        "takeaways_en": [
            "Represents a highly volatile economic cycle characterized by false recoveries.",
            "Can cause severe whipsaws in equity markets and corporate capital expenditures.",
            "Often triggered by premature monetary tightening or recurring macroeconomic shocks."
        ],
        "takeaways_fa": [
            "بیانگر یک چرخه اقتصادی بسیار پرنوسان همراه با سیگنال‌های بهبود کاذب است.",
            "می‌تواند شوک‌های شدیدی به بازارهای سهام و مخارج سرمایه‌ای شرکت‌ها وارد کند.",
            "معمولاً در اثر انقباض زودهنگام سیاست‌های پولی یا شوک‌های مکرر اقتصاد کلان رخ می‌دهد."
        ],
        "bottom_line_en": "W-shaped recoveries trap investors and policymakers who mistake intermediate bounces for long-term growth before macroeconomic structural weaknesses drag the economy back down.",
        "bottom_line_fa": "بهبودهای W شکل سرمایه‌گذاران و سیاست‌گذارانی را به دام می‌اندازد که رشد موقت میان‌دوره‌ای را با رشد بلندمدت اشتباه می‌گیرند، پیش از آنکه ضعف‌های ساختاری اقتصاد را دوباره به زیر بکشد.",
        "sections": [
            {
                "title_en": "Dynamics of a Double-Dip Recession",
                "title_fa": "مکانیسم و دینامیک رکود دوگانه",
                "paragraphs_en": [
                    "In a W-shaped trajectory, gross domestic product (GDP) exhibits two distinct troughs separated by a false dawn. The initial bounce often results from government stimulus, but once stimulus fades, underlying economic vulnerabilities precipitate the second downturn."
                ],
                "paragraphs_fa": [
                    "در مسیر W شکل، تولید ناخالص داخلی (GDP) دو فرورفتگی مجزا را تجربه می‌کند که توسط یک رونق موقت از هم جدا شده‌اند. جهش اولیه غالباً حاصل محرک‌های دولتی است، اما با کمرنگ شدن محرک‌ها، آسیب‌پذیری‌های زمینه‌ای رکود دوم را رقم می‌زنند."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "wage-assignment",
        "term_en": "Wage Assignment",
        "term_fa": "واگذاری دستمزد (کسر از حقوق داوطلبانه)",
        "category": "بانکداری، وام و اعتبارات",
        "category_fa": "بانکداری، وام و اعتبارات",
        "category_en": "Banking, Loans & Credit",
        "definition_en": "A wage assignment is a voluntary agreement in which an employee permits their employer to deduct a specified portion of their salary to remit directly to a creditor for debt repayment.",
        "definition_fa": "واگذاری دستمزد یک توافق داوطلبانه است که طی آن کارمند به کارفرمای خود اجازه می‌دهد بخش مشخصی از حقوق ماهانه او را کسر کرده و مستقیماً به بستانکار جهت تسویه بدهی بپردازد.",
        "takeaways_en": [
            "Voluntary arrangement agreed upon between debtor and creditor, unlike court-ordered garnishment.",
            "Commonly used to secure personal loans, consumer leases, or child support obligations.",
            "Subject to statutory percentage ceilings under consumer protection regulations."
        ],
        "takeaways_fa": [
            "بر خلاف توقیف قضایی دستمزد، یک توافق کاملاً داوطلبانه میان بدهکار و بستانکار است.",
            "معمولاً برای تضمین بازپرداخت وام‌های شخصی، اجاره‌های اعتباری یا نفقه استفاده می‌شود.",
            "طبق قوانین حمایت از مصرف‌کننده، دارای سقف درصدی مجاز در کسر از حقوق است."
        ],
        "bottom_line_en": "Wage assignments provide lenders with reliable repayment mechanisms while giving borrowers a streamlined method to manage delinquent debt without court litigation.",
        "bottom_line_fa": "واگذاری دستمزد سازوکار مطمئنی برای بازپرداخت وام‌دهندگان فراهم می‌کند و به وام‌گیرندگان اجازه می‌دهد بدون دعاوی قضایی، بدهی‌های خود را مدیریت کنند.",
        "sections": [
            {
                "title_en": "Wage Assignment vs. Wage Garnishment",
                "title_fa": "تفاوت واگذاری دستمزد با توقیف قضایی حقوق",
                "paragraphs_en": [
                    "While wage garnishment requires a formal court judgment and court order served directly to an employer, a wage assignment is contractually executed at the inception of loan origination or through mutual consent."
                ],
                "paragraphs_fa": [
                    "در حالی که توقیف قضایی دستمزد نیازمند حکم قطعی دادگاه و ابلاغیه قضایی به کارفرما است، واگذاری دستمزد از طریق توافق قراردادی در زمان اعطای وام یا رضایت دوجانبه انجام می‌شود."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "wage-expense",
        "term_en": "Wage Expense",
        "term_fa": "هزینه دستمزد (حقوق و دستمزد مستقیم)",
        "category": "حسابداری و استانداردهای مالی",
        "category_fa": "حسابداری و استانداردهای مالی",
        "category_en": "Accounting & Financial Standards",
        "definition_en": "Wage expense represents the total aggregate cost incurred by a business entity to compensate hourly employees, contractors, and production personnel during an accounting period.",
        "definition_fa": "هزینه دستمزد بیانگر کل هزینه‌هایی است که یک واحد تجاری در طول یک دوره مالی برای جبران خدمات کارکنان ساعتی، فریلنسرها و نیروهای تولیدی خود پرداخت می‌کند.",
        "takeaways_en": [
            "Reported on the income statement as either cost of goods sold (COGS) or operating expenses (OPEX).",
            "Includes gross wages earned before deductions for payroll taxes, health insurance, and retirement plans.",
            "Accrual accounting requires recording unpaid earned wages as an accrued wage liability."
        ],
        "takeaways_fa": [
            "در صورت سود و زیان بسته به ماهیت به عنوان بهای تمام‌شده کالای فروش‌رفته (COGS) یا هزینه عملیاتی ثبت می‌شود.",
            "شامل دستمزد ناخالص قبل از کسورات مالیات بر درآمد، بیمه و بازنشستگی است.",
            "بر مبنای حسابداری تعهدی، دستمزدهای پرداخت‌نشده دوره باید به عنوان بدهی جاری تعهدی ثبت شوند."
        ],
        "bottom_line_en": "Accurately classifying and controlling wage expense is fundamental to monitoring operational efficiency, gross margins, and labor productivity ratios.",
        "bottom_line_fa": "طبقه‌بندی دقیق و کنترل هزینه دستمزد برای نظارت بر کارایی عملیاتی، حاشیه سود ناخالص و شاخص‌های بهره‌وری نیروی کار حیاتی است.",
        "sections": [
            {
                "title_en": "Accounting Treatment of Wage Expense",
                "title_fa": "نحوه ثبت حسابداری هزینه دستمزد",
                "paragraphs_en": [
                    "Direct labor costs tied directly to manufacturing are capitalized into inventory and expensed under COGS, whereas supervisory and administrative wages are treated as selling, general, and administrative (SG&A) period costs."
                ],
                "paragraphs_fa": [
                    "دستمزد مستقیم نیروی کار در خط تولید به بهای تمام‌شده موجودی کالا منظور شده و در سرفصل COGS قرار می‌گیرد، اما دستمزد نیروهای اداری و ستادی در زمره هزینه‌های عمومی و اداری (SG&A) ثبت می‌گردد."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "wage-push-inflation",
        "term_en": "Wage Push Inflation",
        "term_fa": "تورم ناشی از فشار دستمزد",
        "category": "اقتصاد کلان و سیاست‌های پولی",
        "category_fa": "اقتصاد کلان و سیاست‌های پولی",
        "category_en": "Macroeconomics & Monetary Policy",
        "definition_en": "Wage-push inflation is a form of cost-push inflation where aggregate real wages rise faster than labor productivity, forcing employers to raise prices on goods and services to maintain profit margins.",
        "definition_fa": "تورم ناشی از فشار دستمزد نوعی از تورم فشار هزینه است که در آن دستمزدهای واقعی سریع‌تر از بهره‌وری نیروی کار افزایش می‌یابند و کارفرمایان را مجبور می‌سازند برای حفظ حاشیه سود خود، قیمت کالاها و خدمات را افزایش دهند.",
        "takeaways_en": [
            "Occurs primarily in tight labor markets with near full employment and strong union bargaining power.",
            "Can trigger a self-reinforcing wage-price spiral as workers demand further wage hikes to counter rising inflation.",
            "Central banks combat it by raising interest rates to soften aggregate demand and labor tightness."
        ],
        "takeaways_fa": [
            "عمدتاً در بازارهای کار فشرده با اشتغال کامل و قدرت چانه‌زنی بالای اتحادیه‌های کارگری رخ می‌دهد.",
            "می‌تواند به مارپیچ دستمزد-قیمت منجر شود که در آن کارگران برای جبران گرانی‌ها مجدداً خواهان افزایش دستمزد می‌شوند.",
            "بانک‌های مرکزی با افزایش نرخ بهره و تعدیل تقاضای کل برای مهار آن مداخله می‌کنند."
        ],
        "bottom_line_en": "Wage-push inflation underscores the delicate equilibrium between labor earnings and economic output, highlighting how wage growth without matching productivity gains drives systemic inflation.",
        "bottom_line_fa": "تورم فشار دستمزد بر تعادل حساس میان درآمد نیروی کار و تولید واقعی تأکید دارد و نشان می‌دهد رشد دستمزد بدون افزایش بهره‌وری، محرک تورم ساختاری است.",
        "sections": [
            {
                "title_en": "The Wage-Price Spiral Dynamics",
                "title_fa": "سازوکار مارپیچ دستمزد-قیمت",
                "paragraphs_en": [
                    "When general prices escalate, consumer purchasing power diminishes. Employees demand higher compensation to maintain their standard of living. Businesses comply but consequently raise end-product prices, creating a continuous upward spiral in price levels."
                ],
                "paragraphs_fa": [
                    "با افزایش قیمت‌های عمومی، قدرت خرید کاهش می‌یابد و کارکنان خواستار دستمزد بالاتر می‌شوند. شرکت‌ها با افزایش دستمزدها موافقت کرده اما به ناچار قیمت نهایی محصولات را گران می‌کنند و چرخه‌ای ادامه‌دار شکل می‌گیرد."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "waiting-period",
        "term_en": "Waiting Period",
        "term_fa": "دوره انتظار (دوره بررسی صلاحیت)",
        "category": "مدیریت ریسک، بیمه و اکچوئری",
        "category_fa": "مدیریت ریسک، بیمه و اکچوئری",
        "category_en": "Risk Management, Insurance & Actuarial",
        "definition_en": "A waiting period is a specified span of time that must elapse between an individual's enrollment or policy inception and the effective commencement of full insurance coverage or benefit eligibility.",
        "definition_fa": "دوره انتظار به بازه زمانی مشخصی گفته می‌شود که باید بین ثبت‌نام یا صدور بیمه‌نامه تا آغاز رسمی پوشش بیمه‌ای یا دریافت مزایا سپری شود.",
        "takeaways_en": [
            "Protects insurers from adverse selection and immediate claims on preexisting conditions.",
            "Common in health, disability, and unemployment insurance plans.",
            "Also applies in corporate vesting schedules before employees can exercise stock options."
        ],
        "takeaways_fa": [
            "از شرکت‌های بیمه در برابر گزینش نامساعد و ادعاهای خسارت زودهنگام بیماری‌های قبلی محافظت می‌کند.",
            "در بیمه‌های درمانی، ازکارافتادگی و مقرری بیکاری کاربرد گسترده‌ای دارد.",
            "در برنامه‌های سهام تشویقی شرکت‌ها قبل از اعطای حق اعمال سهام نیز به کار می‌رود."
        ],
        "bottom_line_en": "Waiting periods balance moral hazard and underwriting viability for financial institutions, ensuring participants maintain sustained policy commitment.",
        "bottom_line_fa": "دوره‌های انتظار مخاطرات اخلاقی را کاهش داده و بقای مالی نهادهای بیمه‌گر را تضمین می‌نمایند تا افراد تعهد بلندمدت‌تری به بیمه‌نامه داشته باشند.",
        "sections": [
            {
                "title_en": "Applications Across Insurance and Retirement",
                "title_fa": "کاربردها در صنعت بیمه و طرح‌های بازنشستگی",
                "paragraphs_en": [
                    "In disability insurance, the elimination period acts as a waiting period between the onset of disability and when benefit checks begin. In retirement plans, probationary waiting periods must be completed prior to employer 401(k) matching contributions."
                ],
                "paragraphs_fa": [
                    "در بیمه ازکارافتادگی، دوره حذف به عنوان دوره انتظار میان آغاز ناتوانی تا پرداخت مستمری عمل می‌کند. در طرح‌های بازنشستگی نیز برای مشمول شدن کمک‌های کارفرما دوره‌های انتظار اعمال می‌شود."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "waiver-of-notice",
        "term_en": "Waiver of Notice",
        "term_fa": "انصراف از اخطار رسمی (حقوق شرکتی)",
        "category": "قوانین و صورت‌های مالی",
        "category_fa": "قوانین و صورت‌های مالی",
        "category_en": "Financial Regulations & Reporting",
        "definition_en": "A waiver of notice is a legal corporate document in which directors, shareholders, or committee members formally relinquish their statutory right to advance formal notification before a corporate meeting.",
        "definition_fa": "انصراف از اخطار رسمی یک سند حقوقی شرکتی است که در آن اعضای هیئت‌مدیره، سهامداران یا اعضای کمیته‌ها رسماً از حق قانونی خود مبنی بر دریافت دعوت‌نامه رسمی قبلی برای تشکیل جلسه صرف‌نظر می‌کنند.",
        "takeaways_en": [
            "Enables corporations to hold urgent emergency meetings legally without waiting out statutory notice periods.",
            "Can be executed before, during, or after the meeting takes place to validate corporate actions.",
            "Prevents absent or dissenting parties from nullifying decisions based on technical procedural defects."
        ],
        "takeaways_fa": [
            "به شرکت‌ها اجازه می‌دهد جلسات اضطراری را بدون سپری شدن مهلت قانونی ارسال دعوت‌نامه برگزار کنند.",
            "می‌تواند قبل، حین یا پس از جلسه جهت تنفیذ تصمیمات امضا و ثبت شود.",
            "مانع از ابطال مصوبات توسط افراد غایب به بهانه نقایص تشریفاتی دعوت می‌گردد."
        ],
        "bottom_line_en": "Waivers of notice provide agile governance flexibility in fast-moving commercial environments while maintaining procedural legitimacy under corporate bylaws.",
        "bottom_line_fa": "فرم‌های انصراف از اخطار، انعطاف‌پذیری و سرعت تصمیم‌گیری حاکمیت شرکتی را در شرایط بحرانی تضمین کرده و مشروعیت مصوبات را حفظ می‌کنند.",
        "sections": [
            {
                "title_en": "Legal Significance in Corporate Governance",
                "title_fa": "اهمیت حقوقی در حاکمیت شرکتی",
                "paragraphs_en": [
                    "Corporate bylaws mandate advance notice (often 10 to 60 days) to ensure stakeholders can prepare for votes. A waiver signed by all parties affirms that all participants consented to hold the meeting and ratify binding resolutions immediately."
                ],
                "paragraphs_fa": [
                    "اساسنامه‌های شرکتی ارسال اخطار قبلی (معمولاً بین ۱۰ تا ۶۰ روز) را الزامی می‌دانند. امضای فرم انصراف توسط تمام اعضا نشان می‌دهد که همگان با برگزاری فوری جلسه و تصویب مصوبات الزام‌آور موافقت کرده‌اند."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "warranty",
        "term_en": "Warranty",
        "term_fa": "ضمانت‌نامه / گارانتی معتبر",
        "category": "قوانین و صورت‌های مالی",
        "category_fa": "قوانین و صورت‌های مالی",
        "category_en": "Financial Regulations & Reporting",
        "definition_en": "A warranty is a legally binding guarantee issued by a manufacturer, seller, or service provider assuring the purchaser that the good or service meets specified quality, durability, and performance benchmarks.",
        "definition_fa": "ضمانت‌نامه (گارانتی) یک تعهد الزام‌آور قانونی است که توسط سازنده، فروشنده یا ارائه‌دهنده خدمت صادر می‌شود و به خریدار اطمینان می‌دهد کالا یا خدمت از کیفیت، دوام و استانداردهای عملکردی مشخصی برخوردار است.",
        "takeaways_en": [
            "Differentiated between express warranties (written explicit promises) and implied warranties (assumed by law).",
            "Creates a contingent warranty liability that companies must accrue on financial balance sheets.",
            "Extended warranties can be purchased separately as insurance-like protection contracts."
        ],
        "takeaways_fa": [
            "به دو دسته ضمانت‌های صریح (تعهدات کتبی) و ضمانت‌های ضمنی (مقرر شده توسط قانون) تقسیم می‌شود.",
            "موجب ایجاد بدهی احتمالی ضمانت در ترازنامه مالی شرکت‌ها جهت پوشش خدمات پس از فروش می‌گردد.",
            "گارانتی‌های تمدیدشده را می‌توان به صورت مجزا به عنوان قراردادهای حفاظتی شبه‌بیمه خریداری کرد."
        ],
        "bottom_line_en": "Warranties mitigate transaction risk for buyers while functioning as competitive marketing tools and predictable accounting liabilities for manufacturers.",
        "bottom_line_fa": "ضمانت‌نامه‌ها ریسک معاملات را برای خریداران کاهش می‌دهند و هم‌زمان به عنوان ابزار رقابتی بازاریابی و تعهدات حسابداری در شرکت‌ها شناخته می‌شوند.",
        "sections": [
            {
                "title_en": "Express vs. Implied Warranties",
                "title_fa": "ضمانت‌های صریح در مقابل ضمانت‌های ضمنی",
                "paragraphs_en": [
                    "An express warranty involves specific affirmative claims made about product specifications or repair commitments. An implied warranty, such as the warranty of merchantability, automatically applies by operation of commercial law."
                ],
                "paragraphs_fa": [
                    "ضمانت صریح شامل وعده‌ها و تعهدات مشخص کتبی در مورد مشخصات یا تعمیر کالا است، در حالی که ضمانت ضمنی (مانند ضمانت قابلیت فروش) به صورت خودکار به حکم قانون تجارت اعمال می‌شود."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "whisperstock",
        "term_en": "Whisper Stock",
        "term_fa": "سهم شایعه‌شده (دارای اخبار نهانی غیررسمی)",
        "category": "بورس، سهام و بازار سرمایه",
        "category_fa": "بورس، سهام و بازار سرمایه",
        "category_en": "Stock Markets & Securities",
        "definition_en": "A whisper stock refers to the equity shares of a company that experiences substantial speculative trading activity driven by circulating rumors, unannounced corporate developments, or leaked earnings forecasts.",
        "definition_fa": "سهم شایعه‌شده به سهام شرکتی اطلاق می‌شود که معاملات آن بر اثر شایعات تأییدنشده، اخبار ادغام یا پیش‌بینی‌های غیررسمی درز کرده از درآمد شرکت (ارقام نجوا)، دستخوش نوسان و رفتارهای سوداگرانه شدید می‌شود.",
        "takeaways_en": [
            "Driven by unofficial estimates ('whisper numbers') that circulate among Wall Street institutional desks.",
            "Exhibits heightened volatility and speculative trading volume prior to official corporate filings.",
            "Poses significant downside risk if official earnings or acquisition announcements disappoint rumor-fueled expectations."
        ],
        "takeaways_fa": [
            "معمولاً از ارقام غیررسمی (Whisper Numbers) که میان معامله‌گران نهادی زمزمه می‌شود الگو می‌گیرد.",
            "پیش از گزارش‌های رسمی شرکت با نوسانات بسیار شدید و حجم معاملات غیرعادی همراه است.",
            "در صورت برآورده نشدن شایعات توسط گزارش‌های واقعی، خطر سقوط قیمتی بسیار بالایی برای سرمایه‌گذاران دارد."
        ],
        "bottom_line_en": "Trading whisper stocks carries substantial asymmetric risk, as prices frequently price in exaggerated rumors and succumb to 'buy the rumor, sell the news' profit taking.",
        "bottom_line_fa": "معامله سهام شایعه‌شده ریسک نامتقارن بالایی دارد، زیرا قیمت‌ها شایعات اغراق‌آمیز را پیش‌خور کرده و بر اساس پدیده «با شایعه بخر، با خبر بفروش» به سرعت دچار افت می‌شوند.",
        "sections": [
            {
                "title_en": "Whisper Numbers and Market Impact",
                "title_fa": "ارقام نجوا (Whisper Numbers) و اثر آن بر بازار",
                "paragraphs_en": [
                    "Whisper numbers represent the real unpublished earnings consensus among professional traders, often differing substantially from published consensus analyst targets compiled by major consensus agencies."
                ],
                "paragraphs_fa": [
                    "ارقام نجوا بیانگر اجماع واقعی و غیررسمی معامله‌گران حرفه‌ای در مورد سود هر سهم است که اغلب تفاوت چشمگیری با اجماع رسمی تحلیل‌گران وال‌استریت دارد."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    },
    {
        "slug": "working-tax-credit-wtc",
        "term_en": "Working Tax Credit (WTC)",
        "term_fa": "اعتبار مالیاتی شاغلین کم‌درآمد",
        "category": "مالیات، حقوق مالی و مقررات",
        "category_fa": "مالیات، حقوق مالی و مقررات",
        "category_en": "Taxation, Financial Law & Regulation",
        "definition_en": "The Working Tax Credit (WTC) is a state welfare and tax benefit system designed to supplement the earnings of low-income workers, incentivizing employment and reducing poverty.",
        "definition_fa": "اعتبار مالیاتی شاغلین (WTC) یک نظام رفاهی و تسهیلات مالیاتی دولتی است که برای تکمیل درآمد نیروی کار کم‌درآمد طراحی شده و هدف آن تشویق به اشتغال و کاهش فقر است.",
        "takeaways_en": [
            "Provides non-taxable regular cash top-ups directly to eligible working households.",
            "Calculated based on household income, hours worked per week, disability, and childcare costs.",
            "Widely phased into unified benefit systems like Universal Credit in modernized welfare jurisdictions."
        ],
        "takeaways_fa": [
            "کمک‌های نقدی معاف از مالیات را به صورت منظم به خانوارهای شاغل واجد شرایط واریز می‌کند.",
            "میزان آن بر اساس درآمد کل خانوار، ساعات کار هفتگی، افراد دارای معلولیت و هزینه‌های نگهداری فرزند محاسبه می‌شود.",
            "در بسیاری از کشورها با طرح‌های جامع رفاهی مدرن نظیر اعتبار فراگیر (Universal Credit) ادغام شده است."
        ],
        "bottom_line_en": "Working tax credits represent targeted fiscal policy instruments that maintain incentives to remain employed while providing an economic safety net for working families.",
        "bottom_line_fa": "اعتبارات مالیاتی شاغلین ابزارهای هدفمند سیاست مالی هستند که انگیزه ماندن در بازار کار را حفظ کرده و یک شبکه ایمنی اقتصادی برای خانواده‌ها ایجاد می‌کنند.",
        "sections": [
            {
                "title_en": "Eligibility Criteria and Structure",
                "title_fa": "شرایط احراز و ساختار اعطای اعتبار مالیاتی",
                "paragraphs_en": [
                    "To qualify, claimants must meet specific age thresholds, work a minimum number of paid hours per week (typically 16, 24, or 30 hours depending on family status), and earn below statutory household income caps."
                ],
                "paragraphs_fa": [
                    "برای واجد شرایط بودن، متقاضیان باید شرایط سنی، حداقل ساعات کار در هفته (معمولاً ۱۶، ۲۴ یا ۳۰ ساعت بسته به وضعیت تأهل و فرزندان) و درآمدی کمتر از سقف مجاز قانونی را داشته باشند."
                ],
                "items_en": [],
                "items_fa": []
            }
        ]
    }
]

def main():
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    dict_map = {t.get("slug"): t for t in data if t.get("slug")}
    
    updated_count = 0
    for w in W_TERMS_DATA:
        slug = w["slug"]
        if slug in dict_map:
            target = dict_map[slug]
            target["definition_en"] = w["definition_en"]
            target["definition_fa"] = w["definition_fa"]
            target["takeaways_en"] = w["takeaways_en"]
            target["takeaways_fa"] = w["takeaways_fa"]
            target["bottom_line_en"] = w["bottom_line_en"]
            target["bottom_line_fa"] = w["bottom_line_fa"]
            target["sections"] = w["sections"]
            target["category"] = w["category"]
            target["category_fa"] = w["category_fa"]
            target["category_en"] = w["category_en"]
            target["deep_enriched"] = True
            updated_count += 1
            print(f"[OK] Enriched: {w['term_en']} ({slug})")
        else:
            print(f"[WARN] Slug not found in dict: {slug}")

    # Save dictionary atomically
    tmp = DICT_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DICT_FILE)
    print(f"Successfully saved {updated_count} enriched terms to {DICT_FILE}!")

if __name__ == "__main__":
    main()
