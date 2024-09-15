py --version

Write-Output "Creating and activating Virtual Environment"
py -m venv .venv
.venv/Scripts/activate.ps1

Write-Output "Replace '==' with '>=' in requirements.txt"
$content = Get-Content -Path '.\requirements.txt'
$newContent = $content -replace '==', '>='
$newContent | Set-Content -Path '.\requirements.txt'

Write-Output "Installing and Upgrade required Python Packages"
py -m pip install --upgrade pip
pip install -r requirements.txt --upgrade

Write-Output "Freeze requirements.txt"
pip freeze > requirements.txt

deactivate