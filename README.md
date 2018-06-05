# Conversational Agent

Conversational agents have several applications, namely for remote automatic assistance. On the other hand, if a conversational agent has a conversational behavior that makes it indistinguishable from the behavior expected in a human being, it may be considered that this agent has human-level intelligence. <br>
This project consists in the development of a conversational agent with the following characteristics:
- Natural language processing for some common sentences type;
- Ability to accumulate information given by interlocutors and produce answers to questions based on the accumulated information;
- For grammatically incorrect or not supported sentences, react in a ”seemingly intelligent” way;

## Dependencies
Besides python3, you need to have [NLTK](https://www.nltk.org/). You can install it using pip:

```
sudo pip install -U nltk
```

After that, you'll need to use [NLTK](https://www.nltk.org/) to obtain punkt and averaged_perceptron_tagger resources. Use the following commands:

```
python3
»»» import nltk
»»» nltk.download('punkt')
»»» nltk.download('averaged_perceptron_tagger')

```
## Supported Sentences
The conversation agent can support several sentences and questions. Here are some of the most important input examples:
- My phone is on the table
- The table is in the room
- The room is in the house
- Where is my phone?
- The food is in the fridge
- I need a snake
- I have a white boat
- What is the color of my boat?
- I have an old dog
- What is the age of my dog?
- Do I have a dog?
- My name is John
- My name is Earl Smith
- What is my name?
- A cat is an animal
- Bob is nice
- Bob is my friend
- Bob is a cat
- Who is bob?

### Examples
The file [example.txt](https://github.com/tiagohpf/si-2018-chatbot/blob/master/example.txt) shows some examples that's possible to follow in the execution of the application. It shows different scenarios and the interaction between the user and the conversational agent.
