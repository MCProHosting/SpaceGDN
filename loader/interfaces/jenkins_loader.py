
import urllib2
import json
import re
import sys
import math


def get_json(endpoint):
	url = "%s/api/json?pretty=true" % (endpoint if endpoint[-1] != "/" else endpoint[0:-1])
	opener = urllib2.build_opener()
	opener.addheaders = [("User-Agent", "Mozilla/5.0")]

	return json.loads(opener.open(url).read())


def get_version_from_data(data):
	if isinstance(data, list):
		for item in data:
			result = get_version_from_data(item)
			if result:
				return result
	elif isinstance(data, dict):
		for key, item in data.iteritems():
			result = get_version_from_data(item)
			if result:
				return result
	elif isinstance(data, (basestring, str)):
		m = re.search(r"[0-9].[0-9].[0-9]{1,2}(-R[0-9].[0-9])?", data)
		if m:
			return m.group(0)
	return None


class loader_jenkins:

	def create_build_data(self, build):
		build_data = get_json(build["url"])
		if build_data["result"].lower() != "success":
			return None

		artifact_url = None
		if len(build_data["artifacts"]) > 0:
			artifact_url = build_data["artifacts"][0].get("relativePath", None)

		return {
			"build": build_data["number"],
			"version": get_version_from_data(build_data),
			"url": "%s/%s" % (
				build["url"] if build["url"][-1] != "/" else build["url"][0:-1],
				artifact_url
			)
		}


	def load(self, channel, last_build):
		builds = []

		data = get_json(channel["url"])

		for i, build in enumerate(data["builds"]):
			if build["number"] <= last_build:
				continue

			build = self.create_build_data(build)
			build["config"] = channel["config"]
			if build:
				builds.append(build)

		return builds
