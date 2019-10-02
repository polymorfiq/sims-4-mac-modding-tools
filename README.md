# sims_4_package_parser

Steps to run:
1. Install Docker
2. Clone repo and `cd` into it
2. Run `docker-compose build && docker-compose run app /bin/bash`
3. In Docker, run `cd tools && python dump_package.py`


Useful commands:

*Decompile Sims Python Files:*
`decompile_sims_python`

*Package your script and install in scripts folder:*
`package_mod YOUR_SCRIPT_FOLDER your_script_name`
