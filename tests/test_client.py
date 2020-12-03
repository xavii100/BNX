from app.client import ClientCommonFramework as client
from app.properties import Properties

class TestClientCommonFramework():

    def test_common_framework(self, mocker):
        self.mock_properties(mocker)
        request = mocker.patch('app.client.req.post')
        request().status_code = 200
        
        path_dir_names = [
            'inbox'
        ]
        file_name = 'Cat_Holding_20200530.xls'
        response = client.common_framework(path_dir_names, file_name)
        assert response.status_code == 200
    
    def test_orquestrate(self, mocker):
        self.mock_properties(mocker)
        request = mocker.patch('app.client.req.post')
        request().status_code = 200
        
        path_dir_names = [
            'outbox',
            '20201201'
        ]
        file_name = 'PYSB_LIBROCIEGO.3676'
        response = client.orquestrate(path_dir_names, file_name)
        assert response.status_code == 200

    def test_invalid_conexion(self, mocker):
        self.mock_properties(mocker)
        request = mocker.patch('app.client.req.post')
        request.side_effect = ConnectionError()
        
        path_dir_names = [
            'outbox',
            '20201201'
        ]
        file_name = 'PYSB_LIBROCIEGO.3676'
        response = client.orquestrate(path_dir_names, file_name)
        assert response is None

    def mock_properties(self, mocker):
        mocker.patch.object(Properties, 'UUID', '87954')
        mocker.patch.object(Properties, 'COMMON_FRAMEWORK_API', '/treasury/common-framework/move')
        mocker.patch.object(Properties, 'COMMON_FRAMEWORK_URI', 'http://localhost:8180')
        mocker.patch.object(Properties, 'COMMON_FRAMEWORK_PREFIX', '/api/v1')
        mocker.patch.object(Properties, 'CONTENT_LANGUAGE', 'es')
        mocker.patch.object(Properties, 'ORCHESTRATE_API', '/treasury/common-framework/orchestrate')