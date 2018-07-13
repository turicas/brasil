import json
from urllib.request import urlopen
from urllib.parse import urlencode, urljoin


class BrasilIO:

    api_url = 'https://brasil.io/api/'

    def __init__(self, api_url=None, page_size=1000):
        if api_url is not None:
            self.api_url = api_url
        self.page_size = page_size

    def _create_url(self, endpoint, params=None, *args):
        url = urljoin(self.api_url, endpoint)
        if params is not None:
            url = url + '?' + urlencode(params)
        return url

    def _get_json(self, url, timeout=5):
        return json.load(urlopen(url, timeout=timeout))

    def _paginate(self, endpoint, params=None, timeout=None):
        if params is None:
            params = {}
        if 'page_size' not in params:
            params['page_size'] = self.page_size
        url = self._create_url(endpoint, params)

        finished = False
        while not finished:
            response = self._get_json(url, timeout=timeout)
            for row in response['results']:
                yield row
            next_page = response.get('next', None)
            if next_page is not None:
                url = next_page
            else:
                finished = True

    def datasets(self, *args, **kwargs):
        """Get list of datasets"""

        return self._paginate('datasets', params=kwargs)

    def dataset(self, slug):
        """Get full dataset information"""

        return self._get_json(self._create_url('dataset/' + slug))

    def dataset_table_data(self, slug, tablename, *args, **kwargs):
        """Get data for a specific table in a dataset

        You can pass filters, like:
            `dataset_data('some-dataset', some_field='some value')`
        Or use the full-text search:
            `dataset_data('some-dataset', search='a query')`
        """

        return self._paginate(
            self._create_url('dataset/' + slug + '/' + tablename + '/data'),
            params=kwargs,
        )

    def holdings(self, cnpj):
        url = self._create_url(
            'especiais/grafo/sociedades/empresas-mae',
            params={'identificador': cnpj},
        )
        response = self._get_json(url)
        return [node for node in response['network']['nodes']
                if 'EmpresaMae' in node['labels']]

    def family(self, cnpj):
        url = self._create_url(
            'especiais/grafo/sociedades/subsequentes',
            params={'identificador': cnpj},
        )
        response = self._get_json(url)
        return response['network']['nodes']
