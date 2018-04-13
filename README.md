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
