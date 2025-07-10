@echo off
echo 🔄 Python loyihangizdan .env faylni tarixdan tozalash...

:: 1. Git filter-repo o'rnatilganmi?
pip show git-filter-repo >nul 2>&1
if %errorlevel% neq 0 (
    echo ❗ git-filter-repo o'rnatilmagan. Iltimos, quyidagini bajarib o'rnating:
    echo pip install git-filter-repo
    pause
    exit /b
)
:: 2. Loyihaga o'tish
cd /d %~d
p0

:: 3. Git tarixdan .env faylni olib tashlash
git filter-repo --path .env --invert-paths

:: 4. .gitignore faylga .env ni qo'shish
echo .env>>.gitignore

:: 5. Commit qilish
git add .gitignore
git commit -m "Removed .env from history and added to .gitignore"

:: 6. GitHub'ga kuch bilan push qilish
git push -f origin main

echo ✅ Tayyor! .env GitHub tarixidan tozalandi.
pause
