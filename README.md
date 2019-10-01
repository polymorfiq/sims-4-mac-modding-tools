# sims_4_package_parser

Steps to run:
1. Install Docker
2. Clone repo and `cd` into it
2. Run `docker-compose build && docker-compose run app /bin/bash`
3. In Docker, run `cd tools && python dump_package.py`


Useful commands:
- `uncompyle6 -o Sims4Files/decompiled_simulation Sims4Files/simulation/**/*.pyc`
- `for f in $(find Sims4Files/simulation/ -name '*.pyc'); do local_replacement="${f/Sims4Files\//Sims4Files\/decompiled/}"; uncompyle6 -o ${local_replacement/\.pyc/\.py} $f; done`
- `python -m compileall .`
