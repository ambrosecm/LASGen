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
CMAKE_SOURCE_DIR = /home/ambrose/vsproject/TestLib/LuPng

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ambrose/vsproject/TestLib/LuPng

# Include any dependencies generated for this target.
include CMakeFiles/LuPng.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/LuPng.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/LuPng.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/LuPng.dir/flags.make

CMakeFiles/LuPng.dir/lupng.c.o: CMakeFiles/LuPng.dir/flags.make
CMakeFiles/LuPng.dir/lupng.c.o: lupng.c
CMakeFiles/LuPng.dir/lupng.c.o: CMakeFiles/LuPng.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ambrose/vsproject/TestLib/LuPng/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/LuPng.dir/lupng.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/LuPng.dir/lupng.c.o -MF CMakeFiles/LuPng.dir/lupng.c.o.d -o CMakeFiles/LuPng.dir/lupng.c.o -c /home/ambrose/vsproject/TestLib/LuPng/lupng.c

CMakeFiles/LuPng.dir/lupng.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/LuPng.dir/lupng.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/ambrose/vsproject/TestLib/LuPng/lupng.c > CMakeFiles/LuPng.dir/lupng.c.i

CMakeFiles/LuPng.dir/lupng.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/LuPng.dir/lupng.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/ambrose/vsproject/TestLib/LuPng/lupng.c -o CMakeFiles/LuPng.dir/lupng.c.s

# Object files for target LuPng
LuPng_OBJECTS = \
"CMakeFiles/LuPng.dir/lupng.c.o"

# External object files for target LuPng
LuPng_EXTERNAL_OBJECTS =

libLuPng.a: CMakeFiles/LuPng.dir/lupng.c.o
libLuPng.a: CMakeFiles/LuPng.dir/build.make
libLuPng.a: CMakeFiles/LuPng.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ambrose/vsproject/TestLib/LuPng/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library libLuPng.a"
	$(CMAKE_COMMAND) -P CMakeFiles/LuPng.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/LuPng.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/LuPng.dir/build: libLuPng.a
.PHONY : CMakeFiles/LuPng.dir/build

CMakeFiles/LuPng.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/LuPng.dir/cmake_clean.cmake
.PHONY : CMakeFiles/LuPng.dir/clean

CMakeFiles/LuPng.dir/depend:
	cd /home/ambrose/vsproject/TestLib/LuPng && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ambrose/vsproject/TestLib/LuPng /home/ambrose/vsproject/TestLib/LuPng /home/ambrose/vsproject/TestLib/LuPng /home/ambrose/vsproject/TestLib/LuPng /home/ambrose/vsproject/TestLib/LuPng/CMakeFiles/LuPng.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/LuPng.dir/depend

