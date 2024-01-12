# TCGPlayerPricer

Quickly price TCGPlayer CSV files generated from the Pricing Tab.

## Instructions

First, in the Pricing tab of your TCGPlayer seller portal click "Export Filtered CSV". Then set all parameters accordingly, I'd suggest checking the boxes that say "Export only from Live Inventory" and "Exclude Listings with Photos". Then move the generated CSV to the folder with the reprice script.

Then in reprice.py,
1. Set the variable FILENAME_INPUT to the name of your file.
2. Define price_formula by making it return the price you want based on card information.

Finally, run reprice.py and a new csv file with <filename>_repriced.csv will be generated.
