"""Geometry methods and functions

"""
import pytest

from cjio import models


@pytest.fixture(scope='module')
def data_geometry():
    vertices = [
        (0.0,1.0,0.0),
        (1.0,1.0,0.0),
        (2.0,1.0,0.0),
        (3.0,1.0,0.0),
        (4.0,1.0,0.0),
        (5.0,1.0,0.0)
    ]
    
    geometry = [{
        'type': 'CompositeSolid',
        'lod': 2,
        'boundaries': [
            [
                [
                    [[0, 0, 0, 0, 0]], [[1, 1, 1, 1]], [[2, 2, 2, 2]], [[3, 3, 3, 3]]
                ],
                [
                    [[2, 2, 2, 2]], [[3, 3, 3, 3]], [[4, 4, 4, 4]], [[5, 5, 5, 5]]
                ]
            ],
            [
                [[[0, 0, 0, 0, 0]], [[1, 1, 1, 1]], [[2, 2, 2, 2]], [[3, 3, 3, 3]]]
            ]
        ],
        'semantics': {
            'surfaces': [
                {
                    'type': 'WallSurface',
                    'slope': 33.4,
                    'children': [2],
                    'parent': 1
                },
                {
                    'type': 'RoofSurface',
                    'slope': 66.6,
                    'children': [0]
                },
                {
                    'type': 'Door',
                    'parent': 0,
                    'colour': 'blue'
                },
                {
                    'type': 'Door',
                    'parent': 0,
                    'colour': 'blue'
                }
            ],
            'values': [
                [[2, 1, 0, 3], [2, 1, 0, 3]],
                [None]
            ]
        }
    }]

    yield (geometry, vertices)


@pytest.fixture(scope='module')
def surfaces():
    srf = {
        0: {
            'type': 'WallSurface',
            'attributes': {
                'slope': 33.4,
            },
            'children': [2,3],
            'parent': 1,
            'surface_idx': [[0, 0, 2], [0, 1, 2]]
        },
        1: {
            'type': 'RoofSurface',
            'attributes': {
                'slope': 66.6,
            },
            'children': [0],
            'surface_idx': [[0, 0, 1], [0, 1, 1]]
        },
        2: {
            'type': 'Door',
            'attributes': {
                'colour': 'blue'
            },
            'parent': 0,
            'surface_idx': [[0, 0, 0], [0, 1, 0]]
        },
        3: {
            'type': 'Door',
            'attributes': {
                'colour': 'red'
            },
            'parent': 0,
            'surface_idx': [[0, 0, 3], [0, 1, 3]]
        }
    }
    yield srf


