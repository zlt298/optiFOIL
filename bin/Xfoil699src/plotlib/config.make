
#=======================================#
# Makefile options for Xplot11 library  #
#   Set up or select a set of compile   #
#   options for your system             # 
#=======================================#


# Set library name 
PLTLIB = libPltDP.a

# Some fortrans need trailing underscores in C interface symbols (see Xwin.c)
# This should work for most of the "unix" fortran compilers
DEFINE = -DUNDERSCORE

FC = ifort
CC  = gcc
DP = -r8

FFLAGS  = -O3 $(DP)
CFLAGS  = -O3 $(DEFINE) -I/opt/local/include
AR = ar r
RANLIB = ranlib 
LINKLIB = -L/usr/X11/lib -lX11

