#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import os
import bottle
from bottle import default_app, request, route, response, get, template, static_file
from lib.Server import Server
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

#------------ get All Infos from raw mobility traces ---------------------------------
@route('/getInfosSBForm')
def getInfosSBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getInfosSBResult')

@route('/getInfosSBResult', method='POST')
def getInfosSBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        return "-"*60+"<br>"+traces.filename+" Results with stop based algorithme <br>"+"-"*60+"<br>"+server.stringPOI()+"<br>"+server.stringVisits()+"<br>"+server.stringTrajectories()
    return "You missed a field."

@route('/getInfosWBForm')
def getInfosSBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getInfosWBResult')

@route('/getInfosWBResult', method='POST')
def getInfosSBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="WB")
        server.getPoiVisitsAndTrajectories()
        return "-"*60+"<br>"+traces.filename+" Results with Weight based algorithme <br>"+"-"*60+"<br>"+server.stringPOI()+"<br>"+server.stringVisits()+"<br>"+server.stringTrajectories()
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ get Zip File ------------------------------------------------------------
@route('/getZipSBForm')
def getZipForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getZipSBResult')

@route('/getZipSBResult', method='POST')
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

@route('/getZipWBForm')
def getZipWBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getZipWBResult')

@route('/getZipWBResult', method='POST')
def getZipWBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="WB")
        server.getPoiVisitsAndTrajectories()
        zipFileName=server.createZipFilePoiVisitsTrajectories()
        return template('templates/downloadZipFile.tpl', filename=zipFileName,downloadedZipFileName=nameTraces)
    return "You missed a field."
#-------------------------------------------------------------------------------------

#------------ draw figure of raw mobility traces -------------------------------------
@route('/RawMobilityTracesFigureSBForm')
def rawMobilityTracesFigureSBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/RawMobilityTracesFigureSBResult')

@route('/RawMobilityTracesFigureSBResult', method='POST')
def rawMobilityTracesFigureSBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        imgFileName=server.drawMobilityTraceFigure()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."


@route('/RawMobilityTracesFigureWBForm')
def rawMobilityTracesFigureWBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/RawMobilityTracesFigureWBResult')

@route('/RawMobilityTracesFigureWBResult', method='POST')
def rawMobilityTracesFigureWBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="WB")
        imgFileName=server.drawMobilityTraceFigure()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ draw heatmap fo the weight based algorithme -----------------------------

@route('/WBHeatmapForm')
def WBHeatmapForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/WBHeatmapResult')

@route('/WBHeatmapResult', method='POST')
def WBHeatmapResult():
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
@route('/PoiFigureSBForm')
def PoiFigureSBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/PoiFigureSBResult')

@route('/PoiFigureSBResult', method='POST')
def PoiFigureSBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        imgFileName=server.drawPoi()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."


@route('/PoiFigureWBForm')
def PoiFigureWBForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/PoiFigureWBResult')

@route('/PoiFigureWBResult', method='POST')
def PoiFigureWBResults():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="WB")
        server.getPoiVisitsAndTrajectories()
        imgFileName=server.drawPoi()
        return template('templates/showImage.tpl', filename=imgFileName)
    return "You missed a field."
#--------------------------------------------------------------------------------------

#------------ get CEMMM ---------------------------------------------------------------
@route('/getCemmmForm')
def getCemmmForm() :
    return template("templates/mobilityTracesUploadForm.tpl",postMethod='/getCemmmResult')

@route('/getCemmmResult', method='POST')
def getCemmmResult():
    traces = request.files.traces
    if traces and traces.file :
        nameTraces, extTraces = os.path.splitext(traces.filename)
        linesTraces = traces.file.read().splitlines()
        server=Server(linesTraces=linesTraces,method="SB")
        server.getPoiVisitsAndTrajectories()
        server.getCEMMM()
        return server.stringCEMMM()
    return "You missed a field."

@route('/getCemmmForm2')
def getCemmmForm2() :
    return template("templates/PoiAndVisitsUploadForm.tpl",postMethod='/getCemmmResult2')

@route('/getCemmmResult2', method='POST')
def getCemmmResult2():
    poi = request.files.poi
    visits = request.files.visits
    if poi and poi.file and visits and visits.file :
        linesPoi = poi.file.read().splitlines()
        linesVisits = visits.file.read().splitlines()
        server=Server(linesPoi=linesPoi,linesVisits=linesVisits)
        server.getCEMMM()
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

