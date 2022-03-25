# PublicEcon_seminar
The data is collected from [Datafordeler.dk](https://datafordeler.dk/)
See the GeoDanmark-vejledning-til-Datafordeleren-v1 file that is a guide about how to access the data. (Danish)

The raw data set is the Danish BBR register (Bolig og Bygnings Register = House and Buildings Register).

See an [Overwiev of the full data set here](http://grunddatamodel.datafordeler.dk/).

Since the Dataset is a large one about 6 520 758 000 lines in JSON format and uses 247.281 GB menory, it is splitted into 15 files with max 434 717 lines in each. Using SplitTextFile, that can be downloaded [here](https://www.withdata.com/big-text-file-splitter/download.html).

The Splitted files are then edited such that the dictionary is loadable.


