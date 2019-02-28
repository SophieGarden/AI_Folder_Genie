# AI_Folder_Genie
A Super COOL Chrome Extension that Magically download files to the right folder! A Browser Download Manager ^^


I developed my first ever MVP, I named AI Folder Genie, it is a Chrome Extension that can automatically download files to the right folder. I am very excited about this product, since I wrote my own machine learning algorithm for it (hierarchical classification), and I also applied NLP techniques to process the file names. It’s the first product I created that is useful to a lot of people, not limited to academia. Also, I am very proud of myself that I did it within a couple of weeks, and it has a very positive feedback so far from people who use it!


This is a project I did for my bootcamp. So I could only spend 2-3 wks on it. I would love to keep working on it once I got a job offer ^^. I am actively looking for machine learning engineer/data scientist positions!

(I have been busy looking for jobs, so I will update the code, as well as instructions of how to install the Chrome Extension later)

See the youtube &slides demo for details!

[Youtube demo](https://www.youtube.com/watch?v=Xv6-8A2dM4w&feature=youtu.be)

[Slides demo](https://github.com/SophieGarden/AI_Folder_Genie/blob/master/AI%20Folder%20Genie_demo_full_version.pdf)


![user interface for input main file directory](https://github.com/SophieGarden/AI_Folder_Genie/blob/master/user_interface_1.png)


I developed “AI Folder Genie”, a Chrome Extension that downloads files to the right folder.

If you’re like me, you probably download files every day 

Then all files directly go to the default Downloads folder, 

But then it costs time and effort to manually move files to where they belong, especially when they belong to a nested folder.

Because of this, my filesystem is now a total mess! But...

...What if there was a way to automatically determine the best folder/subfolder to place a downloaded file?

To solve this, I’ve developed AI Folder Genie, which automatically predicts the best folder or sub-folder for your downloaded file, for each user, and it will learn your file structure habits and predict according to your own file system.

Here is how AI Folder Genie works: Go to demo page.

The Chrome Extension is installed, Right click open this option window, users input the root folder, the main folder of all the files they created, and the default downloads folder of their local computer.

My friend sent me this awesome unsupervised learning video, then I click download, now, instead of going to the default download folder, it goes to the nested Data-Science-Video folder under video folder under the main folder.

Then I just click save, the file directly goes to where it belongs, time and effort are saved too.

You might wonder how AI Folder Genie make predictions: This is a text classification problem, using features derived from file names and extensions, and where the files’ containing folder names are the labels. For my own computer, I have about 16 thousand files.

I processed file names with Natural Language Processing techniques.

I removed symbols, then I did tokenization, stemming, as well as removing stop words. Here is an example of the original files and the engineered version.

Then I count the number of occurrences of tokens extracted from the file names. This finishes my feature engineering process.

These are some examples of the features I extracted from the file names: we can see that the important features not only include file extensions, but also the most frequent words in file names.



As we all know, folders can be nested. And users wouldn’t be happy if my product can only predict to the very first level, i.e, Pic/CS/Research. So in order to predict to deeper levels, I engineered the labels according to the levels they are in. For example, if a file lives in this Python folder, the corresponding label would be this string. I refer to these as level flattened labels.

Once I have the level-flattened labels, the first prediction algorithm I tried is a flat classification algorithm that doesn’t leverage the relationships between different levels. So basically, users first set the level that they want to go to. Then all the files would be labeled by level-flatten- label to the desired level. This is a multi-label classification problem now. 

For example, if user picked level 3, Then all the files would be level-flattened labeled to at most level 3.

For the prediction algorithm, I tried several algorithm, and I picked Logistic regression as my final choice. It can achieve  over 90% accuracy on the first level.


But this level-flattened classification model has two shortcomings: the first is that the data is unbalanced, if we first set an level that we want to go to, some folders would suffer from having only a few training examples. 

The second shortcoming is that even for folders with same amount of files inside, the precision/recall of predictions can also vary vastly.

even folders at the same depth could have vastly different performance in terms of precision and recall, o it’s hard to know a priori what to set for the maximum  depth.

Here is the evaluation of this flatten-out approach, we can see that the prediction dropped to 65% even for a depth of 2. 

To solve this problem, I developed hierarchical classification algorithm.




So I engineer the labels to Hierarchical structures as well. 
For example, if a file lives in this Python folder, this file would have a corresponding label at each level; while for level-flattened labels, there is only one label corresponding to the desired level. 

Now that the feature and label engineering are complete, I wrote my own Hierarchical algorithm.   I trained one softmax classifier at each folder. Each classifier only uses the files that live in the current folder and the nested folders as training examples. So I have the same number of classifiers with the number of folders

When making a prediction, the algorithm advance deeper only when the corresponding classifier is confident. In other words, the prediction will only stop and report the last level folder prediction when the predict_prob of the classifier corresponding to the current folder is less than a threshold value.

To evaluate this model, I performed 10-fold cross validation on the files in my local computer.
Overall, 81% of the predictions go to the right path, by which I mean, the algorithm doesn’t make any wrong splits. For example, if a file lives in this Python folder, and if any one of the green folders is predicted, then it’s considered to be in the Right Path! On the contrary, if the prediction makes any wrong SPLITS, hence goes to one of the red folders, it is counted as a wrong path.

So you may wonder how close to the actual folder my algorithm gets. This figure shows that of those 82% predictions that are on the right path, the majority are distance 0 or 1 away from the actual folder. This means that, when using AI folder genie, users typically need to do nothing or just give 1 simple double-click.

Here we can clearly see the improvement of hierarchical algorithm. In order to achieve the the same overall accuracy, the level-flattened method has to confine its predictions only  to the first level, hence  80% of the data are  at least 4 levels (and therefore at least 4 frustrating double-clicks) away from the actual depth.


------
My name is Sophie Chen, I have a PhD from Electrical & Computer Engineering from University of Illinois at Urbana-Champaign. During my PhD I did lots of analysis on spectral and time domain data. In my spare time, I like to do flowers species classification outdoor with my own eyes.

[LinkedIn](https://www.linkedin.com/in/sophie-chen-data/)
During my PhD in the department of Electrical and Computer Engineering at the University of Illinois at Urbana-Champaign, I focused heavily on data analysis and computational modeling of laser optics. In particular, I developed physical models, which were then verified computationally by ensuring that simulated predictions agreed closely with real data I gathered. During this time, I became increasingly interested in machine learning, and realized that much of what I was doing aligned very closely with the type of modeling work that machine learning practitioners typically perform: gather data, try to develop a model to explain the data, and then evaluate the model in terms of how well it explains heretofore unseen data (in my case, data gathered in different laboratory conditions). I was delighted to find that much of the skills I developed during my time in academia lent themselves rather seamlessly to real-world machine learning problems encountered in the software domain.

However, developing models for data gathered in carefully controlled laboratory conditions versus models which must be robust in the wake of a relatively unpredictable user interactions are two very different things. I developed my first production-deployed machine learning system during my time as an Insight Fellow, when I wrote AI Folder Genie. Implemented as a Chrome extension, AI Folder Genie learns how users organize their files and recommends locations to store newly downloaded files based on contextual and file-specific features. I felt very impressed with myself when I was able to complete the MVP in a mere two weeks, as the modeling portion required natural language processing techniques in order to extract text features, and hierarchical classification techniques in order to make good predictions down users’ directory trees, thereby alleviating them of the manual tedium of navigating to the correct folder via searching and clicking (especially annoying on MacOS). However, it took longer to obtain consistent positive feedback from users, as this required making the product perform well under adversarial usage patterns and to develop careful automatic monitoring and sane fallbacks when the straightforward application of the learned model could give a bad user experience. Since then, I have been primarily interested in understanding: how do we unlock to great potential of machine learning techniques to augment our lives in a way that a) relieves users of manual tedium, and b) requires minimal developer effort? I believe solutions to these sorts of problems are extremely valuable as they have the highest gradient pointed in the direction of making machine learning reliable across a variety of problems. At the point of general reliability, machine learning can be ubiquitous in our lives and allow us to direct our attention on other big problems the world is facing. 
