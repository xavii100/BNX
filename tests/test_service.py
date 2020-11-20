from app.service_impl import ServiceImpl
from app.properties import Properties

service = ServiceImpl()
SUCCESS = 1
FAILED = 0

class TestServiceImpl():

    def test_send_file(self, mocker):
        self.mock_properties(mocker)
        response = mocker.patch('requests.models.Response')
        response.status_code = 200

        mocker.patch('app.service_impl.client_common_framework.common_framework', 
            return_value = response)
        mocker.patch('app.service_impl.client_common_framework.orquestrate', 
            return_value = response)
        
        response = service.send_file('Cat_Per_Rel')
        assert response is SUCCESS
        
    def test_send_file_400_response_move_input(self, mocker):
        self.mock_properties(mocker)
        response = mocker.patch('requests.models.Response')
        response.status_code = 400

        mocker.patch('app.service_impl.client_common_framework.common_framework', 
            return_value = response)
        mocker.patch('app.service_impl.client_common_framework.orquestrate', 
            return_value = response)
        
        response = service.send_file('Cat_Per_Rel')
        assert response is FAILED

    def test_send_file_500_response_move_input(self, mocker):
        self.mock_properties(mocker)
        response = mocker.patch('requests.models.Response')
        response.status_code = 500

        mocker.patch('app.service_impl.client_common_framework.common_framework', 
            return_value = response)
        mocker.patch('app.service_impl.client_common_framework.orquestrate', 
            return_value = response)
        
        response = service.send_file('Cat_Per_Rel')
        assert response is FAILED

    def test_send_file_400_response_orchestrate(self, mocker):
        self.mock_properties(mocker)
        response = mocker.patch('requests.models.Response')
        response.status_code = 200
        response_orchestrate = mocker.patch('requests.models.Response')
        response_orchestrate.status_code = 400

        mocker.patch('app.service_impl.client_common_framework.common_framework', 
            return_value = response)
        mocker.patch('app.service_impl.client_common_framework.orquestrate', 
            return_value = response_orchestrate)
        
        response = service.send_file('Cat_Per_Rel')
        assert response is FAILED
        
    def test_send_file_500_response_orchestrate(self, mocker):
        self.mock_properties(mocker)
        response = mocker.patch('requests.models.Response')
        response.status_code = 200
        response_orchestrate = mocker.patch('requests.models.Response')
        response_orchestrate.status_code = 500

        mocker.patch('app.service_impl.client_common_framework.common_framework', 
            return_value = response)
        mocker.patch('app.service_impl.client_common_framework.orquestrate', 
            return_value = response_orchestrate)
        
        response = service.send_file('Cat_Per_Rel')
        assert response is FAILED

    def mock_properties(self, mocker):
        inbox_path = ['nas', 'inbox']

        mocker.patch.object(Properties, 'INBOX_PATH', inbox_path)