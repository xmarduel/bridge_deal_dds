# --------------------- INFORMATION --------------------------------

# This the DDS Makefile for Windows and the mingw GNU g++
# compiler.  It assumes a Unix-like setup for some commands.

# The "windres" and "cvtres" tools are used for putting version
# information into the DLL in a way that Windows can see.
# It is not mandatory, and if you don't have those tools,
# You can remove $(VFILE).obj in the target line below.

# --------------------- CONFIGURATION ------------------------------

# You can configure the following:

# 1. The threading systems that you want in the DLL/executable.
# You will always get single-threading.  If you have multiple
# threading systems, the default will be the multi-threading one
# with the lowest number (see System.cpp).  All that matters is
# CC_THREADING.

# GCD doesn't work on Windows.
#THR_BOOST	= -DDDS_THREADS_BOOST
THR_BOOST	=
THR_GCD		= -DDDS_THREADS_GCD
THR_OPENMP	= -DDDS_THREADS_OPENMP
THR_WINAPI	= -DDDS_THREADS_WINAPI
THR_STL		= -DDDS_THREADS_STL

THREADING	= $(THR_BOOST) $(THR_OPENMP) $(THR_STL)

# If you need to add something for a threading system, this is
# the place.

#CC_BOOST_LINK	= -lboost_system -lboost_thread
#CC_BOOST_LINK	= -lboost_system-mt -lboost_thread-mt
CC_BOOST_LINK	= 

#THREAD_COMPILE	= -fopenmp
#THREAD_COMPILE	= -fopenmp
THREAD_LINK	= -lgomp $(CC_BOOST_LINK)

# 2. Debugging options.  (There are more granular options in debug.h.)

DEBUG_ALL	= -DDDS_DEBUG_ALL 
TIMING		= -DDDS_TIMING
SCHEDULER	= -DDDS_SCHEDULER

# All that matters from no. 2 and no. 3 is the following.  Here you
# can add $(SMALL_MEMORY) etc.

DDS_BEHAVIOR	=

# ----------------------- OFTEN OK    ------------------------------

# From here on you you don't have to change anything to CONFIGURE
# the compilation.  But you may well have to change something to 
# get it to compile.

INCL_SOURCE	= Makefiles/sources.txt
INCL_DEPENDS	= Makefiles/depends_obj.txt

# If your compiler name is not given here, change it.
CC		= g++

# We compile with aggressive warnings, but we have to turn off some
# of them as they appear in libraries in great numbers...

WARN_FLAGS	= 		\
	-Wshadow 		\
	-Wsign-conversion 	\
	-pedantic -Wall -Wextra  \
	-Wcast-align -Wcast-qual \
	-Wctor-dtor-privacy 	\
	-Wdisabled-optimization \
	-Wformat=2 		\
	-Winit-self 		\
	-Wlogical-op 		\
	-Wmissing-declarations 	\
	-Wmissing-include-dirs 	\
	-Wnoexcept 		\
	-Wold-style-cast 	\
	-Woverloaded-virtual 	\
	-Wsign-promo 		\
	-Wstrict-null-sentinel 	\
	-Wstrict-overflow=1 	\
	-Wswitch-default -Wundef \
	-Werror 		\
	-Wno-unused 		\
	-Wno-unknown-pragmas 	\
	-Wno-long-long

COMPILE_FLAGS	= -O3 -DBUILDING_EXAMPLE_DLL -fopenmp \
		$(WARN_FLAGS) \
		$(DDS_BEHAVIOR) $(THREAD_COMPILE) $(THREADING)

LINK1_FLAGS	= -shared
LINK2_FLAGS	= 		\
	$(THREAD_LINK)		\
	-Wl,--out-implib,libdds.a \
	-Wl,--no-undefined

DLLBASE		= dds
DLL 		= $(DLLBASE).dll
DLIB 		= $(DLLBASE).lib
EXPORTER	= Exports.def

VFILE		= ddsres
WINDRES_FLAG	= -F pe-x86-64

include $(INCL_SOURCE)

O_FILES 	= $(subst .cpp,.o,$(SOURCE_FILES)) $(VFILE).o

mingw:	$(O_FILES)
	$(CC) $(LINK1_FLAGS) $(O_FILES) \
	-o $(DLL) $(LINK2_FLAGS)

%.o:	%.cpp
	$(CC) $(COMPILE_FLAGS) -c $<

$(DLLBASE).res:	$(DLLBASE).rc
	windres $(DLLBASE).rc $(DLLBASE).res

$(VFILE).o:	$(DLLBASE).rc
	windres $(WINDRES_FLAG) $(DLLBASE).rc $(VFILE).o

depend:
	makedepend -Y -- $(SOURCE_FILES)

clean:
	rm -f $(O_FILES) $(DLL) $(DLLBASE).{lib,def,exp,res}

install:
	test -d ../test || mkdir ../test
	test -d ../examples || mkdir ../examples
	cp $(DLL) $(DLLBASE).def ../test
	cp $(DLL) $(DLLBASE).def ../examples

# If you don't have a Linux-like setup, use "del" instead of "rm"
# and "copy" instead of "cp".

include $(INCL_DEPENDS)

