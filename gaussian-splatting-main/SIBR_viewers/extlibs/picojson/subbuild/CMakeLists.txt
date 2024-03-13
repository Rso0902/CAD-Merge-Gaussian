# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.16.3)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(picojson-populate NONE)

include(ExternalProject)
ExternalProject_Add(picojson-populate
                     "GIT_REPOSITORY" "https://gitlab.inria.fr/sibr/libs/picojson.git" "GIT_TAG" "7cf8feee93c8383dddbcb6b64cf40b04e007c49f"
                    SOURCE_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/picojson/picojson"
                    BINARY_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/picojson/build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
