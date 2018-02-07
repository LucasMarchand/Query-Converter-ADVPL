import sys
import os
import os.path
from cx_Freeze import setup, Executable

# executable options
script = 'App.py'
if sys.platform == "win32" :
  base = "Win32GUI"      

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

icon = 'icon_01.ico'                  # nome (ou diretório) do icone do executável
targetName = 'cQuery.exe'             # nome do .exe que será gerado

# build options
packages = ['os', 'tkinter']          # lista de bibliotecas a serem incluídas
includes = []                         # lista de módulos a serem incluídos
include_files = [
  os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
  os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
  'icone-anexo.png'
]          # lista de outros arquivos a serem incluídos (imagens, dados...)

# shortcut options
shortcut_name = 'cQuery'                 # nome do atalho que será criado no processo de instalação

# bdist_msi options
company_name = 'Query Converter'
product_name = 'Query Converter'
upgrade_code = '{66620F3A-DC3A-11E2-B341-002234E9B01E}'
add_to_path = False

# setup options
name = 'cQuery'                                   # Nome do programa na descrição
version = '1.2'                                   # versão do programa na descrição
description = 'Programa que adapta a query de SQL para ADVPL'     # descrição do programa

build_exe_options = {
    "include_files": [
        ('resources', 'resources'),
        ('config.ini', 'config.ini')
    ]
}

msi_data = {'Shortcut': 
  [
    ( "DesktopShortcut",         # Shortcut
      "DesktopFolder",           # Directory_
      shortcut_name,             # Name
      "TARGETDIR",               # Component_
      "[TARGETDIR]/{}".format(targetName),  # Target
      None,                      # Arguments
      None,                      # Description
      None,                      # Hotkey
      None,                      # Icon
      None,                      # IconIndex
      None,                      # ShowCmd
      "TARGETDIR",               # WkDir
    ),

    ( "ProgramMenuShortcut",     # Shortcut
      "ProgramMenuFolder",       # Directory_
      shortcut_name,             # Name
      "TARGETDIR",               # Component_
      "[TARGETDIR]/{}".format(targetName),  # Target
      None,                      # Arguments
      None,                      # Description
      None,                      # Hotkey
      None,                      # Icon
      None,                      # IconIndex
      None,                      # ShowCmd
      "TARGETDIR",               # WkDir
    )
  ]
}

opt = {
    'build_exe': {'packages': packages,
                  'includes': includes,
                  'include_files': include_files,
                  'include_msvcr': True,
                  'replace_paths': [("*", "")]
                  },
    'bdist_msi': {'upgrade_code': upgrade_code,
                  'add_to_path': add_to_path,
                  'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
                  'data': msi_data
                  }
}

exe = Executable(
    script=script,
    base=base,
    icon=icon,
    targetName=targetName
)

setup(name=name,
      version=version,
      description=description,
      options=dict(opt),
      executables=[exe]
      )