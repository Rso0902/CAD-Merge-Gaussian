
if(NOT "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitinfo.txt" IS_NEWER_THAN "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E remove_directory "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout "https://gitlab.inria.fr/sibr/libs/mrf.git" "mrf"
    WORKING_DIRECTORY "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://gitlab.inria.fr/sibr/libs/mrf.git'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout 30c3c9494a00b6346d72a9e37761824c6f2b7207 --
  WORKING_DIRECTORY "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: '30c3c9494a00b6346d72a9e37761824c6f2b7207'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitinfo.txt"
    "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/subbuild/mrf-populate-prefix/src/mrf-populate-stamp/mrf-populate-gitclone-lastrun.txt'")
endif()

