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
import subprocess
import shutil

class ButecoWebApp:
    def __init__(self):
        self.app = Flask(__name__, static_folder='static')
        self.app.secret_key = 'buteco_do_nal_2024'
        self.arquivo_dados = "dados_espetinho.json"
        self.dados = self.carregar_dados()
        self.configurar_rotas()
        
        # Inicializar Git se estivermos no Railway
        if os.environ.get('PORT'):
            self.inicializar_git()
        
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_dados):
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    # Garantir que as chaves existam
                    if 'vendas' not in dados:
                        dados['vendas'] = []
                    if 'despesas' not in dados:
                        dados['despesas'] = []
                    if 'espetinhos' not in dados:
                        dados['espetinhos'] = {}
                    return dados
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
            
            # Log de salvamento (sem commit automático por enquanto)
            print(f"💾 Dados salvos em {self.arquivo_dados}")
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def fazer_commit_automatico(self):
        """Faz commit automático para o GitHub"""
        try:
            # Verificar se estamos no Railway (tem variável PORT)
            if os.environ.get('PORT'):
                print("🔄 Tentando fazer commit automático para GitHub...")
                
                # Verificar se é um repositório Git
                if not os.path.exists('.git'):
                    print("⚠️ Repositório Git não encontrado. Pulando commit automático.")
                    return
                
                # Configurar Git (se necessário)
                subprocess.run(['git', 'config', 'user.email', 'railway@buteco.com'], 
                             capture_output=True, text=True)
                subprocess.run(['git', 'config', 'user.name', 'Railway Bot'], 
                             capture_output=True, text=True)
                
                # Adicionar arquivo
                subprocess.run(['git', 'add', self.arquivo_dados], 
                             capture_output=True, text=True)
                
                # Fazer commit
                commit_msg = f"Atualização automática de vendas - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Commit realizado com sucesso!")
                    
                    # Verificar se existe branch main
                    branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                                 capture_output=True, text=True)
                    current_branch = branch_result.stdout.strip()
                    
                    if not current_branch:
                        # Criar branch main se não existir
                        subprocess.run(['git', 'checkout', '-b', 'main'], 
                                     capture_output=True, text=True)
                        current_branch = 'main'
                    
                    # Tentar fazer push
                    push_result = subprocess.run(['git', 'push', 'origin', current_branch], 
                                               capture_output=True, text=True)
                    if push_result.returncode == 0:
                        print("✅ Push para GitHub realizado com sucesso!")
                    else:
                        print(f"⚠️ Erro no push: {push_result.stderr}")
                else:
                    print(f"⚠️ Erro no commit: {result.stderr}")
                    
        except Exception as e:
            print(f"⚠️ Erro no commit automático: {e}")
    
    def inicializar_git(self):
        """Inicializa o repositório Git no Railway"""
        try:
            print("🔧 Inicializando repositório Git...")
            
            # Verificar se já é um repositório Git
            if os.path.exists('.git'):
                print("✅ Git já está configurado!")
                return
            
            # Inicializar Git
            result = subprocess.run(['git', 'init'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Repositório Git inicializado!")
                
                # Configurar Git
                subprocess.run(['git', 'config', 'user.name', 'Railway Bot'], 
                             capture_output=True, text=True)
                subprocess.run(['git', 'config', 'user.email', 'railway@buteco.com'], 
                             capture_output=True, text=True)
                
                # Adicionar remote
                subprocess.run(['git', 'remote', 'add', 'origin', 
                              'https://github.com/marcos-r3tech/marcos-r3tech.git'], 
                             capture_output=True, text=True)
                
                # Fazer pull do repositório existente
                print("🔄 Fazendo pull do repositório...")
                pull_result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                           capture_output=True, text=True)
                if pull_result.returncode == 0:
                    print("✅ Pull realizado com sucesso!")
                else:
                    print(f"⚠️ Erro no pull: {pull_result.stderr}")
                    # Se não conseguir fazer pull, criar branch main
                    subprocess.run(['git', 'checkout', '-b', 'main'], 
                                 capture_output=True, text=True)
                    print("✅ Branch main criada!")
                
                print("✅ Git configurado com sucesso!")
            else:
                print(f"⚠️ Erro ao inicializar Git: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ Erro ao inicializar Git: {e}")
    
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
        
        @self.app.route('/favicon.ico')
        def favicon():
            """Servir favicon"""
            return self.app.send_static_file('favicon.ico')
        
        @self.app.route('/favicon-<int:size>.png')
        def favicon_png(size):
            """Servir favicon PNG"""
            return self.app.send_static_file(f'favicon-{size}x{size}.png')
        
        @self.app.route('/apple-touch-icon.png')
        def apple_touch_icon():
            """Servir ícone para Apple"""
            return self.app.send_static_file('apple-touch-icon.png')
        
        @self.app.route('/site.webmanifest')
        def manifest():
            """Servir manifest"""
            return self.app.send_static_file('site.webmanifest')
        
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
                
                # Verificar se deve alterar estoque
                alterar_estoque = data.get('alterar_estoque', True)
                
                # Verificar estoque se necessário
                if alterar_estoque:
                    estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
                    if estoque_atual < quantidade:
                        return jsonify({'success': False, 'message': f'Estoque insuficiente! Disponível: {estoque_atual} unidades'}), 400
                
                # Criar venda
                venda = {
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'espetinho': espetinho,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'total': total,
                    'alterou_estoque': alterar_estoque,
                    'origem': 'web'
                }
                
                # Adicionar venda
                if 'vendas' not in self.dados:
                    self.dados['vendas'] = []
                
                self.dados['vendas'].append(venda)
                
                # Atualizar estoque apenas se necessário
                if alterar_estoque:
                    self.dados['espetinhos'][espetinho]['estoque'] -= quantidade
                
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
        
        @self.app.route('/api/despesas', methods=['POST'])
        def api_criar_despesa():
            """API para criar nova despesa"""
            try:
                data = request.get_json()
                
                if not data or 'descricao' not in data or 'valor' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                descricao = data['descricao']
                valor = float(data['valor'])
                data_despesa = data.get('data', datetime.now().strftime('%d/%m/%Y %H:%M'))
                
                # Criar despesa
                despesa = {
                    'data': data_despesa,
                    'descricao': descricao,
                    'valor': valor
                }
                
                if 'despesas' not in self.dados:
                    self.dados['despesas'] = []
                
                self.dados['despesas'].append(despesa)
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Despesa adicionada com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/despesas/<int:indice>', methods=['PUT'])
        def api_editar_despesa(indice):
            """API para editar despesa existente"""
            try:
                data = request.get_json()
                
                if indice < 0 or indice >= len(self.dados.get('despesas', [])):
                    return jsonify({'success': False, 'message': 'Despesa não encontrada'}), 404
                
                if 'descricao' in data:
                    self.dados['despesas'][indice]['descricao'] = data['descricao']
                if 'valor' in data:
                    self.dados['despesas'][indice]['valor'] = float(data['valor'])
                if 'data' in data:
                    self.dados['despesas'][indice]['data'] = data['data']
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Despesa atualizada com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/despesas/<int:indice>', methods=['DELETE'])
        def api_excluir_despesa(indice):
            """API para excluir despesa"""
            try:
                if indice < 0 or indice >= len(self.dados.get('despesas', [])):
                    return jsonify({'success': False, 'message': 'Despesa não encontrada'}), 404
                
                despesa_excluida = self.dados['despesas'].pop(indice)
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Despesa excluída com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/vendas/hoje/<int:indice>', methods=['DELETE'])
        def api_excluir_venda_hoje(indice):
            """API para excluir uma venda de hoje específica"""
            try:
                # Obter vendas de hoje para encontrar a venda correta
                hoje = datetime.now().strftime('%d/%m/%Y')
                vendas_hoje = []
                indices_hoje = []
                
                for i, venda in enumerate(self.dados.get('vendas', [])):
                    if venda.get('data', '').startswith(hoje):
                        vendas_hoje.append(venda)
                        indices_hoje.append(i)
                
                # Verificar se o índice é válido para vendas de hoje
                if indice < 0 or indice >= len(vendas_hoje):
                    return jsonify({'success': False, 'message': 'Venda não encontrada'}), 404
                
                # Obter o índice real da venda no array global
                indice_real = indices_hoje[indice]
                venda_excluida = self.dados['vendas'][indice_real]
                
                # Se a venda alterou estoque, devolver ao estoque
                if venda_excluida.get('alterou_estoque', True):
                    espetinho = venda_excluida['espetinho']
                    quantidade = venda_excluida['quantidade']
                    if espetinho in self.dados.get('espetinhos', {}):
                        self.dados['espetinhos'][espetinho]['estoque'] += quantidade
                
                # Remover venda usando o índice real
                del self.dados['vendas'][indice_real]
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Venda excluída com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar alterações'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/vendas/<int:indice>', methods=['DELETE'])
        def api_excluir_venda(indice):
            """API para excluir uma venda específica (todas as vendas)"""
            try:
                vendas = self.dados.get('vendas', [])
                if 0 <= indice < len(vendas):
                    venda_excluida = vendas.pop(indice)
                    
                    # Se a venda alterou estoque, devolver ao estoque
                    if venda_excluida.get('alterou_estoque', True):
                        espetinho = venda_excluida['espetinho']
                        quantidade = venda_excluida['quantidade']
                        if espetinho in self.dados.get('espetinhos', {}):
                            self.dados['espetinhos'][espetinho]['estoque'] += quantidade
                    
                    if self.salvar_dados():
                        return jsonify({'success': True, 'message': 'Venda excluída com sucesso!'})
                    else:
                        return jsonify({'success': False, 'message': 'Erro ao salvar alterações'}), 500
                else:
                    return jsonify({'success': False, 'message': 'Venda não encontrada'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/espetinhos', methods=['POST'])
        def api_criar_espetinho():
            """API para criar novo espetinho"""
            try:
                data = request.get_json()
                
                if not data or 'nome' not in data or 'valor' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                nome = data['nome']
                valor = float(data['valor'])
                custo = float(data.get('custo', 0))
                estoque = int(data.get('estoque', 0))
                
                # Verificar se já existe
                if nome in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho já existe'}), 400
                
                # Criar espetinho
                self.dados['espetinhos'][nome] = {
                    'valor': valor,
                    'custo': custo,
                    'estoque': estoque
                }
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Espetinho criado com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/espetinhos/<nome>', methods=['PUT'])
        def api_editar_espetinho(nome):
            """API para editar espetinho existente"""
            try:
                data = request.get_json()
                
                if nome not in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 404
                
                if 'valor' in data:
                    self.dados['espetinhos'][nome]['valor'] = float(data['valor'])
                if 'custo' in data:
                    self.dados['espetinhos'][nome]['custo'] = float(data['custo'])
                if 'estoque' in data:
                    self.dados['espetinhos'][nome]['estoque'] = int(data['estoque'])
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Espetinho atualizado com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/espetinhos/<nome>', methods=['DELETE'])
        def api_excluir_espetinho(nome):
            """API para excluir espetinho"""
            try:
                if nome not in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 404
                
                del self.dados['espetinhos'][nome]
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Espetinho excluído com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/estoque/adicionar', methods=['POST'])
        def api_adicionar_estoque():
            """API para adicionar estoque a um espetinho"""
            try:
                data = request.get_json()
                
                if not data or 'espetinho' not in data or 'quantidade' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                espetinho = data['espetinho']
                quantidade = int(data['quantidade'])
                
                if espetinho not in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 404
                
                self.dados['espetinhos'][espetinho]['estoque'] += quantidade
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': f'Estoque atualizado! Novo estoque: {self.dados["espetinhos"][espetinho]["estoque"]}'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/estoque/zerar', methods=['POST'])
        def api_zerar_estoque():
            """API para zerar estoque de um espetinho"""
            try:
                data = request.get_json()
                
                if not data or 'espetinho' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                espetinho = data['espetinho']
                
                if espetinho not in self.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 404
                
                self.dados['espetinhos'][espetinho]['estoque'] = 0
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': f'Estoque de {espetinho} zerado!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/estoque/zerar-todos', methods=['POST'])
        def api_zerar_todos_estoques():
            """API para zerar estoque de todos os espetinhos"""
            try:
                for espetinho in self.dados.get('espetinhos', {}):
                    self.dados['espetinhos'][espetinho]['estoque'] = 0
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Todos os estoques foram zerados!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/status')
        def api_status():
            """API para verificar status do sistema"""
            return jsonify({
                'status': 'online',
                'total_vendas': len(self.dados.get('vendas', [])),
                'vendas_hoje': len(self.obter_vendas_hoje()),
                'total_espetinhos': len(self.dados.get('espetinhos', {})),
                'total_despesas': len(self.dados.get('despesas', [])),
                'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            })
        
        @self.app.route('/api/backup')
        def api_backup():
            """API para fazer backup dos dados"""
            try:
                # Salvar dados atuais
                if self.salvar_dados():
                    return jsonify({
                        'success': True, 
                        'message': 'Backup realizado com sucesso!',
                        'arquivo': self.arquivo_dados,
                        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    })
                else:
                    return jsonify({'success': False, 'message': 'Erro ao fazer backup'}), 500
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
    
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

