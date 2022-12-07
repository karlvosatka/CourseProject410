
# Sentiment Analysis of Letterboxd Movies
The **Sentiment Analysis of Letterboxd** tool assesses the sentiment of 120 or so of the most popular reviews on Letterboxd.com. Through a GUI interface, users can provide the link to the main page of a film of interest on letterboxd.com. The program then employs various sentiment analysis tools from the NLTK toolkit, including a unique trained model, to calculate the sentiment of each review and provide an overall assessment based on the average sentiment across the reviews. The sentiment analysis results are also compared to the rating for each review and of the film as a whole as a measure of accuracy, where a rating is considered positive if its rating is above the average sitewide rating for a film, and negative if below.

# Video Demo

**[Watch Presentation Here](https://drive.google.com/file/d/1GS4v6SozYyYePNSruSn5qZXpTLSxUiZK/view?usp=share_link)** 

## Related Work

 Used Libraries/Models:
 - NLTK Library
	 - Valence Aware Dictionary and sEntiment Reader (VADER) sentiment analysis model 
	 - NLTK.corpus.movie_reviews
	 - NLTK.classify.scikitlearn
 - BeautifulSoup Library 
 - Requests Library
 - Maven
 - JavaFX

## Implementation of Software
### Scraper
The scraper component of the software (letterboxd_scraper.py) utilizes the Requests and BeautifulSoup4 libraries in Python. Using the get function in the Requests library, given a url and the standard set of headers defined in letterboxd_scraper.py, HTML content is acquired and organized in an object. A dictionary of HTTP header information to standardize output is provided to each request via the headers parameter. Then, via the BeautifulSoup library, working with this HTML object, information can be extracted from the HTML text file via HTML tags. Both libraries are employed in letterboxd_scraper.py, which will pull relevant data when provided with the url for the central page for a film. For example, for the 1999 film The Matrix, one would provide the following url: 

`https://letterboxd.com/film/the-matrix/`
 
The data collected by the scraper includes the film title and release year, the overall average user rating of the film, and the 120 most popular text reviews of the film along with the corresponding numerical rating for each film. Analysis of “ground truth” sentiment is conducted based on this numerical rating, where scores above the sitewide average score of ~6.5 for all films (as calculated from a comprehensive Kaggle dataset) are considered positive and those below it are negative. For some written reviews a score is not provided, in which case the rating is labeled as ‘not given’.  

### Sentiment Model Construction

NLTK built-in movie reviews was used as a training data set, which include 2000 labeled reviews, for two reasons, first, it has built-in functions available, and second, its size is manageable and perfect for the project. For feature selection, all the words in the whole collection were extracted, (about 40000 words), then was ranked based on their term frequency (TF). The top N frequent words are used as feature vectors for the unigram model. The stopwords are removed during this process. Then, a feature map was created for all reviews.

The Standard Vector Machine model from Sci-kit Learn was then used to train the unigram model. Different feature size has been tested, and building and training time for the 5000 features model is about 6 hours, achieving a test accuracy of 74% (for 9:1 train and test split). To further improve the accuracy, Karl suggested trying different N-gram models, so a bigram and a trigram model were built.

Different combinations of N-gram models were tested (Unigram, Bigram, Trigram) across a total of 10 training algorithms, with feature sizes ranging from 500 to 20000 tested, and some parameter tuning was conducted (e.g., tree depths). The  best set in this test was the bigram model trained by Multinomial Naive Bayes classifier with a feature size of 8000, which gives us 98% testing accuracy. This model was saved and used as a pre-trained model in the sentiment analyzer. 

### Sentiment Analyzer

The model will take movie reviews as input and provide statistics such as the number of positive and negative reviews, overall sentiment, and most positive/most negative reviews. Review data are standardized to remove stopwords and symbols and set all characters to lowercase. For reviews shorter than 200 words, the built-in sentiment analyzer Valence Aware Dictionary and sEntiment Reader (VADER) from the NLTK API was applied. We chose this approach because VADER is well suited to analysis of short pieces of text written in internet slang, which is appropriate for the majority of these reviews. For larger reviews, we apply a sentiment analysis model built as described above using NLTK and Scikit-Learn’s Standard Vector Machine model based on multinomial bigram collocations and trained using NLTK’s movie review dataset. 

Model ratings are compared to scraped reviews to get two measures of accuracy. The first compares the overall sentiment across the analyzed reviews to the sentiment derived from the overall average user rating for the film. The other accuracy measure assesses whether the model's prediction of sentiment matches the sentiment of a review on a per-review basis. Both statistics, along with descriptive information about each film, are stored in a text file that is displayed in the UI.

### UI Interface
UI screens were made using the frontend framework of JavaFX. UI is separated into 2 threads, the front end thread which is responsible for the users interactions with the GUI and the backend thread which is responsible for running the python scripts to scrape letterbox reviews and get the sentiment analysis of said reviews.

The backend thread is implemented by making a class called ProgramRunner which extends thread. In Java the way to start the code that will be running in the thread is by using the .start() method. The .start method is implemented using the abstract method run(). The method run() in the ProgramRunner class contains the code that will be ran in the backend thread once the .start() method is called.

The GUI runs Python scripts using the ProcessBuilder package, which is a Java abstraction for fork exec. This means that the GUI backend will be fork execing the python scripts and waiting for each one to finish before starting the next one.

The backend thread uses the Consumer object callback to send messages to the GUI thread to inform the GUI thread of the backend threads progress towards finishing running all the scripts.

## Software Usage

### Dependency Installation Instructions

 - BeautifulSoup4, a tool for extracting useful data from HTML-coded
   text, version 4.11.1 
   - Installed via the `pip install beautifulsoup4` command 
   - More detailed instructions are available **[here](https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.html)** 
  - Lxml, an html parser needed for running BeautifulSoup, version 4.8.0 
	  - Installed via the `pip install lxml` command 
	  - More detailed instructions are available **[here](https://lxml.de/installation.html)** 
  - NLTK, Natural Language Toolkit, a set of tools that aid in processing text data, version 3.7 
	  - Installed via the `pip install nltk` command 
	  - More detailed instructions are available **[here](https://www.nltk.org/install.html)**
  - Sci-Kit Learn, a set of tools for statistical modeling, version 1.1.0
	  - Installed via the `pip install scikit-learn` command 
	  - NOTE: ensure that you have installed at least version 1.1.0 to prevent unpickling errors. Otherwise, you should update your sci-kit learn module.
	  - More detailed instructions are available **[here](https://scikit-learn.org/stable/install.html)** 
  - Maven 
	  - Refer to the maven_install.rtf file in the supplementary directory for detailed installation information. Note that these are from the CS 342 course at UIC and all credit goes to UIC, Professor Hallebeck, and the TA’s that worked on this tutorial.
	  - For alternate instructions, follow [this link](https://maven.apache.org/install.html) from the Apache Maven website.

### Software Installation Instructions
No specific installation is required once dependencies are installed. Simply download the github repository.

### Software Usage Guide

1. Open a terminal window and navigate to the GUI_410 folder. 
2.  Compile the project by entering the command `mvn compile`
3. Execute the program using the command `mvn exec::java`. The GUI window will appear. 
4. Enter the Letterboxd URL for a movie of interest into the  textbox (e.g. [https://letterboxd.com/film/walle/](https://letterboxd.com/film/walle/)) and click Run. This will cause the GUI to go to a waiting screen. 
6. Wait for the results screen to come up. This typically takes anywhere from 1-3 minutes. After the results screen comes up you can review the results of the sentiment analysis. 
7. When you are done viewing the results, click the back button to enter a different URL if desired

### Potential Pitfalls

 1. Errors with Sklearn and the MultinomialNB.pkl pickle file
	 - These can present as a keyerror related to the unpickling task
	 - The error stream will likely mention the unpickler object, or may contain a warning about your version of sklearn
	 - To resolve, ensure that your sklearn version is at least 1.1.0. Follow the instructions above for installing sklearn and re-install it or update it via pip
 2.  Errors with locating the proper link
	 - If an improper link is provided to the GUI, the console will print
   the “Error: incorrect link format” message
	  - If no link is provided, the console will print the “Usage: letterboxd_scraper.py letterboxd_url” message
	  - Ensure that your link is taken from the Letterboxd page and retry. The link should follow this format: `https://letterboxd.com/film/{FILM ID}/`
	  - The film ID is specific to the Letterboxd site and does not follow a regular pattern, so the user has to navigate to the appropriate page first through Letterboxd before providing the link to the GUI. 

## Team Member Contributions
### Karl
Built Web Scraper
Collaborated on parts of Sentiment Analysis
### Rui
Built Bigram-based Sentiment Analysis Model
Collaborated on Sentiment Analysis
### Matt
Built GUI
