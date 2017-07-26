import copy

from accounts.models import *
from commons.models.commons import Location, Skill, Interest

def update_locations(locations, instance):
    def location_get_or_create(location):
        loc = copy.copy(location)
        loc.pop('distance', None)
        loc['title'] = loc.get('title', '')
        new_location, _ = Location.objects.get_or_create(**loc)
        return new_location

    candidate_locations_current = instance.locations.filter(candidatelocation__current=True)
    candidate_locations_potential = set(instance.locations.filter(candidatelocation__current=False))

    locations_current   = locations.get('current', {})
    locations_potential = locations.get('potential', [])

    if locations_current:
        if not candidate_locations_current.filter(
                lat=locations_current['lat'],
                lon=locations_current['lon']).exists():
            CandidateLocation.objects.filter(candidate__id=instance.id, current=True).delete()
            location = location_get_or_create(locations_current)
            CandidateLocation.objects.create(candidate=instance,
                                             location=location,
                                             current=True)

    if locations_potential:
        potential_instances = set()
        for l in locations_potential:
            potential_instances.add(location_get_or_create(l))

        potential_to_delete = candidate_locations_potential - potential_instances
        potential_to_add = potential_instances - candidate_locations_potential

        if potential_to_delete:
            CandidateLocation.objects.filter(candidate__id=instance.id,
                                             location__in=potential_to_delete,
                                             current=False).delete()


