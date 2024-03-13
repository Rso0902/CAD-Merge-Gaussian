# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.16.3)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(cudarasterizer-populate NONE)

include(ExternalProject)
ExternalProject_Add(cudarasterizer-populate
                     "GIT_REPOSITORY" "https://github.com/graphdeco-inria/diff-gaussian-rasterization.git" "GIT_TAG" "3509be80f83ee30599b23bb3542d45aea2174a03"
                    SOURCE_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/CudaRasterizer/CudaRasterizer"
                    BINARY_DIR          "/home/rso/codes/gaussian-splatting-main/SIBR_viewers/extlibs/CudaRasterizer/build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
