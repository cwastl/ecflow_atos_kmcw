#!/usr/bin/env python3
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
#    ci.load("harp_io.def")
    ci.suspend("/harp_io")  # so that we can resume manually in ecflow_ui
    ci.replace("/harp_io", "harp_io.def")
    ci.begin_suite("/harp_io")

except RuntimeError as e:
    print ("(!) Failed:"),   e
