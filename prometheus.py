'''

# Prometheus

## Making the knowledge base: storing the facts and the rules

We will store all the facts in a file (maybe .cvs? it would be easy to manipulate) in tuples, where we will specify each fact, the question associated with it, and its code. E.g:

"p1" : "The apple is red." : "Is the apple red?"

N.B. I talked with the TA, turns out sometimes asking for a Yes/No answer for every fact is stupid. For instance, if you want to know the symptoms that someone is having for a possible
disease, it might be useful to just present all the symptoms and the person just ticks all the ones he has. It's silly to ask a lot of repeated Yes/No questions.

Or something similar, so that we can refer to facts (or to questions) with their code (e.g. "p1"). I think dictionaries in python may make this easy.
We will then have another file which specifies all the rules that apply, in the form:

p1, p2, p3 => p4

N.B. The TA mentioned the fact that we may also have conditions where, instead of needing all facts to be true for the condition to be true, there could be a threshold
where a minimum of N facts need to be true for the conclusion to be true. I guess we could solve this by including in the data structure also counters such as:

p1, p2, p3 => p4 : 0 : 3
T, p6, p7, p8 => p9 : 1 : 3

In the first case, all 3 facts need to be true for the rule to activate, but there are 0 true facts at the moment. In the second one, only three out of 4 facts need to be true
but one is already true (it has been changed from p5 to T). This would also make it much easier to check whether rules have been activated.

In order to use these facts, we need a parser, which will read and encode both the file with the facts (e.g. as a dictionary) and the file with the rules (I'm not sure how
would be a good way to do this).
All of this may be done in a class of its own, and a couple of methods could be useful here:

- A method that returns the dictionary associated with the facts. It would just read the facts from a file, parse them into a dicrionary, and return it.

- A method that returns the rule base as some data structure. Same thing as for the facts, but I'm unsure as to the data structure.

- Would it be useful to have methods that get statistics from the data?

## Making the inference engine

Here we should assume we have the facts and the rule easily accessible. The engine could easily consist of one class with an internal state (the knowledge base) and
methods. I will list methods that come to mind as useful:

- A method which returns the question that needs to be asked currently. This may be done as follows: for each fact p, count the occurrences of p in the premises, and then for each
  consequence c in which rules p appears, count the number of occurrences of c and add that to the counter. Do that recursively. The aim is to get a measure of how useful a certain premise will be towards resolving as many rules as possible. Ties may be broken at random.

- A method which edits the rule base. As the user responds within the GUI, answers will be received through this method. Answers will be of the type T or F for specific facts.
  Each proposition in a premise will be marked T or F in the rule base to specify its state. The counters for each rule will also be updated.

'''

print("Is your C code working? (yes/no)")
answer = raw_input().lower()
if answer == 'yes':
    print("Then it probably doesn't contain any bug.")

elif answer == 'no':
    print("Then it probably contains some bug.")

else:
    print("I'm not prepared for this.")
