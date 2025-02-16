# Developer Notes

These are personal notes for the development of the project.

## Adding a new GCC release

TBD.

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
       Manually         │    Triggered    │    Automatically    
     Triggered CI       │   GH Releases   |    triggered CI     
                        │                 │                     
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
