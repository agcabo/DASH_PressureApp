# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:51:04 2020

@author: Antonija Grubisic-Cabo
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import h5py
import pandas as pdsudo
import plotly
import plotly.graph_objs as go
import plotly.express as px
from collections import deque
import time
import os
import datetime as dt

max_length = 86400 #seconds in a day


time.sleep(30)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['bWLwgP.css']
app = dash.Dash('Baltazar-pressure-log', external_stylesheets=external_stylesheets)
server = app.server

app_color = {"graph_bg": " #B3B7F7", "graph_line": "  #00FFFF"}


f1 = h5py.File('/media/data/Logs/Pressure/today.h5', 'r', libver='latest', swmr=True)
a1=np.array(f1['tstamp'][:f1['ind'][0]].astype('<M8[s]'),dtype='datetime64')
 	
t1=a1.tolist()


STR1=list(np.power(10,f1['STR']))
HHG1=list(np.power(10,f1['HHG']))
LL1=list(np.power(10,f1['LL']))
MC1=list(np.power(10,f1['MC']))
PC1=list(np.power(10,f1['PC']))
PRE1=list(np.power(10,f1['PRE']))
FOC1=list(np.power(10,f1['FOC']))
 	
ind1=f1['ind'][0]

f2 = h5py.File('/media/data/Logs/Pressure/2021.h5', 'r', libver='latest', swmr=True)
a2=np.array(f2['tstamp'][:f2['ind'][0]].astype('<M8[s]'),dtype='datetime64')
#
t2=a2.tolist()
STR2=list(np.power(10,f2['STR']))
HHG2=list(np.power(10,f2['HHG']))
LL2=list(np.power(10,f2['LL']))
MC2=list(np.power(10,f2['MC']))
PC2=list(np.power(10,f2['PC']))
PRE2=list(np.power(10,f2['PRE']))
FOC2=list(np.power(10,f2['FOC']))
#
ind2=f2['ind'][0]


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Today', children=[
            html.H3('Pressure log @ Baltazar lab with live updates'),
            dcc.Graph(
                id='today-live',
                ),
           dcc.Interval(
                id='graph1-update',
                interval=1000, #in milliseconds. 1 second for daily updates
                n_intervals=0
                ),
           html.Table([
           html.Td([html.Tr(['Load Lock:']), html.Tr(id='LL_label')]),
           html.Td([html.Tr(['Prep Chamber:']), html.Tr(id='PC_label')]),
           html.Td([html.Tr(['Main Chamber:']), html.Tr(id='MC_label')]),
           html.Td([html.Tr(['HHG:']), html.Tr(id='HHG_label')]),
           html.Td([html.Tr(['ReFOCusing:']), html.Tr(id='FOC_label')]),
           html.Td([html.Tr(['STeeRing:']), html.Tr(id='STR_label')]),
           html.Td([html.Tr(['PREvacuum:']), html.Tr(id='PRE_label')]),
          ] ),
           
            
        ]),
        dcc.Tab(label='This year', children=[
            html.H3('Yearly pressure log @ Baltazar lab with live updates'),
            dcc.Graph(
                id='current year-live',
                ),
            dcc.Interval(
                id='graph2-update',
                interval=10000, #1 minute for yearly log #test updatign the web page every 20s
                n_intervals=0
                ),
           html.Table([
           html.Td([html.Tr(['Load Lock:']), html.Tr(id='LL_label2')]),
           html.Td([html.Tr(['Prep Chamber:']), html.Tr(id='PC_label2')]),
           html.Td([html.Tr(['Main Chamber:']), html.Tr(id='MC_label2')]),
           html.Td([html.Tr(['HHG:']), html.Tr(id='HHG_label2')]),
           html.Td([html.Tr(['ReFOCusing:']), html.Tr(id='FOC_label2')]),
           html.Td([html.Tr(['STeeRing:']), html.Tr(id='STR_label2')]),
           html.Td([html.Tr(['PREvacuum:']), html.Tr(id='PRE_label2')]),
           
          ] 
          ),

        ]),
                dcc.Tab(label='Pressure log', children=[
            html.H3('Pressure log @ Baltazar lab. Last 24h and current year'),
            html.Button('Refresh data',id='Refresh'),
            dcc.Graph(
                id='today-static'
                ),
                        dcc.Graph(
                id='current year-static'
                ),
        ]),

]),
    ])


