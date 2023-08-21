# gh-pub-index

```markdown
This is a template for making a public index for cargo-prebuilt.
The instructions to set this up are under the wiki. https://github.com/cargo-prebuilt/gh-pub-index/wiki
Look at the offical index if you need an example of how to setup this.
The offical public index is https://github.com/cargo-prebuilt/index.
```

This is an index, if you are looking for the cli tool it is [here](https://github.com/cargo-prebuilt/cargo-prebuilt).

## Public Key

## Platforms Supported (Targets)

Tier 1: Crates must build on these platforms
- x86_64-unknown-linux-gnu
- x86_64-unknown-linux-musl
- x86_64-apple-darwin
- aarch64-apple-darwin
- aarch64-unknown-linux-gnu
- aarch64-unknown-linux-musl

Tier 2: Crates optionally build for these platforms, but if one fails the entire build fails
- x86_64-pc-windows-msvc
- aarch64-pc-windows-msvc
- x86_64-unknown-freebsd
- riscv64gc-unknown-linux-gnu
- s390x-unknown-linux-gnu
- armv7-unknown-linux-gnueabihf
- armv7-unknown-linux-musleabihf

Tier 3: Crates optionally build for these platforms, but the build will still publish if any fail
- x86_64-unknown-netbsd
- x86_64-unknown-illumos
- x86_64-sun-solaris
- powerpc64-unknown-linux-gnu
- powerpc64le-unknown-linux-gnu
- mips64-unknown-linux-gnuabi64
- mips64-unknown-linux-muslabi64
- mips64el-unknown-linux-gnuabi64
- mips64el-unknown-linux-muslabi64

## Crates

## "API"

See [API](API.md)
