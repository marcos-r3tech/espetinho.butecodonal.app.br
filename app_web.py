#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍖 BUTECO DO NAL - Aplicativo Web para Vendas
Sistema web para lançamento de vendas via celular
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import threading
import time
from datetime import datetime
import socket

class ButecoWebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'buteco_do_nal_2024'
        self.arquivo_dados = "dados_espetinho.json"
        self.dados = self.carregar_dados()
        self.configurar_rotas()
        
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_dados):
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"vendas": [], "despesas": [], "espetinhos": {}}
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return {"vendas": [], "despesas": [], "espetinhos": {}}
    
    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def obter_ip_local(self):
        """Obtém o IP local da máquina"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def configurar_rotas(self):
        """Configura as rotas da aplicação"""
        
        @self.app.route('/')
        def index():
            """Página principal"""
            return render_template('index.html', 
                                 espetinhos=self.dados.get('espetinhos', {}),
                                 vendas_hoje=self.obter_vendas_hoje())
        
        @self.app.route('/api/espetinhos')
        def api_espetinhos():
            """API para obter espetinhos disponíveis"""
            return jsonify(self.dados.get('espetinhos', {}))
        
        @self.app.route('/api/vendas', methods=['POST'])
        def api_adicionar_venda():
            """API para adicionar nova venda"""
            try:
                data = request.get_json()
                
                # Validar dados
                if not data or 'espetinho' not in data or 'quantidade' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                espetinho = data['espetinho']
                quantidade = int(data['quantidade'])
                
                # Verificar se espetinho existe
                if espetinho not in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 400
                
                # Obter dados do espetinho
                dados_espetinho = self.dados['espetinhos'][espetinho]
                valor_unitario = dados_espetinho['valor']
                total = valor_unitario * quantidade
                
                # Criar venda
                venda = {
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'espetinho': espetinho,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'total': total
                }
                
                # Adicionar venda
                if 'vendas' not in self.dados:
                    self.dados['vendas'] = []
                
                self.dados['vendas'].append(venda)
                
                # Salvar dados
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Venda adicionada com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar venda'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/vendas/hoje')
        def api_vendas_hoje():
            """API para obter vendas do dia"""
            return jsonify(self.obter_vendas_hoje())
        
        @self.app.route('/api/vendas/todas')
        def api_vendas_todas():
            """API para obter todas as vendas do histórico"""
            return jsonify(self.dados.get('vendas', []))
        
        @self.app.route('/api/despesas')
        def api_despesas():
            """API para obter despesas"""
            return jsonify(self.dados.get('despesas', []))
        
        @self.app.route('/api/vendas/<int:indice>', methods=['DELETE'])
        def api_excluir_venda(indice):
            """API para excluir uma venda específica"""
            try:
                vendas = self.dados.get('vendas', [])
                if 0 <= indice < len(vendas):
                    venda_excluida = vendas.pop(indice)
                    if self.salvar_dados():
                        return jsonify({'success': True, 'message': 'Venda excluída com sucesso!'})
                    else:
                        return jsonify({'success': False, 'message': 'Erro ao salvar alterações'}), 500
                else:
                    return jsonify({'success': False, 'message': 'Venda não encontrada'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/status')
        def api_status():
            """API para verificar status do sistema"""
            return jsonify({
                'status': 'online',
                'total_vendas': len(self.dados.get('vendas', [])),
                'vendas_hoje': len(self.obter_vendas_hoje()),
                'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            })
    
    def obter_vendas_hoje(self):
        """Obtém vendas do dia atual"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        vendas_hoje = []
        
        for venda in self.dados.get('vendas', []):
            if venda.get('data', '').startswith(hoje):
                vendas_hoje.append(venda)
        
        return vendas_hoje
    
    def iniciar_servidor(self, porta=None):
        """Inicia o servidor web"""
        # Para Railway, usar porta da variável de ambiente
        if porta is None:
            porta = int(os.environ.get('PORT', 5000))
        
        ip = self.obter_ip_local()
        print(f"\n🍖 BUTECO DO NAL - APLICATIVO WEB")
        print(f"🌐 Servidor iniciado em: http://{ip}:{porta}")
        print(f"📱 Acesse pelo celular: http://{ip}:{porta}")
        print(f"💻 Acesse pelo computador: http://localhost:{porta}")
        print(f"🔄 Sincronização em tempo real ativa!")
        print(f"⏹️  Pressione Ctrl+C para parar\n")
        
        self.app.run(host='0.0.0.0', port=porta, debug=False, threaded=True)

if __name__ == '__main__':
    app = ButecoWebApp()
    app.iniciar_servidor()
