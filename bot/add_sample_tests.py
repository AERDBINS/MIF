# bot/add_sample_tests.py
from bot.database import add_test, add_question, init_db
import sqlite3

init_db()

# Testni qo‘shish
add_test("🧮 Matematika testi", 3600)

# So‘nggi qo‘shilgan test ID sini olish
conn = sqlite3.connect("tests.db")
cur = conn.cursor()
cur.execute("SELECT MAX(id) FROM tests")
test_id = cur.fetchone()[0]
conn.close()

# test_id = 1 deb taxmin qilamiz
add_question(
    test_id=test_id,
    question="1) Uchburchakning ikkita tomoni 24 va 11 ga, ular orasidagi burchagi 120° ga teng. Shu uchburchakka tashqi chizilgan aylananing radiusini toping.",
    options=["31/√3", "40/√3", "20/√3", "3√2"],
    correct="31/√3"  # A
)

add_question(
    test_id=test_id,
    question="2) Agar f(4) = 5, f(3) = 4, f(2) = 3 bo‘lsa, (f⁻¹(3) + f⁻¹(4)) · f(4) ifodaning qiymatini hisoblang.",
    options=["35", "25", "15", "20"],
    correct="25"  # B
)

add_question(
    test_id=test_id,
    question="3) D(–1;0), C(0;–1), B(1;0), A(0;1) nuqtalardan hosil bo‘lgan ABCD to‘rtburchakning simmetriya nuqtasi koordinatalarini toping.",
    options=["(0;0)", "(1;1)", "(0;–1)", "(–1;–1)"],
    correct="(0;0)"  # A
)

add_question(
    test_id=test_id,
    question="4) (x, y) sonlar jufti {3x/(1–x) + y/(y+1) = 5, x/(1–x) + 3y/(y+1) = 7} tenglamalar sistemasining yechimi bo‘lsa, 6x + y ning qiymatini toping.",
    options=["–2", "0", "1", "–1"],
    correct="–1"  # C
)

add_question(
    test_id=test_id,
    question="5) 27/13 soni 5 1/3 ga ortgan bo‘lsa, necha marta ko‘paygan?",
    options=["5 1/3", "3", "46/81", "2 1/3"],
    correct="3"  # B
)

add_question(
    test_id=test_id,
    question="6) Rasmda ifodalangandek OD va CE kesmalar AB diametrga perpendikulyar bo‘lib, AO = 2CE bo‘lsa, S_ACB : S_ADB nisbatini toping.",
    options=["3:2", "1:4", "2:1", "1:2"],
    correct="1:2", # D,
    image_path ="image/q6.png"

)

add_question(
    test_id=test_id,
    question="7) Taqqoslang: a = 30¹³ va b = 17¹³ + 13¹³",
    options=["a = b", "a < b", "a > b", "a + 30 < b"],
    correct="a > b"  # C
)

add_question(
    test_id=test_id,
    question="8) Agar (sin(α – β))/(cos(α)cos(β)) = 2/√3 bo‘lsa, tgα – tgβ ni toping.",
    options=["√3/3", "2√3/3", "4√3/3", "√3"],
    correct="2√3/3"  # B
)

add_question(
    test_id=test_id,
    question="9) Hisoblang: ∫ 1/((1 + x²) arctg x) dx",
    options=["½ ln(arctg x) + C", "ln(1 + x²) + C", "(1 + x²) ln(arctg x)", "ln(arctg x) + C"],
    correct="ln(arctg x) + C"  # D
)

add_question(
    test_id=test_id,
    question="10) Katetlari 3 – 2√5 + x² = 0 tenglama ildizlariga teng bo‘lgan to‘g‘ri burchakli uchburchakning yuzini toping.",
    options=["4", "1.5", "2", "5"],
    correct="1.5"  # B
)
add_question(
    test_id=test_id,
    question="11) Muntazam parallelepipedning balandligi asosining tomonidan √6 marta katta. Parallelepipedning diagonali asos tekisligi bilan qanday burchak tashkil etadi?",
    options=["arccos(1/√6)", "30°", "60°", "arccos(1/2√3)"],
    correct="60°"
)

add_question(
    test_id=test_id,
    question="12) Arifmetik progressiyada a₁ + a₇ = 6 ga teng, a₉² – 2 ni toping.",
    options=["7", "1", "2", "3"],
    correct="7"
)

add_question(
    test_id=test_id,
    question="13) 20 / (1 + 20 / (1 + 20 / ... )) + 1 ni hisoblang.",
    options=["10", "6", "8", "5"],
    correct="5"
)

add_question(
    test_id=test_id,
    question="14) 2 + arcsin²x ≤ 2 / (tg²x + ctg²x) tengsizlikni yeching.",
    options=["π/4 + πn, n∈R", "[-π/2; π/2]", "R", "∅"],
    correct="∅"
)

