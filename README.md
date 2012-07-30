solarmon
=============

The Solarmon watches over solar panels, and provides realtime reporting of input and output voltage, current and power.

Running
----------
For extra fun, the solarmon is made up of 3 components:

acquire.py:
This simple script reads serial input from the XBee, decodes the message, translates input values into voltage, current, etc. and outputs a line of text for each data point into a file.

htmlstatus.py:
This script watches a data file, as outputed by acquire.py, and generates a pretty html status page.  Actual rendering of charts is done via javascript on the client side, this script mostly handles averaging the data into buffers for hour, day and week display.

janitor.py:
This script cleans up after acquire.  Data is archived into proto records as defined in data.proto.  Running this script will archive each raw text file in the data directory (and remove them), except for the latest file which is assumed to be the currently updating input.  This script is set to save 1 data point per minute.

To run the monitoring system, simply hook up the XBee receiver and then execute acquire.py followed by htmlstatus.py.  All data is dumped into a directory called "data" with the same root as the scripts (assumed to exist).  The janitor script should be run as a nightly cron job to save space (a raw text log is ~20MB for a day while the proto is 45k).