class TestGeometry:
    @pytest.mark.parametrize('type, boundary, result', [
        ('multipoint', [], []),
        ('multipoint',
         [2,4,5],
         [(2.0,1.0,0.0),(4.0,1.0,0.0),(5.0,1.0,0.0)]),
        ('multisurface',
         [[[2,4,5]]],
         [[[(2.0,1.0,0.0),(4.0,1.0,0.0),(5.0,1.0,0.0)]]]),
        ('multisurface',
         [[[2,4,5],[2,4,5]]],
         [[[(2.0,1.0,0.0),(4.0,1.0,0.0),(5.0,1.0,0.0)],[(2.0,1.0,0.0),(4.0,1.0,0.0),(5.0,1.0,0.0)]]]),
        ('solid',
         [
             [ [[0, 3, 2]], [[4, 5, 1]], [[0, 1, 5]] ],
             [ [[0, 3, 2]], [[4, 5, 1]], [[0, 1, 5]] ]
         ],
         [
             [ [[(0.0, 1.0, 0.0), (3.0, 1.0, 0.0), (2.0, 1.0, 0.0)]], [[(4.0, 1.0, 0.0), (5.0, 1.0, 0.0), (1.0, 1.0, 0.0)]],
               [[(0.0, 1.0, 0.0), (1.0, 1.0, 0.0), (5.0, 1.0, 0.0)]]],
             [ [[(0.0, 1.0, 0.0), (3.0, 1.0, 0.0), (2.0, 1.0, 0.0)]], [[(4.0, 1.0, 0.0), (5.0, 1.0, 0.0), (1.0, 1.0, 0.0)]],
               [[(0.0, 1.0, 0.0), (1.0, 1.0, 0.0), (5.0, 1.0, 0.0)]]]
         ]
         ),
        ('compositesolid',
         [
            [ [ [[0, 3, 2]], [[4, 5, 1]], [[0, 1, 5]] ] ],
            [ [ [[0, 3, 2]], [[4, 5, 1]], [[0, 1, 5]] ] ]
        ],
         [
             [[[[(0.0, 1.0, 0.0), (3.0, 1.0, 0.0), (2.0, 1.0, 0.0)]], [[(4.0, 1.0, 0.0), (5.0, 1.0, 0.0), (1.0, 1.0, 0.0)]],
               [[(0.0, 1.0, 0.0), (1.0, 1.0, 0.0), (5.0, 1.0, 0.0)]]]],
             [[[[(0.0, 1.0, 0.0), (3.0, 1.0, 0.0), (2.0, 1.0, 0.0)]], [[(4.0, 1.0, 0.0), (5.0, 1.0, 0.0), (1.0, 1.0, 0.0)]],
               [[(0.0, 1.0, 0.0), (1.0, 1.0, 0.0), (5.0, 1.0, 0.0)]]]]
         ]
         )
    ])
    def test_dereference_boundaries(self, data_geometry, type, boundary, result):
        vertices = data_geometry[1]
        geom = models.Geometry(type=type, boundaries=boundary, vertices=vertices)
        assert geom.boundaries == result


    def test_dereference_boundaries_wrong_type(self, data_geometry):
        geometry, vertices = data_geometry
        geometry[0]['type'] = 'CompositeSurface'
        with pytest.raises(TypeError) as e:
            models.Geometry(type=geometry[0]['type'],
                            boundaries=geometry[0]['boundaries'],
                            vertices=vertices)
            assert e == "Boundary definition does not correspond to MultiSurface or CompositeSurface"


    @pytest.mark.parametrize('values, surface_idx', [
        (
            None,
            dict()
        ),
        (
            [None],
            dict()
        ),
        (
            [[[0, 1, 2, None], [0, 1, 2, None]], [None]],
            {0: [[0, 0, 0],[0, 1, 0]],
             1: [[0, 0, 1],[0, 1, 1]],
             2: [[0, 0, 2],[0, 1, 2]]}
        )
    ])
    def test_index_surface_boundaries(self, values, surface_idx):
        res = models.Geometry._index_surface_boundaries(values)
        assert res == surface_idx


    @pytest.mark.parametrize('surface_idx, boundaries, surfaces', [
        (
                [],
                [],
                []
        ),
        (
                None,
                [],
                []
        ),
        (
                [[0]],  # 1. surface in a MultiSurface
                [[[0]], [[1]]],
                [[[0]]]
        ),
        (
                [[0], [1]],  # 1.,2. surface in a MultiSurface
                [[[0], [1]], [[2]]],
                [[[0], [1]], [[2]]]
        ),
        (
                [[0, 1], [0, 2], [1, 0]],
                # 2.,3. surface in exterior shell of Solid, 1. surface in interior shell of Solid
                [[[[0, 0]], [[0, 1]], [[0, 2]]], [[[1, 0]], [[1, 1]], [[1, 2]]]],
                [[[0, 1]], [[0, 2]], [[1, 0]]]
        ),
        (
                [[0, 0, 0], [0, 0, 2], [1, 0, 0]],
                # 1.,3. surf. of exterior of 1. Solid, 1. surface of exterior of 2. Solid
                [[[[[0, 0, 0]], [[0, 0, 1]], [[0, 0, 2]]]], [[[[1, 0, 0]], [[1, 0, 1]], [[1, 0, 2]]]]],
                [[[0, 0, 0]], [[0, 0, 2]], [[1, 0, 0]]]
        )
    ])
    def test_get_surface_boundaries(self, boundaries, surface_idx, surfaces):
        geom = models.Geometry()
        geom.boundaries = boundaries
        res = geom.get_surface_boundaries(surface_idx)
        assert res == surfaces

    def test_dereference_surfaces(self, data_geometry, surfaces):
        geometry, vertices = data_geometry
        geom = models.Geometry(type='CompositeSolid')
        geom.boundaries = geometry[0]['boundaries']
        geom.surfaces = geom._dereference_surfaces(geometry[0]['semantics'])
        result = {
            0: {
                'type': 'WallSurface',
                'attributes': {
                    'slope': 33.4,
                },
                'children': [2],
                'parent': 1,
                'surface_idx': [[0, 0, 2],[0, 1, 2]]
            },
            1: {
                'type': 'RoofSurface',
                'attributes': {
                    'slope': 66.6,
                },
                'children': [0],
                'surface_idx': [[0, 0, 1],[0, 1, 1]]
            },
            2: {
                'type': 'Door',
                'attributes': {
                    'colour': 'blue'
                },
                'parent': 0,
                'surface_idx': [[0, 0, 0],[0, 1, 0]]
            }
        }
        assert geom.surfaces == surfaces


    def test_get_surfaces(self, data_geometry, surfaces):
        geometry, vertices = data_geometry
        geom = models.Geometry(type='CompositeSolid')
        geom.boundaries = geometry[0]['boundaries']
        # geom.surfaces = {
        #     0: {
        #         'type': 'WallSurface',
        #         'attributes': {
        #             'slope': 33.4,
        #         },
        #         'children': [2],
        #         'parent': 1,
        #         'surface_idx': [[0, 0, 2],[0, 1, 2]]
        #     },
        #     1: {
        #         'type': 'RoofSurface',
        #         'attributes': {
        #             'slope': 66.6,
        #         },
        #         'children': [0],
        #         'surface_idx': [[0, 0, 1],[0, 1, 1]]
        #     },
        #     2: {
        #         'type': 'Door',
        #         'attributes': {
        #             'colour': 'blue'
        #         },
        #         'parent': 0,
        #         'surface_idx': [[0, 0, 0],[0, 1, 0]]
        #     },
        #     3: {
        #         'type': 'Door',
        #         'attributes': {
        #             'colour': 'red'
        #         },
        #         'parent': 0,
        #         'surface_idx': [[0, 0, 3], [0, 1, 3]]
        #     }
        # }
        geom.surfaces = surfaces
        roof = list(geom.get_surfaces('roofsurface'))
        wall = list(geom.get_surfaces('wallsurface'))
        door = list(geom.get_surfaces('door'))
        assert roof == [{
            'type': 'RoofSurface',
            'attributes': {
                'slope': 66.6,
            },
            'children': [0],
            'surface_idx': [[0, 0, 1], [0, 1, 1]]
        }]
        assert wall == [{
            'type': 'WallSurface',
            'attributes': {
                'slope': 33.4,
            },
            'children': [2],
            'parent': 1,
            'surface_idx': [[0, 0, 2], [0, 1, 2]]
        }]
        assert door == [
            {
                'type': 'Door',
                'attributes': {
                    'colour': 'blue'
                },
                'parent': 0,
                'surface_idx': [[0, 0, 0], [0, 1, 0]]
            },
            {
                'type': 'Door',
                'attributes': {
                    'colour': 'red'
                },
                'parent': 0,
                'surface_idx': [[0, 0, 3], [0, 1, 3]]
            }
        ]

    def test_get_surface_children(self, surfaces):
        geom = models.Geometry(type='CompositeSolid')
        geom.surfaces = surfaces
        res = {
            2: {
            'type': 'Door',
            'attributes': {
                'colour': 'blue'
            },
            'parent': 0,
            'surface_idx': [[0, 0, 0], [0, 1, 0]]
            },
            3: {
                'type': 'Door',
                'attributes': {
                    'colour': 'red'
                },
                'parent': 0,
                'surface_idx': [[0, 0, 3], [0, 1, 3]]
            }
        }
        wall = {
            0: {
                'type': 'WallSurface',
                'attributes': {
                    'slope': 33.4,
                },
                'children': [2, 3],
                'parent': 1,
                'surface_idx': [[0, 0, 2], [0, 1, 2]]
            }
        }
        surface = wall[0]
        if 'children' in surface:
            children = {j:geom.surfaces[j] for j in surface['children']}
        assert children == res

    def test_get_surface_parent(self, data_geometry):
        # TODO BD: get surface parent
        pytest.xfail("not implemented")

