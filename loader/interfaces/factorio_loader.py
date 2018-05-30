
from BeautifulSoup import BeautifulSoup
import requests

FACTORIO_URLS = {
	"stable": "https://factorio.com/download-headless",
	"experimental": "https://factorio.com/download-headless/experimental"
}

BASE = "https://www.factorio.com"

class loader_factorio:

	def load(self, channel, last_build):
		builds = []

		url = FACTORIO_URLS[channel]
		print "Downloading %s" % channel
		data = requests.get(url)
		soup = BeautifulSoup(data.content)

		releases = soup.find("div", {"class": "container"})
		for ul in releases.findAll("ul"):
			element = ul.find("li").find("a", href=True)
			if not element:
				continue

			version = element["href"].split("/")[2]

			download = "%s%s" % (BASE, element["href"])
			print version, download
			builds.append({
				"version": version,
				"size": None,
				"checksum": None,
				"url": download,
				"jar_name": "factorio." + version,
				"jar_ext": "tar.gz".
				"build": int(version.replace(".", ""))
			})

		return builds
