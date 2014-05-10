Cell Tower Population Estimation
================================

Work for Thyago


Notes
-----

Data file is ignored from git since it is so large. There should be a file in this directory, named ```CIV10adjv3.asc``` for everything to work. If not, the Abidjan dataset may be used; it is located in ```abidjan```.


Procedure
---------

0. (Optional) Run ```./clustering.py``` to cluster cell towers together

1. Open ```Voronoi Cell Towers/tesselation2.html``` in an HTML5 web browser to calculate Voronoi Tesselation. ```tesselation2.html``` already includes the Ivory Coast cell tower dataset which can be updated/replaced using ```setup.sh```.

2. Click "Export Geometries to CSV"

3. Save the resultant data to a file (```polygons.dat``` for example, saved as WKT (Well Known Text))

3. Run ```./Voronoi\ Cell\ Towers/polygon_processor.rb [polygon-datafile]``` to convert the Voronoi datafile to a CSV which is saved at ```Voronoi Cell Towers/OUTPUT/parsed_polygons.csv```

4. Run ```./grid_converter.py input_file geometry_file output_file``` to convert the population grid-map to a CSV with longitude, latitude, population

5. Run ```./population_estimator.py Voronoi\ Cell\ Towers/OUTPUT/parsed_polygons.csv gridconverter_output_file populations``` to actually estimate the population for each cell tower polygon, stored in a CSV file with tower_id, population. This may take a while depending on the dataset.


Validation
----------

So far, the system has been validated with the Abidjan dataset. The aggregate sum of the population estimates is very close to the actual population reported by census data, as should be expected.


Example Commands
----------------
Abidjan estimation: ```% python population_estimator.py abidjan/abidjan_polygons.csv abidjan/abidjan_geometry.csv abidjan/abidjan_pop.csv abidjan/abidjan_estimates.csv```
Ivory Coast estimation: ```% python population_estimator.py ivorycoast/ivorycoast_polygons.csv ivorycoast/ivorycoast_geometry.csv OUT.csv ivorycoast/ivorycoast_estimates.csv```
