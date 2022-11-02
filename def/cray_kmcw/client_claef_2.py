#!/usr/bin/env python3
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
#    ci.load("claef_2.def")
    ci.suspend("/claef_2")  # so that we can resume manually in ecflow_ui
    ci.replace("/claef_2", "claef_2.def")
    ci.begin_suite("/claef")

except RuntimeError as e:
    print ("(!) Failed:"),   e