@app.callback([Output('today-live', 'figure'),Output('LL_label','children'), Output('PC_label','children'),Output('MC_label','children') , Output('HHG_label','children'), Output('FOC_label','children'), Output('STR_label','children'), Output('PRE_label','children')],
              [Input('graph1-update','n_intervals')]
              )




def gen_today_update(interval):
 	f1 = h5py.File('/media/data/Logs/Pressure/today.h5', 'r', libver='latest', swmr=True)
 	f1['tstamp'].refresh()
 	f1['ind'].refresh()
# 	ind1=f1['ind'][0]
 	a1=np.array(f1['tstamp'][:f1['ind'][0]].astype('<M8[s]'),dtype='datetime64')
 	
 	t1=a1.tolist()
 	
 	f1['STR'].refresh()
 	f1['HHG'].refresh()
 	f1['LL'].refresh()
 	f1['MC'].refresh()
 	f1['PC'].refresh()
 	f1['PRE'].refresh()
 	f1['FOC'].refresh()
 	STR1=list(np.power(10,f1['STR']))
 	HHG1=list(np.power(10,f1['HHG']))
 	LL1=list(np.power(10,f1['LL']))
 	MC1=list(np.power(10,f1['MC']))
 	PC1=list(np.power(10,f1['PC']))
 	PRE1=list(np.power(10,f1['PRE']))
 	FOC1=list(np.power(10,f1['FOC']))
 	 	
 	
 	ind1=f1['ind'][0]
 	points1=ind1-600
    
 	figure1={
                'data': [
 	
                    {'x': t1[points1:ind1], 'y': FOC1[points1:ind1], 'type': 'line', 'name': 'Focusing'},
                    {'x': t1[points1:ind1], 'y': HHG1[points1:ind1], 'type': 'line', 'name': 'HHG'},
                    {'x': t1[points1:ind1], 'y': LL1[points1:ind1], 'type': 'line', 'name': 'Load Lock'},
                    {'x': t1[points1:ind1], 'y': MC1[points1:ind1], 'type': 'line', 'name': 'Main Chamber'},
                    {'x': t1[points1:ind1], 'y': PC1[points1:ind1], 'type': 'line', 'name': 'Preparation Chamber'},
                    {'x': t1[points1:ind1], 'y': PRE1[points1:ind1], 'type': 'line', 'name': 'Pre-vacuum'},
                    {'x': t1[points1:ind1], 'y': STR1[points1:ind1], 'type': 'line', 'name': 'Steering Chamber'}
                ],
                'layout':{
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    'color_discrete_sequence':'px.colors.sequential.Plasma',
                    'xaxis':{'range':[t1[points1], dt.datetime.now()]},
    #                'yaxis':{'type':'log'},
                    'yaxis':{'type':'log','showesponent':'all', 'exponentformat':'e', 'title': 'Pressure [mbar]'}
                }
                }
    
 	return figure1, "{:.2E}".format(LL1[ind1])+' mbar',"{:.2E}".format(PC1[ind1])+' mbar' ,"{:.2E}".format(MC1[ind1])+' mbar' ,"{:.2E}".format(HHG1[ind1])+ ' mbar', "{:.2E}".format(FOC1[ind1])+' mbar', "{:.2E}".format(STR1[ind1])+' mbar', "{:.2E}".format(PRE1[ind1])+' mbar'


@app.callback(Output('current year-live', 'figure'),Output('LL_label2','children'),Output('PC_label2','children'), Output('MC_label2','children'), Output('HHG_label2','children'), 
Output('FOC_label2','children'), Output('STR_label2','children'), Output('PRE_label2','children'),
              [Input('graph2-update','n_intervals')]
              )


