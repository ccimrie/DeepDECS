set (SOURCE_FILES
	main.cpp
	robot.cpp
)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

add_executable(robot_floor_validate_01 ${SOURCE_FILES})
target_include_directories(robot_floor_validate_01 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(robot_floor_validate_01 PUBLIC box2d ${PYTHON_LIBRARIES})
set_target_properties(robot_floor_validate_01 PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)