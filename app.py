#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv

import bottle
from bottle import default_app, request, route, response, get, template, static_file

from lib.cemmm.cemmm import cemmm
from lib.sbAlgorithme.Essai import essai
from lib.mine import mine
from lib.getPoi import getPoi

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

bottle.debug(True)


@route('/images/<filename:re:.*\.png>')
def makeImage(filename):
    return static_file(filename, root='./', mimetype='image/png')


@route('/traces')
def tracesForm() :
    return template("templates/mobilityTracesUploadForm.tpl")


@route('/tracesResults', method='POST')
def do_upload_for_traces():
    traces = request.files.traces
    if traces and traces.file :
        linesTraces = traces.file.read().splitlines()
        figure=essai(linesTraces)
        canvas=FigureCanvas(figure)
        canvas.print_figure("image.png")
        return template('templates/showImage.tpl', filename="image.png")
    return "You missed a field."



@route('/')
def cemmmForm() :
    return template("templates/uploadForm.tpl")

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
        return getPoi(linesTraces)
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


#bottle.run(host='localhost', port=8080)
bottle.run(host='0.0.0.0', port=argv[1])
