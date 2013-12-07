import sys
import os
import process
import utilities


def buildFeatures(strVal):
	utils = utilities.Utilities()
	lines = strVal.split('\n')
	features = []

	for line in lines:
		# split into words
		wordTags = line.split()

		for i in range(0, len(wordTags)):

			# get words

				newFeature = Feature(wordTags[i], prevWordTag, prev2WordTag, nextWordTag, next2WordTag)

				features.append(newFeature)

		return features

