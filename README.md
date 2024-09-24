# README 
This repository contains the implementation of a master thesis project that tries to predict prior to the NFL draft whether a college player is going to be a "good" or "bust" pick, using machine learning. 
Offense positions that are evaluated are Quarterbacks, Running Backs, Wide Receivers, and Tight Ends, while on the defensive side the Defensive Backs as well as Linebackers and Defensive Linemen are evaluated. The features vary depending on the position group, and are chosen through feature selection process. 

The whole thesis, including the whole machine learning pipeline, the origin of the data, and the process from preprocessing to the results, can be found at the website of my university, [FH Hagenberg](https://search-fho.obvsg.at/primo-explore/fulldisplay?docid=FHO_alma2139523270004527&context=L&adaptor=Local%20Search%20Engine&vid=FHO&lang=de_DE&search_scope=default_scope&tab=default_tab&query=addsrcrid,exact,AC16706015). 

The main code can be found in [python-scripts](./python_scripts/), which has files for every positional group that make use of the modularized pipeline, of which the main implementation is in [nfl_machinelearning.py](./python_scripts/nfl_machine_learning.py). 