def gen_year_update(interval):#testing for a bug in 2020/h5 file!!! running code with today file to test if bug still appears
#	f2 = h5py.File('/media/data/Logs/Pressure/today.h5', 'r', libver='latest', swmr=True)   
	f2 = h5py.File('/media/data/Logs/Pressure/2021.h5', 'r', libver='latest', swmr=True)
	f2['tstamp'].refresh()
	f2['ind'].refresh()
	a2=np.array(f2['tstamp'][:f2['ind'][0]].astype('<M8[s]'),dtype='datetime64')
	ind2=f2['ind'][0]
	
	t2=a2.tolist()

	
	f2['STR'].refresh()
	f2['HHG'].refresh()
	f2['LL'].refresh()
	f2['MC'].refresh()
	f2['PC'].refresh()
	f2['PRE'].refresh()
	f2['FOC'].refresh()

	STR2=list(np.power(10,f2['STR']))
	HHG2=list(np.power(10,f2['HHG']))
	LL2=list(np.power(10,f2['LL']))
	MC2=list(np.power(10,f2['MC']))
	PC2=list(np.power(10,f2['PC']))
	PRE2=list(np.power(10,f2['PRE']))
	FOC2=list(np.power(10,f2['FOC']))
	
	ind2=f2['ind'][0]#-1 #added -1 to see if 1970 issue can be avoided
	#ind2=ind2-1
	#testing if the odd bug of 1.jan.1970 can be avoided if we plot from [1] istead of [0]
	points2=ind2-3600#720#3600 #3600 = 60 h approx 2.5 days. Index out of range because we don't have2.5 days worth of data. test for 12 h (720 min)

    
	figure2={
                'data': [
	
                    {'x': t2[points2:ind2], 'y': FOC2[points2:ind2], 'type': 'line', 'name': 'Focusing'},
                    {'x': t2[points2:ind2], 'y': HHG2[points2:ind2], 'type': 'line', 'name': 'HHG'},
                    {'x': t2[points2:ind2], 'y': LL2[points2:ind2], 'type': 'line','name': 'Load Lock'},
                    {'x': t2[points2:ind2], 'y': MC2[points2:ind2], 'type': 'line', 'name': 'Main Chamber'},
                    {'x': t2[points2:ind2], 'y': PC2[points2:ind2], 'type': 'line', 'name': 'Preparation Chamber'},
                    {'x': t2[points2:ind2], 'y': PRE2[points2:ind2], 'type': 'line', 'name': 'Pre-vacuum'},
                    {'x': t2[points2:ind2], 'y': STR2[points2:ind2], 'type': 'line', 'name': 'Steering Chamber'}
                ],
                'layout':{
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                   'xaxis':{'range':[t2[points2], dt.datetime.now()]},#### testing for the 1970 bug #t2[points2] workinf, max(t2) not updating...
                    #'yaxis':{'type':'log'}
                    'yaxis':{'type':'log','showesponent':'all', 'exponentformat':'e', 'title': 'Pressure [mbar]'}
                    }
                }
    
	return figure2, "{:.2E}".format(LL2[ind2])+' mbar', "{:.2E}".format(PC2[ind2])+' mbar',"{:.2E}".format(MC2[ind2])+' mbar' , "{:.2E}".format(HHG2[ind2])+ ' mbar', "{:.2E}".format(FOC2[ind2])+' mbar', "{:.2E}".format(STR2[ind2])+' mbar', "{:.2E}".format(PRE2[ind2])+' mbar'


@app.callback(Output('today-static', 'figure'),
              [Input('Refresh', 'n_clicks')]
              )

	
