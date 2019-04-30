#!/bin/bash

env/bin/pip freeze | egrep -v "pkg-resources|lxml" > requirements.txt
