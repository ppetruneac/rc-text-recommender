 # rc-text-recommender 
  ============================== 

 This project idenitfies textual duplicates and recommends similar resources. 
 
 ## Duplicates
 Similar resources are identified based on cosine similarity. 
 
 > Assumtion: 
 Raw data read from source (i.e. MySQL) has language as attribute / column. If note, please use [detect_language.py](https://github.com/ppetruneac/rc-text-recommender/blob/master/src/functions/detect_language.py) in *src/functions* to detect the language, then upload the data back to MySQL. 

 
 ## Recommending similar resources 
 > Nothing on this at the moment.



  
  Project Organization
  ------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── sample         <- A sample of the original data.
    │
    ├── docs               <- Project Documentation that includes busines problem, assumtions, data wrangling & exploration, 
    │                         model methodology, development and implementation.
    │
    ├── logs               <- Logs directory
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Notebooks (i.e. 'notebook.xyz')
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml    <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `conda env export > environment.yml`
    │
    ├── dockerfile         <- File to automate building a Docker container off the code in src, dependencies, and notebooks
    │
    ├── src                <- Source code for use in this project.
       ├── main.xyz        <- Main code to run. 
       │
       ├── functions       <- Scripts to download/generate data; build features, train models or visualize data. 
          |
          └── make_dataset.xyz
          └── build_features.xyz
          └── train.xyz
          └── visualize.xyz

    <p><small>Project structure inspired by [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/).</small></p>
  
  
