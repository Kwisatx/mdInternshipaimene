#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
import os
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
@route('/downloadZipFile/<filename:re:.*\.zip>')
def makeZip(filename):
    return static_file(filename, root='./', mimetype='application/zip')
#-------------------------------------------------------------------------------------

#----------- Download File -----------------------------------------------------------
@route('/images/<filename:re:.*\.png>')
def makeImage(filename):
    return static_file(filename, root='./', mimetype='image/png')
#-------------------------------------------------------------------------------------

#------------ get Poi ----------------------------------------------------------------
@route('/getInfosForm')
def getInfosForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getInfosResult')

@route('/getInfosResult', method='POST')
def getInfosResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        return "-"*60+"<br>"+traces.filename+" Results <br>"+"-"*60+"<br>"+server.stringPOI()+"<br>"+server.stringVisits()+"<br>"+server.stringTrajectories()
    return "You missed a field."
#-------------------------------------------------------------------------------------

#------------ get Zip File ------------------------------------------------------------
@route('/getZipForm')
def getZipForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getZipResult')

@route('/getZipResult', method='POST')
def getZipResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        zipFileName=server.createZipFilePoiVisitsTrajectories()
        return template('templates/downloadZipFile.tpl', filename=zipFileName,downloadedZipFileName=nameTraces)
    return "You missed a field."
#-------------------------------------------------------------------------------------

@route('/')
def cemmmForm() :
    return "Hello i'm Aymen"

#-------------------------------------------------------------------------------------

#bottle.run(host='localhost', port=8080)
bottle.run(host='0.0.0.0', port=argv[1])
