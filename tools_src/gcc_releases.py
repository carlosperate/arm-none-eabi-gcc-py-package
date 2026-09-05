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
            "sha256": "f074615953f76036e9a51b87f6577fdb4ed8e77d3322a6f68214e92e7859888f",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "d5fb1ae60e4d67eb2986837dbcd6a066",
            "sha256": "2d9e717dd4f7751d18936ae1365d25916534105ebcb7583039eff1092b824505",
            "wheel_plat": "macosx_12_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "40d1c9208aed7fab08b0f27e5383dcef",
            "sha256": "c7c78ffab9bebfce91d99d3c24da6bf4b81c01e16cf551eb2ff9f25b9e0a3818",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "fcdcd7c8d5b22d2d0cc6bf3721686e69",
            "sha256": "62a63b981fe391a9cbad7ef51b17e49aeaa3e7b0d029b36ca1e9c3b2a9b78823",
            "wheel_plat": "manylinux_2_28_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "342d6d9dc75e6d4c05a748f2cecc96a6",
            "sha256": "87330bab085dd8749d4ed0ad633674b9dc48b237b61069e3b481abd364d0a684",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "13.3.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "39d9882ca0eb475e81170ae826c1435d",
            "sha256": "e46fda043c0ce83582bc8db4b3ef85f77f4beb7333344c2f4193c17e1167a095",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "4bb141e44b831635fde4e8139d470f1f",
            "sha256": "1ab00742d1ed0926e6f227df39d767f8efab46f5250505c29cb81f548222d794",
            "wheel_plat": "macosx_12_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "f1c18320bb3121fa89dca11399273f4e",
            "sha256": "fb6921db95d345dc7e5e487dd43b745e3a5b4d5c0c7ca4f707347148760317b4",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "0601a9588bc5b9c99ad2b56133b7f118",
            "sha256": "95c011cee430e64dd6087c75c800f04b9c49832cc1000127a92a97f9c8d83af4",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "303102d97b877ebbeb36b3158994b218",
            "sha256": "c8824bffd057afce2259f7618254e840715f33523a3d4e4294f471208f976764",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "13.2.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "7fd677088038cdf82f33f149e2e943ee",
            "sha256": "51d933f00578aa28016c5e3c84f94403274ea7915539f8e56c13e2196437d18f",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "41d49840b0fc676d2ae35aab21a58693",
            "sha256": "075faa4f3e8eb45e59144858202351a28706f54a6ec17eedd88c9fb9412372cc",
            "wheel_plat": "macosx_11_0_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "2c43e9d72206c1f81227b0a685df5ea6",
            "sha256": "39c44f8af42695b7b871df42e346c09fee670ea8dfc11f17083e296ea2b0d279",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "791754852f8c18ea04da7139f153a5b7",
            "sha256": "6cd1bbc1d9ae57312bcd169ae283153a9572bd6a8e4eeae2fedfbc33b115fdbb",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "5a08122e6d4caf97c6ccd1d29e62599c",
            "sha256": "8fd8b4a0a8d44ab2e195ccfbeef42223dfb3ede29d80f14dcf2183c34b8d199a",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "12.3.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "36c3f864ae8a4ded4a464e67c74f4973",
            "sha256": "d52888bf59c5262ebf3e6b19b9f9e6270ecb60fd218cf81a4e793946e805a654",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "13ae2cc016564507c91a4fcffb6e3c54",
            "sha256": "e6ed8bf930fad9ce33e120ab90b36957b1f779fccaa6de6c9ca9a58982c04291",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "53d034e9423e7f470acc5ed2a066758e",
            "sha256": "3b2eee0bdf71c1bbeb3c3b7424fbf7bd9d5c3f0f5a3a4a78159c9e3ad219e7bd",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "00ebb1b70b1f88906c61206457eacb61",
            "sha256": "12a2815644318ebcceaf84beabb665d0924b6e79e21048452c5331a56332b309",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "02c9b0d3bb1110575877d8eee1f223f2",
            "sha256": "14c0487d5753f6071d24e568881f7c7e67f80dd83165dec5164b3731394af431",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "12.2.Rel1": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "0122a821c28b200f251cd23d2edc38c5",
            "sha256": "ad1427496cde9bbe7604bc448ec6e115c6538e04af1c8275795ebb1c2b7b2830",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "b98c6f58a4ccf64c38f92b456eb3b3d1",
            "sha256": "00c0eeb57ae92332f216151ac66df6ba17d2d3b306dac86f4006006f437b2902",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "mac_arm64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-darwin-arm64-arm-none-eabi.tar.xz",
            "md5": "26329762f802bb53ac73385d85b11646",
            "sha256": "21a9e875250bcb0db8df4cb23dd43c94c00a1d3b98ecba9cdd6ed51586b12248",
            "wheel_plat": "macosx_11_0_arm64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "f3d1d32c8ac58f1e0f9dbe4bc56efa05",
            "sha256": "84be93d0f9e96a15addd490b6e237f588c641c8afdf90e7610a628007fc96867",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "2014a0ebaae3168da555efdcabf03f2a",
            "sha256": "7ee332f7558a984e239e768a13aed86c6c3ac85c90b91d27f4ed38d7ec6b3e8c",
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
            "sha256": "826353d45e7fbaa9b87c514e7c758a82f349cb7fc3fd949423687671539b29cf",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-x86_64-arm-none-eabi.tar.xz",
            "md5": "8cb33f7ec29682f2f9cdc0b4e687f9a6",
            "sha256": "d420d87f68615d9163b99bbb62fe69e85132dc0a8cd69fca04e813597fe06121",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-aarch64-arm-none-eabi.tar.xz",
            "md5": "f020e29a861c5dbf199dce93643d68cc",
            "sha256": "6c713c11d018dcecc16161f822517484a13af151480bbb722badd732412eb55e",
            "wheel_plat": "manylinux_2_27_aarch64",
        },
    },
    "11.2-2022.02": {
        "win32": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-mingw-w64-i686-arm-none-eabi.zip",
            "md5": "e2bb05445200ed8e8c9140fad6a0afb5",
            "sha256": "585156432d73c9c2c8b4742e342564a75d47886d90ac821f88d2b564c33e6766",
            "wheel_plat": "win_amd64",
        },
        "mac_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-darwin-x86_64-arm-none-eabi.tar.xz",
            "md5": "c51d8257b67d7555047f172698730685",
            "sha256": "31d6d3b400db89e204ab1a7ff3f4bb6230d2cdf5a551514ae9deedeebbb07bac",
            "wheel_plat": "macosx_10_15_x86_64",
        },
        "linux_x86_64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi.tar.xz",
            "md5": "a48e6f8756be70b071535048a678c481",
            "sha256": "8c5acd5ae567c0100245b0556941c237369f210bceb196edfe5a2e7532c60326",
            "wheel_plat": "manylinux2014_x86_64",
        },
        "linux_aarch64": {
            "url": "https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-aarch64-arm-none-eabi.tar.xz",
            "md5": "746f20d2eb8acad4e7085e1395665219",
            "sha256": "ef1d82e5894e3908cb7ed49c5485b5b95deefa32872f79c2b5f6f5447cabf55f",
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
