 # rc-text-recommender 
  
 This project is meant to identify textual duplicates and to recommend similar resources based on resource topic. 

 Folder structure: 
 - `data`: 
   - contains sample folders used in processing. These can also be created at run time
   - `all_duplicates.csv`: this file contains duplicates already identified and manually validated.  The field `certainty` contains the validation status. More on this in [ReadMe](./detect_duplicates/README.md). 
 - `detect_duplicates`: this is the folder with the code to identify duplicated resources. Check [ReadMe](./detect_duplicates/README.md) file for more info.
 - `notebooks`: used in data exploration. The code was already converted into the python scripts. This folder is archive. 
 
 ### Recommending similar resources 
 
 Nothing on this at the moment but the first attempt was still based on the same method as identifying duplicate resources. 


 
