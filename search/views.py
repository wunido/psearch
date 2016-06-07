from django.http import HttpResponse, HttpResponseRedirect
from elasticsearch import Elasticsearch
from django.shortcuts import render
from .forms import SearchForm
import urllib
import json
import chardet
import search.query

es = Elasticsearch([{
    'host': 'api.exiletools.com',
    'port': 80,
    'http_auth': 'apikey:DEVELOPMENT-Indexer'
}])


def mapping(request):
    """ API MAPPING """
    r = urllib.request.urlopen('http://api.exiletools.com/endpoints/mapping')
    rawdata = r.read()
    enc = chardet.detect(rawdata)
    data = rawdata.decode(enc['encoding'])
    mapping_all = data.split('\n')
    return render(request, 'search/mapping.html', {'mapping_all': mapping_all})


def leagues_test(request):
    """ Active leagues + API connection test """
    r = urllib.request.urlopen('http://api.exiletools.com/ladder?activeleagues=1')
    # leagues saved in dictionary type
    leagues = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    # checking connection to api
    response = es.search(
        search_type="count",
        index="index",
        body={
            "aggs": {
                "leagues": {
                    "terms": {
                        "field": "attributes.league",
                        }
                    }
                }
             }
        )
    if response['hits']['total'] > 0:
        exiletools = 'success %d total hits (exiletools)' % response['hits']['total']
    else:
        exiletools = 'error connecting exiletools api'
    return render(request, 'search/leagues.html', {
                    'leagues': sorted(leagues.values()),    # sort+returning list
                    'exiletools': exiletools})


def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            # search
            response = es.search(index="index", body=search.query.query(request))
            # getting back data
            item_data = convert_resp(response)
            hitsNumber = 'success %d total items' % response['hits']['total']
            return render(request, 'search/search_results.html', {'item_data': item_data, 'hitsNumber': hitsNumber,})
        else:
            return HttpResponse('Form Error')
    else:
        form = SearchForm()
    return render(request, 'search/index.html', {'form': form})


def convert_resp(request):
    """ converting json input into dict with chosen data """
    item_data = {}
    for hit in request['hits']['hits']:
        item_id = hit["_source"]["uuid"]
        full_name = hit["_source"]["info"]["fullName"]
        seller_account = hit["_source"]["shop"]["sellerAccount"]
        if 'chaosEquiv' in hit["_source"]["shop"].keys():
            chaos_equiv = hit["_source"]["shop"]["chaosEquiv"]
        else:
            chaos_equiv = 'no price'
        if 'modsTotal' in hit["_source"].keys():
            mods_total = hit["_source"]["modsTotal"]
        else:
            mods_total = None

        # adding results to item_data
        item_data[item_id] = {'full_name': full_name,
                              'chaos_equiv': chaos_equiv,
                              'seller_account': seller_account,
                              'mods_total': mods_total}
    return item_data


def test(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            s_type = request.POST.get('s_type')
            s_name = request.POST.get('s_name')
            return render(request, 'search/test.html', {'response': s_type, 'response2': s_name,
                                                        'query': search.query.query(request)})
    else:
        form = SearchForm()
    return render(request, 'search/index.html', {'form': form})
