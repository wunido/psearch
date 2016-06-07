from elasticsearch import Elasticsearch

es = Elasticsearch([{
    'host': 'api.exiletools.com',
    'port': 80,
    'http_auth': 'apikey:DEVELOPMENT-Indexer'
}])
