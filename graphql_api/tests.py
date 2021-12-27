from graphene_django.utils.testing import GraphQLTestCase


class GraphQLArtistTest(GraphQLTestCase):
    fixtures = ["artists.json"]

    def test_retrieve_by_id(self):
        expected = {
            "data": {
                "artist": {
                    "id": "2",
                    "name": "Avril Lavigne",
                }
            }
        }
        res = self.query(
            """
            {
              artist(id: 2) {
                id
                name
              }
            }
            """
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, res.json())

    def test_create_artist(self):
        expected = {
            "data": {
                "createArtist": {
                    "ok": True,
                    "artist": {
                        "id": "4",
                        "name": "Ahmad kmal"
                    }
                }
            }
        }
        res = self.query(
            """
            mutation createArtist {
              createArtist(input: {
                name: "Ahmad kmal"
              }) {
                ok
                artist {
                  id
                  name
                }
              }
            }
            """
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(expected, res.json())

# Create your tests here.
