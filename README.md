# TNT_text_analysis
This project analyze data from [Taiwan National Treasure](https://github.com/national-treasures-tw) (hereafter TNT)
TNT builds a free and public digital archive of Taiwan's historical documents scattered in US National Archives.
The data is uploaded by volunteers in image format then transform to text via google OCR api. 
The total size of data is 70k images, and is increasing in a speed of few thousand document per month.
Through TNT api we can access to the raw data, including metadata, images, ORC, google translate(traditional chinese) and google NLP entities analysis.
This data can be very challenge due to mixing type of document, discretized document (each image is consider as independent document), and inaccurate ocr result.
Our goal is to create functional recommend system base on topic modeling and provide visualized data insight.
If possible, I'd like to try to train convolutionary neuron netword for text generator.

ToDo list
- Data exploring
- Simple data cleaning - NLTK, gensim
- Visualization - ScatterText, PyLDAvis
- LDA/NFM topic modeling - ScikitLearn
- Recommendation system
- CNN text generator
- AWS deploy
