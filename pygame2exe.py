##############################################################################
# 2exe.py
##############################################################################
# Script for invoking py2exe to turn a game into an exe
##############################################################################

##############################################################################
# IMPORTS
##############################################################################
from distutils.core import setup
import py2exe
import sys
import os
import glob
import shutil
import pygame
from modulefinder import Module

##############################################################################
# GLOBAL DATA
##############################################################################

VERSION = '0.1'
AUTHOR_NAME = 'Haxsie'
AUTHOR_EMAIL = 'createblankdevelop@gmail.com'
AUTHOR_URL = "htttp://kuuri.net"
PRODUCT_NAME = "KOBATO"
SCRIPT_MAIN = 'main.py'
VERSIONSTRING = PRODUCT_NAME + " BETA " + VERSION

PYGAMEDIR = os.path.split(pygame.base.__file__)[0]

ICONFILE = "data/icon.ico"

#all .dlls from the pygame directory will be copied to the dist dir
SDL_DLLS = glob.glob(os.path.join(PYGAMEDIR,'*.dll'))

#if true, the build directory will be deleted at the end of the build
REMOVE_BUILD_ON_EXIT = True

#Extra files to be included in the dist directory  
                  #directory #files 
extra_files = data_files = [
	('data', [
		"data/char.data", 
		"data/se_clash.wav", 
		"data/se_gem.wav", 
		"data/se_move.wav", 
		"data/se_incubation.wav", 
		"data/se_level_up.wav", 
		"data/kobato.ogg"
		]
	),
	('', ["Readme_ja.md", "Readme_en.md"])
	]
	
#list of modules to be excluded from the .exe
MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'base64',
'compiler',
'pydoc']


INCLUDE_STUFF = ['encodings',"encodings.latin_1",]

##############################################################################
# OVERRIDE OF BUILDEXE
##############################################################################

#override is used to ensure the default font is included
class BuildExe(py2exe.build_exe.py2exe):
	def copy_extensions(self,extensions):
		defaultFont = os.path.join(PYGAMEDIR,pygame.font.get_default_font())

		extensions.append(Module("pygame.font",defaultFont))
		py2exe.build_exe.py2exe.copy_extensions(self,extensions)

##############################################################################
# EXECUTION
##############################################################################

#append 'py2exe' to the arguments to invoke py2exe
sys.argv.append("py2exe")

#if the dist directory already exists, delete it
if os.path.exists('dist/'): shutil.rmtree('dist/')

#call setup with the correct parameters
setup(
	cmdclass = {'py2exe':BuildExe},
	windows=[
		{'script': SCRIPT_MAIN,
			'other_resources': [(u"VERSIONTAG",1,VERSIONSTRING)],
			'icon_resources': [(1,ICONFILE)]
			}],
	options = {"py2exe": {
		"optimize": 2,
		"includes": INCLUDE_STUFF,
		"compressed": 1,
		# "ascii": 1,
		"bundle_files": 2,
		"ignores": ['tcl','AppKit','Numeric','Foundation'],
		"excludes": MODULE_EXCLUDES} },
	name = PRODUCT_NAME,
	version = VERSION,
	data_files = extra_files,
	zipfile = None,
	author = AUTHOR_NAME,
	author_email = AUTHOR_EMAIL,
	url = AUTHOR_URL)


#clean up
if os.path.exists('dist/tcl'): shutil.rmtree('dist/tcl')

# Remove the build tree
if REMOVE_BUILD_ON_EXIT:
	shutil.rmtree('build/')

if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')

for f in SDL_DLLS:
	fname = os.path.basename(f)
	try:
		shutil.copyfile(f,os.path.join('dist',fname))
	except: pass