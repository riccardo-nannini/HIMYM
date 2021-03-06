# HOW I MET YOUR MALWARE
## Machine learning driven malware detection :robot:

The project goal is to evaluate the application of different Machine Learning techniques in order to classify PE files as malicious or benign.<br>
The data set can be found [here](https://www.kaggle.com/amauricio/pe-files-malwares).<br><br>
Each sample has more than 70 features obtained through static analysis of its correspondent PE file (e.g. SizeOfCode, SectionMaxEntropy etc.).<br>
The data set contains 19,611 sample of which 14,599 malicious and 5,012 benign.  <br><br>
We used three supervised classification techniques:
- K Nearest Neighbors
- Support Vector Machine (3rd order polynomial kernel)
- Logistic Regression

We performed 5-fold cross validation on each technique in order to find the optimal hyperparameter: the number K of neighbors, the C values for tuning the margin and the regularization parameter respectively.


## Developers :busts_in_silhouette:
 #### Riccardo Nannini :it:
- [GitHub](https://github.com/riccardo-nannini), [Linkedin](https://www.linkedin.com/in/riccardo-nannini/), [Twitter](https://twitter.com/NanniniRiccardo)
#### Veronica Grosso :it:
- [GitHub](https://github.com/Veronica-gg), [Linkedin](https://www.linkedin.com/in/veronica-grosso/)
#### Andrea Giarduz :it:
- [GitHub](https://github.com/andrea-gi), [Linkedin](https://www.linkedin.com/in/andrea-gi/)
