#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from sys import argv
import os
import bottle
from bottle import default_app, request, route, response, get, template, static_file
from lib.Server import Server

#bottle.debug(True)

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

#------------ get All Infos from raw mobility traces ---------------------------------
@route('/getInfosForm/<method>')
def getInfosForm(method) :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getInfosResult/{0}'.format(method))

@route('/getInfosResult/<method>', method='POST')
def getInfosResults(method):
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method=method)
        server.getPoiVisitsAndTrajectories()
        return "-"*60+"<br>"+traces.filename+" Results with stop based algorithme <br>"+"-"*60+"<br>"+server.stringPOI()+"<br>"+server.stringVisits()+"<br>"+server.stringTrajectories()
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ get Zip File ------------------------------------------------------------
@route('/getZipForm/<method>')
def getZipForm(method) :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getZipResult/{0}'.format(method))

@route('/getZipResult/<method>', method='POST')
def getZipResults(method):
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method=method)
        server.getPoiVisitsAndTrajectories()
        zipFileName=server.createZipFilePoiVisitsTrajectories()
        return template('templates/downloadZipFile.tpl', filename=zipFileName,downloadedZipFileName=nameTraces)
    return "You missed a field."
#-------------------------------------------------------------------------------------

#------------ draw figure of raw mobility traces -------------------------------------
@route('/RawMobilityTracesFigureForm/<method>')
def rawMobilityTracesFigureForm(method) :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/RawMobilityTracesFigureResult/{0}'.format(method))

@route('/RawMobilityTracesFigureResult/<method>', method='POST')
def rawMobilityTracesFigureResults(method):
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method=method)
        imgFileName=server.drawMobilityTraceFigure()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ draw heatmap fo the weight based algorithme -----------------------------

@route('/HeatmapForm')
def HeatmapForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/HeatmapResult')

@route('/HeatmapResult', method='POST')
def HeatmapResult():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="WB")
        imgFileName=server.drawHeatmap()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."

#--------------------------------------------------------------------------------------

#------------ draw figure of Poi ------------------------------------------------------
@route('/PoiFigureForm/<method>')
def PoiFigureForm(method) :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/PoiFigureResult/{0}'.format(method))

@route('/PoiFigureResult/<method>', method='POST')
def PoiFigureResults(method):
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method=method)
        server.getPoiVisitsAndTrajectories()
        imgFileName=server.drawPoi()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ get CEMMM ---------------------------------------------------------------
@route('/getCemmmForm')
@route('/getCemmmForm/<method>/<postprocessing>')
def getCemmmForm(method="SB",postprocessing="K-FIRST") :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getCemmmResult/{0}/{1}'.format(method,postprocessing))

@route('/getCemmmResult/<method>/<postprocessing>', method='POST')
def getCemmmResult(method,postprocessing):
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method=method)
        server.getPoiVisitsAndTrajectories()
        server.getCEMMM(method=postprocessing)
        return server.stringCEMMM()
    return "You missed a field."

@route('/getCemmmPreCalculatedForm')
@route('/getCemmmPreCalculatedForm/<postprocessing>')
def getCemmmPreCalculatedForm(postprocessing="K-FIRST") :
    return template("templates/PoiAndVisitsUploadForm.tpl",postMethod='/getCemmmPreCalculatedResult/{0}'.format(postprocessing))

@route('/getCemmmPreCalculatedResult/<postprocessing>', method='POST')
def getCemmmPreCalculatedResult(postprocessing):
    poi = request.files.poi
    visits = request.files.visits
    if poi and poi.file and visits and visits.file :
        linesPoi = poi.file.read().splitlines()
        linesVisits = visits.file.read().splitlines()
        server=Server(linesPoi=linesPoi,linesVisits=linesVisits)
        server.getCEMMM(method=postprocessing)
        return server.stringCEMMM()
    return "You missed a field."
#--------------------------------------------------------------------------------------

LOCALHOST="localhost:8080"
HEROKU="https://calm-waters-6506.herokuapp.com"

BASEPATH=HEROKU
@route('/')
def index() :
    return template('templates/index.tpl')

if (BASEPATH==LOCALHOST) : bottle.run(host='localhost', port=8080)
else : bottle.run(host='0.0.0.0', port=argv[1]) 
#--------------------------------------------------------------------------------------

