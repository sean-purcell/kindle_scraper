#!/bin/bash

env/bin/pip freeze | egrep -v "pkg-resources|lxml|multidict|yarl|six" > requirements.txt
