# gpt-chat-autoresponder
Due to the fact that VK has blocked access to the "sendMessage" API, messsages are will be sent by emulating actions in the browser via selenium. 
## So,for this tool works fine,you need to install chomedriver via this command:
+ pip install chromedriver-binary
## And also necessary requirements by:
+ pip install -r requirements.txt

## Also,for usage you need to:
+ find your VK token,wich provides an access to the API's and gptChat key.
+ Set up all id's for responding in file called "id.txt". If its not exist,create it.
## On the first launch, you will be asked to fill in all the required data.After that,they will be contained in "data.json" file
