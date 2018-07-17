
import urllib2
import json
import re
import sys
import math


def get_json(endpoint):
	url = "%s/api/json?pretty=true" % (endpoint if endpoint[-1] != "/" else endpoint[0:-1])
	return json.loads(urllib2.urlopen(url).read())


def get_version_from_data(data):
	if isinstance(data, list):
		for item in data:
			result = get_version_from_data(item)
			if result:
				return result
	elif isinstance(data, dict):
		for key, item in data.iteritems():
			

class loader_jenkins:

	def create_build_data(self, build):
		build_data = get_json(build["url"])
		if build_data["result"].lower() != "success":
			return None



	def load(self, channel, last_build):
		builds = []

		data = get_json(channel["url"])
		need_build = math.floor(len(data["builds"]) / 20)
		
		if need_build <= 0:
			return builds

		for i, build in enumerate(data["builds"]):
			if build["number"] <= last_build:
				continue

			build = self.create_build_data(build)
			if build:
				builds.append(build)

		return builds
