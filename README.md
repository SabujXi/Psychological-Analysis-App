# Psychological Analysis Desktop Application by Md. Sabuj Sarker
This is a desktop application for Psychological analysis for a research project. I developed this in Python.

I developed it back in 2016 and have rewritten it completely in 2018 with many improvements.

This desktop application is a four-in-one application that shows different images, let the subject select tempereature, ratings, etc. and also sends temperatures to a hardware device attached to the subject. (A human is indicated by the word 'subject' here).

# Coding practice improvements overtime.
I am programming continuously for more than a decade now. My coding practices changed extremely in this long period of time. Though there is no free time to look back how much my architectural thoughts changed along with the coding practices, I was surprised to see it when I started rewriting this application. I do not keep global states, but in last two years I am also unwilling to keep a module for configs as global states. I import such modules in controlling part and then propagate that through other objects down to the rabbit hole. Many times, I do not directly send or use the module, instead I create another wrapper objects.

Whatever, that is just one single minor change/improvement. There are a lot of other changes and improvements. Architectural changes are everywhere, pattern changes are in every corner. With these changes, bugs have gone down to the ground level, reusability have skyrocketed and sudden feature introduction or changes do not give as much pain as it used to give years ago.

I am writing this section to tell you to keep coding every day of your life and you will see that some day you have become a great programmer without you noticing that. No, the world does not need to do that. We are like backstage singers, we drive success, we do not want to be the celebrities - we make them.

## Err
I need to clean up many parts of this application <s>along with many print()'s</s>. So, just ignore them. There are some dead code (especially the configs) that I will also need to remove. I will do this housekeeping job whenever I have some free time or I am taking rest off of other work. But, there is no guarantee that I will complete the housekeeping.
I did not keep my previous code in any version control, neighter I includied the 2016's version in this repository. This repository contains 2018's code (SEP-OCT).

Also, remember that this was a Python 2.7 application. <s>The difference with 3.x is not much there in the code - it is just print statement instead of print() function.</s> Module import names may also vary. I will try to remove this inconsistency when I have got some time.
