project('pendulum C extensions', 'c')

py_mod = import('python')
py = py_mod.find_installation()
py_dep = py.dependency()

extensions = [
  ['_helpers', 'pendulum/_extensions/_helpers.c', meson.source_root() / 'pendulum/_extensions/'],
  ['_iso8601', 'pendulum/parsing/_iso8601.c', meson.source_root() / 'pendulum/parsing/'],
]

foreach extension : extensions
  py.extension_module(
    extension[0],
    extension[1],
    dependencies : py_dep,
    install : true,
    install_dir: extension[2]
  )
endforeach
