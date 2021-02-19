DASH web app for pressure tracking in Baltazar lab, version 1.3
Antonija Grubisic-Cabo, 2020

Web app for pressure logging.

It is running within a python environment DASH_PressureApp (activate with conda activate DASH_PressureApp) and it should be
kept so to avoid any problems.

App py is located in "pressure" folder, and can be activated by running "python PressureApp.py" form the DASH environment.

There are 3 tabs:
One for today's pressure with 1s updates
One for the current year with 1 min update 
One for pressur logging for the last 24 h and full year

Today's pressure is refreshed every 1 second, current year every 10 s.
Todays shows last 10 minutes with continous update, and current year last 2.5 days. 
WARNING! If you have less than 10 min (2.5 days) worht of data, these gaphe will be empty. You can change the period displayed by changing 'ind' for these tabs.
x-axis is showing time, y-axis is showing pressure (log scale).
Latest updated pressure value for each gauge is displayed under the graph.

Pressure logging is not updated constanty, but new data can be added with a "Refresh data" button.
This tab is useful if you are interested in certain (part of the) day and want to zoom-in on the region etc (cannot do it with continous update as it refreshes).
x-axis is showing time, y-axis is showing pressure (log scale).







server address: http://130.237.20.24/

Testing is done on local server (demo/testinf server 127.0.0.2:8050). Do not test the app while making changes to the pressure logging code.

python environment specs:
python 3.6, dash 1.14.0, 
dash-core-components 1.10.2, dash-html-components 1.0.3, 
h5py 2.10.0 (latest), numpy 1.16.4, pandas 0.24.2
