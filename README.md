# sims_4_package_parser

Steps to run:
1. Install Docker
2. Clone repo and `cd` into it
2. Run `docker-compose build && docker-compose run app /bin/bash`
3. In Docker, run `cd tools && python dump_package.py`


Useful commands:
- `uncompyle6 -o uncompiled_python_dir *.pyc`
- `uncompyle6 -o decompiled wickedwhims/**/*.pyc`
