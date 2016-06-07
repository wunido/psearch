from django import forms
import search.data


class SearchForm(forms.Form):

    # attributes.league
    s_league = forms.ChoiceField(choices=search.data.leagues, label='League')

    # attributes.itemType / attributes.equipType
    s_type = forms.ChoiceField(choices=search.data.item, label='Item Type', required=False)

    # info.fullName / info.name / info.tokenized.fullName
    s_name = forms.CharField(label='Name', required=False)

    # propertiesPseudo.Armour.estimatedQ20.Armour
    s_armourMax = forms.IntegerField(label='Armour Max', required=False)
    s_armourMin = forms.IntegerField(label='Min', required=False)

    # propertiesPseudo.Armour.estimatedQ20.Evasion Rating
    s_evasionMax = forms.IntegerField(label='Evasion Max', required=False)
    s_evasionMin = forms.IntegerField(label='Min', required=False)

    # mods.Shield.explicit.+#% Chance to Block
    s_blockMax = forms.IntegerField(label='Block Max', required=False)
    s_blockMin = forms.IntegerField(label='Min', required=False)

    # propertiesPseudo.Armour.estimatedQ20.Energy Shield
    s_shieldMax = forms.IntegerField(label='Shield Max', required=False)
    s_shieldMin = forms.IntegerField(label='Min', required=False)

    # properties.Weapon.Total DPS
    s_dpsMax = forms.IntegerField(label='DPS Max', required=False)
    s_dpsMin = forms.IntegerField(label='Min', required=False)

    # properties.Weapon.Attacks per Second
    s_apsMax = forms.IntegerField(label='APS Max', required=False)
    s_apsMin = forms.IntegerField(label='Min', required=False)

    # properties.Weapon.Physical DPS
    s_pdpsMax = forms.IntegerField(label='PDPS Max', required=False)
    s_pdpsMin = forms.IntegerField(label='Min', required=False)

    # properties.Weapon.Elemental DPS
    s_edpsMax = forms.IntegerField(label='EDPS Max', required=False)
    s_edpsMin = forms.IntegerField(label='Min', required=False)

    # sockets.allSockets
    s_socketsMax = forms.IntegerField(label='Sockets Max', required=False)
    s_socketsMin = forms.IntegerField(label='Min', required=False)

    # sockets.largestLinkGroup
    s_linksMax = forms.IntegerField(label='Links Max', required=False)
    s_linksMin = forms.IntegerField(label='Min', required=False)

    # mods from files ( modsPseudo.txt / )
    s_mods = forms.ChoiceField(choices=search.data.mapping_tuple('modsPseudo'), label='Mods', required=False)
    s_modsMax = forms.IntegerField(label='Max', required=False)
    s_modsMin = forms.IntegerField(label='Min', required=False)