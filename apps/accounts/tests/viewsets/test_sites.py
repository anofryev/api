import random
from apps.main.tests import APITestCase
from ...factories import SiteFactory


class SiteTest(APITestCase):
    def test_that_sites_available_via_api(self):
        count = random.randint(1, 10)

        for _index in range(count):
            SiteFactory.create()

        resp = self.client.get('/api/v1/auth/sites/')
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), count)
