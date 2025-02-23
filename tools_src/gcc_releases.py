#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# The OS tag is used to specify the Python wheel platform for which the toolchain is built.
# This info can be found in the GCC release notes.
# For Linux, the manylinux_x_y_arch tag uses the Glibc version x.y and the architecture arch.
# CentOS7 -> 2.17 -> manylinux_2_17_arch or manylinux2014_arch
# RHEL7 -> 2.17 -> manylinux_2_17_arch or manylinux2014_arch
# RHEL8 -> 2.28 -> manylinux_2_28_arch
# Ubuntu 16.04 -> 2.23 -> manylinux_2_23_arch
# Ubuntu 18.04 -> 2.27 -> manylinux_2_27_arch
# Ubuntu 20.04 -> 2.31 -> manylinux_2_31_arch
gcc_releases = {
    "14.2.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-eabi.zip",
            "md5": "7426b9eec8b576f0a524ede63013c547",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "d5fb1ae60e4d67eb2986837dbcd6a066",
            "wheel_plat": "macosx_12_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "40d1c9208aed7fab08b0f27e5383dcef",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "fcdcd7c8d5b22d2d0cc6bf3721686e69",
            "wheel_plat": "manylinux_2_28_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "342d6d9dc75e6d4c05a748f2cecc96a6",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "13.3.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "39d9882ca0eb475e81170ae826c1435d",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "4bb141e44b831635fde4e8139d470f1f",
            "wheel_plat": "macosx_12_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "f1c18320bb3121fa89dca11399273f4e",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "0601a9588bc5b9c99ad2b56133b7f118",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "303102d97b877ebbeb36b3158994b218",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "13.2.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "7fd677088038cdf82f33f149e2e943ee",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "41d49840b0fc676d2ae35aab21a58693",
            "wheel_plat": "macosx_11_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "2c43e9d72206c1f81227b0a685df5ea6",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "791754852f8c18ea04da7139f153a5b7",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "5a08122e6d4caf97c6ccd1d29e62599c",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "12.3.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "36c3f864ae8a4ded4a464e67c74f4973",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "13ae2cc016564507c91a4fcffb6e3c54",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "53d034e9423e7f470acc5ed2a066758e",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "00ebb1b70b1f88906c61206457eacb61",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "02c9b0d3bb1110575877d8eee1f223f2",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "12.2.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "0122a821c28b200f251cd23d2edc38c5",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "b98c6f58a4ccf64c38f92b456eb3b3d1",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "26329762f802bb53ac73385d85b11646",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "f3d1d32c8ac58f1e0f9dbe4bc56efa05",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "2014a0ebaae3168da555efdcabf03f2a",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "11.3.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-mingw-w64-i686-arm-none-eabi.zip",
            # Arm"s published MD5 seems incorrect: f1ff0b48304dbc4ff558f0753a3a8860
            # https://community.arm.com/support-forums/f/compilers-and-libraries-forum/53343/arm-gnu-toolchain-11-3-rel1-windows-arm-none-eabi-md5-is-incorrect
            "md5": "b287cf60045910dd56c56cdc2a490049",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "f4a3df0bff51bf872db679c406a9154d",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "8cb33f7ec29682f2f9cdc0b4e687f9a6",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "f020e29a861c5dbf199dce93643d68cc",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "11.2-2022.02": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "e2bb05445200ed8e8c9140fad6a0afb5",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "c51d8257b67d7555047f172698730685",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi.tar.xz",
            "md5": "a48e6f8756be70b071535048a678c481",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-aarch64-arm-none-eabi.tar.xz",
            "md5": "746f20d2eb8acad4e7085e1395665219",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "10.3-2021.10": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-win32.zip",
            "md5": "2bc8f0c4c4659f8259c8176223eeafc1",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-mac.tar.bz2",
            "md5": "7f2a7b7b23797302a9d6182c6e482449",
            "wheel_plat": "macosx_10_14_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2",
            "md5": "2383e4eb4ea23f248d33adc70dc3227e",
            "wheel_plat": "manylinux_2_23_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-aarch64-linux.tar.bz2",
            "md5": "3fe3d8bb693bd0a6e4615b6569443d0d",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    # 10.3-2021.07 & 10.3-2021.10 are both GCC 10.3 releases, as this package versioning only uses the GCC major and minor numbers we ignore this earlier release.
    # "10.3-2021.07": {
    #    "win32": {
    #        "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.07/gcc-arm-none-eabi-10.3-2021.07-win32.zip",
    #        "md5": "fca12668002f8c52cfa174400fd2d03e",
    #        "wheel_plat": "win_amd64",
    #    },
    #    "mac_x86_64": {
    #        "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.07/gcc-arm-none-eabi-10.3-2021.07-mac-10.14.6.tar.bz2",
    #        "md5": "42d5f143cdc303d73a3602fa5052c790",
    #        "wheel_plat": "macosx_10_14_x86_64",
    #    },
    #    "linux_x86_64": {
    #        "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.07/gcc-arm-none-eabi-10.3-2021.07-x86_64-linux.tar.bz2",
    #        "md5": "b56ae639d9183c340f065ae114a30202",
    #        "wheel_plat": "manylinux2014_x86_64",
    #    },
    #    "linux_aarch64": {
    #        "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.07/gcc-arm-none-eabi-10.3-2021.07-aarch64-linux.tar.bz2",
    #        "md5": "c20b0535d01f8d4418341d893c62a782",
    #        "wheel_plat": "manylinux_2_27_aarch64",
    #    },
    # },
    "10-2020-q4": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-win32.zip",
            "md5": "5ee6542a2af847934177bc8fa1294c0d",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-mac.tar.bz2",
            "md5": "e588d21be5a0cc9caa60938d2422b058",
            "wheel_plat": "macosx_10_14_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2",
            "md5": "8312c4c91799885f222f663fc81f9a31",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-aarch64-linux.tar.bz2",
            "md5": "1c3b8944c026d50362eef1f01f329a8e",
            "wheel_plat": "manylinux2014_aarch64",
        },
    },
    "9-2020-q2": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-win32.zip",
            "md5": "184b3397414485f224e7ba950989aab6",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-mac.tar.bz2",
            "md5": "75a171beac35453fd2f0f48b3cb239c3",
            "wheel_plat": "macosx_10_14_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2",
            "md5": "2b9eeccc33470f9d3cda26983b9d2dc6",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2020q2/gcc-arm-none-eabi-9-2020-q2-update-aarch64-linux.tar.bz2",
            "md5": "000b0888cbe7b171e2225b29be1c327c",
            "wheel_plat": "manylinux2014_aarch64",
        },
    },
    "9-2019-q4": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-win32.zip",
            "md5": "82525522fefbde0b7811263ee8172b10",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-mac.tar.bz2",
            "md5": "241b64f0578db2cf146034fc5bcee3d4",
            "wheel_plat": "macosx_10_13_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2",
            "md5": "fe0029de4f4ec43cf7008944e34ff8cc",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-aarch64-linux.tar.bz2",
            "md5": "0dfa059aae18fcf7d842e30c525076a4",
            "wheel_plat": "manylinux2014_aarch64",
        },
    },
}

gcc_short_versions = {
    "14.2.Rel1": "14.2",
    "13.3.Rel1": "13.3",
    "13.2.Rel1": "13.2",
    "12.3.Rel1": "12.3",
    "12.2.Rel1": "12.2",
    "11.3.Rel1": "11.3",
    "11.2-2022.02": "11.2",
    "10.3-2021.10": "10.3",
    "10-2020-q4": "10.2",
    "9-2020-q2": "9.3",
    "9-2019-q4": "9.2",
}
