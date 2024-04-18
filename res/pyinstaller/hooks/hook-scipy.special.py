from PyInstaller.utils.hooks import check_requirement

if check_requirement("scipy >= 1.13.0"):
    hiddenimports = ['scipy.special._cdflib']
