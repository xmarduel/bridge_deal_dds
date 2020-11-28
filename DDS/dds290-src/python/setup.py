from distutils.core import setup, Extension

module1 = Extension('dds',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/usr/local/include'],
                    libraries = ['dds', 'boost_thread-mt'],
                    library_dirs = ['.'],
                    sources = ['wrapper.cpp', 'hands.cpp'])

setup (name = 'dds',
       version = '1.0',
       description = 'This is a demo package',
       author = '',
       author_email = 'xavier.marduel@web.de',
       ext_modules = [module1])
