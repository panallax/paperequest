import requests
import json
from config import SCOPUS_API_KEY

def build_citation(id):
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
          + id
          + "?field=authors,title,publicationName,volume,issueIdentifier,"
          + "prism:pageRange,coverDate,article-number,doi,citedby-count,prism:aggregationType")
    resp = requests.get(url,
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': SCOPUS_API_KEY})
    results = json.loads(resp.text.encode('utf-8'))

    fstring = '{authors}, {title}, {journal}, {volume}, {articlenum}, ({date}). {doi} (cited {cites} times).\n'
    return fstring.format(authors=', '.join([au['ce:indexed-name'] for au in results['abstracts-retrieval-response']['authors']['author']]),
                          title=results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8'),
                          journal=results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8'),
                          volume=results['abstracts-retrieval-response']['coredata']['prism:volume'].encode('utf-8'),
                          articlenum=(results['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or
                              results['abstracts-retrieval-response']['coredata'].get('article-number')).encode('utf-8'),
                          date=results['abstracts-retrieval-response']['coredata']['prism:coverDate'].encode('utf-8'),
                          doi='doi:' + str(results['abstracts-retrieval-response']['coredata']['prism:doi'].encode('utf-8')),
                          cites=int(results['abstracts-retrieval-response']['coredata']['citedby-count'].encode('utf-8')))