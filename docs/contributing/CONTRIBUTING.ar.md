# دليل المساهمة

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/flat.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

<!-- work-only:start -->
## الفروع

| الفرع | الغرض |
| --- | --- |
| `main` | نسخة طبق الأصل من [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). تتم مزامنته يوميًا، ولا تُجرِ أي commit فيه أبدًا. |
| `work` | الفرع الافتراضي. يضم التغييرات الخاصة بهذا الـ fork: CI والأتمتة والوثائق وإصلاحات الـ casks. افتح طلبات السحب (pull requests) عليه. |
| `upstream-submit` | commit جاهز للمستودع الرسمي مبني على `main` الرسمي؛ يُحدَّث تلقائيًا بعد نجاح CI لفرع `work` عندما لا يكون هناك PR مفتوح إلى المستودع الرسمي. |
| `upstream-submit-*` | لقطات مؤقتة ينشئها `scripts/open_upstream_pr.sh`؛ منفصلة عن فرع الإرسال الثابت. |

`main` نسخة طبق الأصل من المستودع الرسمي، لذا لا تُجرِ commit عليه مباشرة. أرسل التغييرات إلى الفرع الافتراضي `work`.

التفاصيل التشغيلية والجداول الزمنية وإضافة Releases السابقة: [MAINTENANCE.md](../../.github/MAINTENANCE.md).
<!-- work-only:end -->

## قبل فتح طلب سحب

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # اختبارات السكربتات
brew style leejongyoung/egovframe/egovframedev-latest   # يتطلب الـ tap: brew tap leejongyoung/egovframe
```

يشغّل CI (`ci.yml`) الاختبارات إضافةً إلى `scripts/check_tap.sh` (`brew readall` و`brew style` و`brew audit`). شغّل الأوامر من جذر المستودع؛ تحتاج اختبارات السكربتات إلى PyYAML، ويثبّته CI بالطريقة نفسها.

- تتبع رسائل commit الأسلوب المستخدم أصلًا في المستودع الرسمي: `feat(casks): add egovframedev@X.Y.Z` و`fix(casks): …` و`docs(readme): …` و`ci: …`.
- لا تعدّل SHA-256 الخاص بأي cask يدويًا. تأتي الإصدارات الجديدة من `scripts/update_casks.py` (سير عمل `Update casks`)؛ ولإعادة التحقق من hash موجود شغّل `gh workflow run update-casks.yml -f verify=<version>`.
- cask واحد لكل سلسلة إصدارات فرعية: عند إضافة `5.0.3` يُحذف `5.0.2` (الاتفاقية نفسها المتبعة في المستودع الرسمي).

## GitHub Actions والفوترة

- **مجاني في المستودعات العامة:** وفق سياسة الفوترة في GitHub، فإن الـ runners القياسية التي تستضيفها GitHub (`ubuntu-latest` و`macos-latest`) **مجانية بلا حد للدقائق في المستودعات العامة**. تُحسب قيمة hash لملفات DMG أثناء التدفق في `update-casks.yml` ولا تُرفع أبدًا كـ artifacts في Actions أو كأصول في Release، لذا لا تُستهلك حصة تخزين Actions أيضًا.
- تُخصم الدقائق من الحصة المجانية لحسابك فقط إذا نسخت المستودع إلى مستودع خاص وشغّلته هناك.

<!-- work-only:start -->
## الإرسال إلى المستودع الرسمي

استخدم السكربت بدلًا من دفع `work` نفسه. فهو ينشئ commit نظيفًا واحدًا فوق فرع المستودع الرسمي انطلاقًا من الفروق بينه وبين `work`، ويستبعد الملفات الخاصة بالـ fork فقط (`.github/MAINTENANCE.md` و`.github/UPSTREAM_PR.md` و`.github/workflows/sync-upstream.yml` و`scripts/open_upstream_pr.sh` و`tests/test_open_upstream_pr.py` والكتل الموسومة بـ `work-only`):

```bash
scripts/open_upstream_pr.sh --dry-run                        # ما الذي سيُرسل
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```
<!-- work-only:end -->

## الأمان

لا تبلّغ عن الثغرات الأمنية في issues؛ اتبع الإجراء الموضح في [SECURITY.ar.md](../security/SECURITY.ar.md).
