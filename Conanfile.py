from conan import ConanFile
from conan.tools.cmake import CMake

class VSMRConan(ConanFile):
    name = "vSMR"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("asio/1.24.0")
        self.requires("libcurl/8.15.0")
        self.requires("rapidjson/cci.20220822")

    def build_requirements(self):
        self.build_requires("cmake/3.25.0")

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def build(self):
        cmake = CMake(self)
        libcurl_include_paths = self.dependencies["libcurl"].cpp_info.includedirs
        cmake.configure(variables={
            "CMAKE_BUILD_TYPE": "Release",
            "CMAKE_INCLUDE_PATH": libcurl_include_paths
        })
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="vSMR")
        self.copy("*.hpp", dst="include", src="vSMR")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["vSMR"]