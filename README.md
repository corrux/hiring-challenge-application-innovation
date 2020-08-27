# corrux Application &amp; Innovation Team Hiring Challenge
First, thanks for your interest in corrux! We put together this coding challenge to give you a chance to show us your
skills by developing an algorithm that works with geotemporal data.

## Problem description
In this problem we make use of two concepts: *Locations* and *Sites*. A *Location* is the combination of a point in
time and a position in space, a *Site* is the combination of an interval in time and an area in space.

### Locations
We represent a *Location* as a JSON object with two attributes: `datetime` and `position`. `datetime` follows
[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations) for its time representation,
while `position` adheres to [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) to represent a point in space. Here is an
example:
```json
{
    "datetime": "2020-08-27T13:53:59Z",
    "position": {
        "type": "Point",
        "coordinates": [11.5756, 48.1371]
    }
}
```

### Sites
We represent a *Site* as a JSON object with three attributes: `start_datetime`, `end_datetime`, `geofence`. `start_datetime`
and `end_datetime` again follow ISO 8601 and represent the start and end of the time interval respectively, where
`start_datetime` is included in the interval and `end_datetime` is not. `geofence` also follows GeoJSON, but it represents
a Polygon in space that describes the area that belongs to the site. Here is an example:
```json
{
    "start_datetime": "2020-08-01T00:00:00Z",
    "end_datetime": "2020-09-01T00:00:00Z",
    "geofence": {
        "type": "Polygon",
        "coordinates": [
            [
                [11.5748, 48.1372],
                [11.5758, 48.1370],
                [11.5764, 48.1372],
                [11.5749, 48.1375],
                [11.5748, 48.1372]
            ]
        ]
    }
}
```

### Relationship Of Locations And Sites
For a *Location* **l** and a *Site* **S**, we say **S** *contains* **l** if and only if the time of **l** is in the time 
interval of **S** and the position of **l** is in the geofence of **S**.

## Your Task
Find all locations that are affected by a modification of the definition of a site. That is, which locations are no
longer contained by it and which locations have been added because of the modification?

### Included files
- `locations.json`: The dataset of locations to evaluate your algorithm on
- `site_old.json`: The old definition of the site
- `site_new.json`: The new definition of the site

## Bonus Round
- Create a visualization of your algorithm! Think about how to show the following:
    * The way it decides which locations are part of the solution
    * Visualizing time and space
- Can you find a streaming solution? Assuming disk space is infinite, a streaming solution must be able to read
    locations from an infinitely large input file and write the solution to an infinitely large output file, but it can
    only use a finite amount of RAM.