def refresh_static1(n_clicks):
    
	f1 = h5py.File('/media/data/Logs/Pressure/today.h5', 'r', libver='latest', swmr=True)
	f1['tstamp'].refresh()
	f1['ind'].refresh()
	a1=np.array(f1['tstamp'][:f1['ind'][0]].astype('<M8[s]'),dtype='datetime64')
	
	t1=a1.tolist()
	
	f1['STR'].refresh()
	f1['HHG'].refresh()
	f1['LL'].refresh()
	f1['MC'].refresh()
	f1['PC'].refresh()
	f1['PRE'].refresh()
	f1['FOC'].refresh()

	STR1=list(np.power(10,f1['STR']))
	HHG1=list(np.power(10,f1['HHG']))
	LL1=list(np.power(10,f1['LL']))
	MC1=list(np.power(10,f1['MC']))
	PC1=list(np.power(10,f1['PC']))
	PRE1=list(np.power(10,f1['PRE']))
	FOC1=list(np.power(10,f1['FOC']))
	
	ind1=f1['ind'][0]
	start=ind1-86400


    
	figure3={
		'data': [
	
                    {'x': t1[:ind1], 'y': FOC1[:ind1], 'type': 'line', 'name': 'Focusing'},
                    {'x': t1[:ind1], 'y': HHG1[:ind1], 'type': 'line', 'name': 'HHG'},
                    {'x': t1[:ind1], 'y': LL1[:ind1], 'type': 'line', 'name': 'Load Lock'},
                    {'x': t1[:ind1], 'y': MC1[:ind1], 'type': 'line', 'name': 'Main Chamber'},
                    {'x': t1[:ind1], 'y': PC1[:ind1], 'type': 'line', 'name': 'Preparation Chamber'},
                    {'x': t1[:ind1], 'y': PRE1[:ind1], 'type': 'line', 'name': 'Pre-vacuum'},
                    {'x': t1[:ind1], 'y': STR1[:ind1], 'type': 'line', 'name': 'Steering Chamber'}
                ],
                'layout':{
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    'title':'Today',
                  #  'yaxis':{'type':'log'}
                  'yaxis':{'type':'log','showesponent':'all', 'exponentformat':'e', 'title': 'Pressure [mbar]'}
                    }
                }
    
	return figure3

	
@app.callback(Output('current year-static', 'figure'),
              [Input('Refresh', 'n_clicks')]
              )

	
def refresh_static2(n_clicks):

	f2 = h5py.File('/media/data/Logs/Pressure/2021.h5', 'r', libver='latest', swmr=True)
	f2['tstamp'].refresh()
	f2['ind'].refresh()
	a2=np.array(f2['tstamp'][:f2['ind'][0]].astype('<M8[s]'),dtype='datetime64')
	
	t2=a2.tolist()
	
	f2['STR'].refresh() #with this form, and f2[tsta,p] and f2[ind] refreshed, lists everything as y=1 after some time. try refresh all of the values
	f2['HHG'].refresh()
	f2['LL'].refresh()
	f2['MC'].refresh()
	f2['PC'].refresh()
	f2['PRE'].refresh()
	f2['FOC'].refresh()

	STR2=list(np.power(10,f2['STR']))
	HHG2=list(np.power(10,f2['HHG']))
	LL2=list(np.power(10,f2['LL']))
	MC2=list(np.power(10,f2['MC']))
	PC2=list(np.power(10,f2['PC']))
	PRE2=list(np.power(10,f2['PRE']))
	FOC2=list(np.power(10,f2['FOC']))
	
	ind2=f2['ind'][0]#-1 #added -1 to see if 1970 issue can be avoided
	end=ind2-1


    
	figure4={
		'data': [
	
                    {'x': t2[:ind2], 'y': FOC2[:ind2], 'type': 'line', 'name': 'Focusing'},
                    {'x': t2[:ind2], 'y': HHG2[:ind2], 'type': 'line', 'name': 'HHG'},
                    {'x': t2[:ind2], 'y': LL2[:ind2], 'type': 'line', 'name': 'Load Lock'},
                    {'x': t2[:ind2], 'y': MC2[:ind2], 'type': 'line', 'name': 'Main Chamber'},
                    {'x': t2[:ind2], 'y': PC2[:ind2], 'type': 'line', 'name': 'Preparation Chamber'},
                    {'x': t2[:ind2], 'y': PRE2[:ind2], 'type': 'line', 'name': 'Pre-vacuum'},
                    {'x': t2[:ind2], 'y': STR2[:ind2], 'type': 'line', 'name': 'Steering Chamber'}
                ],
                'layout':{
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    'title':'Current year',
                    'xaxis':{'range':[t2[0], dt.datetime.now()]},#### testing for the 1970 bug. dt.datetime.now() works OK for axis but values stops updating after some time for some unknown reason.
                   'yaxis':{'type':'log','showesponent':'all', 'exponentformat':'e', 'title': 'Pressure [mbar]'}
                    }
                }
    
	return figure4

if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(debug=True,port=8001, host='0.0.0.0')


