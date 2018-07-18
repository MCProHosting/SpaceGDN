import urllib, urllib2, json, datetime, re
from distutils.version import StrictVersion

class loader_mojang:

    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'

    def get_json(self):
        response = urllib2.urlopen(self.url)
        return json.loads(response.read())

    def to_timestamp(self, dt, epoch=datetime.datetime(1970,1,1)):
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 

    def load(self, channel, last_build):
        data = self.get_json()

        builds = []
        for build in data['versions']:
            if build['type'] != channel['name']:
                continue

            res = json.loads(urllib2.urlopen(build["url"]).read())
            minecraft_version = StrictVersion(res["id"])

            if minecraft_version > StrictVersion("1.7.8"):
                time = datetime.datetime.strptime(re.sub(r'\+[0-9]{2}:[0-9]{2}$', '', build['releaseTime']), '%Y-%m-%dT%H:%M:%S')
                build_number = int(self.to_timestamp(time))

                builds.append({
                    'version': build['id'],
                    'size': None,
                    'checksum': None,
                    'url': res["downloads"]["server"]["url"],
                    'jar_name': 'minecraft_server.' + build['id'],
                    'build': build_number
                })

        return builds
