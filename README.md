NLP module for identifying lung nodules.

# Requirements #

* Python 3.3+
* nltk (for tokenizer)

# Documentation #

Home: https://github.com/kpwhri/crn-lung-nodule
Old Version: https://bitbucket.org/dcronkite/crn-lung-nodule/

## Install ##

* `git clone ...`
* `python setup.py install`
    * This will add the script `crn-algorithm`
    * You can also use the algorithm directly
        * `danforth_algorithm.extract_iterators`: when in list
        * `danforth_algorithm.extract_files`: a directory of files

## Usage ##

Run `crn-algorithm -h` for argument details.

### Input ###

Either of:

* Directory of text files containing lung radiology notes
* List of (identifier, radiology notes) tuples in Python

### Output ###
The application will output a CSV file:


| identifier | True/False for SPN | Nodule size, else -1 |
|------------|--------------------|----------------------|



# Algorithm Description #
There are two algorithms contained in this package, [*danforth*][0] and [*farjah*][1]. The differences in the algorithms can be gleaned from the papers.


## Danforth Algorithm [0] ##

Specify algorithm `--algorithm danforth`. 

### Sentence  Level Search ###

1. Does this sentence contain a Positive Keyword (Table 1.A and Table 1.B)?
    * If No 
        * Does the previous sentence has positive keyword and the previous sentence is not NLP positive?
            * If Yes  keep searching this sentence;
            * If No  consider sentence NLP negative; proceed to next sentence.
    * If Yes 
        * Tag this sentence, keep searching this sentence;

2. Does the sentence contain an Absolutely Disqualifying Term (Table 2), e.g. “adenopathy”?
             If No  keep searching this sentence;
             If Yes  consider sentence NLP negative; proceed to next sentence.

3. Tag the sentence if it contains an Excluded Terms (Table 3), e.g. “scattered”.
4. Tag the sentence if it contains an Offsetting Terms (Table 4), e.g. “lung”.
5. Does this sentence tagged with Excluded Terms in Step 3?
If No keep searching this sentence;
If Yes is there an Off-Setting Term tagged in Step 4?
    * If Yes  keep searching this sentence;
    * If No  consider sentence NLP negative; proceed to next sentence.
6. Does this sentence contains terms in Table 1.B
If Yes  consider sentence NLP positive
If No  keep searching this sentence;

7. Search the qualifying dimension (size) in the sentence:
If the size is > 30 mm  consider sentence NLP negative; proceed to next sentence .
If the largest dimension is > 5 mm && <= 30 mm  consider sentence NLP positive


### Transcript Level Decision ###

Entire transcript will be disqualified based on any sentence with reference to nodule >30mm;
else, if there is an NLP positive sentence, this transcript is positive.

### Table 1.A Positive Keywords Qualifier Required ###

*	densit
*	GGO
*	groundglass
*	ground-glass
*	ground glass
*	lesion
*	mass
*	nodular
*	nodule
*	opacity
*	opacities

### Table 1.B: Positive Keywords No Qualifier Req ###

*	SPN
*	single pulmonary nodule*
*	solitary pulmonary nodule*
*	single nodule*
*	solitary nodule*

### Table 2: Sentence Disqualified if it contains the following (regardless of anything else)###

*	scattered
*	diffuse
*	triangular
*	linear

### Table 3: Excluded Words if no Offsetting Terms ###

*	adenopathy
*	adrenal
*	bladder
*	gallbladder
*	gland
*	hepati
*	kidney
*	liver
*	lymph
*	mediastin
*	pancrea
*	renal
*	spleen
*	thyroid
*	axilla, axillary
*	abdomen, abdominal
*	retroperitoneum
*	retroperitoneal

### Table 4: Offsetting Terms ###

*	lung
*	chest
*	pulmonary
*	thorax
*	hemithorax
*	thoracic


## Farjah Algorithm [1] ##

This is the default, but you'll need to do some additional work with the output by limiting the nodule sizes from 1.0 to 30.0. It is mostly based on the danforth algorithm with a handful of modifications to improve performance.


# Roadmap #

* Alternative sentence splitting
* Options to limit based on nodule size
* Read-in CSV, SAS7BDAT, others?


# License #
MIT License: https://kpwhri.mit-license.org/


# References #
[0]:Danforth KN, Early MI, Ngan S, Kosco AE, Zheng C, Gould MK. Automated Identification of Patients With Pulmonary Nodules in an Integrated Health System Using Administrative Health Plan Data, Radiology Reports, and Natural Language Processing. J Thorac Oncol 2012;7(8):1257-1262.[link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3443078/)

[1]: An Automated Method for Identifying Individuals with a Lung Nodule Can Be Feasibly Implemented Across Health Systems. Farjah F, Halgrim S, Buist DS, Gould MK, Zeliadt SB, Loggers ET, Carrell DS. EGEMS (Wash DC). 2016 Aug 26;4(1):1254. [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5013935/)
