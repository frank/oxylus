# -*- mode: python -*-
import os

block_cipher = None

added_files = [
     ('view','view'),
     ('model','model'),
     ('controller','controller')
     ]

a = Analysis(['oxylus.py'],
             pathex=['C:\\Users\\feget\\Documents\\GitHub\\oxylus\\source'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('log32.ico',os.path.join("log32.ico"),'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='oxylus',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon=os.path.join("log32.ico"))
