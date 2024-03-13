# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.16.3)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(mrf-populate NONE)

include(ExternalProject)
ExternalProject_Add(mrf-populate
                     "GIT_REPOSITORY" "https://gitlab.inria.fr/sibr/libs/mrf.git" "GIT_TAG" "30c3c9494a00b6346d72a9e37761824c6f2b7207"
                    SOURCE_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/mrf"
                    BINARY_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/mrf/build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
