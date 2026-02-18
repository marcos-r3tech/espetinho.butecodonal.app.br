#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍖 BUTECO DO NAL - Aplicativo Web para Vendas
Sistema web para lançamento de vendas via celular
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import threading
import time
from datetime import datetime, timezone, timedelta
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
    
    def obter_data_hora_brasil(self):
        """Obtém data e hora no fuso horário do Brasil (UTC-3) formatada."""
        brasil_tz = timezone(timedelta(hours=-3))
        agora = datetime.now(brasil_tz)
        return agora.strftime('%d/%m/%Y %H:%M')

    def agora_brasil(self):
        """Retorna datetime timezone-aware no fuso do Brasil (UTC-3)."""
        return datetime.now(timezone(timedelta(hours=-3)))
    
    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            
            # Log de salvamento
            print(f"💾 Dados salvos em {self.arquivo_dados}")
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def fazer_backup_automatico(self, operacao):
        """Faz backup automático após operações"""
        try:
            # Salvar dados
            if self.salvar_dados():
                # Criar arquivo de backup com timestamp no fuso do Brasil
                timestamp = self.agora_brasil().strftime('%Y%m%d_%H%M%S')
                backup_file = f"backups/backup_{operacao}_{timestamp}.json"
                
                # Criar pasta de backups se não existir
                os.makedirs('backups', exist_ok=True)
                
                # Copiar arquivo para backup
                with open(self.arquivo_dados, 'r', encoding='utf-8') as source:
                    with open(backup_file, 'w', encoding='utf-8') as target:
                        target.write(source.read())
                
                print(f"✅ Backup automático criado: {backup_file}")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Erro no backup automático: {e}")
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
                commit_msg = f"Atualização automática de vendas - {self.agora_brasil().strftime('%d/%m/%Y %H:%M')}"
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
            """Página principal - apenas para funcionários"""
            # Verificar se é um acesso direto ou via login
            senha = request.args.get('senha', '')
            if senha != 'buteco2024':  # Senha simples para funcionários
                return render_template('login.html')
            
            return render_template('index.html', 
                                 espetinhos=self.dados.get('espetinhos', {}),
                                 vendas_hoje=self.obter_vendas_hoje())
        
        @self.app.route('/cardapio')
        def cardapio():
            """Cardápio público para clientes"""
            # Filtrar apenas espetinhos com estoque > 0
            espetinhos_disponiveis = {}
            for nome, dados in self.dados.get('espetinhos', {}).items():
                if dados.get('estoque', 0) > 0:
                    espetinhos_disponiveis[nome] = dados
            
            return render_template('cardapio.html', 
                                 espetinhos=espetinhos_disponiveis,
                                 total_espetinhos=len(espetinhos_disponiveis))
        
        @self.app.route('/menu')
        def menu():
            """Alias para o cardápio - mais fácil de lembrar"""
            return cardapio()
        
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

                # Tipo de venda: normal ou bonificação (sem cobrança)
                tipo_venda = data.get('tipo_venda', 'normal')

                # Tipo de consumo: local, entrega ou interno
                tipo_consumo = data.get('tipo_consumo', 'local')

                # Valor realmente cobrado do cliente
                valor_cobrado = 0.0 if tipo_venda == 'bonificacao' else total

                # Data/hora da venda e competência (ano-mês) no fuso do Brasil
                data_venda = self.obter_data_hora_brasil()
                try:
                    competencia = datetime.strptime(data_venda, '%d/%m/%Y %H:%M').strftime('%Y-%m')
                except Exception:
                    competencia = None

                # Verificar se deve alterar estoque
                alterar_estoque = data.get('alterar_estoque', True)

                # Verificar estoque se necessário
                if alterar_estoque:
                    estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
                    if estoque_atual < quantidade:
                        return jsonify({'success': False, 'message': f'Estoque insuficiente! Disponível: {estoque_atual} unidades'}), 400

                # Criar venda
                venda = {
                    'data': data_venda,
                    'espetinho': espetinho,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'total': total,
                    'alterou_estoque': alterar_estoque,
                    'origem': 'web',
                    'tipo_venda': tipo_venda,
                    'valor_cobrado': valor_cobrado,
                    'tipo_consumo': tipo_consumo,
                    'competencia': competencia
                }

                # Adicionar venda
                if 'vendas' not in self.dados:
                    self.dados['vendas'] = []

                self.dados['vendas'].append(venda)

                # Atualizar estoque apenas se necessário
                if alterar_estoque:
                    self.dados['espetinhos'][espetinho]['estoque'] -= quantidade

                # Salvar dados e fazer backup
                if self.salvar_dados():
                    self.fazer_backup_automatico('venda')
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
                data_despesa = data.get('data', self.obter_data_hora_brasil())
                
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
                    self.fazer_backup_automatico('despesa')
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
                    self.fazer_backup_automatico('edicao_despesa')
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
                    self.fazer_backup_automatico('exclusao_despesa')
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
                hoje = self.agora_brasil().strftime('%d/%m/%Y')
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
                    self.fazer_backup_automatico('exclusao_venda')
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
                        self.fazer_backup_automatico('exclusao_venda')
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
                    self.fazer_backup_automatico('criacao_espetinho')
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
                    self.fazer_backup_automatico('edicao_espetinho')
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
                    self.fazer_backup_automatico('exclusao_espetinho')
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
                    self.fazer_backup_automatico('alteracao_estoque')
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
                    self.fazer_backup_automatico('zerar_estoque')
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
                    self.fazer_backup_automatico('zerar_todos_estoques')
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
                'timestamp': self.agora_brasil().strftime('%d/%m/%Y %H:%M:%S')
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
                        'timestamp': self.agora_brasil().strftime('%d/%m/%Y %H:%M:%S')
                    })
                else:
                    return jsonify({'success': False, 'message': 'Erro ao fazer backup'}), 500
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/download')
        def api_download():
            """API para baixar o arquivo de dados"""
            try:
                if os.path.exists(self.arquivo_dados):
                    return send_file(
                        self.arquivo_dados,
                        as_attachment=True,
                        download_name=f'dados_espetinho_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                        mimetype='application/json'
                    )
                else:
                    return jsonify({'success': False, 'message': 'Arquivo não encontrado'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/backups')
        def api_listar_backups():
            """API para listar todos os backups"""
            try:
                backups = []
                if os.path.exists('backups'):
                    for arquivo in os.listdir('backups'):
                        if arquivo.endswith('.json'):
                            caminho = os.path.join('backups', arquivo)
                            stat = os.stat(caminho)
                            brasil_tz = timezone(timedelta(hours=-3))
                            backups.append({
                                'arquivo': arquivo,
                                'tamanho': stat.st_size,
                                'data_criacao': datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).astimezone(brasil_tz).strftime('%d/%m/%Y %H:%M:%S'),
                                'operacao': arquivo.split('_')[1] if '_' in arquivo else 'desconhecida'
                            })
                
                # Ordenar por data de criação (mais recente primeiro)
                backups.sort(key=lambda x: x['data_criacao'], reverse=True)
                return jsonify(backups)
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/backups/<nome_arquivo>')
        def api_download_backup(nome_arquivo):
            """API para baixar um backup específico"""
            try:
                caminho = os.path.join('backups', nome_arquivo)
                if os.path.exists(caminho):
                    return send_file(
                        caminho,
                        as_attachment=True,
                        download_name=nome_arquivo,
                        mimetype='application/json'
                    )
                else:
                    return jsonify({'success': False, 'message': 'Backup não encontrado'}), 404
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/consolidar-bancos', methods=['POST'])
        def api_consolidar_bancos():
            """API para consolidar múltiplos arquivos JSON em um único banco"""
            try:
                # Fazer backup antes
                backup_nome = f"backup_antes_consolidacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                try:
                    with open(backup_nome, 'w', encoding='utf-8') as f:
                        json.dump(self.dados, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    return jsonify({'success': False, 'message': f'Erro ao fazer backup: {str(e)}'}), 500
                
                # Dados consolidados (começar com dados atuais)
                fechamentos_atuais = self.dados.get("fechamentos_mensais", self.dados.get("fechamentos_mes", {}))
                dados_consolidados = {
                    "vendas": list(self.dados.get("vendas", [])),
                    "despesas": list(self.dados.get("despesas", [])),
                    "espetinhos": dict(self.dados.get("espetinhos", {})),
                    "fechamentos_mensais": dict(fechamentos_atuais),
                    "pedidos": list(self.dados.get("pedidos", [])),
                    "whatsapp_numbers": list(self.dados.get("whatsapp_numbers", [])),
                    "whatsapp_rotation_index": self.dados.get("whatsapp_rotation_index", 0)
                }
                
                # Criar sets para evitar duplicatas
                vendas_unicas = set()
                despesas_unicas = set()
                
                # Função para criar chave única de venda
                def chave_venda(venda):
                    return (
                        venda.get("data", ""),
                        venda.get("espetinho", ""),
                        venda.get("quantidade", 0),
                        venda.get("valor_unitario", 0),
                        venda.get("total", 0),
                        venda.get("origem", ""),
                        venda.get("pedido_id", None)
                    )
                
                # Função para criar chave única de despesa
                def chave_despesa(despesa):
                    return (
                        despesa.get("data", ""),
                        despesa.get("descricao", ""),
                        despesa.get("valor", 0)
                    )
                
                # Adicionar vendas e despesas atuais aos sets
                for venda in dados_consolidados["vendas"]:
                    vendas_unicas.add(chave_venda(venda))
                for despesa in dados_consolidados["despesas"]:
                    despesas_unicas.add(chave_despesa(despesa))
                
                # Processar cada arquivo enviado
                total_vendas_adicionadas = 0
                total_despesas_adicionadas = 0
                arquivos_processados = 0
                
                for key in request.files:
                    arquivo = request.files[key]
                    if arquivo.filename == '':
                        continue
                    
                    try:
                        # Ler conteúdo do arquivo
                        conteudo = arquivo.read().decode('utf-8')
                        dados_arquivo = json.loads(conteudo)
                        
                        # Processar vendas
                        vendas_arquivo = dados_arquivo.get("vendas", [])
                        for venda in vendas_arquivo:
                            chave = chave_venda(venda)
                            if chave not in vendas_unicas:
                                # Criar cópia completa da venda preservando TODOS os campos
                                venda_completa = dict(venda)  # Copia todos os campos existentes
                                
                                # Garantir que campos obrigatórios existam
                                if "data" not in venda_completa:
                                    continue  # Pula vendas sem data
                                
                                # Preservar todos os campos, incluindo os novos:
                                # - tipo_venda (normal/bonificacao)
                                # - valor_cobrado (valor realmente cobrado)
                                # - tipo_consumo (local/entrega/interno)
                                # - competencia (YYYY-MM)
                                # - origem (web/desktop/online)
                                # - pedido_id (se existir)
                                # - alterou_estoque
                                # - e qualquer outro campo que existir
                                
                                dados_consolidados["vendas"].append(venda_completa)
                                vendas_unicas.add(chave)
                                total_vendas_adicionadas += 1
                        
                        # Processar despesas
                        despesas_arquivo = dados_arquivo.get("despesas", [])
                        for despesa in despesas_arquivo:
                            chave = chave_despesa(despesa)
                            if chave not in despesas_unicas:
                                # Criar cópia completa da despesa preservando TODOS os campos
                                despesa_completa = dict(despesa)  # Copia todos os campos existentes
                                
                                # Garantir que campos obrigatórios existam
                                if "data" not in despesa_completa or "descricao" not in despesa_completa:
                                    continue  # Pula despesas sem dados essenciais
                                
                                # Preservar todos os campos da despesa
                                dados_consolidados["despesas"].append(despesa_completa)
                                despesas_unicas.add(chave)
                                total_despesas_adicionadas += 1
                        
                        # Processar fechamentos mensais
                        fechamentos_arquivo = dados_arquivo.get("fechamentos_mensais", dados_arquivo.get("fechamentos_mes", {}))
                        for competencia, fechamento in fechamentos_arquivo.items():
                            if competencia not in dados_consolidados["fechamentos_mensais"]:
                                dados_consolidados["fechamentos_mensais"][competencia] = fechamento
                        
                        # Atualizar espetinhos (adicionar novos tipos, mas NÃO importar estoque)
                        # O estoque deve permanecer o do arquivo principal (atual)
                        espetinhos_arquivo = dados_arquivo.get("espetinhos", {})
                        for nome_espetinho, dados_espetinho in espetinhos_arquivo.items():
                            if nome_espetinho not in dados_consolidados["espetinhos"]:
                                # Adicionar novo tipo de espetinho, mas sem estoque (ou com estoque 0)
                                dados_consolidados["espetinhos"][nome_espetinho] = {
                                    "valor": dados_espetinho.get("valor", 0),
                                    "custo": dados_espetinho.get("custo", 0),
                                    "estoque": 0  # Sempre começa com estoque 0 para novos tipos
                                }
                            # Se o espetinho já existe, mantém o estoque atual (não sobrescreve)
                        
                        arquivos_processados += 1
                        
                    except Exception as e:
                        continue  # Pula arquivo com erro
                
                # Ordenar vendas e despesas por data E hora (preservando hora completa)
                def parse_data_hora(item):
                    try:
                        data_str = item.get("data", "")
                        if not data_str:
                            return datetime.min
                        
                        # Tentar formatos com hora primeiro
                        formatos_com_hora = [
                            "%d/%m/%Y %H:%M",      # 19/09/2025 13:52
                            "%d/%m/%Y %H:%M:%S",   # 19/09/2025 13:52:30
                            "%Y-%m-%d %H:%M",      # 2025-09-19 13:52
                            "%Y-%m-%d %H:%M:%S",   # 2025-09-19 13:52:30
                        ]
                        
                        # Tentar formatos sem hora
                        formatos_sem_hora = [
                            "%d/%m/%Y",            # 19/09/2025
                            "%Y-%m-%d",            # 2025-09-19
                        ]
                        
                        # Tentar todos os formatos com hora primeiro
                        for formato in formatos_com_hora:
                            try:
                                return datetime.strptime(data_str, formato)
                            except:
                                continue
                        
                        # Se não funcionou, tentar formatos sem hora
                        for formato in formatos_sem_hora:
                            try:
                                return datetime.strptime(data_str, formato)
                            except:
                                continue
                        
                        return datetime.min
                    except:
                        return datetime.min
                
                # Ordenar preservando data e hora completa
                dados_consolidados["vendas"].sort(key=parse_data_hora)
                dados_consolidados["despesas"].sort(key=parse_data_hora)
                
                # Salvar dados consolidados
                self.dados = dados_consolidados
                with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                    json.dump(self.dados, f, ensure_ascii=False, indent=2)
                
                return jsonify({
                    'success': True,
                    'arquivos_processados': arquivos_processados,
                    'vendas_adicionadas': total_vendas_adicionadas,
                    'despesas_adicionadas': total_despesas_adicionadas,
                    'total_vendas': len(dados_consolidados['vendas']),
                    'total_despesas': len(dados_consolidados['despesas']),
                    'backup_nome': backup_nome
                })
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro ao consolidar bancos: {str(e)}'}), 500
        
        @self.app.route('/api/info')
        def api_info_estabelecimento():
            """API para obter informações do estabelecimento"""
            # Obter números WhatsApp configurados
            whatsapp_numbers = self.dados.get('whatsapp_numbers', [
                {'numero': '77981073054', 'nome': 'Nal - Principal', 'ativo': True},
                {'numero': '77999999999', 'nome': 'Backup 1', 'ativo': False},
                {'numero': '77988888888', 'nome': 'Backup 2', 'ativo': False}
            ])
            
            return jsonify({
                'nome': 'Buteco do Nal',
                'telefone': '(77) 98107-3054',
                'whatsapp': '(77) 98107-3054',
                'endereco': 'Travessa Santa Mônica, 42 - Nossa Senhora Aparecida',
                'endereco_maps': 'Travessa Santa Mônica, 42, Nossa Senhora Aparecida',
                'horario': 'Sexta a partir das 18h | Sábado e Domingo a partir do meio-dia',
                'descricao': 'Espetinhos fresquinhos e saborosos!',
                'mensagem_whatsapp': 'Olá! Gostaria de fazer um pedido no Buteco do Nal! 🍖',
                'whatsapp_numbers': whatsapp_numbers
            })
        
        # === SISTEMA DE PEDIDOS ===
        @self.app.route('/api/pedidos', methods=['POST'])
        def api_criar_pedido():
            """API para criar novo pedido"""
            try:
                data = request.get_json()
                
                # Validar dados básicos
                if not data or 'itens' not in data:
                    return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
                
                # Criar pedido
                pedido = {
                    'id': len(self.dados.get('pedidos', [])) + 1,
                    'data': self.obter_data_hora_brasil(),
                    'nome_cliente': data.get('nome_cliente', 'Cliente'),
                    'telefone': data.get('telefone', ''),
                    'endereco': data.get('endereco', ''),
                    'observacoes': data.get('observacoes', ''),
                    'itens': data['itens'],
                    'status': 'pendente',
                    'tempo_status': {
                        'pendente': self.obter_data_hora_brasil(),
                        'aceito': None,
                        'preparando': None,
                        'pronto': None
                    },
                    'total': data.get('total', 0)
                }
                
                # Adicionar pedido
                if 'pedidos' not in self.dados:
                    self.dados['pedidos'] = []
                
                self.dados['pedidos'].append(pedido)
                
                # Salvar dados
                if self.salvar_dados():
                    return jsonify({
                        'success': True, 
                        'message': 'Pedido criado com sucesso!',
                        'pedido_id': pedido['id']
                    })
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar pedido'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/pedidos')
        def api_listar_pedidos():
            """API para listar todos os pedidos"""
            return jsonify(self.dados.get('pedidos', []))
        
        @self.app.route('/api/pedidos/<int:pedido_id>/status', methods=['PUT'])
        def api_atualizar_status_pedido(pedido_id):
            """API para atualizar status do pedido"""
            try:
                data = request.get_json()
                novo_status = data.get('status')
                
                if not novo_status or novo_status not in ['aceito', 'preparando', 'pronto']:
                    return jsonify({'success': False, 'message': 'Status inválido'}), 400
                
                # Encontrar pedido
                pedidos = self.dados.get('pedidos', [])
                pedido = next((p for p in pedidos if p['id'] == pedido_id), None)
                
                if not pedido:
                    return jsonify({'success': False, 'message': 'Pedido não encontrado'}), 404
                
                # Atualizar status e tempo
                pedido['status'] = novo_status
                pedido['tempo_status'][novo_status] = self.obter_data_hora_brasil()
                
                # Se o pedido foi marcado como PRONTO, registrar vendas e baixar estoque
                if novo_status == 'pronto':
                    print(f"\n🔔 Pedido #{pedido_id} marcado como PRONTO - Registrando vendas...")
                    print(f"📋 Itens do pedido: {pedido['itens']}")
                    
                    vendas_registradas = 0
                    
                    # Registrar cada item do pedido como venda
                    for item in pedido['itens']:
                        print(f"\n  Processando item: {item}")
                        
                        # Dados básicos
                        quantidade = item['quantidade']
                        valor_unitario = item['preco']
                        total = valor_unitario * quantidade

                        # Para pedidos online, consideramos venda normal e consumo como entrega
                        tipo_venda = 'normal'
                        tipo_consumo = 'entrega'

                        data_venda = self.obter_data_hora_brasil()
                        try:
                            competencia = datetime.strptime(data_venda, '%d/%m/%Y %H:%M').strftime('%Y-%m')
                        except Exception:
                            competencia = None

                        venda = {
                            'espetinho': item['nome'],
                            'quantidade': quantidade,
                            'valor_unitario': valor_unitario,
                            'total': total,
                            'data': data_venda,
                            'origem': 'online',  # Marcar como venda online
                            'pedido_id': pedido_id,  # Referência ao pedido
                            'tipo_venda': tipo_venda,
                            'valor_cobrado': total,
                            'tipo_consumo': tipo_consumo,
                            'competencia': competencia
                        }
                        
                        print(f"  Venda criada: {venda}")
                        
                        # Adicionar venda
                        if 'vendas' not in self.dados:
                            self.dados['vendas'] = []
                            print("  Criando lista de vendas...")
                        
                        self.dados['vendas'].append(venda)
                        vendas_registradas += 1
                        print(f"  ✅ Venda adicionada! Total de vendas: {len(self.dados['vendas'])}")
                        
                        # Baixar estoque
                        print(f"  Verificando estoque de: {item['nome']}")
                        print(f"  Espetinhos disponíveis: {list(self.dados.get('espetinhos', {}).keys())}")
                        
                        if item['nome'] in self.dados.get('espetinhos', {}):
                            espetinho_estoque = self.dados['espetinhos'][item['nome']]
                            if 'estoque' in espetinho_estoque:
                                estoque_atual = espetinho_estoque['estoque']
                                novo_estoque = max(0, estoque_atual - item['quantidade'])
                                self.dados['espetinhos'][item['nome']]['estoque'] = novo_estoque
                                print(f"  📦 {item['nome']}: {estoque_atual} → {novo_estoque} (vendeu {item['quantidade']})")
                            else:
                                print(f"  ⚠️ {item['nome']} não tem campo 'estoque'")
                        else:
                            print(f"  ⚠️ {item['nome']} não encontrado nos espetinhos!")
                    
                    print(f"\n✅ Pedido #{pedido_id}: {vendas_registradas} vendas registradas!")
                    print(f"📊 Total de vendas no sistema: {len(self.dados.get('vendas', []))}\n")
                    
                    # Remover pedido da lista (já foi convertido em vendas)
                    self.dados['pedidos'] = [p for p in pedidos if p['id'] != pedido_id]
                    print(f"🗑️ Pedido #{pedido_id} removido da lista (convertido em vendas)")
                
                # Salvar dados
                if self.salvar_dados():
                    mensagem = f'Pedido {novo_status} com sucesso!'
                    if novo_status == 'pronto':
                        mensagem += ' Vendas registradas e pedido concluído!'
                    return jsonify({'success': True, 'message': mensagem})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao atualizar pedido'}), 500
                    
            except Exception as e:
                print(f"❌ Erro ao atualizar pedido: {str(e)}")
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
        def api_excluir_pedido(pedido_id):
            """API para excluir pedido"""
            try:
                pedidos = self.dados.get('pedidos', [])
                pedido = next((p for p in pedidos if p['id'] == pedido_id), None)
                
                if not pedido:
                    return jsonify({'success': False, 'message': 'Pedido não encontrado'}), 404
                
                # Remover pedido
                self.dados['pedidos'] = [p for p in pedidos if p['id'] != pedido_id]
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Pedido excluído com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao excluir pedido'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        # === GESTÃO DE NÚMEROS WHATSAPP ===
        @self.app.route('/api/whatsapp/numbers')
        def api_listar_numeros_whatsapp():
            """API para listar números WhatsApp configurados"""
            return jsonify(self.dados.get('whatsapp_numbers', []))
        
        @self.app.route('/api/whatsapp/numbers', methods=['POST'])
        def api_adicionar_numero_whatsapp():
            """API para adicionar novo número WhatsApp"""
            try:
                data = request.get_json()
                print(f"DEBUG - Dados recebidos: {data}")
                
                if not data:
                    print("DEBUG - Nenhum dado recebido")
                    return jsonify({'success': False, 'message': 'Nenhum dado recebido'}), 400
                
                if 'numero' not in data:
                    print("DEBUG - Campo 'numero' não encontrado")
                    return jsonify({'success': False, 'message': 'Campo número é obrigatório'}), 400
                
                if 'nome' not in data:
                    print("DEBUG - Campo 'nome' não encontrado")
                    return jsonify({'success': False, 'message': 'Campo nome é obrigatório'}), 400
                
                numero = ''.join(filter(str.isdigit, data['numero']))  # Remove caracteres não numéricos
                nome = data['nome']
                ativo = data.get('ativo', True)
                
                print(f"DEBUG - Processando: numero={numero}, nome={nome}, ativo={ativo}")
                
                # Verificar se número já existe
                whatsapp_numbers = self.dados.get('whatsapp_numbers', [])
                if any(w['numero'] == numero for w in whatsapp_numbers):
                    return jsonify({'success': False, 'message': 'Número já existe'}), 400
                
                # Adicionar número
                novo_numero = {
                    'numero': numero,
                    'nome': nome,
                    'ativo': ativo
                }
                
                whatsapp_numbers.append(novo_numero)
                self.dados['whatsapp_numbers'] = whatsapp_numbers
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Número adicionado com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/whatsapp/numbers/<int:indice>', methods=['PUT'])
        def api_editar_numero_whatsapp(indice):
            """API para editar número WhatsApp"""
            try:
                data = request.get_json()
                whatsapp_numbers = self.dados.get('whatsapp_numbers', [])
                
                if indice < 0 or indice >= len(whatsapp_numbers):
                    return jsonify({'success': False, 'message': 'Número não encontrado'}), 404
                
                if 'numero' in data:
                    whatsapp_numbers[indice]['numero'] = ''.join(filter(str.isdigit, data['numero']))
                if 'nome' in data:
                    whatsapp_numbers[indice]['nome'] = data['nome']
                if 'ativo' in data:
                    whatsapp_numbers[indice]['ativo'] = data['ativo']
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Número atualizado com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/whatsapp/numbers/<int:indice>', methods=['DELETE'])
        def api_excluir_numero_whatsapp(indice):
            """API para excluir número WhatsApp"""
            try:
                whatsapp_numbers = self.dados.get('whatsapp_numbers', [])
                
                if indice < 0 or indice >= len(whatsapp_numbers):
                    return jsonify({'success': False, 'message': 'Número não encontrado'}), 404
                
                whatsapp_numbers.pop(indice)
                
                if self.salvar_dados():
                    return jsonify({'success': True, 'message': 'Número excluído com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
        
        @self.app.route('/api/whatsapp/next')
        def api_proximo_numero_whatsapp():
            """API para obter próximo número WhatsApp ativo (rotação)"""
            try:
                whatsapp_numbers = self.dados.get('whatsapp_numbers', [])
                numeros_ativos = [w for w in whatsapp_numbers if w.get('ativo', True)]
                
                if not numeros_ativos:
                    # Fallback para número principal
                    return jsonify({'numero': '77981073054', 'nome': 'Principal'})
                
                # Implementar rotação simples
                if 'whatsapp_rotation_index' not in self.dados:
                    self.dados['whatsapp_rotation_index'] = 0
                
                indice = self.dados['whatsapp_rotation_index'] % len(numeros_ativos)
                numero_selecionado = numeros_ativos[indice]
                
                # Avançar para próximo
                self.dados['whatsapp_rotation_index'] = (indice + 1) % len(numeros_ativos)
                self.salvar_dados()
                
                return jsonify(numero_selecionado)
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
    
    def obter_vendas_hoje(self):
        """Obtém vendas do dia atual"""
        hoje = self.agora_brasil().strftime('%d/%m/%Y')
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

