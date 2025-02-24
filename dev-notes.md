# Developer Notes

These are personal notes for the development of the project.

## Adding a new GCC release

- Add the URLs and md5 to the `gcc_releases.py` file
- Check the release notes and ensure the added wheel platform is correct
- Add the "short version" to `gcc_short_versions` in `gcc_releases.py` file
- Add a new row to the release tables in both READMEs
- The CI workflow should **not** need to be updated
- Check if the any of the downloaded zip/tar files do not have a single root
  directory. If any don't, add the exception to `uncompress_toolchain()`

### Toolchain download locations

- https://launchpad.net/gcc-arm-embedded
- https://developer.arm.com/downloads/-/gnu-rm
- https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads

## Pushing a new release or releases

Everything should be automated via CI.

However, because an update the packaging would need to create a GH release
for each GCC release, the automation does not start with the manual creation
of a GH release. Instead the automation is triggered via a manual workflow
trigger.

1. To to the "Build and Release" GH Action workflow:
  https://github.com/carlosperate/arm-none-eabi-gcc-py-package/actions/workflows/release.yml
2. Trigger the workflow via the "Run workflow" button on the top right.

Everything else should happen automatically.

```
                        │                 │                     
       Manually            Triggered from      Automatically    
     Triggered CI       │   GH Releases   |    triggered CI     
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
          │             │                 │                     
          │                                                     
          ▼             │                 │                     
 ┌──────────────────┐                                           
 │                  │   │                 │                     
 │   Build Wheels   │                                           
 │       and        │   │                 │                     
 │   source dist    │                                           
 │                  │   │                 │                     
 └──────────────────┘                                           
          │             │                 │                     
          │                                                     
 ┌────────▼─────────┐   │ ┌────────────┐  │                     
 │                  │     │            │     ┌─────────────────┐
 │    Test Wheels   │ ┌───► GH Release ├─────►  Test release   │
 │                  │ │   │  v13.3.x   │  │  │    wheels &     │
 └────────┬─────────┘ │ │ │            │  │  │  PyPI deploy    │
          │           │   └────────────┘     └─────────────────┘
          │           │ │                 │                     
 ┌────────▼─────────┐ │   ┌────────────┐                        
 │                  │ │ │ │            │  │  ┌─────────────────┐
 │     Publish      ├─┘   │ GH Release │     │  Test release   │
 │   GH Release/s   ├─────►  v13.2.x   ├─────►    wheels &     │
 │                  ├─┐   │            │     │  PyPI deploy    │
 └────────┬─────────┘ │ │ └────────────┘  │  └─────────────────┘
          │           │                                         
          │           │ │      ...        │                     
 ┌────────▼─────────┐ │                                         
 │                  │ │ │ ┌────────────┐  │                     
 │    Generate &    │ │   │            │     ┌─────────────────┐
 │  deploy Simple   │ └───► GH Release ├─────►  Test release   │
 │   Package Repo   │     │   v9.2.x   │     │    wheels &     │
 │                  │   │ │            │  │  │  PyPI deploy    │
 └──────────────────┘     └────────────┘     └─────────────────┘
                        │                 │                     
```

## Manual build source distribution

```bash
cd arm-none-eabi-gcc-toolchain-pypi
python -m build --sdist --config-setting source_wheel=../dist/wheel_file.whl
```