add_question(
    test_id=test_id,
    question="15) |7 – 6x| = |8x – 7| tenglamani yeching.",
    options=["{2; 3}", "{0; 1}", "{0; 2}", "{2; 1}"],
    correct="{0; 1}"
)

add_question(
    test_id=test_id,
    question="16) Agar konus o‘q kesimining yuzi N ga, asosining yuzi M ga teng bo‘lsa, konus yon sirtining yuzini toping.",
    options=["√πMN", "2√MN", "√MN", "√(M² + N²π²)"],
    correct="√(M² + N²π²)"
)

add_question(
    test_id=test_id,
    question="17) 8x – 10x² + x³ + x² ko‘phad, nechta butun koeffitsientli ko‘paytuvchilarga ajraladi?",
    options=["3", "Ko‘paytuvchiga ajralmaydi", "2", "4"],
    correct="3"
)

add_question(
    test_id=test_id,
    question="18) 7^(√2) * (2^(x² – 6)) = 7^x / 2^(2x) tenglamaning katta ildizini toping.",
    options=["–3", "3", "–4", "1"],
    correct="1"
)

add_question(
    test_id=test_id,
    question="19) ABC to‘g‘ri burchakli uchburchakda C to‘g‘ri burchak, BC = 15, AC = 8. Uning B burchagi sinusi va tangensi nisbatini toping.",
    options=["17/15", "15/17", "8/15", "8/17"],
    correct="15/17"
)

add_question(
    test_id=test_id,
    question="20) Agar x, y, z ∈ [–π/2; π/2] va √(2 – tgx – ctgx + √(sin y – 1 + √(cos 2z – 1))) = 0 bo‘lsa, (2x + 5z) / 3y ning qiymatini toping.",
    options=["3", "1/6", "1", "–1/6"],
    correct="1"
)
add_question(
    test_id=test_id,
    question="21) x² + 4ˡᵒᵍ₂ˣ < 8 tengsizlikni yeching.",
    options=["[–2; 2]", "(0; 2]", "(0; 2)", "(–2; 2)"],
    correct="(0; 2)"
)

add_question(
    test_id=test_id,
    question="22) Balandligi 4 sm, asosi 16 sm bo‘lgan teng yonli uchburchakka tashqi chizilgan aylana radiusini toping.",
    options=["11", "9", "10", "8"],
    correct="10"
)

add_question(
    test_id=test_id,
    question="23) √(2x + 6) + √(x – 1) = 6 tenglamaning haqiqiy ildizlari yig‘indisini toping.",
    options=["2", "1", "4", "5"],
    correct="5"
)

add_question(
    test_id=test_id,
    question="24) 2 va 162 sonlari orasiga shunday 3 ta son qo‘shildiki, ular birgalikda ishorasi almashinuvi geometrik progressiyani tashkil qildi. Oraga qo‘shilgan sonlar yig‘indisini toping.",
    options=["0", "78", "42", "–42"],
    correct="42"
)

add_question(
    test_id=test_id,
    question="25) log₂(1 + log₂(1/2) + log₂(1/8)) ni hisoblang.",
    options=["–5", "–3", "–4", "–6"],
    correct="–4"
)

add_question(
    test_id=test_id,
    question="26) y = √(sin x) bo‘lsa, y'·6√(sin x)/cos x ko‘paytmani hisoblang.",
    options=["1", "2", "–2", "3"],
    correct="3"
)

add_question(
    test_id=test_id,
    question="27) ctg2α – ctgα ni hisoblang.",
    options=["1/sin 2α", "1/sin 2α", "1/cos 2α", "1/cos 2α"],
    correct="1/sin 2α"
)

add_question(
    test_id=test_id,
    question="28) ∫[0→π/12] sin x · cos x · cos 2x dx ni hisoblang.",
    options=["1/4", "1", "1/2", "–1/2"],
    correct="1/4"
)

add_question(
    test_id=test_id,
    question="29) Rasmda berilganlarga ko‘ra x ning o‘zgarish oralig‘ini toping.",
    options=["2 < x < 10", "5 < x < 10", "4 < x < 9", "5 < x < 11"],
    correct="5 < x < 10" ,
    image_path ="image/q29.png"

)

add_question(
    test_id=test_id,
    question="30) ax = by = cz = 6 va x + y + z = 36 ekani ma’lum bo‘lsa, 1/a + 1/b + 1/c = ?",
    options=["9", "5", "6", "12"],
    correct="6"
)



# ⬇️ Shu tartibda 11–30 savollar ham mavjud, xohlasangiz barchasini fayl holida eksport qilaman

print(f"✅ Test va savollar qo‘shildi. Test ID: {test_id}")
