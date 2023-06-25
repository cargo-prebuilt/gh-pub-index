#!/usr/bin/python3

import tomllib
import sys

t2_targets = [
    "x86_64-unknown-freebsd",
    "riscv64gc-unknown-linux-gnu",
    "s390x-unknown-linux-gnu",
]

win_targets = [
    "x86_64-pc-windows-msvc",
    "aarch64-pc-windows-msvc"
]

t3_targets = [
    "x86_64-unknown-netbsd",  # Optional Support (64-bit)
    "x86_64-unknown-illumos",
    "x86_64-sun-solaris",
    "powerpc64-unknown-linux-gnu",
    "powerpc64le-unknown-linux-gnu",
    "mips64-unknown-linux-gnuabi64",
    "mips64-unknown-linux-muslabi64",
    "mips64el-unknown-linux-gnuabi64",
    "mips64el-unknown-linux-muslabi64",

    "armv7-unknown-linux-gnueabihf", # Optional Support (32-bit)
    "armv7-unknown-linux-musleabihf",
]


def main(pull_request, index, crate, version, crate_license, dl, checksum, filename):
    pull_request = True if pull_request == "true" else False

    with open(filename, "rb") as file:
        crate_toml = tomllib.load(file)
        unsupported = crate_toml["info"]["unsupported"]
        git_url = crate_toml["info"]["git"]

    with open("./stable.template.yml", "r") as file:
        action_template = file.read()

    action = action_template.replace("%%INDEX%%", index)
    action = action.replace("%%CRATE%%", crate)
    action = action.replace("%%VERSION%%", version)
    action = action.replace("%%LICENSE%%", crate_license)
    action = action.replace("%%DOWNLOAD%%", dl)
    action = action.replace("%%CHECKSUM%%", checksum)
    action = action.replace("%%GIT%%", git_url)
    action = action.replace("%%IF%%", str(not pull_request).lower())

    # Flags
    apple_flags = [None, False, ""]  # FEATURES(0), NO_DEFAULT_FEATURES(1), EXTRA_FLAGS(2)
    linux_flags = [None, False, ""]
    windows_flags = [None, False, ""]

    if "target" in crate_toml:
        targets = crate_toml["target"]
        if "all" in targets:
            if "features" in targets["all"]:
                f = targets["all"]["features"]
                apple_flags[0] = f
                linux_flags[0] = f
                windows_flags[0] = f
            if "no-default-features" in targets["all"]:
                f = targets["all"]["no-default-features"]
                apple_flags[1] = f
                linux_flags[1] = f
                windows_flags[1] = f
            if "flags" in targets["all"]:
                f = targets["all"]["flags"]
                apple_flags[2] = f
                linux_flags[2] = f
                windows_flags[2] = f

        if "apple" in targets:
            if "features" in targets["apple"]:
                apple_flags[0] = targets["apple"]["features"]
            if "no-default-features" in targets["apple"]:
                apple_flags[1] = targets["apple"]["no-default-features"]
            if "flags" in targets["apple"]:
                apple_flags[2] = targets["apple"]["flags"]

        if "linux" in targets:
            if "features" in targets["linux"]:
                linux_flags[0] = targets["linux"]["features"]
            if "no-default-features" in targets["linux"]:
                linux_flags[1] = targets["linux"]["no-default-features"]
            if "flags" in targets["linux"]:
                linux_flags[2] = targets["linux"]["flags"]

        if "windows" in targets:
            if "features" in targets["windows"]:
                windows_flags[0] = targets["windows"]["features"]
            if "no-default-features" in targets["windows"]:
                windows_flags[1] = targets["windows"]["no-default-features"]
            if "flags" in targets["windows"]:
                windows_flags[2] = targets["windows"]["flags"]

    final_apple_flags = ""
    if apple_flags[0] is not None:
        final_apple_flags += f"--features '{apple_flags[0]}' "
    if apple_flags[1]:
        final_apple_flags += "--no-default-features "
    final_apple_flags += apple_flags[2]

    final_linux_flags = ""
    if linux_flags[0] is not None:
        final_linux_flags += f"--features '{linux_flags[0]}' "
    if linux_flags[1]:
        final_linux_flags += "--no-default-features "
    final_linux_flags += linux_flags[2]

    final_windows_flags = ""
    if windows_flags[0] is not None:
        final_windows_flags += f"--features '{windows_flags[0]}' "
    if windows_flags[1]:
        final_windows_flags += "--no-default-features "
    final_windows_flags += windows_flags[2]

    # Write Flags
    action = action.replace("%%APPLE_FLAGS%%", final_apple_flags)
    action = action.replace("%%LINUX_FLAGS%%", final_linux_flags)
    action = action.replace("%%WINDOWS_FLAGS%%", final_windows_flags)

    # T2
    # Cross
    targets = ""
    for possible in t2_targets:
        if possible not in unsupported:
            if len(targets) != 0:
                targets += ","
            targets += possible
    if len(targets) != 0:
        action = action.replace("%%T2_CROSS_HAS_TARGETS%%", "true")
        action = action.replace("%%T2_CROSS_TARGETS%%", targets)
    else:
        action = action.replace("%%T2_CROSS_HAS_TARGETS%%", "false")
        action = action.replace("%%T2_CROSS_TARGETS%%", "err_no_targets")
    # Windows
    targets = ""
    for possible in win_targets:
        if possible not in unsupported:
            if len(targets) != 0:
                targets += ","
            targets += possible
    if len(targets) != 0:
        action = action.replace("%%T2_WIN_HAS_TARGETS%%", "true")
        action = action.replace("%%T2_WIN_TARGETS%%", targets)
    else:
        action = action.replace("%%T2_WIN_HAS_TARGETS%%", "false")
        action = action.replace("%%T2_WIN_TARGETS%%", "err_no_targets")

    # T3
    # Cross
    targets = ""
    for possible in t3_targets:
        if possible not in unsupported:
            if len(targets) != 0:
                targets += ","
            targets += possible
    if len(targets) != 0:
        action = action.replace("%%T3_CROSS_HAS_TARGETS%%", "true")
        action = action.replace("%%T3_CROSS_TARGETS%%", targets)
    else:
        action = action.replace("%%T3_CROSS_HAS_TARGETS%%", "false")
        action = action.replace("%%T3_CROSS_TARGETS%%", "err_no_targets")

    with open("./.github/workflows/stable-" + crate + ".yml", "w") as file:
        file.write(action)


if __name__ == "__main__":
    argv = sys.argv
    main(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8])
