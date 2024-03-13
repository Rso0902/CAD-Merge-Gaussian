# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.16.3)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(xatlas-populate NONE)

include(ExternalProject)
ExternalProject_Add(xatlas-populate
                     "GIT_REPOSITORY" "https://gitlab.inria.fr/sibr/libs/xatlas.git" "GIT_TAG" "0fbe06a5368da13fcdc3ee48d4bdb2919ed2a249"
                    SOURCE_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/xatlas/xatlas"
                    BINARY_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/xatlas/build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
