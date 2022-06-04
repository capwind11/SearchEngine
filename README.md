# Tutorial

## 1. Crawl the news
The first time to run the application, you have to crawl news.

You have to enter the folder `crawler/crawler/` and run the file
crawl.py.

## 2. Build and Run the application

run the main.py

if you are the first time to run, 
you should uncomment the statement to execute the function init_data().

`init_data()` is used to generate inverted indexes and necessary data like tf-idf, categories for news items.

**Note**: If you need to classify the news item, please specify the key `weights_path` and `device` in a dict and pass the dict to the `init_data` function. Concretely, `weights_path` is the weight checkpoint of the BERT model. You can download our pretrained weights from the link mentioned in the report. `device` is the device (e.g., `cpu` or `cuda:0`) to run the classification process.