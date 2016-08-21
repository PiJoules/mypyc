python setup.py bdist_wheel
wheel install dist/pc-?.?.?-py?-none-any.whl --force
wheel install-scripts pc
python setup.py develop

