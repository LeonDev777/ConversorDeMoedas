import unittest
from unittest.mock import MagicMock, patch
from app import ConversorMoedasApp
import tkinter as tk
from tkinter import messagebox

class TestConversorMoedasApp(unittest.TestCase):

    def setUp(self):
        self.patcher_get_default_root = patch('tkinter._get_default_root')
        self.mock_get_default_root = self.patcher_get_default_root.start()
        self.mock_get_default_root.return_value = MagicMock()

        self.mock_root = self.mock_get_default_root.return_value
        self.app = ConversorMoedasApp(self.mock_root)
        self.app.valor_entry = MagicMock()
        self.app.moeda_origem_combo = MagicMock()
        self.app.moeda_destino_combo = MagicMock()
        self.app.resultado_label = MagicMock()

        self.patcher_showerror = patch('tkinter.messagebox.showerror')
        self.mock_showerror = self.patcher_showerror.start()

        self.patcher_requests_get = patch('app.requests.get')
        self.mock_requests_get = self.patcher_requests_get.start()

    def tearDown(self):
        self.patcher_get_default_root.stop()
        self.patcher_requests_get.stop()
        self.patcher_showerror.stop()

    def test_converter_moeda_sucesso(self):
        self.app.valor_entry.get.return_value = "100"
        self.app.moeda_origem_combo.get.return_value = "USD"
        self.app.moeda_destino_combo.get.return_value = "BRL"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": 500, "info": {"rate": 5}}
        self.mock_requests_get.return_value = mock_response

        self.app.converter_moeda()

        self.app.resultado_label.config.assert_called_once_with(text="100.00 USD = 500.00 BRL")

    def test_converter_moeda_erro_api(self):
        self.app.valor_entry.get.return_value = "100"
        self.app.moeda_origem_combo.get.return_value = "USD"
        self.app.moeda_destino_combo.get.return_value = "BRL"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": "Moeda não suportada"}
        self.mock_requests_get.return_value = mock_response

        self.app.converter_moeda()

        self.mock_showerror.assert_called_once_with("Erro", "Conversão falhou!")

    def test_converter_moeda_valor_invalido(self):
        self.app.valor_entry.get.return_value = "abc"

        self.app.converter_moeda()

        self.mock_showerror.assert_called_once_with("Erro", "Digite um valor numérico válido!")

if __name__ == '__main__':
    unittest.main()