# Nike Personal Sales Assistant
Demo using Nike's products of how to use undetected-chromedriver, OpenAI, and Pinecone to create a personal sales assistant

Many websites are now incorporating chatbots to answer user questions about their page and company. However, many ecommerce websites have yet to use chatbots to fulfill a sales representative role. This type of chatbot would be valuable to the company itself, as it would increase sales by persuading the customer to purchase items relevant to their query. Additionally, the chatbot would be useful to customers, who can directly get summarized information about extended product descriptions and reviews without having to individually click through several product pages to find the product(s) they are looking for.

The first step of implementing the chatbot is to get access to product data. Ideally, this type of chatbot would have direct access to the database in which product information would be stored. However, since I do not have access to the database of any ecommerce website, I implement this project by utilizing the scraping tool undetected-chromedriver. I specifically chose undetected-chromedriver over requests or the default Selenium chromedriver as there is potential with the other methods of being denied or banned from the website due to bot detection.

After we get the full contents of the product pages, including long product descriptions and some reviews, we need to embed the contents as vectors and upload them along with some metadata (product title, image, url, etc) to pinecone. Then, once we have a customer query, we can use similarity search to get the product that best matches.

Finally, after getting the matching product information and context (description and reviews), we pass this into an LLM to format the result and try to sell the product to the customer in the way a human sales representative might.
