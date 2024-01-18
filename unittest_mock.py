import requests
import unittest
import smtplib
from unittest.mock import patch, Mock, ANY
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


def send_email(smtp_server, smtp_port, from_addr, to_addr, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_addr, "MyPassword")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    
    
class TestEmail(unittest.TestCase):
    
    @patch('smtplib.SMTP')
    def test_send_mail(self, mock_smtp):
        instance = mock_smtp.return_value
        
        send_email("smtp.example.com", 587, "mymail@exm.com", "hismail@exm.com", "Subject", "Mail Content")
        
        mock_smtp.assert_called_with("smtp.example.com", 587)
        
        instance.starttls.assert_called_with()
        instance.login.assert_called_with("mymail@exm.com", "MyPassword")
        instance.sendmail.assert_called_with("mymail@exm.com", "hismail@exm.com", ANY)
        instance.quit.assert_called_with()


class TestUserData(unittest.TestCase):
    @patch("requests.get")
    def test_get_user_data(self, mock_get):
        mock_response = Mock()
        response_dict = {"name": "John", "email": "john@email.com"}
        mock_response.json.return_value = response_dict

        mock_get.return_value = mock_response

        user_data = get_user_data(1)
        mock_get.assert_called_with("https://api.example.com/users/1")
        self.assertEqual(user_data, response_dict)


if __name__ == "__main__":
    unittest.main()
