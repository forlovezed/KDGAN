from nltk.corpus import wordnet

import string
import calendar
import pycountry

def get_spatial():
  spatial_noun = set()
  for country in pycountry.countries:
    if hasattr(country, 'alpha_2'):
      spatial_noun.add(country.alpha_2.lower())
    if hasattr(country, 'alpha_3'):
      spatial_noun.add(country.alpha_3.lower())
    if hasattr(country, 'name'):
      spatial_noun.add(country.name.lower())
    if hasattr(country, 'official_name'):
      spatial_noun.add(country.official_name.lower())
  for country in pycountry.historic_countries:
    if hasattr(country, 'alpha_3'):
      spatial_noun.add(country.alpha_3.lower())
    if hasattr(country, 'alpha_4'):
      spatial_noun.add(country.alpha_4.lower())
    if hasattr(country, 'name'):
      spatial_noun.add(country.name.lower())
  for subdivision in pycountry.subdivisions:
    if hasattr(subdivision, 'name'):
      spatial_noun.add(subdivision.name.lower())
    if hasattr(subdivision, 'code'):
      spatial_noun.add(subdivision.code.lower())
  return spatial_noun

def get_temporal():
  temporal_noun = set()
  for month in range(1, 13):
    temporal_noun.add(calendar.month_name[month].lower())
    temporal_noun.add(calendar.month_abbr[month].lower())
  for day in range(0, 7):
    temporal_noun.add(calendar.day_name[day].lower())
    temporal_noun.add(calendar.day_abbr[day].lower())
  return temporal_noun

v_char = string.ascii_lowercase + '-'
spatial_noun = get_spatial()
temporal_noun = get_temporal()
def is_valid(noun):
  if any(c not in v_char for c in noun):
    return False
  if noun in spatial_noun:
    return False
  if noun in temporal_noun:
    return False
  synsets = wordnet.synsets(noun)
  for synset in synsets:
    if synset.name().split('.')[1] != 'n':
      return False
  return True

def main():
  unamb_nouns = set()
  wn_nouns = {synset.name().split('.')[0] for synset in wordnet.all_synsets('n')}
  for noun in wn_nouns:
    # print('%s:%s' % (noun, is_valid(noun)))
    if is_valid(noun):
      unamb_nouns.add(noun)
  print('%d->%d' % (len(wn_nouns), len(unamb_nouns)))

if __name__ == '__main__':
  main()
