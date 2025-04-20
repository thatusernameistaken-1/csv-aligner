from setuptools import setup

APP = ["launch.py"]
OPTIONS = {
    # bundle your dependencies
    "packages": ["streamlit", "pandas"],
    # include Streamlit’s internal bootstrap code
    "includes": ["streamlit.web.bootstrap"],
    # argv_emulation removed (avoids Carbon.framework errors)
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
