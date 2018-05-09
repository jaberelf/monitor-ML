import csv
import requests
import sys



li=['http://localhost:9090', 'irate(process_cpu_seconds_total[1m])']

response = requests.get('{0}/api/v1/query'.format(li[0]),
        params={'query': li[1]})
results = response.json()['data']['result']

# Build a list of all labelnames used.
labelnames = set()
for result in results:
      labelnames.update(result['metric'].keys())

# Canonicalize
labelnames.discard('__name__')
labelnames = sorted(labelnames)

writer = csv.writer(sys.stdout)
# Write the header,
writer.writerow(['name', 'timestamp', 'value'] + labelnames)

# Write the rows.
for result in results:
    l = [result['metric'].get('__name__', '')] + result['value']
    for label in labelnames:
        l.append(result['metric'].get(label, ''))
    writer.writerow(l)
