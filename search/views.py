from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
import urllib
import json
import chardet
import search.query
import eslogin
import search.data


def mapping(request):
    """ API MAPPING """
    r = urllib.request.urlopen('http://api.exiletools.com/endpoints/mapping')
    rawdata = r.read()
    enc = chardet.detect(rawdata)
    data = rawdata.decode(enc['encoding'])
    mapping_all = data.split('\n')
    return render(request, 'search/mapping.html', {'mapping_all': mapping_all})


def leagues_test(request):
    """ Active leagues + API connection test / NEED TO REBUILD """
    r = urllib.request.urlopen('http://api.exiletools.com/ladder?activeleagues=1')
    # leagues saved in dictionary type
    leagues = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    # checking connection to api
    response = eslogin.es.search(
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
            response = eslogin.es.search(index="index", body=search.query.Query(request).query_finished())
            # getting back data
            item_data = search.data.convert_resp(response)
            results_nr = 'success %d total items' % response['hits']['total']
            return render(request, 'search/search_results.html', {'item_data': item_data, 'hitsNumber': results_nr, })
        else:
            return HttpResponse('Form Error')
    else:
        form = SearchForm()
    return render(request, 'search/index.html', {'form': form})


def test(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            s_type = request.POST.get('s_type')
            s_name = request.POST.get('s_name')
            return render(request, 'search/test.html', {'response': s_type, 'response2': s_name,
                                                        'query': search.query.Query(request).query_finished()})
    else:
        form = SearchForm()
    return render(request, 'search/index.html', {'form': form})
