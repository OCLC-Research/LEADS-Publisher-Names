# Updated Research Statement (proposed by Jean)

To achieve the long-term goal of making library data more machine-understandable, publisher name strings must be associated with persistent entities. In today's technical environment, the result would be expressible as linked data. 

This is a problem that OCLC must solve to improve its metadata-management production processes. But OCLC's need is not unique. Stakeholders throughout the library community need a better representation of publishers, as they work to improve the user's experience with library search and discovery systems.

A complete technical solution will address the following requirements: 

1) Automatically generate entity descriptions for publishers, using MARC bibliographic data as the primary data source. The solution should be generic and scalable.
2) Identify key attributes of the description, such as the preferred or most dominant name and its spelling variations; names of related entities such as imprints; authors and other creators; subjects; genres; and physical formats associated with the entity.
3) Ideally, a model would be also defined for the publisher entity, and the description would be expressed as instance data for the model.
4) Use the entity description to disambiguate publisher name strings in incoming bibliographic records or other documents.
5) Associate descriptions with unique URIs.

Milestones
This is the full problem statement. During our time together, we will focus on Steps 1 and 2. Step 2 has a lot of detail, and we may decide that some of the steps are only of incremental value. So we should spend the last part of the internship on the evaluation.

1) Prepare gold and test data
	1) Devon and I can help you with this step using the output from the Publisher Name Authority File project.
	
2) Automatically generate publisher entities
	1) Explore how the ISBN prefixes could be used to identify possible clusters of publisher entities. 
	2) Identify other valuable sources of information, such as subjects, authors, dates, etc.
	3) Experiment with other clustering methods: word vectors, tf-idf, bag-of-words.
	4) Balance computational efficiency with accuracy and aim for a more scalable solution in a later version.

5) Evaluate cluster precision and recall with respect to the gold data
	1) Create a model of the publisher entity and generate descriptions as instance data
	2) Test by assigning text strings from incoming data to the appropriate entity description
