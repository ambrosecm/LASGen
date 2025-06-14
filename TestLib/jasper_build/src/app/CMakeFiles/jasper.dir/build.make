# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ambrose/vsproject/TestLib/jasper

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ambrose/vsproject/TestLib/jasper_build

# Include any dependencies generated for this target.
include src/app/CMakeFiles/jasper.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include src/app/CMakeFiles/jasper.dir/compiler_depend.make

# Include the progress variables for this target.
include src/app/CMakeFiles/jasper.dir/progress.make

# Include the compile flags for this target's objects.
include src/app/CMakeFiles/jasper.dir/flags.make

src/app/CMakeFiles/jasper.dir/jasper.c.o: src/app/CMakeFiles/jasper.dir/flags.make
src/app/CMakeFiles/jasper.dir/jasper.c.o: /home/ambrose/vsproject/TestLib/jasper/src/app/jasper.c
src/app/CMakeFiles/jasper.dir/jasper.c.o: src/app/CMakeFiles/jasper.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ambrose/vsproject/TestLib/jasper_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object src/app/CMakeFiles/jasper.dir/jasper.c.o"
	cd /home/ambrose/vsproject/TestLib/jasper_build/src/app && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT src/app/CMakeFiles/jasper.dir/jasper.c.o -MF CMakeFiles/jasper.dir/jasper.c.o.d -o CMakeFiles/jasper.dir/jasper.c.o -c /home/ambrose/vsproject/TestLib/jasper/src/app/jasper.c

src/app/CMakeFiles/jasper.dir/jasper.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/jasper.dir/jasper.c.i"
	cd /home/ambrose/vsproject/TestLib/jasper_build/src/app && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/ambrose/vsproject/TestLib/jasper/src/app/jasper.c > CMakeFiles/jasper.dir/jasper.c.i

src/app/CMakeFiles/jasper.dir/jasper.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/jasper.dir/jasper.c.s"
	cd /home/ambrose/vsproject/TestLib/jasper_build/src/app && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/ambrose/vsproject/TestLib/jasper/src/app/jasper.c -o CMakeFiles/jasper.dir/jasper.c.s

# Object files for target jasper
jasper_OBJECTS = \
"CMakeFiles/jasper.dir/jasper.c.o"

# External object files for target jasper
jasper_EXTERNAL_OBJECTS =

src/app/jasper: src/app/CMakeFiles/jasper.dir/jasper.c.o
src/app/jasper: src/app/CMakeFiles/jasper.dir/build.make
src/app/jasper: src/libjasper/libjasper.so.7.0.0
src/app/jasper: /usr/lib/x86_64-linux-gnu/libjpeg.so
src/app/jasper: /usr/lib/x86_64-linux-gnu/libm.so
src/app/jasper: /usr/lib/x86_64-linux-gnu/libpthread.a
src/app/jasper: src/app/CMakeFiles/jasper.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ambrose/vsproject/TestLib/jasper_build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable jasper"
	cd /home/ambrose/vsproject/TestLib/jasper_build/src/app && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/jasper.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/app/CMakeFiles/jasper.dir/build: src/app/jasper
.PHONY : src/app/CMakeFiles/jasper.dir/build

src/app/CMakeFiles/jasper.dir/clean:
	cd /home/ambrose/vsproject/TestLib/jasper_build/src/app && $(CMAKE_COMMAND) -P CMakeFiles/jasper.dir/cmake_clean.cmake
.PHONY : src/app/CMakeFiles/jasper.dir/clean

src/app/CMakeFiles/jasper.dir/depend:
	cd /home/ambrose/vsproject/TestLib/jasper_build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ambrose/vsproject/TestLib/jasper /home/ambrose/vsproject/TestLib/jasper/src/app /home/ambrose/vsproject/TestLib/jasper_build /home/ambrose/vsproject/TestLib/jasper_build/src/app /home/ambrose/vsproject/TestLib/jasper_build/src/app/CMakeFiles/jasper.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/app/CMakeFiles/jasper.dir/depend