class TestGeometryIntegration:
    """Integration tests for operations on Geometry objects

    These tests mainly meant to mimic user workflow and test concepts
    """
    def test_get_surface_boundaries(self, data_geometry):
        """Test how to get the boundaries (geometry) of semantic surfaces"""
        geometry, vertices = data_geometry
        geom = models.Geometry(type=geometry[0]['type'],
                               lod=geometry[0]['lod'],
                               boundaries=geometry[0]['boundaries'],
                               semantics_obj=geometry[0]['semantics'],
                               vertices=vertices)
        roofsurfaces = geom.get_surfaces('roofsurface')
        rsrf_bndry = [geom.get_surface_boundaries(rsrf['surface_idx'])
                      for rsrf in roofsurfaces]
        roof_geom = [
            [
                [[(1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 0.0)]],
                [[(3.0, 1.0, 0.0), (3.0, 1.0, 0.0), (3.0, 1.0, 0.0), (3.0, 1.0, 0.0)]]
            ]
        ]
        assert rsrf_bndry == roof_geom

        doorsurfaces = geom.get_surfaces('door')
        dsrf_bndry = [geom.get_surface_boundaries(dsrf['surface_idx'])
                      for dsrf in doorsurfaces]
        door_geom = [
            [
                [[(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)]],
                [[(2.0, 1.0, 0.0), (2.0, 1.0, 0.0), (2.0, 1.0, 0.0), (2.0, 1.0, 0.0)]]
            ],
            [
                [[(3.0, 1.0, 0.0), (3.0, 1.0, 0.0), (3.0, 1.0, 0.0), (3.0, 1.0, 0.0)]],
                [[(5.0, 1.0, 0.0), (5.0, 1.0, 0.0), (5.0, 1.0, 0.0), (5.0, 1.0, 0.0)]]
            ]
        ]
        assert dsrf_bndry == door_geom

    def test_set_surface_attributes(self, data_geometry):
        """Test how to set attributes on semantic surfaces"""
        geometry, vertices = data_geometry
        geom = models.Geometry(type=geometry[0]['type'],
                               lod=geometry[0]['lod'],
                               boundaries=geometry[0]['boundaries'],
                               semantics_obj=geometry[0]['semantics'],
                               vertices=vertices)
        roofsurfaces = geom.get_surfaces('roofsurface')
        for i, rsrf in roofsurfaces.items():
            if 'attributes' in rsrf.keys():
                rsrf['attributes']['colour'] = 'red'
            else:
                rsrf['attributes'] = {}
                rsrf['attributes']['colour'] = 'red'
            # overwrite the surface directly in the Geometry object
            geom.surfaces[i] = rsrf
        roofsurfaces_new = geom.get_surfaces('roofsurface')
        for i,rsrf in roofsurfaces_new.items():
            assert rsrf['attributes']['colour'] == 'red'

    def test_split_semantics(self, data_geometry):
        """Test how to split surfaces by creating new semantics"""
        geometry, vertices = data_geometry
        geom = models.Geometry(type=geometry[0]['type'],
                               lod=geometry[0]['lod'],
                               boundaries=geometry[0]['boundaries'],
                               semantics_obj=geometry[0]['semantics'],
                               vertices=vertices)
        roofsurfaces = geom.get_surfaces('roofsurface')
        max_id = max(geom.surfaces.keys()) # surface keys are always integers
        old_ids = []
        for i,rsrf in roofsurfaces.items():
            old_ids.append(i)
            boundaries = geom.get_surface_boundaries(rsrf['surface_idx'])
            for i,boundary_geometry in enumerate(boundaries):
                surface_index = rsrf['surface_idx'][i]
                for multisurface in boundary_geometry:
                    # Do any geometry operation here
                    x,y,z = multisurface[0]
                    if x < 2.0:
                        new_srf = {
                            'type': rsrf['type'],
                            'children': rsrf['children'], # it should be checked if surface has children
                            'surface_idx': surface_index
                        }
                        if 'attributes' in rsrf.keys():
                            rsrf['attributes']['orientation'] = 'north'
                        else:
                            rsrf['attributes'] = {}
                            rsrf['attributes']['orientation'] = 'north'
                        new_srf['attributes'] = rsrf['attributes']
                    else:
                        new_srf = {
                            'type': rsrf['type'],
                            'children': rsrf['children'],
                            'surface_idx': surface_index
                        }
                        if 'attributes' in rsrf.keys():
                            rsrf['attributes']['orientation'] = 'south'
                        else:
                            rsrf['attributes'] = {}
                            rsrf['attributes']['orientation'] = 'south'
                        new_srf['attributes'] = rsrf['attributes']
                    if i in geom.surfaces.keys():
                        del geom.surfaces[i]
                    max_id = max_id + 1
                    geom.surfaces[max_id] = new_srf

        roofsurfaces_new = geom.get_surfaces('roofsurface')
        for i,rsrf in roofsurfaces_new.items():
            assert i not in old_ids
            assert 'orientation' in rsrf['attributes'].keys()




