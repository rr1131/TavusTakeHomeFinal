# TavusTakeHome


#Intro

For the Customer Advocate TakeHome assignment, I wanted to focus on what I believe to be the most valuable aspect of Tavus' CVI -- real time visual perception and conversational fluency. Initially I wanted to go for a Personal Trainer use case but there were a few obstacles that I felt were out of the scope of this assignment such as body kinematics for my KB and figuring out a way to frame the call in such a way for the PAL to be able to make out exactly what I was doing. Since I still wanted to showcase Tavus' CVI's ability to react intelligently to users physical behavior and body movements, I opted for smaller scale with a public speaking coach focused on eye contact, facial expression and overall body language while speaking. 




#Implementation


I was admittedly torn on whether to do my project in the Tavus Platform or by integrating with the Tavus API. Since I think both are important for solutions engineers I opted for a hybrid approach. I created 'Chuck the public speaking coach' persona, customized his perception queries, selected a stock replica for him, and made a brief word doc for "Keys to Public Speaking" for his knowledge base all in the Tavus Platform. In this repo I used FastAPI to mimic how a customer using just the Tavus API would leverage CVI. 




#Reusability


You could theoretically use this backend to generate conversations for other Persona's, Replica's or general conversational use cases. Clone the repo and modify the attributes in .env to your desired API KEY, PERSONA_ID, REPLICA_ID, DOCUMENT_IDS, and REQUIRE_AUTH. I hardcoded the conversational attributes in Main.py but you can also modify those to any specific use case by modifying: conversation_name, custom_greeting and conversational_context. 



#Architecture


main.py: 

  - Serves the UI
  
  - Exposes POST /start
  
  - Programmatically creates a Tavus conversation
  
  - Returns conversation_url
  
tavus.py: 

  - Lightweight Tavus API client
  
  - Constructs JSON payload
 
  - Sends authenticated POST to /v2/conversations
  
  - Logs payload for transparency
  
  - Returns structured response object


index.html: 

  - very lightweight html frontend
  - start session button


main.js


  - Calls /start
  - Receives conversation_url
