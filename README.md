# Soiling_Forecast_Algorithm

The scope of this project is to develop a new soiling forecast algorithm for a Parabolic Through Collector
(PTC) system installed in Limassol, Cyprus's largest soft drink factory, KEAN,
in order to predict its reflectivity by estimating the soiling rate.

The physical mechanisms and the equations that are calculated in this soiling model are derived from
existing atmospheric dust transport models considering the dry deposition of dust over geographic regions, and
have been applied to the problem of the soiling of parabolic through collector mirrors (PTC). 

The SFA model is located in **src** folder.

In order to make a soiling forecast estimation possible, meteorological and particulate matter data are required. 
In the **data** folder are situated the respective input data that was utilized as inputs in the model. There are 2 subfolders:
1. Meteorological_Data containing the meteorological input data and
2. ΡΜ, which contains the particulate matter's input data.
Further, in the **data** folder are also located the relfectivity measurements, which are utilized for the validation of the model's
outcomes. 

SFA's results are saved in the **output** folder. 


## src folder - Explanation of scripts

- The ref_optima.py file constitutes the main script of the SFA. In this particular Python code, the procedure of reflectivity
prediction is executed with a 4-day time step.

- The **model_parameters.py** contains all the necessary parameters of the model. 

- The **constants.py** contains constant variables.

- The **functions_optima.py** script contains the formulas and the respective functions for the computation of each soiling mechanism.

For the importation of the input data, two scripts were utilized:
 
1) The **ads.py** script is used so that the particulate matter's data can be imported into the main script. The respective data are
derived from the [CAMS global atmospheric composition forecasts](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=form). 

2) Accordingly, the **file merge_files.py** is used for the importation of the meteorological conditions.                             


## Execution 

The model can be executed through the main script **Ref_optima.py** by opening and running the 
code through a Python compiler (i.e., Spyder or PyCharm). It should be mentioned that this step is conditional 
on the respective Python compiler that the user utilizes.
The results are saved in the **outputs** folder.


## Planning a simulation

In this case, the model is prepared for a specific case study. If you want to plan a new simulation from scratch, you must execute the 
next important steps: 
1. Import the input conditions in the **data** folder.
2. If your simulation does not concern this particular PTC system, you must change the respective location features (i.e., latitude).
After the completion of the above-required steps, the model will be executed through **Ref_optima.py** 
where the results will be shown in the **output** folder.

---------------------------------------------------------------------------------------------------------------------------
Anticipating results according the respective plots:

A) **Reflectivity estimation**:
![alt text](https://github.com/ThanosVouke/Soiling_Forecast_Algorithm/blob/main/output/Plots/SR_3_June_2019.jpg?raw=true)
