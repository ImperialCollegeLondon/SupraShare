# Is my cage porous?

Adapted from: [Lukas Turcani Source Code](http://www.github.com/lukasturcani/cage_prediction)

Part of [www.jelfs-group.org](http://www.jelfs-group.org)

This site does not collect or store any information about you or your molecules.

This is a very simple app which uses trained machine learning models to predict if an organic cage will be shape persistent or collapsed. These models are discussed in detail in our [paper](https://doi.org/10.26434/chemrxiv.6995018).

To use the app, place the SMILES of the cage building block and linker in the appropriate columns. The SMILES of molecules are readily available on wikipedia or they can be generated with ChemDraw (go to Edit -> Copy As -> SMILES and then paste into the column). The "model" column specifies which machine learning model should be used to make a prediction. For example, "alkyne2 alkyne3" means a model trained on cages generated with alkyne linkers and alkyne building blocks. The "aldehyde2 amine3" model is trained on cages generated with aldehyde linkers and amine building blocks, and so on. All models assume the cage has a tetrahedral, Tri4Di6, topology from a \[4+6\] reaction. For the most accurate predictions, the model should match your own linkers and building blocks. In cases of faulty SMILES the model will still provide an answer.

The database holding the cages used for training is available at DOI: [10.14469/hpc/4618](https://doi.org/10.14469/hpc/4618).

An example amine2 aldehyde3 shape persistent cage is CC3, which has the linker SMILES of "N\[C@H\]1CCCC\[C@@H\]1N" and building block SMILES of "O=Cc1cc(C=O)cc(C=O)c1". An example of a collapsed cage can be seen using the linker "NCCCCCCN" and building block "O=Cc1cc(C=O)cc(C=O)c1".
