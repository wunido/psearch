import ast

def query(request):
    s_name = request.POST.get('s_name')
    """
    if s_name:
        name_part =  '"query": {'\
                       '"query_string": {'\
                            '"default_field": "info.fullName",'\
                                '"query": s_name'\
                            '}'
    """
    query_full = {
                "query": {
                    "filtered": {
                        "filter": {
                            "bool": {
                                "must": [
                                        query_filters(request)
                                ]
                            }
                        }
                    }
                },
                "size": 100
                }
    return query_full


def query_filters(request):
    s_name = request.POST.get('s_name')
    s_type = request.POST.get('s_type')
    s_league = request.POST.get('s_league')
    q_dict = []
    q_dict.append('{"term": {"attributes.league":"%s"}},' % s_league)
    if s_type:
        for i_type, name in ast.literal_eval(s_type).items():
            string = '{"term": {"%s":"%s"}},' % (i_type, name)
            q_dict.append(string)

    s_armourMax = request.POST.get('s_armourMax')
    s_armourMin = request.POST.get('s_armourMin')
    if s_armourMax or s_armourMin:
        q_dict.append(query_part(s_armourMax, s_armourMin, 'propertiesPseudo.Armour.estimatedQ20.Armour'))

    s_evasionMax = request.POST.get('s_evasionMax')
    s_evasionMin = request.POST.get('s_evasionMin')
    if s_evasionMax or s_evasionMin:
        q_dict.append(query_part(s_evasionMax, s_evasionMin, 'propertiesPseudo.Armour.estimatedQ20.Evasion Rating'))

    s_blockMax = request.POST.get('s_blockMax')
    s_blockMin = request.POST.get('s_blockMin')
    if s_blockMax or s_blockMin:
        q_dict.append(query_part(s_blockMax, s_blockMin, 'mods.Shield.explicit.+#% Chance to Block'))

    s_shieldMax = request.POST.get('s_shieldMax')
    s_shieldMin = request.POST.get('s_shieldMin')
    if s_shieldMax or s_shieldMin:
        q_dict.append(query_part(s_shieldMax, s_shieldMin, 'propertiesPseudo.Armour.estimatedQ20.Energy Shield'))

    s_dpsMax = request.POST.get('s_dpsMax')
    s_dpsMin = request.POST.get('s_dpsMin')
    if s_dpsMax or s_dpsMin:
        q_dict.append(query_part(s_dpsMax, s_dpsMin, 'properties.Weapon.Total DPS'))

    s_apsMax = request.POST.get('s_apsMax')
    s_apsMin = request.POST.get('s_apsMin')
    if s_apsMax or s_apsMin:
        q_dict.append(query_part(s_apsMax, s_apsMin, 'properties.Weapon.Attacks per Second'))

    s_pdpsMax = request.POST.get('s_pdpsMax')
    s_pdpsMin = request.POST.get('s_pdpsMin')
    if s_pdpsMax or s_pdpsMin:
        q_dict.append(query_part(s_pdpsMax, s_pdpsMin, 'properties.Weapon.Physical DPS'))

    s_edpsMax = request.POST.get('s_edpsMax')
    s_edpsMin = request.POST.get('s_edpsMin')
    if s_edpsMax or s_edpsMin:
        q_dict.append(query_part(s_edpsMax, s_edpsMin, 'properties.Weapon.Elemental DPS'))

    s_socketsMax = request.POST.get('s_socketsMax')
    s_socketsMin = request.POST.get('s_socketsMin')
    if s_socketsMax or s_socketsMin:
        q_dict.append(query_part(s_socketsMax, s_socketsMin, 'sockets.allSockets'))

    s_linksMax = request.POST.get('s_linksMax')
    s_linksMin = request.POST.get('s_linksMin')
    if s_linksMax or s_linksMin:
        q_dict.append(query_part(s_linksMax, s_linksMin, 'sockets.largestLinkGroup'))

    s_mods = request.POST.get('s_mods')
    s_modsMax = request.POST.get('s_modsMax')
    s_modsMin = request.POST.get('s_modsMin')
    if s_mods:
        q_dict.append(query_part(s_modsMax, s_modsMin, s_mods))

    #if s_name:
        #q_dict.append('{"term": {"info.tokenized.fullName":"%s"}},' % s_name)

    str_query = ''.join(q_dict)
    query_full = ast.literal_eval(str_query)
    return query_full


def query_part(max_, min_, term):
    if max_ and min_:
        qDict = '{"range": {"%s":{"gte":"%s","lte":"%s"}}},' % (term, min_, max_)
    elif min_:
        qDict = '{"range": {"%s":{"lte":"%s"}}},' % (term, min_)
    else:
        qDict = '{"range": {"%s":{"gte":"%s"}}},' % (term, max_)
    return qDict