set(PROJECT_NAME vSMR)

################################################################################
# Source groups
################################################################################
set(no_group_source_files
    "ReadMe.txt"
)
source_group("" FILES ${no_group_source_files})

set(Header_Files
    "AircraftTypeLookup.hpp"
    "CallsignLookup.hpp"
    "ColorManager.h"
    "Config.hpp"
    "Constant.hpp"
    "CPDLCSettingsDialog.hpp"
    "DataLinkDialog.hpp"
    "HttpHelper.hpp"
    "InsetWindow.h"
    "Logger.h"
    "rapidjson/document.h"
    "rapidjson/filestream.h"
    "rapidjson/prettywriter.h"
    "rapidjson/rapidjson.h"
    "rapidjson/reader.h"
    "rapidjson/stringbuffer.h"
    "rapidjson/writer.h"
    "resource.h"
    "Rimcas.hpp"
    "SMRPlugin.hpp"
    "SMRRadar.hpp"
    "stdafx.h"
    "targetver.h"
    "vSMR.hpp"
)
source_group("Header Files" FILES ${Header_Files})

set(Resource_Files
    "../ml_blau_link.cur"
    "../move.cur"
    "arrow.cur"
    "cursor1.cur"
    "POINTER1.cur"
    "res/vSMR.rc2"
)
source_group("Resource Files" FILES ${Resource_Files})

set(Source_Files
    "AircraftTypeLookup.cpp"
    "CallsignLookup.cpp"
    "Config.cpp"
    "CPDLCSettingsDialog.cpp"
    "DataLinkDialog.cpp"
    "HttpHelper.cpp"
    "InsetWindow.cpp"
    "Rimcas.cpp"
    "SMRPlugin.cpp"
    "SMRRadar.cpp"
    "stdafx.cpp"
    "vSMR.cpp"
    "vSMR.def"
)
source_group("Source Files" FILES ${Source_Files})

set(ALL_FILES
    ${no_group_source_files}
    ${Header_Files}
    ${Resource_Files}
    ${Source_Files}
)

################################################################################
# Target
################################################################################
add_library(${PROJECT_NAME} SHARED ${ALL_FILES})

target_precompile_headers(${PROJECT_NAME} PRIVATE
    "$<$<COMPILE_LANGUAGE:CXX>:${CMAKE_CURRENT_SOURCE_DIR}/stdafx.h>"
)

use_props(${PROJECT_NAME} "${CMAKE_CONFIGURATION_TYPES}" "${DEFAULT_CXX_PROPS}")
set(ROOT_NAMESPACE vSMR)

set_target_properties(${PROJECT_NAME} PROPERTIES
    VS_GLOBAL_KEYWORD "MFCDLLProj"
)
set_target_properties(${PROJECT_NAME} PROPERTIES
    INTERPROCEDURAL_OPTIMIZATION         "TRUE"
)
################################################################################
# MSVC runtime library
################################################################################
get_property(MSVC_RUNTIME_LIBRARY_DEFAULT TARGET ${PROJECT_NAME} PROPERTY MSVC_RUNTIME_LIBRARY)
string(CONCAT "MSVC_RUNTIME_LIBRARY_STR"
    $<$<CONFIG:Debug>:
        MultiThreadedDebug
    >
    $<$<CONFIG:Release>:
        MultiThreaded
    >
    $<$<NOT:$<OR:$<CONFIG:Debug>,$<CONFIG:Release>>>:${MSVC_RUNTIME_LIBRARY_DEFAULT}>
)
set_target_properties(${PROJECT_NAME} PROPERTIES MSVC_RUNTIME_LIBRARY ${MSVC_RUNTIME_LIBRARY_STR})

################################################################################
# Include directories
################################################################################
target_include_directories(${PROJECT_NAME} PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/../lib/include"
)

################################################################################
# Compile definitions
################################################################################
target_compile_definitions(${PROJECT_NAME} PRIVATE
    "$<$<CONFIG:Debug>:"
        "_DEBUG"
    ">"
    "$<$<CONFIG:Release>:"
        "NDEBUG"
    ">"
    "WIN32;"
    "_WINDOWS;"
    "_USRDLL;"
    "CURL_STATICLIB;"
    "CURL_STATIC;"
    "ASIO_STANDALONE;"
    "_MBCS"
)

################################################################################
# Compile and link options
################################################################################
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE
        $<$<CONFIG:Debug>:
            /Gm-;
            /Od;
            /Zi
        >
        $<$<CONFIG:Release>:
            /O2;
            ${DEFAULT_CXX_DEBUG_INFORMATION_FORMAT}
        >
        /std:c++17;
        /Oi;
        /sdl;
        /Gy;
        /W3;
        ${DEFAULT_CXX_EXCEPTION_HANDLING};
        /Zc:wchar_t-
    )
    target_link_options(${PROJECT_NAME} PRIVATE
        $<$<CONFIG:Release>:
            /OPT:REF;
            /OPT:ICF;
            /NODEFAULTLIB:LIBCMTD
        >
        /DEBUG;
        /SUBSYSTEM:WINDOWS;
        /INCREMENTAL:NO;
        /IGNORE:4099
    )
endif()

################################################################################
# Dependencies
################################################################################
set(ADDITIONAL_LIBRARY_DEPENDENCIES
    "$<$<CONFIG:Release>:"
        "winmm"
    ">"
    "..\lib\EuroScopePlugInDll"
)
target_link_libraries(${PROJECT_NAME} PUBLIC "${ADDITIONAL_LIBRARY_DEPENDENCIES}")

target_link_directories(${PROJECT_NAME} PUBLIC
    "$<$<CONFIG:Debug>:"
        "${CMAKE_SOURCE_DIR}/lib/include/asio;"
        "${CMAKE_SOURCE_DIR}/lib/include/curl;"
        "${CMAKE_SOURCE_DIR}/lib/include/rapidjson;"
        "${CMAKE_SOURCE_DIR}/lib/include/boost_1_85_0/boost"
    ">"
)

