#!/bin/bash -e
echo '---Installing flake8---'
pip install flake8==3.8.4 pep8==1.7.1 pydocstyle==5.1.1 flake8-docstrings==1.5.0 flake8-class-attributes-order==0.1.2
echo '---Running flake8---'
flake8 config photo_manager utils --ignore="E722,W504,E501,Q000,N802,D401,D413" \
  --exclude=".venv,migrations,manage.py,__init__.py,data_processor.py" \
  --per-file-ignores=admin.py:CCE001 \
  --class-attributes-order="docstring,nested_class,field,meta_class,expression,__new__,__init__,__post_init__,__str__,magic_method,save,delete,property_method,private_property_method,method,private_method"
echo '---flake8 passed---'