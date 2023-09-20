from PyInstaller.utils.hooks import collect_data_files, copy_metadata

datas = collect_data_files("pmr2.wfctrl")
datas.extend(copy_metadata("pmr2.wfctrl"))
