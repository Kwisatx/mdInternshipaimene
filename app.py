#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
import bottle
from bottle import default_app, request, route, response, get, template, static_file
from lib.Server import Server
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

bottle.debug(True)

#----------- Show image --------------------------------------------------------------
@route('/images/<filename:re:.*\.png>')
def makeImage(filename):
    return static_file(filename, root='./', mimetype='image/png')
#-------------------------------------------------------------------------------------

#------------ get Poi ----------------------------------------------------------------
@route('/getPoiForm')
def getPoiForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getPoiResult')

@route('/getPoiResult', method='POST')
def getPoiResults():
    traces = request.files.traces
    if traces and traces.file :
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        return server.stringPOI()+"<br>"+server.stringVisits()+"<br>"+stringTrajectories()
    return "You missed a field."
#-------------------------------------------------------------------------------------

@route('/')
def cemmmForm() :
    return "Hello i'm Aymen"

#-------------------------------------------------------------------------------------

"""
@route('/results', method='POST')
def do_upload():
    poi = request.files.poi
    visits = request.files.visits
    if poi and visits and poi.file and visits.file :
        linesPoi = poi.file.read().splitlines()
        linesVisits = visits.file.read().splitlines()
        return cemmm(linesPoi,linesVisits)
    return "You missed a field."

@route('/getPoi')
def getPoiForm() :
    return template("templates/getPoiUploadForm.tpl")

@route('/poiResults', method='POST')
def getPoiResults():
    traces = request.files.traces
    if traces and traces.file :
        linesTraces = traces.file.read().splitlines()
        return template('templates/showImage.tpl', filename="image.png")
    return "You missed a field."
	
@route('/mine')
def tracesForm() :
    return template("templates/mineUploadForm.tpl")

@route('/mineResults', method='POST')
def mineResults():
    traces = request.files.traces
    if traces and traces.file :
        linesTraces = traces.file.read().splitlines()
        return mine(linesTraces)
    return "You missed a field."
"""

#bottle.run(host='localhost', port=8080)
bottle.run(host='0.0.0.0', port=argv[1])
