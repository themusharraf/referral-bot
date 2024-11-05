# Python bilan telegram bot uchun noyob havola yaratish
## 1. User Modeli Ta'rifi
User modeli har bir foydalanuvchini ma'lumotlar bazasida ifodalaydi va asosiy ma'lumotlarni saqlash uchun maydonlarga ega:

id: Har bir foydalanuvchi uchun noyob integer identifikatori, asosiy kalit `(pk=True)` sifatida belgilangan.
`user_id:` Foydalanuvchining noyob identifikatori, bu Telegram user_id yoki boshqa noyob ID bo'lishi mumkin.` unique=True` bilan yagona bo'lishi ta'minlangan.
`referral_code`: 36 belgigacha bo'lgan noyob satr `(CharField)` maydoni. Bu kod foydalanuvchining `referal identifikatori` sifatida xizmat qiladi.
`referred_by:` Boshqa bir foydalanuvchiga ishora qiluvchi xorijiy kalit. Bu maydon foydalanuvchini boshqa bir foydalanuvchi tomonidan taklif qilinganligini ko'rsatadi. Agar foydalanuvchi hech kim tomonidan taklif qilinmagan bo'lsa, bu maydon null=True bo'lib qoladi.
`referral_count:` 0 ga teng bo'lgan boshlang'ich qiymatga ega integer maydoni. Bu har bir foydalanuvchi tomonidan taklif qilingan odamlar sonini kuzatib boradi.
Meta Klass
Meta klassida model uchun jadval nomi "`users`" deb belgilangan.
`generate_unique_referral_code` Metodi
Bu sinf usuli `(@classmethod) `bo'lib, har bir foydalanuvchi uchun noyob referal kodini yaratadi.
Metod random `UUID (universial noyob identifikator)` yaratadi va bazada bunday kod mavjudligini tekshiradi` (await cls.filter(referral_code=referral_code).exists()).`
Agar noyob kod topilsa, u qaytariladi.
## 2. add_user Funksiyasi
add_user funksiyasi yangi foydalanuvchini tizimga ro'yxatdan o'tkazadi va agar kerak bo'lsa, uni referal orqali o'rnatadi.

`user_id:` Foydalanuvchining noyob identifikatori (ehtimol, Telegram orqali olingan).
`referred_by_code:` Bu ixtiyoriy parametr bo'lib, foydalanuvchini taklif qilgan boshqa foydalanuvchining referal kodi hisoblanadi. Agar bu berilgan bo'lsa, funksiyada taklif qiluvchining `referral_count` qiymati oshiriladi.
Qadamlar:

Referal Kod Yaratish: generate_unique_referral_code chaqirilib, yangi noyob referal kodi yaratiladi.
Foydalanuvchi Yaratish: Yangi `User` obyekti `user_id, referral_code, va referred_by` `None` bo'lgan holda yaratiladi.
Taklif Qiluvchini Tekshirish: Agar `referred_by_code` berilgan bo'lsa:
Mazkur referal kodiga ega User yozuvini olib keladi.
Agar taklif qiluvchi foydalanuvchi topilsa (`referrer)`, unda `user.referred_by` qiymati shu taklif qiluvchiga o'rnatiladi va taklif qiluvchi foydalanuvchining `referral_count` qiymati 1 ga oshiriladi va saqlanadi.

Foydalanuvchini Saqlash: Yaratilgan yangi user ma'lumotlar bazasida saqlanadi.
## 3. startup Funktsiyasi
startup funksiyasi Tortoise ORM ni ishga tushiradi va ma'lumotlar bazasidagi sxemani yaratadi.

`await Tortoise.init(...): sqlite://db.sqlite3` bilan `SQLite` ma'lumotlar bazasiga ulanadi va model aniqlamalarini __main__ dan olishini bildiradi.
`await Tortoise.generate_schemas():` Kerakli jadval tuzilmalarini yaratadi (User modeli uchun "users" jadvalini yaratadi).
Ishlash Jarayonining Qisqacha Tavsifi
Foydalanuvchini Ro'yxatdan O'tkazish: Yangi foydalanuvchi ro'yxatdan o'tganida, add_user chaqiriladi. Agar foydalanuvchi boshqa bir foydalanuvchi tomonidan taklif qilingan bo'lsa, `referred_by` maydoni o'rnatiladi va taklif qiluvchining referral_count qiymati oshiriladi.
Referallarni Kuzatish: Har bir foydalanuvchi noyob `referral_code` ga ega bo'lib, boshqalar bu kod orqali ro'yxatdan o'tishi mumkin.
Ma'lumotlar Bazasini Sozlash: `startup` ma'lumotlar bazasiga ulanishni ishga tushiradi va kerakli jadval tuzilmalari yaratadi.
Bu kod har bir foydalanuvchiga noyob `referal` kod berishni, referallarni kuzatishni va referal sonini dinamik tarzda yangilashni ta'minlaydi.
### database architecture
![Screenshot 2024-11-05 at 16 47 16](https://github.com/user-attachments/assets/d8b11345-799c-4676-8a14-e6dda9d8cd3c)
![Screenshot 2024-11-05 at 16 46 00](https://github.com/user-attachments/assets/fc46745e-4c2f-4a03-b45f-aa96c7c29bdc)
