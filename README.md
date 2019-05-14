# content-scoper
Example scripts for identifying content that falls within scope of a web crawl using machine learning

##running the code

- Check the two training data url files included in 'training_data/urls'. Each contains a list of urls preceeded by an index. The first file contains Egyptian Urls and the second file contains Arabic Urls (not Egyptian).

- Run python myspider.py
- This will scrap the content of the home page of each url, preprocess and normalize the Arabic text. Then, save the resulted text based on its index into the 'training_data/content' folder. 

- Run python mlearning.py
- This will read the training data content, split it into 80% trainng data and 20% test data. Then will train the model and evaluate it.

 
