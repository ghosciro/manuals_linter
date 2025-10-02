cmake_minimum_required(VERSION 3.10)
project(manuals_linter  CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5Core REQUIRED)
find_package(PkgConfig REQUIRED)

pkg_check_modules(POPPLER_QT5 REQUIRED poppler-qt5)

# Usa pkg-config per trovare poppler-cpp
find_package(PkgConfig REQUIRED)
pkg_check_modules(POPPLER REQUIRED poppler-cpp)

add_executable(manuals_linter main.cpp)

set(MY_INCLUDES
    ${POPPLER_QT5_INCLUDE_DIRS}
    ${Qt5Core_INCLUDE_DIRS}
    ${POPPLER_INCLUDE_DIRS}
)

set(MY_LIBS
    ${POPPLER_QT5_LIBRARIES}
    Qt5::Core
    ${POPPLER_LIBRARIES}
)

# Applica include e link
target_include_directories(manuals_linter PRIVATE ${MY_INCLUDES})
target_link_libraries(manuals_linter PRIVATE ${MY_LIBS})