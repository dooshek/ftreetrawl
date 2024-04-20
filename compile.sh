#!/bin/bash
pyinstaller --onefile ftreetrawl.py && chmod +x dist/ftreetrawl && mv dist/ftreetrawl .