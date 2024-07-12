from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="transcribify",
    version="0.1.1",
    author="Luke Hiura",
    author_email="lhiur001@gmail.com",
    description="A tool for transcribing audio files with optional speaker diarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukehiura/transcribify",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "transformers",
        "pyannote.audio",
        "pydub",
        "PySimpleGUI",
        "Jinja2",
        "pyaudio",
        "numpy"
    ],
)