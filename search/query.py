import ast


class Query:
    def __init__(self, response):
        self.response = response

    def query_finished(self):
        """ Query builder """
        # s_name = request.POST.get('s_name')
        """  work in progress
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
                                            self.query_filters(self.response)
                                    ]
                                }
                            }
                        }
                    },
                    "size": 100
                    }
        return query_full

    def query_filters(self, request):
        """ Query filters / need to rebuild """
        # s_name = request.POST.get('s_name')
        s_type = request.POST.get('s_type')
        s_league = request.POST.get('s_league')
        q_list = []

        q_list.append('{"term": {"attributes.league":"%s"}},' % s_league)

        # if s_name:
        # q_list.append('{"term": {"info.tokenized.fullName":"%s"}},' % s_name)

        if s_type:
            for i_type, name in ast.literal_eval(s_type).items():
                string = '{"term": {"%s":"%s"}},' % (i_type, name)
                q_list.append(string)

        s_armourMax = request.POST.get('s_armourMax')
        s_armourMin = request.POST.get('s_armourMin')
        if s_armourMax or s_armourMin:
            q_list.append(self.query_range(s_armourMax, s_armourMin, 'propertiesPseudo.Armour.estimatedQ20.Armour'))

        s_evasionMax = request.POST.get('s_evasionMax')
        s_evasionMin = request.POST.get('s_evasionMin')
        if s_evasionMax or s_evasionMin:
            q_list.append(self.query_range(s_evasionMax, s_evasionMin, 'propertiesPseudo.Armour.estimatedQ20.Evasion Rating'))

        s_blockMax = request.POST.get('s_blockMax')
        s_blockMin = request.POST.get('s_blockMin')
        if s_blockMax or s_blockMin:
            q_list.append(self.query_range(s_blockMax, s_blockMin, 'mods.Shield.explicit.+#% Chance to Block'))

        s_shieldMax = request.POST.get('s_shieldMax')
        s_shieldMin = request.POST.get('s_shieldMin')
        if s_shieldMax or s_shieldMin:
            q_list.append(self.query_range(s_shieldMax, s_shieldMin, 'propertiesPseudo.Armour.estimatedQ20.Energy Shield'))

        s_dpsMax = request.POST.get('s_dpsMax')
        s_dpsMin = request.POST.get('s_dpsMin')
        if s_dpsMax or s_dpsMin:
            q_list.append(self.query_range(s_dpsMax, s_dpsMin, 'properties.Weapon.Total DPS'))

        s_apsMax = request.POST.get('s_apsMax')
        s_apsMin = request.POST.get('s_apsMin')
        if s_apsMax or s_apsMin:
            q_list.append(self.query_range(s_apsMax, s_apsMin, 'properties.Weapon.Attacks per Second'))

        s_pdpsMax = request.POST.get('s_pdpsMax')
        s_pdpsMin = request.POST.get('s_pdpsMin')
        if s_pdpsMax or s_pdpsMin:
            q_list.append(self.query_range(s_pdpsMax, s_pdpsMin, 'properties.Weapon.Physical DPS'))

        s_edpsMax = request.POST.get('s_edpsMax')
        s_edpsMin = request.POST.get('s_edpsMin')
        if s_edpsMax or s_edpsMin:
            q_list.append(self.query_range(s_edpsMax, s_edpsMin, 'properties.Weapon.Elemental DPS'))

        s_socketsMax = request.POST.get('s_socketsMax')
        s_socketsMin = request.POST.get('s_socketsMin')
        if s_socketsMax or s_socketsMin:
            q_list.append(self.query_range(s_socketsMax, s_socketsMin, 'sockets.allSockets'))

        s_linksMax = request.POST.get('s_linksMax')
        s_linksMin = request.POST.get('s_linksMin')
        if s_linksMax or s_linksMin:
            q_list.append(self.query_range(s_linksMax, s_linksMin, 'sockets.largestLinkGroup'))

        s_mods = request.POST.get('s_mods')
        s_modsMax = request.POST.get('s_modsMax')
        s_modsMin = request.POST.get('s_modsMin')
        if s_mods:
            q_list.append(self.query_range(s_modsMax, s_modsMin, s_mods))

        str_query = ''.join(q_list)
        query_full = ast.literal_eval(str_query)
        return query_full

    def query_range(self, max_, min_, term):
        """ Returns range filters """
        if max_ and min_:
            q_str = '{"range": {"%s":{"gte":"%s","lte":"%s"}}},' % (term, min_, max_)
        elif max_:
            q_str = '{"range": {"%s":{"lte":"%s"}}},' % (term, max_)
        else:
            q_str = '{"range": {"%s":{"gte":"%s"}}},' % (term, min_)
        return q_str
