#Georgetown Data Science Certificate

##Personalizing an Audio Content Stream

###Authors: Nicole Donnelly, Sujit Ray, Anthea Watson Strong

**May 21, 2016**
 
[SlideDeck](http://www.slideshare.net/antheawatson/personalizing-a-stream-of-content)
[Paper](https://github.com/SujitKRay/Listener_Classification_Public/blob/master/PersonalizinganAudioContentStreamCapstoneReport.pdf)

####Abstract

A legacy media organization with a nationwide audience recently released a mobile app in an attempt to capture audience share among listeners who access audio content through digital distribution channels.   The team signed an NDA with this organization, and will refer to this partner as the “Broadcaster” within our published materials.  

The Broadcaster’s app surfaces a stream of audio content to users.  Users can hear one of two types of content.

1.  News-- including the top of the hour newscasts, local and national news, and stories from the Broadcaster’s flagship news programs.

2.   Podcast-- including podcasts created by the Broadcaster and also independently created content like “Another Round” from Buzzfeed.  

In app, users can skip, thumbs-up, share, or search for content.  The Broadcaster has provided user data gathered by this app to our team.  In this paper, the team describes our work building a model that will allow the Broadcaster to determine, for any given user, at any given hour, whether the app should surface news or a podcast to the user.  


####Repo Overview
**Data provided for this project was received with an NDA and cannot be made publicly available.**

Information in the repo is described by folder below.

**ingest** - code for our initial cleaning/ merging process.

**modeling** - code and data for the steps in our modeling proces:

  * feature_weighting: code for using ExtraTrees and RandomForest Classifiers to weight the features

  * model_refinement-extracted_features: final modeling with feature extracted data

  * model_refinement-provided: final modeling with provided extracted data

  * validation: validation of the final models with hold-out data

**wrangle**: feature extraction from provided data


