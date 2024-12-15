# PropaInsight

This is the official code repository for our COLING 2025 paper: PropaInsight: PropaInsight: Toward Deeper Understanding of Propaganda in Terms of Techniques, Appeals, and Intent

#### Our New Framework for Analyzing Propaganda Corpus
![We abstract key elements of propaganda from social science literature. A comprehensive propaganda frame includes the techniques employed, the appeals evoked in readers, and the author’s underlying intent.](https://github.com/Lumos-Jiateng/PropaInsight/blob/main/images/propainsight.png)
We abstract key elements of propaganda from social science literature. A comprehensive propaganda frame includes the techniques employed, the appeals evoked in readers, and the author’s underlying intent. 

#### Our Partially Controlled Data Generation Pipeline

![Partially controlled data generation pipeline: We first collect real-world news articles and derive an objective summary to extract events. Then we generate event-based intent, and randomly sample specific propaganda techniques to insert into the event descriptions. Lastly, we generate appeals from a reader’s perspective, aiming at making the appeals grounded to the text.](https://github.com/Lumos-Jiateng/PropaInsight/blob/main/images/pipeline.png)
Partially controlled data generation pipeline: We first collect real-world news articles and derive an objective summary to extract events. Then we generate event-based intent, and randomly sample specific propaganda techniques to insert into the event descriptions. Lastly, we generate appeals from a reader’s perspective, aiming at making the appeals grounded to the text.

#### PropaGaze: The first dataset designed for Propaganda Analysis

PropaGaze is a high quality dataset for propaganda analysis where propaganda-full articles are annotated with propaganda techniques, aroused appeals among human readers, and the underlying intent. The dataset is splited into three subsets of PTC-Gaze, RUWA-Gaze, and Polifact-Gaze. While the first split is human annotated data, the remaining are high quality generated synthetic data from our controlled generation pipeline. We will open-source the dataset step by step. 


### Catalog 
#### Version-1.0 Update:
  1. Release the first dataset designed for Propaganda Analysis: PropaGaze, Updated Dec 13th, 2024
 
