# Soiling_Forecast_Algorithm2

In this study, a new soiling forecast algorithm is proposed to 
predict the accumulation of dust on the mirrors of a PTC plant. 

This soiling model is based on existing models for the dry deposition of dust over geographic regions.

The scope of this paper is to develop a new soiling forecast algorithm for a PTC system installed in Limassol, 
Cyprus's largest soft drink factory, KEAN, in order to predict its reflectivity by estimating the soiling rate.

The physical mechanisms and the equations that are calculated are derived from existing atmospheric dust transport models and 
have been applied to the problem of the soiling of parabolic through collector mirrors (PTC). 

Tο μοντέλο βρίσκεται αποθηκευμένο στον φάκελο src.

Στον φάκελο data βρίσκονται αποθηκευμένα τα δεδομένα που χρησιμοποιούνται σαν είσοδο στο μοντέλο. Υπάρχουν 2 υποφάκελοι:
1) Meteorological_Data containing the meteorological input data and,
2) ΡΜ which contains the particulate matter's input data.
Furthrmore, in data folder are located also the relfectivity measurements which are utilized for the validation of the model's 
outcomes. 

The SFA's results are saved in the output folder. 


## Φάκελος src - Επεξήγηση των ρουτινών

- Το αρχείο Ref_optima.py αποτελεί τον πηγαίο κώδικα. Μέσα σε αυτόν εκτελούνται όλες οι διαδικασίες εκτίμησης
    της ανακλαστικότητας.

- Το model_parameters.py περιέχει όλες τις μεταβλητές που λαμβάνονται σαν είσοδο στο μοντέλο.

+ Το constants.py περιλαμβάνει διάφορες σταθερές.

* Η ρουτίνα functions_optima.py περιέχει όλες τις συναρτήσεις που χρησιμοποιούνται στον πηγαίο κώδικα. Αυτές οι συναρτήσεις 
   χρησιμοποιούνται για τον υπολογισμό σημαντικών μεταβλητών του μοντέλου. 

Για την είσοδο των αρχικών συνθηκών υπάρχουν 2 ρουτίνες :
 
1) Η ρουτίνα ads.py χρησιμοποιείται για την εισαγωγή των δεδομένων που αφορούν τα αιωρούμενα σωματίδια from 
[CAMS global atmospheric composition forecasts](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=form).

. 

2) Αντίστοιχα το αρχείο merge_files.py χρησιμοποιείται για την εισαγωγή των μετεωρολογικών δεδομένων.                              


					      ## Εκτέλεση του αλγορίθμου 

Το μοντέλο εκτελείται απο τον πηγαίο κώδικα Ref_optima.py. Ανοίγετε τον αλγόριθμο μέσω ενός compiler πχ Spyder και στην συνέχεια
πατάτε Run. Τα αποτελέσματα θα αποθηκευτούν στον φάκελο outputs. Επίσης στην οθόνη θα εμφανιστούν όλες οι γραφικές παραστάσεις. 

!!ΠΡΟΣΟΧΗ!! Αν έχετε τρέξει ήδη μια φορά αυτή την προσομοίωση θα πρέπει να διαγράψετε τα αρχεία από τον φάκελο output και τον 
φάκελο Plots αν θέλετε να την ξανατρέξετε καθώς η Python δεν επιτρέπει να γίνεται overwrite στα αρχεία.  


					 ## Εκτέλεση του αλγορίθμου- σχεδιασμός προσομοίωσης

Το μοντέλο είναι στημένο για μια συγκεκριμένη πρόγνωση. Αν επιθυμείτε να σχεδιάσετε μια προσομοίωση εξ ολοκλήρου από την αρχή 
θα πρέπει να βάλετε στον φάκελο data τις κατάλληλα δεδομένα. Είναι η μοναδική διαδικασία που απαιτείται για την προσομοίωση. 
Μετά από αυτό το βήμα, όπως και παραπάνω, ανοίγεται τον πηγαίο κώδικα Ref_optima.py και πατάτε Run. Ομοίως τα αποτελέσματα σας θα 
αποθηκευτούν στον φάκελο output.

---------------------------------------------------------------------------------------------------------------------------
Anticipating results according the respective plots:

A) **Reflectivity estimation**:
![alt text](https://github.com/ThanosVouke/Soiling_Forecast_Algorithm/blob/main/output/Plots/SR_3_June_2019.jpg?raw=true)
