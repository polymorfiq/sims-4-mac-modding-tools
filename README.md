# sims_4_package_parser

Steps to run:
1. Install [Docker](https://docs.docker.com/v17.09/engine/installation/#desktop)
2. Clone repo and `cd` into it
3. Run `docker-compose build && docker-compose run app /bin/bash`


Useful commands:

*Decompile Sims Python Files:*
`decompile_sims_python`

*Package your script and automatically install in Mods folder:*
`package_mod YOUR_SCRIPT_FOLDER your_script_name`

*Unpackage a .package file*:
`python tools/dump_package.py YOUR_PACKAGE.package`

(Your package will be dumped to the tmp/data folder)
