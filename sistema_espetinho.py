import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import json
import os
from datetime import datetime, timedelta
import math
import calendar
import threading
import socket


class ModalModerno:
    """Classe para criar modais modernos e bonitos"""
    
    def __init__(self, parent, cores=None):
        self.parent = parent
        self.cores = cores or {
            'fundo_principal': '#1a1a1a',
            'fundo_secundario': '#2d2d2d',
            'fundo_card': '#3a3a3a',
            'texto_principal': '#ffffff',
            'destaque': '#00d4aa',
            'info': '#74b9ff',
            'erro': '#ff6b6b',
            'sucesso': '#00d4aa',
            'aviso': '#ffa726'
        }
        self.janela = None
    
    def criar_modal(self, titulo, largura=500, altura=400, centralizar=True):
        """Cria um modal moderno"""
        self.janela = tk.Toplevel(self.parent)
        self.janela.title(titulo)
        self.janela.geometry(f"{largura}x{altura}")
        self.janela.configure(bg=self.cores['fundo_principal'])
        self.janela.resizable(False, False)
        self.janela.grab_set()
        
        # Remover bordas da janela para efeito moderno
        self.janela.overrideredirect(False)
        
        # Centralizar janela
        if centralizar:
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (largura // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (altura // 2)
            self.janela.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Frame principal com bordas arredondadas simuladas
        frame_principal = tk.Frame(self.janela, bg=self.cores['fundo_secundario'], relief='flat', bd=0)
        frame_principal.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Cabeçalho do modal
        frame_cabecalho = tk.Frame(frame_principal, bg=self.cores['destaque'], height=50)
        frame_cabecalho.pack(fill='x', pady=(0, 0))
        frame_cabecalho.pack_propagate(False)
        
        # Título do modal
        label_titulo = tk.Label(frame_cabecalho, text=titulo, 
                               font=('Arial', 14, 'bold'),
                               fg=self.cores['fundo_principal'],
                               bg=self.cores['destaque'])
        label_titulo.pack(side='left', padx=20, pady=15)
        
        # Botão fechar
        btn_fechar = tk.Button(frame_cabecalho, text="✕", 
                              command=self.fechar_modal,
                              font=('Arial', 12, 'bold'),
                              fg=self.cores['fundo_principal'],
                              bg=self.cores['destaque'],
                              relief='flat',
                              bd=0,
                              width=3,
                              height=1)
        btn_fechar.pack(side='right', padx=10, pady=10)
        
        # Frame do conteúdo
        frame_conteudo = tk.Frame(frame_principal, bg=self.cores['fundo_secundario'])
        frame_conteudo.pack(fill='both', expand=True, padx=20, pady=20)
        
        return frame_conteudo
    
    def criar_botoes_modal(self, frame, botoes):
        """Cria botões modernos para o modal"""
        frame_botoes = tk.Frame(frame, bg=self.cores['fundo_secundario'])
        frame_botoes.pack(fill='x', pady=(20, 0))
        
        for i, (texto, comando, cor) in enumerate(botoes):
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                           font=('Arial', 10, 'bold'),
                           fg=self.cores['fundo_principal'],
                           bg=cor,
                           relief='flat',
                           bd=0,
                           padx=20,
                           pady=8)
            btn.pack(side='right' if i == 0 else 'left', padx=5)
        
        return frame_botoes
    
    def fechar_modal(self):
        """Fecha o modal"""
        if self.janela:
            self.janela.destroy()
    
    def mostrar_modal_confirmacao(self, titulo, mensagem, callback_sim=None, callback_nao=None):
        """Mostra modal de confirmação moderno"""
        frame = self.criar_modal(titulo, 400, 200)
        
        # Ícone e mensagem
        frame_icone = tk.Frame(frame, bg=self.cores['fundo_secundario'])
        frame_icone.pack(fill='x', pady=(0, 20))
        
        label_icone = tk.Label(frame_icone, text="⚠️", 
                              font=('Arial', 24),
                              fg=self.cores['aviso'],
                              bg=self.cores['fundo_secundario'])
        label_icone.pack(side='left', padx=(0, 15))
        
        label_mensagem = tk.Label(frame_icone, text=mensagem,
                                 font=('Arial', 11),
                                 fg=self.cores['texto_principal'],
                                 bg=self.cores['fundo_secundario'],
                                 wraplength=300,
                                 justify='left')
        label_mensagem.pack(side='left', fill='x', expand=True)
        
        # Botões
        def sim():
            if callback_sim:
                callback_sim()
            self.fechar_modal()
        
        def nao():
            if callback_nao:
                callback_nao()
            self.fechar_modal()
        
        self.criar_botoes_modal(frame, [
            ("✅ Sim", sim, self.cores['sucesso']),
            ("❌ Não", nao, self.cores['erro'])
        ])
    
    def mostrar_modal_sucesso(self, titulo, mensagem):
        """Mostra modal de sucesso moderno"""
        frame = self.criar_modal(titulo, 400, 200)
        
        # Ícone e mensagem
        frame_icone = tk.Frame(frame, bg=self.cores['fundo_secundario'])
        frame_icone.pack(fill='x', pady=(0, 20))
        
        label_icone = tk.Label(frame_icone, text="✅", 
                              font=('Arial', 24),
                              fg=self.cores['sucesso'],
                              bg=self.cores['fundo_secundario'])
        label_icone.pack(side='left', padx=(0, 15))
        
        label_mensagem = tk.Label(frame_icone, text=mensagem,
                                 font=('Arial', 11),
                                 fg=self.cores['texto_principal'],
                                 bg=self.cores['fundo_secundario'],
                                 wraplength=300,
                                 justify='left')
        label_mensagem.pack(side='left', fill='x', expand=True)
        
        # Botão OK
        self.criar_botoes_modal(frame, [
            ("✅ OK", self.fechar_modal, self.cores['sucesso'])
        ])
    
    def mostrar_modal_erro(self, titulo, mensagem):
        """Mostra modal de erro moderno"""
        frame = self.criar_modal(titulo, 400, 200)
        
        # Ícone e mensagem
        frame_icone = tk.Frame(frame, bg=self.cores['fundo_secundario'])
        frame_icone.pack(fill='x', pady=(0, 20))
        
        label_icone = tk.Label(frame_icone, text="❌", 
                              font=('Arial', 24),
                              fg=self.cores['erro'],
                              bg=self.cores['fundo_secundario'])
        label_icone.pack(side='left', padx=(0, 15))
        
        label_mensagem = tk.Label(frame_icone, text=mensagem,
                                 font=('Arial', 11),
                                 fg=self.cores['texto_principal'],
                                 bg=self.cores['fundo_secundario'],
                                 wraplength=300,
                                 justify='left')
        label_mensagem.pack(side='left', fill='x', expand=True)
        
        # Botão OK
        self.criar_botoes_modal(frame, [
            ("✅ OK", self.fechar_modal, self.cores['erro'])
        ])
from flask import Flask, render_template, request, jsonify

class CalendarioWidget:
    """Widget de calendário personalizado"""
    def __init__(self, parent, entry_widget, callback=None, cores=None, incluir_hora=False):
        self.parent = parent
        self.entry_widget = entry_widget
        self.callback = callback
        self.cores = cores or {
            'fundo_secundario': '#2d2d2d',
            'fundo_card': '#3a3a3a',
            'texto_principal': '#ffffff',
            'destaque': '#00d4aa',
            'fundo_principal': '#1a1a1a',
            'info': '#74b9ff',
            'erro': '#ff6b6b'
        }
        self.incluir_hora = incluir_hora
        self.janela = None
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        
    def mostrar_calendario(self):
        """Mostra o calendário"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
            
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("📅 Selecionar Data")
        self.janela.geometry("300x350")
        self.janela.configure(bg=self.cores['fundo_secundario'])
        self.janela.resizable(False, False)
        self.janela.grab_set()
        
        # Centralizar janela
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 150
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 175
        self.janela.geometry(f"300x350+{x}+{y}")
        
        # Frame principal
        frame = tk.Frame(self.janela, bg=self.cores['fundo_secundario'])
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Cabeçalho com navegação
        self.criar_cabecalho(frame)
        
        # Calendário
        self.criar_calendario(frame)
        
        # Botões
        self.criar_botoes(frame)
    
    def criar_cabecalho(self, parent):
        """Cria o cabeçalho do calendário"""
        frame_cabecalho = tk.Frame(parent, bg=self.cores['fundo_secundario'])
        frame_cabecalho.pack(fill='x', pady=(0, 10))
        
        # Botão anterior
        btn_ant = tk.Button(frame_cabecalho, text="◀", 
                           command=self.mes_anterior,
                           bg=self.cores['destaque'],
                           fg=self.cores['fundo_principal'],
                           font=('Arial', 12, 'bold'),
                           relief='flat',
                           width=3)
        btn_ant.pack(side='left')
        
        # Mês/Ano
        self.label_mes_ano = tk.Label(frame_cabecalho, 
                                    text=f"{self.get_nome_mes()} {self.ano_atual}",
                                    font=('Arial', 14, 'bold'),
                                    fg=self.cores['texto_principal'],
                                    bg=self.cores['fundo_secundario'])
        self.label_mes_ano.pack(side='left', expand=True)
        
        # Botão próximo
        btn_prox = tk.Button(frame_cabecalho, text="▶", 
                            command=self.mes_proximo,
                            bg=self.cores['destaque'],
                            fg=self.cores['fundo_principal'],
                            font=('Arial', 12, 'bold'),
                            relief='flat',
                            width=3)
        btn_prox.pack(side='right')
    
    def criar_calendario(self, parent):
        """Cria a grade do calendário"""
        frame_calendario = tk.Frame(parent, bg=self.cores['fundo_secundario'])
        frame_calendario.pack(fill='both', expand=True, pady=(0, 10))
        
        # Dias da semana
        dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
        for i, dia in enumerate(dias_semana):
            label = tk.Label(frame_calendario, text=dia,
                           font=('Arial', 10, 'bold'),
                           fg=self.cores['destaque'],
                           bg=self.cores['fundo_secundario'],
                           width=4)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Botões dos dias
        self.botoes_dias = []
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        
        for semana in range(6):
            for dia_semana in range(7):
                btn = tk.Button(frame_calendario, text="",
                              command=lambda s=semana, d=dia_semana: self.selecionar_dia(s, d),
                              bg=self.cores['fundo_card'],
                              fg=self.cores['texto_principal'],
                              font=('Arial', 10),
                              relief='flat',
                              width=4,
                              height=2)
                btn.grid(row=semana+1, column=dia_semana, padx=1, pady=1)
                self.botoes_dias.append(btn)
        
        self.atualizar_calendario()
    
    def criar_botoes(self, parent):
        """Cria os botões do calendário"""
        frame_botoes = tk.Frame(parent, bg=self.cores['fundo_secundario'])
        frame_botoes.pack(fill='x')
        
        # Botão Hoje
        btn_hoje = tk.Button(frame_botoes, text="🕐 Hoje",
                           command=self.definir_hoje,
                           bg=self.cores['info'],
                           fg=self.cores['fundo_principal'],
                           font=('Arial', 10, 'bold'),
                           relief='flat',
                           width=10)
        btn_hoje.pack(side='left', padx=(0, 10))
        
        # Botão Cancelar
        btn_cancelar = tk.Button(frame_botoes, text="❌ Cancelar",
                               command=self.janela.destroy,
                               bg=self.cores['erro'],
                               fg=self.cores['fundo_principal'],
                               font=('Arial', 10, 'bold'),
                               relief='flat',
                               width=10)
        btn_cancelar.pack(side='right')
    
    def get_nome_mes(self):
        """Retorna o nome do mês"""
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return meses[self.mes_atual - 1]
    
    def mes_anterior(self):
        """Vai para o mês anterior"""
        self.mes_atual -= 1
        if self.mes_atual < 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        self.atualizar_calendario()
    
    def mes_proximo(self):
        """Vai para o mês próximo"""
        self.mes_atual += 1
        if self.mes_atual > 12:
            self.mes_atual = 1
            self.ano_atual += 1
        self.atualizar_calendario()
    
    def atualizar_calendario(self):
        """Atualiza o calendário"""
        self.label_mes_ano.config(text=f"{self.get_nome_mes()} {self.ano_atual}")
        
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        hoje = datetime.now()
        
        for i, btn in enumerate(self.botoes_dias):
            semana = i // 7
            dia_semana = i % 7
            
            if semana < len(cal) and cal[semana][dia_semana] != 0:
                dia = cal[semana][dia_semana]
                btn.config(text=str(dia), state='normal')
                
                # Destacar dia atual
                if (self.ano_atual == hoje.year and 
                    self.mes_atual == hoje.month and 
                    dia == hoje.day):
                    btn.config(bg=self.cores['destaque'], fg=self.cores['fundo_principal'])
                else:
                    btn.config(bg=self.cores['fundo_card'], fg=self.cores['texto_principal'])
            else:
                btn.config(text="", state='disabled')
    
    def selecionar_dia(self, semana, dia_semana):
        """Seleciona um dia"""
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        if semana < len(cal) and cal[semana][dia_semana] != 0:
            dia = cal[semana][dia_semana]
            data_str = f"{dia:02d}/{self.mes_atual:02d}/{self.ano_atual}"
            
            # Se for edição de venda, adicionar hora atual
            if hasattr(self, 'incluir_hora') and self.incluir_hora:
                hora_atual = datetime.now().strftime('%H:%M')
                data_str += f" {hora_atual}"
            
            self.entry_widget.delete(0, 'end')
            self.entry_widget.insert(0, data_str)
            
            if self.callback:
                self.callback(data_str)
            
            self.janela.destroy()
    
    def definir_hoje(self):
        """Define a data de hoje"""
        hoje = datetime.now()
        data_str = hoje.strftime('%d/%m/%Y')
        
        # Se for edição de venda, adicionar hora atual
        if hasattr(self, 'incluir_hora') and self.incluir_hora:
            data_str += f" {hoje.strftime('%H:%M')}"
        
        self.entry_widget.delete(0, 'end')
        self.entry_widget.insert(0, data_str)
        
        if self.callback:
            self.callback(data_str)
        
        self.janela.destroy()

class ServidorWeb:
    """Servidor web para aplicativo mobile"""
    def __init__(self, sistema_espetinho):
        self.sistema = sistema_espetinho
        self.app = Flask(__name__)
        self.app.secret_key = 'buteco_do_nal_2024'
        self.configurar_rotas()
        self.thread_servidor = None
        self.servidor_rodando = False
        
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
        """Configura as rotas da aplicação web"""
        
        @self.app.route('/')
        def index():
            """Página principal"""
            return render_template('index.html', 
                                 espetinhos=self.sistema.dados.get('espetinhos', {}),
                                 vendas_hoje=self.obter_vendas_hoje())
        
        @self.app.route('/api/espetinhos')
        def api_espetinhos():
            """API para obter espetinhos disponíveis"""
            return jsonify(self.sistema.dados.get('espetinhos', {}))
        
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
                if espetinho not in self.sistema.dados.get('espetinhos', {}):
                    return jsonify({'success': False, 'message': 'Espetinho não encontrado'}), 400
                
                # Obter dados do espetinho
                dados_espetinho = self.sistema.dados['espetinhos'][espetinho]
                valor_unitario = dados_espetinho['valor']
                total = valor_unitario * quantidade

                # Tipo de venda (normal / bonificação)
                tipo_venda = data.get('tipo_venda', 'normal')

                # Tipo de consumo (para app mobile, padrão local)
                tipo_consumo = data.get('tipo_consumo', 'local')

                # Valor realmente cobrado
                valor_cobrado = 0.0 if tipo_venda == 'bonificacao' else total

                # Data/hora e competência
                data_venda = datetime.now().strftime('%d/%m/%Y %H:%M')
                try:
                    competencia = datetime.now().strftime('%Y-%m')
                except Exception:
                    competencia = None
                
                # Verificar se deve alterar estoque
                alterar_estoque = data.get('alterar_estoque', True)
                
                # Verificar estoque se necessário
                if alterar_estoque:
                    estoque_atual = self.sistema.dados['espetinhos'][espetinho]['estoque']
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
                    'origem': 'mobile',  # Identificar venda mobile
                    'tipo_venda': tipo_venda,
                    'valor_cobrado': valor_cobrado,
                    'tipo_consumo': tipo_consumo,
                    'competencia': competencia
                }
                
                # Adicionar venda
                if 'vendas' not in self.sistema.dados:
                    self.sistema.dados['vendas'] = []
                
                self.sistema.dados['vendas'].append(venda)
                
                # Atualizar estoque apenas se necessário
                if alterar_estoque:
                    self.sistema.dados['espetinhos'][espetinho]['estoque'] -= quantidade
                
                # Salvar dados
                if self.sistema.salvar_dados():
                    # Atualizar interface desktop AUTOMATICAMENTE
                    self.sistema.root.after(0, self.sistema.atualizar_lista_vendas)
                    self.sistema.root.after(0, self.sistema.atualizar_lista_espetinhos)
                    self.sistema.root.after(0, self.sistema.atualizar_dashboard)
                    
                    # Mostrar notificação de venda mobile
                    self.sistema.root.after(0, lambda: self.sistema.mostrar_notificacao_mobile(
                        f"📱 Venda Mobile: {quantidade}x {espetinho} - R$ {total:.2f}"
                    ))
                    
                    # Animar indicador mobile
                    self.sistema.root.after(0, lambda: self.sistema.animar_indicador_mobile())
                    
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
            try:
                # Adicionar origem se não existir
                for venda in self.sistema.dados['vendas']:
                    if 'origem' not in venda:
                        venda['origem'] = 'desktop'
                
                return jsonify(self.sistema.dados['vendas'])
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/despesas')
        def api_despesas():
            """API para obter todas as despesas do histórico"""
            try:
                return jsonify(self.sistema.dados.get('despesas', []))
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/status')
        def api_status():
            """API para verificar status do sistema"""
            return jsonify({
                'status': 'online',
                'total_vendas': len(self.sistema.dados.get('vendas', [])),
                'vendas_hoje': len(self.obter_vendas_hoje()),
                'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            })
        
        @self.app.route('/api/vendas/<int:indice>', methods=['DELETE'])
        def api_excluir_venda(indice):
            """API para excluir venda por índice"""
            try:
                # Obter vendas de hoje para encontrar a venda correta
                hoje = datetime.now().strftime('%d/%m/%Y')
                vendas_hoje = []
                indices_hoje = []
                
                for i, venda in enumerate(self.sistema.dados.get('vendas', [])):
                    if venda.get('data', '').startswith(hoje):
                        vendas_hoje.append(venda)
                        indices_hoje.append(i)
                
                # Verificar se o índice é válido para vendas de hoje
                if indice < 0 or indice >= len(vendas_hoje):
                    return jsonify({'success': False, 'message': 'Venda não encontrada'}), 404
                
                # Obter o índice real da venda no array global
                indice_real = indices_hoje[indice]
                venda = self.sistema.dados['vendas'][indice_real]
                
                # Debug: mostrar qual venda está sendo excluída
                print(f"DEBUG: Excluindo venda {indice} de hoje -> índice real {indice_real}")
                print(f"DEBUG: Venda: {venda.get('espetinho', 'N/A')} - R$ {venda.get('total', 0):.2f}")
                
                # Se for venda com espetinho e alterou estoque, devolver ao estoque
                if 'espetinho' in venda and venda.get('alterou_estoque', True):
                    espetinho = venda['espetinho']
                    quantidade = venda['quantidade']
                    self.sistema.dados['espetinhos'][espetinho]['estoque'] += quantidade
                
                # Remover venda usando o índice real
                del self.sistema.dados['vendas'][indice_real]
                
                # Salvar dados
                if self.sistema.salvar_dados():
                    # Atualizar interface desktop AUTOMATICAMENTE
                    self.sistema.root.after(0, self.sistema.atualizar_lista_vendas)
                    self.sistema.root.after(0, self.sistema.atualizar_lista_espetinhos)
                    self.sistema.root.after(0, self.sistema.atualizar_dashboard)
                    
                    # Mostrar notificação de exclusão mobile
                    self.sistema.root.after(0, lambda: self.sistema.mostrar_notificacao_mobile(
                        f"🗑️ Venda Mobile Excluída: {venda.get('espetinho', 'N/A')} - R$ {venda['total']:.2f}"
                    ))
                    
                    # Animar indicador mobile
                    self.sistema.root.after(0, lambda: self.sistema.animar_indicador_mobile())
                    
                    return jsonify({'success': True, 'message': 'Venda excluída com sucesso!'})
                else:
                    return jsonify({'success': False, 'message': 'Erro ao salvar dados'}), 500
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Erro: {str(e)}'}), 500
    
    def obter_vendas_hoje(self):
        """Obtém vendas do dia atual"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        vendas_hoje = []
        
        for venda in self.sistema.dados.get('vendas', []):
            if venda.get('data', '').startswith(hoje):
                # Garantir que a venda tenha origem definida
                if 'origem' not in venda:
                    venda['origem'] = 'desktop'  # Vendas antigas são consideradas desktop
                vendas_hoje.append(venda)
        
        return vendas_hoje
    
    def iniciar_servidor(self, porta=5000):
        """Inicia o servidor web em thread separada"""
        if self.servidor_rodando:
            return
            
        def rodar_servidor():
            try:
                self.servidor_rodando = True
                self.app.run(host='0.0.0.0', port=porta, debug=False, threaded=True, use_reloader=False)
            except Exception as e:
                print(f"Erro no servidor web: {e}")
                self.servidor_rodando = False
        
        self.thread_servidor = threading.Thread(target=rodar_servidor, daemon=True)
        self.thread_servidor.start()
        
        # Aguardar um pouco para o servidor inicializar
        import time
        time.sleep(1)
        
        if self.servidor_rodando:
            ip = self.obter_ip_local()
            print(f"\n🌐 SERVIDOR WEB INICIADO!")
            print(f"📱 Acesse pelo celular: http://{ip}:{porta}")
            print(f"💻 Acesse pelo computador: http://localhost:{porta}")
            print(f"🔄 Sincronização em tempo real ativa!")
            print(f"⚠️  Mantenha o sistema desktop aberto para o app funcionar\n")
            
            # Atualizar status no sistema desktop
            if hasattr(self.sistema, 'atualizar_status_web'):
                self.sistema.atualizar_status_web("🌐 Web: Online")

class SistemaEspetinho:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍖 Buteco do Nal - Sistema de Controle Moderno")
        
        # Configuração responsiva para telas pequenas
        self.root.state('zoomed')  # Maximiza a janela
        self.root.minsize(800, 600)  # Tamanho mínimo
        self.root.configure(bg='#1a1a1a')
        
        # Configurar redimensionamento
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Obter tamanho da tela para responsividade
        self.obter_tamanho_tela()  # Preto moderno
        self.root.resizable(True, True)
        
        # Configurar ícone da janela (se disponível)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configurar estilo moderno
        self.configurar_estilo_moderno()
        
        # Inicializar sistema de modais modernos
        self.modal = ModalModerno(self.root, self.cores)
        
        # Arquivo para salvar os dados
        self.arquivo_dados = "dados_espetinho.json"
        
        # Catálogo de espetinhos com valores fixos, custos e estoque inicial
        self.espetinhos = {
            "GADO": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "PORCO": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "FRANGO": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "TULIPA": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "CORAÇÃO": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "MEDALHÃO DE CARNE": {"valor": 9.00, "custo": 7.41, "estoque": 0},
            "MEDALHÃO DE FRANGO": {"valor": 9.00, "custo": 7.41, "estoque": 0},
            "QUEIJO": {"valor": 9.00, "custo": 7.41, "estoque": 0},
            "KAFTA": {"valor": 7.00, "custo": 5.50, "estoque": 0},
            "LINGUIÇA DEFUMADA": {"valor": 6.00, "custo": 4.50, "estoque": 0},
            "PÃO DE ALHO": {"valor": 4.00, "custo": 3.00, "estoque": 0},
            "CAMARÃO": {"valor": 10.00, "custo": 8.00, "estoque": 0}
        }
        
        # Carregar dados existentes
        self.dados = self.carregar_dados()
        
        # Inicializar servidor web
        self.servidor_web = ServidorWeb(self)
        self.iniciar_servidor_web()
        
        self.criar_interface()
    
    def iniciar_servidor_web(self):
        """Inicia o servidor web automaticamente"""
        try:
            # Verificar se Flask está instalado
            import flask
            self.servidor_web.iniciar_servidor()
            self.atualizar_status_web("🌐 Web: Online")
        except ImportError:
            print("⚠️  Flask não encontrado. Instalando...")
            self.atualizar_status_web("🌐 Web: Instalando...")
            try:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3"])
                print("✅ Flask instalado com sucesso!")
                self.servidor_web.iniciar_servidor()
                self.atualizar_status_web("🌐 Web: Online")
            except Exception as e:
                print(f"❌ Erro ao instalar Flask: {e}")
                print("💡 Instale manualmente: pip install Flask")
                self.atualizar_status_web("🌐 Web: Erro")
    
    def atualizar_status_web(self, status):
        """Atualiza o status do servidor web no header"""
        if hasattr(self, 'label_web_status'):
            self.label_web_status.config(text=status)
    
    def obter_tamanho_tela(self):
        """Obtém o tamanho da tela para responsividade"""
        self.root.update_idletasks()
        self.largura_tela = self.root.winfo_screenwidth()
        self.altura_tela = self.root.winfo_screenheight()
        
        # Ajustar para telas pequenas
        if self.largura_tela < 1024:
            self.fator_escala = 0.8
        elif self.largura_tela < 1366:
            self.fator_escala = 0.9
        else:
            self.fator_escala = 1.0
    
    def configurar_estilo_moderno(self):
        """Configura o estilo visual moderno do sistema"""
        # Paleta de cores moderna
        self.cores = {
            'fundo_principal': '#1a1a1a',      # Preto moderno
            'fundo_secundario': '#2d2d2d',     # Cinza escuro
            'fundo_card': '#3a3a3a',          # Cinza médio
            'fundo_claro': '#4a4a4a',         # Cinza claro
            'texto_principal': '#ffffff',      # Branco
            'texto_secundario': '#b0b0b0',    # Cinza claro
            'destaque': '#00d4aa',            # Verde água moderno
            'destaque_hover': '#00b894',      # Verde água hover
            'sucesso': '#00d4aa',             # Verde moderno
            'erro': '#ff6b6b',                # Vermelho moderno
            'aviso': '#feca57',               # Amarelo moderno
            'info': '#74b9ff',                # Azul moderno
            'borda': '#555555',               # Cinza borda
            'gradiente_inicio': '#667eea',    # Azul gradiente
            'gradiente_fim': '#764ba2'        # Roxo gradiente
        }
        
        # Configurar estilo do ttk moderno
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar fontes responsivas
        tamanho_base = int(9 * self.fator_escala)
        self.fonte_principal = ('Segoe UI', max(8, tamanho_base))
        self.fonte_titulo = ('Segoe UI', max(12, int(16 * self.fator_escala)), 'bold')
        self.fonte_subtitulo = ('Segoe UI', max(10, int(12 * self.fator_escala)), 'bold')
        self.fonte_pequena = ('Segoe UI', max(7, int(8 * self.fator_escala)))
        
        # Estilos personalizados modernos
        style.configure('TNotebook', 
                       background=self.cores['fundo_principal'],
                       borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.cores['fundo_secundario'],
                       foreground=self.cores['texto_principal'],
                       padding=[25, 12],
                       font=self.fonte_principal)
        style.map('TNotebook.Tab', 
                 background=[('selected', self.cores['destaque']),
                           ('active', self.cores['fundo_card'])],
                 foreground=[('selected', self.cores['fundo_principal']),
                           ('active', self.cores['texto_principal'])])
        
        style.configure('TLabelFrame', 
                       background=self.cores['fundo_principal'],
                       foreground=self.cores['texto_principal'],
                       borderwidth=0,
                       relief='flat')
        style.configure('TLabelFrame.Label',
                       background=self.cores['fundo_principal'],
                       foreground=self.cores['destaque'],
                       font=self.fonte_subtitulo)
        
        # Botões modernos
        style.configure('Modern.TButton',
                       background=self.cores['destaque'],
                       foreground=self.cores['fundo_principal'],
                       font=self.fonte_principal,
                       padding=[15, 8],
                       borderwidth=0,
                       relief='flat')
        style.map('Modern.TButton',
                 background=[('active', self.cores['destaque_hover']),
                           ('pressed', self.cores['fundo_card'])])
        
        style.configure('Secondary.TButton',
                       background=self.cores['fundo_card'],
                       foreground=self.cores['texto_principal'],
                       font=self.fonte_principal,
                       padding=[12, 6],
                       borderwidth=1,
                       relief='flat')
        style.map('Secondary.TButton',
                 background=[('active', self.cores['fundo_claro']),
                           ('pressed', self.cores['fundo_secundario'])])
        
        # Entradas modernas
        style.configure('Modern.TEntry',
                       background=self.cores['fundo_card'],
                       foreground=self.cores['texto_principal'],
                       font=self.fonte_principal,
                       borderwidth=1,
                       relief='flat',
                       fieldbackground=self.cores['fundo_card'])
        
        style.configure('Modern.TCombobox',
                       background=self.cores['fundo_card'],
                       foreground=self.cores['texto_principal'],
                       font=self.fonte_principal,
                       borderwidth=1,
                       relief='flat',
                       fieldbackground=self.cores['fundo_card'])
        
        # Treeview moderno
        style.configure('Modern.Treeview',
                       background=self.cores['fundo_card'],
                       foreground=self.cores['texto_principal'],
                       font=self.fonte_principal,
                       borderwidth=0,
                       relief='flat',
                       rowheight=25)
        style.configure('Modern.Treeview.Heading',
                       background=self.cores['fundo_secundario'],
                       foreground=self.cores['texto_principal'],
                       font=self.fonte_subtitulo,
                       borderwidth=0,
                       relief='flat')
        style.map('Modern.Treeview',
                 background=[('selected', self.cores['destaque'])],
                 foreground=[('selected', self.cores['fundo_principal'])])
        
    def carregar_dados(self):
        """Carrega os dados salvos do arquivo"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    # Garantir que a estrutura tenha espetinhos
                    if 'espetinhos' not in dados:
                        dados['espetinhos'] = self.espetinhos
                    return dados
            except:
                return {"vendas": [], "despesas": [], "espetinhos": self.espetinhos}
        return {"vendas": [], "despesas": [], "espetinhos": self.espetinhos}
    
    def salvar_dados(self):
        """Salva os dados no arquivo"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
            return False

    def consolidar_bancos(self):
        """Importa e consolida múltiplos arquivos JSON em um único banco"""
        try:
            # Abrir diálogo para selecionar múltiplos arquivos
            arquivos = filedialog.askopenfilenames(
                title="Selecione os arquivos JSON para consolidar",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not arquivos:
                return
            
            if len(arquivos) == 0:
                messagebox.showinfo("Info", "Nenhum arquivo selecionado.")
                return
            
            # Confirmar ação
            resposta = messagebox.askyesno(
                "Confirmar Consolidação",
                f"Você selecionou {len(arquivos)} arquivo(s).\n\n"
                "Isso irá:\n"
                "- Juntar todas as vendas (evitando duplicatas)\n"
                "- Juntar todas as despesas (evitando duplicatas)\n"
                "- Manter espetinhos do arquivo principal\n"
                "- Fazer backup antes de consolidar\n\n"
                "Deseja continuar?"
            )
            
            if not resposta:
                return
            
            # Fazer backup antes
            try:
                backup_nome = f"backup_antes_consolidacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(backup_nome, 'w', encoding='utf-8') as f:
                    json.dump(self.dados, f, ensure_ascii=False, indent=2)
            except Exception as e:
                messagebox.showwarning("Aviso", f"Não foi possível fazer backup: {str(e)}")
            
            # Dados consolidados (começar com dados atuais)
            # Suportar ambos os nomes: fechamentos_mensais e fechamentos_mes
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
            # Considera também origem e pedido_id para evitar duplicatas de pedidos online
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
            
            # Processar cada arquivo
            total_vendas_adicionadas = 0
            total_despesas_adicionadas = 0
            arquivos_processados = 0
            
            for arquivo_path in arquivos:
                try:
                    with open(arquivo_path, 'r', encoding='utf-8') as f:
                        dados_arquivo = json.load(f)
                    
                    # Processar vendas (preservando TODOS os campos, incluindo data/hora completa)
                    vendas_arquivo = dados_arquivo.get("vendas", [])
                    for venda in vendas_arquivo:
                        chave = chave_venda(venda)
                        if chave not in vendas_unicas:
                            # Criar cópia completa da venda preservando TODOS os campos
                            venda_completa = dict(venda)  # Copia todos os campos existentes
                            
                            # Garantir que campos obrigatórios existam
                            if "data" not in venda_completa:
                                continue  # Pula vendas sem data
                            
                            # Preservar todos os campos: data/hora, tipo_venda, valor_cobrado, 
                            # tipo_consumo, competencia, origem, pedido_id, alterou_estoque, etc.
                            dados_consolidados["vendas"].append(venda_completa)
                            vendas_unicas.add(chave)
                            total_vendas_adicionadas += 1
                    
                    # Processar despesas (preservando TODOS os campos, incluindo data completa)
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
                    
                    # Processar fechamentos mensais (se existirem)
                    # Suportar ambos os nomes: fechamentos_mensais e fechamentos_mes
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
                    messagebox.showerror("Erro", f"Erro ao processar arquivo {os.path.basename(arquivo_path)}:\n{str(e)}")
                    continue
            
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
            
            # Atualizar dados do sistema
            self.dados = dados_consolidados
            
            # Salvar dados consolidados
            if self.salvar_dados():
                # Atualizar interface
                self.atualizar_dashboard()
                self.atualizar_lista_vendas()
                self.atualizar_lista_despesas()
                
                messagebox.showinfo(
                    "✅ Consolidação Concluída!",
                    f"Consolidação realizada com sucesso!\n\n"
                    f"📊 Arquivos processados: {arquivos_processados}/{len(arquivos)}\n"
                    f"💰 Vendas adicionadas: {total_vendas_adicionadas}\n"
                    f"💸 Despesas adicionadas: {total_despesas_adicionadas}\n"
                    f"📦 Total de vendas: {len(dados_consolidados['vendas'])}\n"
                    f"📋 Total de despesas: {len(dados_consolidados['despesas'])}\n\n"
                    f"Backup salvo como: {backup_nome}"
                )
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados consolidados.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consolidar bancos:\n{str(e)}")

    def get_valor_cobrado(self, venda):
        """
        Retorna o valor realmente cobrado de uma venda.
        Compatível com vendas antigas (sem campo valor_cobrado).
        """
        try:
            return float(venda.get('valor_cobrado', venda.get('total', 0)))
        except Exception:
            return venda.get('total', 0)
    
    def criar_interface(self):
        """Cria a interface moderna do sistema"""
        # Header com título e status
        self.criar_header()
        
        # Notebook para abas responsivo
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configurar redimensionamento do notebook
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Aba Dashboard
        self.criar_aba_dashboard(notebook)
        
        # Aba de Espetinhos
        self.criar_aba_espetinhos(notebook)
        
        # Aba de Vendas
        self.criar_aba_vendas(notebook)
        
        # Aba de Despesas
        self.criar_aba_despesas(notebook)
        
        # Aba de Relatórios
        self.criar_aba_relatorios(notebook)
        
        # Configurar atalhos de teclado
        self.configurar_atalhos()
    
    def criar_header(self):
        """Cria o header moderno do sistema"""
        header_frame = tk.Frame(self.root, bg=self.cores['fundo_secundario'], height=80)
        header_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        header_frame.grid_propagate(False)
        
        # Título principal
        titulo = tk.Label(header_frame, 
                         text="🍖 BUTECO DO NAL", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_secundario'])
        titulo.pack(side='left', padx=20, pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(header_frame, 
                           text="Sistema de Controle Moderno", 
                           font=self.fonte_pequena, 
                           fg=self.cores['texto_secundario'], 
                           bg=self.cores['fundo_secundario'])
        subtitulo.pack(side='left', padx=(0, 20), pady=20)
        
        # Status do sistema (lado direito)
        self.label_status = tk.Label(header_frame, 
                                   text="🟢 Sistema Online", 
                                   font=self.fonte_pequena, 
                                   fg=self.cores['sucesso'], 
                                   bg=self.cores['fundo_secundario'])
        self.label_status.pack(side='right', padx=20, pady=20)
        
        # Status do servidor web
        self.label_web_status = tk.Label(header_frame, 
                                        text="🌐 Web: Iniciando...", 
                                        font=self.fonte_pequena, 
                                        fg=self.cores['info'], 
                                        bg=self.cores['fundo_secundario'])
        self.label_web_status.pack(side='right', padx=(0, 20), pady=20)
        
        # Indicador de vendas mobile
        self.label_mobile_indicator = tk.Label(header_frame, 
                                             text="📱", 
                                             font=('Segoe UI', 16), 
                                             fg=self.cores['destaque'], 
                                             bg=self.cores['fundo_secundario'])
        self.label_mobile_indicator.pack(side='right', padx=(0, 10), pady=20)
        
        # Data/hora atual
        self.label_data = tk.Label(header_frame, 
                                 text=datetime.now().strftime("%d/%m/%Y %H:%M"), 
                                 font=self.fonte_pequena, 
                                 fg=self.cores['texto_secundario'], 
                                 bg=self.cores['fundo_secundario'])
        self.label_data.pack(side='right', padx=(0, 20), pady=20)
        
        # Atualizar data/hora a cada minuto
        self.atualizar_data_hora()
    
    def criar_aba_dashboard(self, notebook):
        """Cria a aba do dashboard moderno"""
        frame_dashboard = ttk.Frame(notebook)
        notebook.add(frame_dashboard, text="📊 Dashboard")
        
        # Título do dashboard
        titulo = tk.Label(frame_dashboard, 
                         text="📊 DASHBOARD EXECUTIVO", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=20)
        
        # Frame para métricas principais responsivo
        self.frame_metricas = tk.Frame(frame_dashboard, bg=self.cores['fundo_principal'])
        self.frame_metricas.pack(fill='x', padx=10, pady=10)
        
        # Configurar grid responsivo
        self.frame_metricas.grid_columnconfigure(0, weight=1)
        self.frame_metricas.grid_columnconfigure(1, weight=1)
        self.frame_metricas.grid_columnconfigure(2, weight=1)
        self.frame_metricas.grid_columnconfigure(3, weight=1)
        
        # Métricas em cards
        self.criar_card_metricas(self.frame_metricas)
        
        # Frame para gráficos e análises
        frame_analises = tk.Frame(frame_dashboard, bg=self.cores['fundo_principal'])
        frame_analises.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Gráfico de vendas por dia (simulado)
        self.criar_grafico_vendas(frame_analises)
        
        # Atualizar dashboard
        self.atualizar_dashboard()
    
    def criar_card_metricas(self, parent):
        """Cria os cards de métricas principais responsivos"""
        # Card 1: Vendas Hoje
        self.card_vendas_hoje = self.criar_card(parent, "💰 Vendas Hoje", "R$ 0,00", self.cores['sucesso'])
        self.card_vendas_hoje.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        # Card 2: Estoque Baixo
        self.card_estoque_baixo = self.criar_card(parent, "⚠️ Estoque Baixo", "0 itens", self.cores['aviso'])
        self.card_estoque_baixo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Card 3: Lucro do Dia
        self.card_lucro_hoje = self.criar_card(parent, "📈 Lucro Hoje", "R$ 0,00", self.cores['info'])
        self.card_lucro_hoje.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        
        # Card 4: Total Vendas
        self.card_total_vendas = self.criar_card(parent, "📊 Total Vendas", "R$ 0,00", self.cores['destaque'])
        self.card_total_vendas.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        # Configurar grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
    
    def criar_card(self, parent, titulo, valor, cor):
        """Cria um card de métrica"""
        card = tk.Frame(parent, bg=self.cores['fundo_card'], relief='flat', bd=1)
        
        # Título do card
        label_titulo = tk.Label(card, text=titulo, 
                              font=self.fonte_pequena, 
                              fg=self.cores['texto_secundario'], 
                              bg=self.cores['fundo_card'])
        label_titulo.pack(pady=(15, 5))
        
        # Valor do card
        label_valor = tk.Label(card, text=valor, 
                             font=('Segoe UI', 18, 'bold'), 
                             fg=cor, 
                             bg=self.cores['fundo_card'])
        label_valor.pack(pady=(0, 15))
        
        return card
    
    def criar_grafico_vendas(self, parent):
        """Cria um gráfico simples de vendas"""
        frame_grafico = tk.LabelFrame(parent, text="📈 Vendas dos Últimos 7 Dias", 
                                    font=self.fonte_subtitulo,
                                    fg=self.cores['destaque'],
                                    bg=self.cores['fundo_principal'])
        frame_grafico.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas para o gráfico (simulado)
        canvas = tk.Canvas(frame_grafico, bg=self.cores['fundo_card'], height=200)
        canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Desenhar gráfico simples
        self.desenhar_grafico_simples(canvas)
    
    def desenhar_grafico_simples(self, canvas):
        """Desenha um gráfico simples de barras"""
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Dados simulados para os últimos 7 dias
        dados = [120, 150, 200, 180, 250, 300, 280]
        max_valor = max(dados) if dados else 1
        
        # Desenhar barras
        bar_width = (width - 100) // len(dados)
        for i, valor in enumerate(dados):
            bar_height = (valor / max_valor) * (height - 50)
            x1 = 50 + i * bar_width
            y1 = height - 25
            x2 = x1 + bar_width - 10
            y2 = y1 - bar_height
            
            # Cor da barra (gradiente)
            cor = self.cores['destaque'] if i == len(dados) - 1 else self.cores['info']
            canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")
            
            # Valor no topo da barra
            canvas.create_text(x1 + bar_width//2, y2 - 10, 
                             text=f"R$ {valor}", 
                             fill=self.cores['texto_principal'],
                             font=self.fonte_pequena)
    
    def atualizar_data_hora(self):
        """Atualiza a data e hora no header"""
        self.label_data.config(text=datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.root.after(60000, self.atualizar_data_hora)  # Atualizar a cada minuto
    
    def atualizar_dashboard(self):
        """Atualiza as métricas do dashboard"""
        # Calcular vendas de hoje
        hoje = datetime.now().strftime('%d/%m/%Y')
        vendas_hoje = sum(self.get_valor_cobrado(venda) for venda in self.dados['vendas'] 
                         if venda['data'].startswith(hoje))
        
        # Calcular estoque baixo
        estoque_baixo = sum(1 for espetinho in self.dados['espetinhos'].values() 
                           if espetinho['estoque'] < 10)
        
        # Calcular lucro de hoje
        lucro_hoje = 0
        for venda in self.dados['vendas']:
            if venda['data'].startswith(hoje) and 'espetinho' in venda:
                espetinho = venda['espetinho']
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    lucro_hoje += (venda['valor_unitario'] - custo_unitario) * venda['quantidade']
        
        # Calcular total de vendas
        total_vendas = sum(self.get_valor_cobrado(venda) for venda in self.dados['vendas'])
        
        # Atualizar cards do dashboard
        try:
            if hasattr(self, 'card_vendas_hoje'):
                # Atualizar vendas hoje
                labels_vendas = self.card_vendas_hoje.winfo_children()
                if len(labels_vendas) >= 2:
                    labels_vendas[1].config(text=f"R$ {vendas_hoje:.2f}")
                
                # Atualizar estoque baixo
                labels_estoque = self.card_estoque_baixo.winfo_children()
                if len(labels_estoque) >= 2:
                    labels_estoque[1].config(text=f"{estoque_baixo} itens")
                
                # Atualizar lucro hoje
                labels_lucro = self.card_lucro_hoje.winfo_children()
                if len(labels_lucro) >= 2:
                    labels_lucro[1].config(text=f"R$ {lucro_hoje:.2f}")
                
                # Atualizar total vendas
                labels_total = self.card_total_vendas.winfo_children()
                if len(labels_total) >= 2:
                    labels_total[1].config(text=f"R$ {total_vendas:.2f}")
        except Exception as e:
            print(f"Erro ao atualizar dashboard: {e}")
    
    def configurar_atalhos(self):
        """Configura atalhos de teclado"""
        self.root.bind('<Control-n>', lambda e: self.focar_aba_vendas())
        self.root.bind('<Control-e>', lambda e: self.focar_aba_espetinhos())
        self.root.bind('<Control-d>', lambda e: self.focar_aba_despesas())
        self.root.bind('<Control-r>', lambda e: self.focar_aba_relatorios())
        self.root.bind('<F5>', lambda e: self.atualizar_todas_abas())
    
    def focar_aba_vendas(self):
        """Foca na aba de vendas"""
        # Implementar foco na aba
        pass
    
    def focar_aba_espetinhos(self):
        """Foca na aba de espetinhos"""
        # Implementar foco na aba
        pass
    
    def focar_aba_despesas(self):
        """Foca na aba de despesas"""
        # Implementar foco na aba
        pass
    
    def focar_aba_relatorios(self):
        """Foca na aba de relatórios"""
        # Implementar foco na aba
        pass
    
    def atualizar_todas_abas(self):
        """Atualiza todas as abas"""
        self.atualizar_dashboard()
        # Atualizar outras abas
        pass
    
    def mostrar_notificacao_sucesso(self, mensagem):
        """Mostra uma notificação de sucesso moderna"""
        # Criar janela de notificação
        notif = tk.Toplevel(self.root)
        notif.title("Sucesso")
        notif.geometry("400x100")
        notif.configure(bg=self.cores['fundo_secundario'])
        notif.resizable(False, False)
        
        # Centralizar na tela
        notif.transient(self.root)
        notif.grab_set()
        
        # Posicionar no centro
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        notif.geometry(f"400x100+{x}+{y}")
        
        # Ícone de sucesso
        label_icon = tk.Label(notif, text="✅", font=('Segoe UI', 24), 
                            fg=self.cores['sucesso'], bg=self.cores['fundo_secundario'])
        label_icon.pack(pady=10)
        
        # Mensagem
        label_msg = tk.Label(notif, text=mensagem, font=self.fonte_principal, 
                           fg=self.cores['texto_principal'], bg=self.cores['fundo_secundario'])
        label_msg.pack()
        
        # Fechar automaticamente após 3 segundos
        notif.after(3000, notif.destroy)
    
    def mostrar_notificacao_erro(self, mensagem):
        """Mostra uma notificação de erro moderna"""
        # Criar janela de notificação
        notif = tk.Toplevel(self.root)
        notif.title("Erro")
        notif.geometry("400x100")
        notif.configure(bg=self.cores['fundo_secundario'])
        notif.resizable(False, False)
        
        # Centralizar na tela
        notif.transient(self.root)
        notif.grab_set()
        
        # Posicionar no centro
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        notif.geometry(f"400x100+{x}+{y}")
        
        # Ícone de erro
        label_icon = tk.Label(notif, text="❌", font=('Segoe UI', 24), 
                            fg=self.cores['erro'], bg=self.cores['fundo_secundario'])
        label_icon.pack(pady=10)
        
        # Mensagem
        label_msg = tk.Label(notif, text=mensagem, font=self.fonte_principal, 
                           fg=self.cores['texto_principal'], bg=self.cores['fundo_secundario'])
        label_msg.pack()
        
        # Fechar automaticamente após 4 segundos
        notif.after(4000, notif.destroy)
    
    def mostrar_notificacao_mobile(self, mensagem):
        """Mostra notificação especial para vendas mobile"""
        # Criar janela de notificação mobile
        notif = tk.Toplevel(self.root)
        notif.title("📱 Venda Mobile")
        notif.geometry("450x120")
        notif.configure(bg=self.cores['fundo_secundario'])
        notif.resizable(False, False)
        
        # Centralizar na tela
        notif.transient(self.root)
        notif.grab_set()
        
        # Posicionar no centro
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 225
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 60
        notif.geometry(f"450x120+{x}+{y}")
        
        # Ícone mobile
        label_icon = tk.Label(notif, text="📱", font=('Segoe UI', 20), 
                            fg=self.cores['info'], bg=self.cores['fundo_secundario'])
        label_icon.pack(pady=10)
        
        # Mensagem
        label_msg = tk.Label(notif, text=mensagem, font=self.fonte_principal, 
                           fg=self.cores['texto_principal'], bg=self.cores['fundo_secundario'])
        label_msg.pack()
        
        # Fechar automaticamente após 3 segundos
        notif.after(3000, notif.destroy)
    
    def animar_indicador_mobile(self):
        """Anima o indicador mobile quando uma venda é lançada"""
        if hasattr(self, 'label_mobile_indicator'):
            # Piscar o indicador
            self.label_mobile_indicator.config(fg=self.cores['sucesso'])
            self.root.after(500, lambda: self.label_mobile_indicator.config(fg=self.cores['destaque']))
            self.root.after(1000, lambda: self.label_mobile_indicator.config(fg=self.cores['sucesso']))
            self.root.after(1500, lambda: self.label_mobile_indicator.config(fg=self.cores['destaque']))
    
    def criar_aba_espetinhos(self, notebook):
        """Cria a aba de espetinhos moderna"""
        frame_espetinhos = ttk.Frame(notebook)
        notebook.add(frame_espetinhos, text="🍖 Espetinhos")
        
        # Título moderno
        titulo = tk.Label(frame_espetinhos, text="🍖 CATÁLOGO DE ESPETINHOS", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=20)
        
        # Frame para adicionar estoque
        frame_estoque = ttk.LabelFrame(frame_espetinhos, text="📦 Adicionar Estoque")
        frame_estoque.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_estoque, text="Espetinho:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.combo_estoque = ttk.Combobox(frame_estoque, width=25, state='readonly', style='Modern.TCombobox')
        self.combo_estoque.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_estoque, text="Quantidade:", font=self.fonte_principal).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        self.entry_qtd_estoque = ttk.Entry(frame_estoque, width=10, style='Modern.TEntry')
        self.entry_qtd_estoque.grid(row=0, column=3, padx=10, pady=10)
        self.entry_qtd_estoque.insert(0, "0")  # Valor padrão 0
        
        ttk.Button(frame_estoque, text="📦 Adicionar ao Estoque", command=self.adicionar_estoque, style='Modern.TButton').grid(row=0, column=4, padx=10, pady=10)
        ttk.Button(frame_estoque, text="🔄 Zerar Este", command=self.zerar_estoque_individual, style='Secondary.TButton').grid(row=0, column=5, padx=10, pady=10)
        
        # Frame para editar custos
        frame_custo = ttk.LabelFrame(frame_espetinhos, text="💰 Editar Custos")
        frame_custo.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_custo, text="Espetinho:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.combo_custo = ttk.Combobox(frame_custo, width=25, state='readonly', style='Modern.TCombobox')
        self.combo_custo.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_custo, text="Novo Custo:", font=self.fonte_principal).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        self.entry_novo_custo = ttk.Entry(frame_custo, width=10, style='Modern.TEntry')
        self.entry_novo_custo.grid(row=0, column=3, padx=10, pady=10)
        
        ttk.Button(frame_custo, text="💰 Atualizar Custo", command=self.atualizar_custo, style='Modern.TButton').grid(row=0, column=4, padx=10, pady=10)
        
        # Frame para zerar estoque
        frame_zerar = ttk.LabelFrame(frame_espetinhos, text="🔄 Controle de Estoque")
        frame_zerar.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_zerar, text="Ação:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        ttk.Button(frame_zerar, text="🔄 Zerar Todo Estoque", command=self.zerar_todo_estoque, style='Modern.TButton').grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(frame_zerar, text="📦 Zerar Estoque Individual", command=self.zerar_estoque_individual, style='Secondary.TButton').grid(row=0, column=2, padx=10, pady=10)
        
        
        # Lista de espetinhos
        frame_lista = ttk.LabelFrame(frame_espetinhos, text="📋 Espetinhos Cadastrados")
        frame_lista.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview moderno para mostrar espetinhos
        colunas = ('Espetinho', 'Custo', 'Venda', 'Lucro', 'Markup', 'Margem', 'Estoque')
        altura_tabela = max(8, int(12 * self.fator_escala))
        self.tree_espetinhos = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=altura_tabela, style='Modern.Treeview')
        
        # Larguras otimizadas para cada coluna (responsivo)
        larguras = {
            'Espetinho': max(100, int(120 * self.fator_escala)),
            'Custo': max(70, int(80 * self.fator_escala)),
            'Venda': max(70, int(80 * self.fator_escala)),
            'Lucro': max(70, int(80 * self.fator_escala)),
            'Markup': max(70, int(80 * self.fator_escala)),
            'Margem': max(70, int(80 * self.fator_escala)),
            'Estoque': max(70, int(80 * self.fator_escala))
        }
        
        # Configurar headers
        headers = {
            'Espetinho': '🍖 Espetinho',
            'Custo': '💰 Custo',
            'Venda': '💵 Venda', 
            'Lucro': '📈 Lucro',
            'Markup': '📊 Markup',
            'Margem': '🎯 Margem',
            'Estoque': '📦 Estoque'
        }
        
        for col in colunas:
            self.tree_espetinhos.heading(col, text=headers[col])
            self.tree_espetinhos.column(col, width=larguras[col])
        
        scrollbar_espetinhos = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_espetinhos.yview)
        self.tree_espetinhos.configure(yscrollcommand=scrollbar_espetinhos.set)
        
        # Configurar scroll com mouse wheel
        self.configurar_scroll_mouse(self.tree_espetinhos)
        
        # Frame para botões de ajuda
        frame_ajuda = tk.Frame(frame_lista, bg=self.cores['fundo_principal'])
        frame_ajuda.pack(fill='x', padx=5, pady=5)
        
        # Botões de ajuda para Markup e Margem
        btn_ajuda_markup = tk.Button(frame_ajuda, 
                                   text="❓ O que é Markup?", 
                                   command=self.mostrar_tooltip_markup_simples,
                                   bg=self.cores['info'],
                                   fg=self.cores['fundo_principal'],
                                   font=self.fonte_pequena,
                                   relief='flat',
                                   padx=10,
                                   pady=5)
        btn_ajuda_markup.pack(side='left', padx=5)
        
        btn_ajuda_margem = tk.Button(frame_ajuda, 
                                   text="❓ O que é Margem?", 
                                   command=self.mostrar_tooltip_margem_simples,
                                   bg=self.cores['info'],
                                   fg=self.cores['fundo_principal'],
                                   font=self.fonte_pequena,
                                   relief='flat',
                                   padx=10,
                                   pady=5)
        btn_ajuda_margem.pack(side='left', padx=5)
        
        self.tree_espetinhos.pack(side='left', fill='both', expand=True)
        scrollbar_espetinhos.pack(side='right', fill='y')
        
        # Atualizar lista de espetinhos
        self.atualizar_lista_espetinhos()
        self.atualizar_combo_estoque()
        self.atualizar_combo_custo()
    
    def criar_aba_vendas(self, notebook):
        """Cria a aba de vendas moderna"""
        frame_vendas = ttk.Frame(notebook)
        notebook.add(frame_vendas, text="💰 Vendas")
        
        # Título moderno
        titulo = tk.Label(frame_vendas, text="💰 CONTROLE DE VENDAS", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=20)
        
        # Formulário de nova venda (compacto)
        frame_form = ttk.LabelFrame(frame_vendas, text="🛒 Nova Venda")
        frame_form.pack(fill='x', padx=20, pady=5)
        
        # Seleção de espetinho
        ttk.Label(frame_form, text="Espetinho:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.combo_espetinho = ttk.Combobox(frame_form, width=25, state='readonly', style='Modern.TCombobox')
        self.combo_espetinho.grid(row=0, column=1, padx=5, pady=5)
        self.combo_espetinho.bind('<<ComboboxSelected>>', self.on_espetinho_selected)
        
        # Quantidade
        ttk.Label(frame_form, text="Quantidade:", font=self.fonte_principal).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entry_qtd_venda = ttk.Entry(frame_form, width=10, style='Modern.TEntry')
        self.entry_qtd_venda.grid(row=0, column=3, padx=5, pady=5)
        self.entry_qtd_venda.insert(0, "1")  # Valor padrão
        self.entry_qtd_venda.bind('<KeyRelease>', lambda e: self.calcular_total_venda())
        
        # Valor unitário (preenchido automaticamente)
        ttk.Label(frame_form, text="Valor Unitário:", font=self.fonte_principal).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_valor_venda = ttk.Entry(frame_form, width=15, state='readonly', style='Modern.TEntry')
        self.entry_valor_venda.grid(row=1, column=1, padx=5, pady=5)
        
        # Total (calculado automaticamente)
        ttk.Label(frame_form, text="Total:", font=self.fonte_principal).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.label_total = tk.Label(frame_form, text="R$ 0,00", font=self.fonte_subtitulo, fg=self.cores['destaque'], bg=self.cores['fundo_principal'])
        self.label_total.grid(row=1, column=3, padx=5, pady=5)
        
        # Campo de data/hora para vendas retroativas
        ttk.Label(frame_form, text="Data/Hora:", font=self.fonte_principal).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        frame_data_venda = ttk.Frame(frame_form)
        frame_data_venda.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        self.entry_data_venda = ttk.Entry(frame_data_venda, width=15, style='Modern.TEntry')
        self.entry_data_venda.pack(side='left', padx=(0, 5))
        self.entry_data_venda.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
        
        # Botão do calendário
        ttk.Button(frame_data_venda, text="📅", command=self.abrir_calendario_venda, style='Secondary.TButton').pack(side='left', padx=(0, 5))
        
        # Botão para usar data atual
        ttk.Button(frame_data_venda, text="🕐 Agora", command=self.definir_data_atual, style='Secondary.TButton').pack(side='left')
        
        # Checkbox para controle de estoque
        self.var_alterar_estoque = tk.BooleanVar(value=True)
        self.check_estoque = tk.Checkbutton(frame_form, 
                                          text="Alterar Estoque (desmarque para venda sem estoque)",
                                          variable=self.var_alterar_estoque,
                                          bg=self.cores['fundo_principal'],
                                          fg=self.cores['texto_principal'],
                                          font=self.fonte_pequena,
                                          selectcolor=self.cores['destaque'],
                                          activebackground=self.cores['fundo_principal'],
                                          activeforeground=self.cores['texto_principal'])
        self.check_estoque.grid(row=3, column=0, columnspan=4, sticky='w', padx=5, pady=5)

        # Tipo de venda (normal / bonificação)
        ttk.Label(frame_form, text="Tipo de Venda:", font=self.fonte_principal).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.combo_tipo_venda = ttk.Combobox(frame_form, width=20, state='readonly', style='Modern.TCombobox')
        self.combo_tipo_venda['values'] = ("Normal", "Bonificação")
        self.combo_tipo_venda.grid(row=4, column=1, padx=5, pady=5)
        self.combo_tipo_venda.set("Normal")

        # Tipo de consumo (local / entrega / interno)
        ttk.Label(frame_form, text="Tipo de Consumo:", font=self.fonte_principal).grid(row=4, column=2, sticky='w', padx=5, pady=5)
        self.combo_tipo_consumo = ttk.Combobox(frame_form, width=20, state='readonly', style='Modern.TCombobox')
        self.combo_tipo_consumo['values'] = ("Local", "Entrega", "Interno")
        self.combo_tipo_consumo.grid(row=4, column=3, padx=5, pady=5)
        self.combo_tipo_consumo.set("Local")
        
        # Botão adicionar
        ttk.Button(frame_form, text="🍖 Adicionar Venda", command=self.adicionar_venda, style='Modern.TButton').grid(row=5, column=0, columnspan=4, padx=5, pady=8)
        
        # Atualizar lista de espetinhos no combobox
        self.atualizar_combo_espetinhos()
        
        # Frame para filtros e botões (distribuído pela largura total)
        frame_filtros = ttk.Frame(frame_vendas)
        frame_filtros.pack(fill='x', padx=20, pady=2)
        
        # Seção de filtros (lado esquerdo)
        frame_filtros_esquerda = ttk.Frame(frame_filtros)
        frame_filtros_esquerda.pack(side='left', fill='x', expand=True)
        
        ttk.Label(frame_filtros_esquerda, text="🔍 Filtros:", font=self.fonte_pequena).pack(side='left', padx=(0, 8))
        
        ttk.Label(frame_filtros_esquerda, text="De:", font=self.fonte_pequena).pack(side='left', padx=(0, 3))
        self.entry_data_inicial = ttk.Entry(frame_filtros_esquerda, width=12, style='Modern.TEntry')
        self.entry_data_inicial.pack(side='left', padx=(0, 15))
        self.entry_data_inicial.insert(0, "01/01/2024")
        
        ttk.Label(frame_filtros_esquerda, text="Até:", font=self.fonte_pequena).pack(side='left', padx=(0, 3))
        self.entry_data_final = ttk.Entry(frame_filtros_esquerda, width=12, style='Modern.TEntry')
        self.entry_data_final.pack(side='left', padx=(0, 15))
        self.entry_data_final.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        # Botões de filtro
        ttk.Button(frame_filtros_esquerda, text="🔍 Filtrar", command=self.filtrar_vendas, style='Secondary.TButton', width=10).pack(side='left', padx=5)
        ttk.Button(frame_filtros_esquerda, text="📋 Todas", command=self.mostrar_todas_vendas, style='Secondary.TButton', width=10).pack(side='left', padx=5)
        
        # Seção de botões de ação (lado direito)
        frame_botoes_direita = ttk.Frame(frame_filtros)
        frame_botoes_direita.pack(side='right')
        
        ttk.Button(frame_botoes_direita, text="✏️ Editar", command=self.editar_venda, style='Secondary.TButton', width=10).pack(side='left', padx=5)
        ttk.Button(frame_botoes_direita, text="🗑️ Excluir", command=self.excluir_venda, style='Secondary.TButton', width=10).pack(side='left', padx=5)
        ttk.Button(frame_botoes_direita, text="🔄 Atualizar", command=self.atualizar_lista_vendas, style='Secondary.TButton', width=10).pack(side='left', padx=5)
        
        # Lista de vendas (MAIOR) - sem botões duplicados
        frame_lista = ttk.LabelFrame(frame_vendas, text="📋 Vendas Registradas")
        frame_lista.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Treeview moderno para mostrar vendas (MÁXIMO)
        colunas = ('Data', 'Descrição', 'Quantidade', 'Valor Unit.', 'Total', 'Origem')
        altura_tabela = max(25, int(30 * self.fator_escala))  # MÁXIMO para aproveitar todo espaço economizado!
        self.tree_vendas = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=altura_tabela, style='Modern.Treeview')
        
        # Larguras otimizadas para cada coluna
        larguras = {
            'Data': max(100, int(120 * self.fator_escala)),
            'Descrição': max(150, int(200 * self.fator_escala)),
            'Quantidade': max(80, int(100 * self.fator_escala)),
            'Valor Unit.': max(100, int(120 * self.fator_escala)),
            'Total': max(100, int(120 * self.fator_escala)),
            'Origem': max(60, int(80 * self.fator_escala))
        }
        
        for col in colunas:
            self.tree_vendas.heading(col, text=col)
            self.tree_vendas.column(col, width=larguras[col])
        
        scrollbar_vendas = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_vendas.yview)
        self.tree_vendas.configure(yscrollcommand=scrollbar_vendas.set)
        
        # Configurar scroll com mouse wheel
        self.configurar_scroll_mouse(self.tree_vendas)
        
        self.tree_vendas.pack(side='left', fill='both', expand=True)
        scrollbar_vendas.pack(side='right', fill='y')
        
        # Atualizar lista de vendas
        self.atualizar_lista_vendas()
    
    def criar_aba_despesas(self, notebook):
        """Cria a aba de despesas moderna"""
        frame_despesas = ttk.Frame(notebook)
        notebook.add(frame_despesas, text="💸 Despesas")
        
        # Título moderno
        titulo = tk.Label(frame_despesas, text="💸 CONTROLE DE DESPESAS", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=20)
        
        # Formulário de nova despesa
        frame_form = ttk.LabelFrame(frame_despesas, text="💸 Nova Despesa")
        frame_form.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_form, text="Descrição:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.entry_desc_despesa = ttk.Entry(frame_form, width=30, style='Modern.TEntry')
        self.entry_desc_despesa.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_form, text="Valor:", font=self.fonte_principal).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        self.entry_valor_despesa = ttk.Entry(frame_form, width=15, style='Modern.TEntry')
        self.entry_valor_despesa.grid(row=0, column=3, padx=10, pady=10)
        
        # Campo de data/hora para despesas retroativas
        ttk.Label(frame_form, text="Data/Hora:", font=self.fonte_principal).grid(row=1, column=0, sticky='w', padx=10, pady=10)
        
        frame_data_despesa = ttk.Frame(frame_form)
        frame_data_despesa.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        self.entry_data_despesa = ttk.Entry(frame_data_despesa, width=15, style='Modern.TEntry')
        self.entry_data_despesa.pack(side='left', padx=(0, 5))
        self.entry_data_despesa.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
        
        # Botão do calendário
        ttk.Button(frame_data_despesa, text="📅", command=self.abrir_calendario_despesa, style='Secondary.TButton').pack(side='left', padx=(0, 5))
        
        # Botão para usar data atual
        ttk.Button(frame_data_despesa, text="🕐 Agora", command=self.definir_data_atual_despesa, style='Secondary.TButton').pack(side='left')
        
        ttk.Button(frame_form, text="💸 Adicionar Despesa", command=self.adicionar_despesa, style='Modern.TButton').grid(row=2, column=0, columnspan=4, padx=10, pady=15)
        
        # Frame para filtros de período
        frame_filtros = ttk.LabelFrame(frame_despesas, text="Filtros por Período")
        frame_filtros.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_filtros, text="Data Inicial:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_data_inicial_despesa = ttk.Entry(frame_filtros, width=12)
        self.entry_data_inicial_despesa.grid(row=0, column=1, padx=5, pady=5)
        self.entry_data_inicial_despesa.insert(0, "01/01/2024")
        
        ttk.Label(frame_filtros, text="Data Final:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entry_data_final_despesa = ttk.Entry(frame_filtros, width=12)
        self.entry_data_final_despesa.grid(row=0, column=3, padx=5, pady=5)
        self.entry_data_final_despesa.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        ttk.Button(frame_filtros, text="🔍 Filtrar", command=self.filtrar_despesas).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_filtros, text="📋 Mostrar Todas", command=self.mostrar_todas_despesas).grid(row=0, column=5, padx=5, pady=5)
        
        # Lista de despesas
        frame_lista = ttk.LabelFrame(frame_despesas, text="Despesas Registradas")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame para botões de ação
        frame_botoes = ttk.Frame(frame_lista)
        frame_botoes.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(frame_botoes, text="✏️ Editar Despesa", command=self.editar_despesa).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="🗑️ Excluir Despesa", command=self.excluir_despesa).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="🔄 Atualizar Lista", command=self.atualizar_lista_despesas).pack(side='left', padx=5)
        
        # Treeview para mostrar despesas
        colunas = ('Data', 'Descrição', 'Valor')
        altura_tabela = max(6, int(10 * self.fator_escala))
        self.tree_despesas = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=altura_tabela)
        
        largura_coluna = max(120, int(200 * self.fator_escala))
        for col in colunas:
            self.tree_despesas.heading(col, text=col)
            self.tree_despesas.column(col, width=largura_coluna)
        
        scrollbar_despesas = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_despesas.yview)
        self.tree_despesas.configure(yscrollcommand=scrollbar_despesas.set)
        
        # Configurar scroll com mouse wheel
        self.configurar_scroll_mouse(self.tree_despesas)
        
        self.tree_despesas.pack(side='left', fill='both', expand=True)
        scrollbar_despesas.pack(side='right', fill='y')
        
        # Atualizar lista de despesas
        self.atualizar_lista_despesas()
    
    def criar_aba_relatorios(self, notebook):
        """Cria a aba de relatórios moderna"""
        frame_relatorios = ttk.Frame(notebook)
        notebook.add(frame_relatorios, text="📊 Relatórios")
        
        # Título moderno
        titulo = tk.Label(frame_relatorios, text="📊 RELATÓRIOS FINANCEIROS", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=20)
        
        # Frame para filtros de período nos relatórios
        frame_filtros_rel = ttk.LabelFrame(frame_relatorios, text="🔍 Filtros por Período")
        frame_filtros_rel.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_filtros_rel, text="Data Inicial:", font=self.fonte_principal).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.entry_data_inicial_rel = ttk.Entry(frame_filtros_rel, width=15, style='Modern.TEntry')
        self.entry_data_inicial_rel.grid(row=0, column=1, padx=10, pady=10)
        self.entry_data_inicial_rel.insert(0, "01/01/2024")
        
        ttk.Label(frame_filtros_rel, text="Data Final:", font=self.fonte_principal).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        self.entry_data_final_rel = ttk.Entry(frame_filtros_rel, width=15, style='Modern.TEntry')
        self.entry_data_final_rel.grid(row=0, column=3, padx=10, pady=10)
        self.entry_data_final_rel.insert(0, datetime.now().strftime('%d/%m/%Y'))
        
        # Botões de relatório
        ttk.Button(frame_filtros_rel, text="📊 Relatório por Período", command=self.gerar_relatorio_periodo, style='Modern.TButton').grid(row=0, column=4, padx=10, pady=10)
        ttk.Button(frame_filtros_rel, text="📈 Relatório Completo", command=self.atualizar_relatorios, style='Modern.TButton').grid(row=0, column=5, padx=10, pady=10)

        # Linha para fechamento mensal (usa mês/ano da data final)
        ttk.Label(frame_filtros_rel, text="Fechamento Mensal usa o mês da Data Final", font=self.fonte_pequena).grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=(0, 10))
        ttk.Button(frame_filtros_rel, text="📅 Fechamento Mensal", command=self.gerar_fechamento_mensal, style='Modern.TButton').grid(row=1, column=3, padx=10, pady=(0, 10))
        ttk.Button(frame_filtros_rel, text="📚 Histórico de Fechamentos", command=self.gerar_relatorio_fechamentos_mensais, style='Secondary.TButton').grid(row=1, column=4, padx=10, pady=(0, 10))
        
        # Frame para botões de relatórios específicos
        frame_relatorios_especificos = ttk.LabelFrame(frame_relatorios, text="📋 Relatórios Específicos")
        frame_relatorios_especificos.pack(fill='x', padx=20, pady=10)
        
        # Botões para relatórios específicos
        ttk.Button(frame_relatorios_especificos, text="🏆 Top Espetinhos", command=self.gerar_relatorio_top_espetinhos, style='Secondary.TButton').grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="📊 Análise por Espetinho", command=self.gerar_relatorio_por_espetinho, style='Secondary.TButton').grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="💰 Análise de Lucro", command=self.gerar_relatorio_lucro, style='Secondary.TButton').grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="📅 Relatório Diário", command=self.gerar_relatorio_diario, style='Secondary.TButton').grid(row=0, column=3, padx=10, pady=10)
        
        # Segunda linha de botões
        ttk.Button(frame_relatorios_especificos, text="📱 Vendas Mobile", command=self.gerar_relatorio_mobile, style='Modern.TButton').grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="💻 Vendas Desktop", command=self.gerar_relatorio_desktop, style='Secondary.TButton').grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="🕐 Vendas por Hora", command=self.gerar_relatorio_vendas_por_hora, style='Modern.TButton').grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(frame_relatorios_especificos, text="📦 Consolidar Bancos", command=self.consolidar_bancos, style='Modern.TButton').grid(row=1, column=3, padx=10, pady=10)
        
        # Frame para mostrar resumo
        frame_resumo = ttk.LabelFrame(frame_relatorios, text="📊 Resumo Financeiro")
        frame_resumo.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Criar scrollable text widget
        fonte_relatorio = ('Consolas', max(8, int(10 * self.fator_escala)))
        self.text_resumo = tk.Text(frame_resumo, 
                                  font=fonte_relatorio, 
                                  bg=self.cores['fundo_card'], 
                                  fg=self.cores['texto_principal'],
                                  wrap='word',
                                  height=max(12, int(20 * self.fator_escala)))
        scrollbar_resumo = ttk.Scrollbar(frame_resumo, orient='vertical', command=self.text_resumo.yview)
        self.text_resumo.configure(yscrollcommand=scrollbar_resumo.set)
        
        self.text_resumo.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_resumo.pack(side='right', fill='y', pady=10)
        
        # Atualizar relatórios inicialmente
        self.atualizar_relatorios()
    
    def adicionar_venda(self):
        """Adiciona uma nova venda"""
        try:
            espetinho = self.combo_espetinho.get()
            quantidade = int(self.entry_qtd_venda.get())
            valor_unitario = float(self.entry_valor_venda.get().replace(',', '.'))
            alterar_estoque = self.var_alterar_estoque.get()
            data_venda = self.entry_data_venda.get().strip()
            tipo_venda_str = self.combo_tipo_venda.get() or "Normal"
            tipo_consumo_str = self.combo_tipo_consumo.get() or "Local"

            if not espetinho:
                self.mostrar_notificacao_erro("❌ Selecione um espetinho!")
                return
            
            # Verificar se quantidade é válida
            if quantidade <= 0:
                self.mostrar_notificacao_erro("❌ Quantidade deve ser maior que zero!")
                return
            
            # Validar data/hora
            if not data_venda:
                self.mostrar_notificacao_erro("❌ Data/hora é obrigatória!")
                return
            
            try:
                # Validar formato da data
                dt_obj = datetime.strptime(data_venda, '%d/%m/%Y %H:%M')
            except ValueError:
                self.mostrar_notificacao_erro("❌ Formato de data inválido! Use DD/MM/AAAA HH:MM")
                return

            # Definir competência (ano-mês)
            competencia = dt_obj.strftime('%Y-%m')

            # Mapear tipo de venda
            tipo_venda = 'bonificacao' if tipo_venda_str.lower().startswith('boni') else 'normal'

            # Mapear tipo de consumo
            tipo_consumo_lower = tipo_consumo_str.lower()
            if tipo_consumo_lower.startswith('entre'):
                tipo_consumo = 'entrega'
            elif tipo_consumo_lower.startswith('inter'):
                tipo_consumo = 'interno'
            else:
                tipo_consumo = 'local'
            
            # Verificar estoque apenas se a opção estiver marcada
            if alterar_estoque:
                estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
                if estoque_atual < quantidade:
                    self.mostrar_notificacao_erro(f"❌ Estoque insuficiente! Disponível: {estoque_atual} unidades")
                    return

            total = quantidade * valor_unitario
            valor_cobrado = 0.0 if tipo_venda == 'bonificacao' else total

            venda = {
                'data': data_venda,
                'espetinho': espetinho,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario,
                'total': total,
                'alterou_estoque': alterar_estoque,
                'origem': 'desktop',  # Identificar venda desktop
                'tipo_venda': tipo_venda,
                'valor_cobrado': valor_cobrado,
                'tipo_consumo': tipo_consumo,
                'competencia': competencia
            }
            
            # Adicionar venda
            self.dados['vendas'].append(venda)
            
            # Atualizar estoque apenas se a opção estiver marcada
            if alterar_estoque:
                self.dados['espetinhos'][espetinho]['estoque'] -= quantidade
            
            if self.salvar_dados():
                self.atualizar_lista_vendas()
                self.atualizar_lista_espetinhos()
                self.atualizar_dashboard()
                self.limpar_campos_venda()
                status_estoque = "com alteração de estoque" if alterar_estoque else "sem alteração de estoque"
                self.mostrar_notificacao_sucesso(f"✅ Venda de {quantidade} {espetinho} adicionada! ({status_estoque})")
            
        except ValueError:
            self.mostrar_notificacao_erro("❌ Valores inválidos! Use números para quantidade e valor.")
        except Exception as e:
            self.mostrar_notificacao_erro(f"❌ Erro ao adicionar venda: {str(e)}")
    
    def adicionar_despesa(self):
        """Adiciona uma nova despesa"""
        try:
            descricao = self.entry_desc_despesa.get().strip()
            valor = float(self.entry_valor_despesa.get().replace(',', '.'))
            data_despesa = self.entry_data_despesa.get().strip()
            
            if not descricao:
                self.mostrar_notificacao_erro("❌ Descrição é obrigatória!")
                return
            
            # Validar data/hora
            if not data_despesa:
                self.mostrar_notificacao_erro("❌ Data/hora é obrigatória!")
                return
            
            try:
                # Validar formato da data
                datetime.strptime(data_despesa, '%d/%m/%Y %H:%M')
            except ValueError:
                self.mostrar_notificacao_erro("❌ Formato de data inválido! Use DD/MM/AAAA HH:MM")
                return
            
            despesa = {
                'data': data_despesa,
                'descricao': descricao,
                'valor': valor
            }
            
            self.dados['despesas'].append(despesa)
            
            if self.salvar_dados():
                self.atualizar_lista_despesas()
                self.atualizar_dashboard()
                self.limpar_campos_despesa()
                self.mostrar_notificacao_sucesso("✅ Despesa adicionada com sucesso!")
            
        except ValueError:
            self.mostrar_notificacao_erro("❌ Valor inválido! Use números.")
        except Exception as e:
            self.mostrar_notificacao_erro(f"❌ Erro ao adicionar despesa: {str(e)}")
    
    def atualizar_lista_vendas(self):
        """Atualiza a lista de vendas"""
        # Limpar lista atual
        for item in self.tree_vendas.get_children():
            self.tree_vendas.delete(item)
        
        # Adicionar vendas
        for venda in self.dados['vendas']:
            # Verificar se é venda nova (com espetinho) ou antiga (com descrição)
            descricao = venda.get('espetinho', venda.get('descricao', ''))
            origem = venda.get('origem', 'desktop')
            origem_emoji = "📱 MOBILE" if origem == 'mobile' else "💻 DESKTOP"
            valor_cobrado = self.get_valor_cobrado(venda)
            
            self.tree_vendas.insert('', 'end', values=(
                venda['data'],
                descricao,
                venda['quantidade'],
                f"R$ {venda['valor_unitario']:.2f}",
                f"R$ {valor_cobrado:.2f}",
                origem_emoji
            ))
    
    def atualizar_lista_despesas(self):
        """Atualiza a lista de despesas"""
        # Limpar lista atual
        for item in self.tree_despesas.get_children():
            self.tree_despesas.delete(item)
        
        # Adicionar despesas
        for despesa in self.dados['despesas']:
            self.tree_despesas.insert('', 'end', values=(
                despesa['data'],
                despesa['descricao'],
                f"R$ {despesa['valor']:.2f}"
            ))
    
    def atualizar_relatorios(self):
        """Atualiza os relatórios financeiros com análise completa"""
        # Calcular totais básicos (usando valor realmente cobrado)
        total_vendas = sum(self.get_valor_cobrado(venda) for venda in self.dados['vendas'])
        total_despesas = sum(despesa['valor'] for despesa in self.dados['despesas'])
        
        # Calcular custo total das vendas (baseado nos custos definidos por espetinho)
        total_custo_vendas = 0
        for venda in self.dados['vendas']:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                quantidade = venda['quantidade']
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += quantidade * custo_unitario
        
        # Calcular lucros e margens
        lucro_bruto = total_vendas - total_custo_vendas
        margem_lucro = (lucro_bruto / total_vendas * 100) if total_vendas > 0 else 0
        saldo_final = total_vendas - total_despesas
        
        # Análise por espetinho
        vendas_por_espetinho = {}
        for venda in self.dados['vendas']:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho:
                    vendas_por_espetinho[espetinho] = {
                        'quantidade': 0, 'valor_total': 0, 'custo_total': 0
                    }
                vendas_por_espetinho[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho[espetinho]['valor_total'] += self.get_valor_cobrado(venda)
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    vendas_por_espetinho[espetinho]['custo_total'] += venda['quantidade'] * custo_unitario
        
        # Encontrar mais e menos vendidos
        if vendas_por_espetinho:
            mais_vendido = max(vendas_por_espetinho.items(), key=lambda x: x[1]['quantidade'])
            menos_vendido = min(vendas_por_espetinho.items(), key=lambda x: x[1]['quantidade'])
        else:
            mais_vendido = ("Nenhum", {'quantidade': 0, 'valor_total': 0, 'custo_total': 0})
            menos_vendido = ("Nenhum", {'quantidade': 0, 'valor_total': 0, 'custo_total': 0})
        
        # Criar relatório simples e claro
        resumo = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           📊 RESUMO FINANCEIRO SIMPLES                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

💰 O QUE VOCÊ FATUROU:
   • Total de Vendas: R$ {total_vendas:,.2f}
   • Transações: {len(self.dados['vendas'])} vendas

💸 O QUE VOCÊ GASTOU:
   • Total de Despesas: R$ {total_despesas:,.2f}
   • Registros: {len(self.dados['despesas'])} despesas

📈 SEU LUCRO:
   • Lucro: R$ {saldo_final:,.2f}
   • Margem: {(saldo_final/total_vendas*100):.1f}%""" if total_vendas > 0 else f"""
📈 SEU LUCRO:
   • Lucro: R$ {saldo_final:,.2f}
   • Margem: N/A (sem vendas no período)
"""
        resumo += """

   • Fórmula: VENDAS - DESPESAS = LUCRO

🏆 TOP ESPETINHOS:
   • Mais Vendido: {mais_vendido[0]} ({mais_vendido[1]['quantidade']} unidades)
   • Menos Vendido: {menos_vendido[0]} ({menos_vendido[1]['quantidade']} unidades)

📊 ANÁLISE POR ESPETINHO:
"""
        
        # Adicionar análise detalhada por espetinho
        for espetinho, dados in sorted(vendas_por_espetinho.items(), 
                                     key=lambda x: x[1]['quantidade'], reverse=True):
            lucro_espetinho = dados['valor_total'] - dados['custo_total']
            margem_espetinho = (lucro_espetinho / dados['valor_total'] * 100) if dados['valor_total'] > 0 else 0
            resumo += f"   • {espetinho}: {dados['quantidade']} unid. | R$ {dados['valor_total']:,.2f} | Lucro: R$ {lucro_espetinho:,.2f} ({margem_espetinho:.1f}%)\n"
        
        # Calcular ticket médio com proteção contra divisão por zero
        ticket_medio_geral = total_vendas / len(self.dados['vendas']) if len(self.dados['vendas']) > 0 else 0
        
        resumo += f"""
📋 RESUMO GERAL:
   • Total de Despesas: {len(self.dados['despesas'])} registros
   • Ticket Médio: R$ {ticket_medio_geral:.2f} por venda
   • Status: {'✅ LUCRO' if saldo_final > 0 else '❌ PREJUÍZO' if saldo_final < 0 else '⚖️ EQUILIBRADO'}
        """
        
        # Atualizar o widget de texto
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, resumo)
    
    def gerar_relatorio_top_espetinhos(self):
        """Gera relatório dos espetinhos mais e menos vendidos"""
        vendas_por_espetinho = {}
        for venda in self.dados['vendas']:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho:
                    vendas_por_espetinho[espetinho] = {
                        'quantidade': 0, 'valor_total': 0, 'custo_total': 0
                    }
                vendas_por_espetinho[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho[espetinho]['valor_total'] += self.get_valor_cobrado(venda)
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    vendas_por_espetinho[espetinho]['custo_total'] += venda['quantidade'] * custo_unitario
        
        if not vendas_por_espetinho:
            relatorio = "❌ Nenhuma venda encontrada!"
        else:
            # Ordenar por quantidade vendida
            sorted_espetinhos = sorted(vendas_por_espetinho.items(), 
                                     key=lambda x: x[1]['quantidade'], reverse=True)
            
            relatorio = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🏆 TOP ESPETINHOS VENDIDOS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

🥇 RANKING POR QUANTIDADE VENDIDA:
"""
            for i, (espetinho, dados) in enumerate(sorted_espetinhos, 1):
                lucro = dados['valor_total'] - dados['custo_total']
                margem = (lucro / dados['valor_total'] * 100) if dados['valor_total'] > 0 else 0
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                
                relatorio += f"""
{emoji} {espetinho.upper()}
   • Quantidade: {dados['quantidade']} unidades
   • Faturamento: R$ {dados['valor_total']:,.2f}
   • Lucro: R$ {lucro:,.2f} ({margem:.1f}%)
   • Ticket Médio: R$ {dados['valor_total']/dados['quantidade']:.2f}
"""
            
            # Mais e menos vendidos
            mais_vendido = sorted_espetinhos[0]
            menos_vendido = sorted_espetinhos[-1]
            
            relatorio += f"""
📊 DESTAQUES:
   • 🏆 MAIS VENDIDO: {mais_vendido[0]} ({mais_vendido[1]['quantidade']} unidades)
   • 📉 MENOS VENDIDO: {menos_vendido[0]} ({menos_vendido[1]['quantidade']} unidades)
   • 📈 DIFERENÇA: {mais_vendido[1]['quantidade'] - menos_vendido[1]['quantidade']} unidades
"""
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_por_espetinho(self):
        """Gera relatório detalhado por espetinho"""
        vendas_por_espetinho = {}
        for venda in self.dados['vendas']:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho:
                    vendas_por_espetinho[espetinho] = {
                        'quantidade': 0, 'valor_total': 0, 'custo_total': 0, 'vendas': []
                    }
                vendas_por_espetinho[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho[espetinho]['valor_total'] += self.get_valor_cobrado(venda)
                vendas_por_espetinho[espetinho]['vendas'].append(venda)
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    vendas_por_espetinho[espetinho]['custo_total'] += venda['quantidade'] * custo_unitario
        
        if not vendas_por_espetinho:
            relatorio = "❌ Nenhuma venda encontrada!"
        else:
            relatorio = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        📊 ANÁLISE DETALHADA POR ESPETINHO                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
            for espetinho, dados in sorted(vendas_por_espetinho.items(), 
                                         key=lambda x: x[1]['quantidade'], reverse=True):
                lucro = dados['valor_total'] - dados['custo_total']
                margem = (lucro / dados['valor_total'] * 100) if dados['valor_total'] > 0 else 0
                ticket_medio = dados['valor_total'] / dados['quantidade'] if dados['quantidade'] > 0 else 0
                
                relatorio += f"""
🍖 {espetinho.upper()}
{'='*60}
   📊 VENDAS:
      • Quantidade Total: {dados['quantidade']} unidades
      • Faturamento Total: R$ {dados['valor_total']:,.2f}
      • Ticket Médio: R$ {ticket_medio:.2f}
      • Número de Transações: {len(dados['vendas'])}
   
   💰 LUCRO:
      • Custo Total: R$ {dados['custo_total']:,.2f}
      • Lucro Total: R$ {lucro:,.2f}
      • Margem de Lucro: {margem:.1f}%
      • Lucro por Unidade: R$ {lucro/dados['quantidade']:.2f}
   
   📈 PERFORMANCE:
      • Status: {'✅ EXCELENTE' if margem > 50 else '✅ BOM' if margem > 30 else '⚠️ REGULAR' if margem > 15 else '❌ BAIXO'}
      • Ranking: #{list(vendas_por_espetinho.keys()).index(espetinho) + 1} de {len(vendas_por_espetinho)}
"""
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_lucro(self):
        """Gera relatório focado em análise de lucro"""
        total_vendas = sum(self.get_valor_cobrado(venda) for venda in self.dados['vendas'])
        total_despesas = sum(despesa['valor'] for despesa in self.dados['despesas'])
        
        # Calcular custo total das vendas
        total_custo_vendas = 0
        for venda in self.dados['vendas']:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                quantidade = venda['quantidade']
                if espetinho in self.dados['espetinhos']:
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += quantidade * custo_unitario
        
        lucro_bruto = total_vendas - total_custo_vendas
        margem_lucro = (lucro_bruto / total_vendas * 100) if total_vendas > 0 else 0
        saldo_final = total_vendas - total_despesas
        
        # Calcular ticket médio com proteção contra divisão por zero
        ticket_medio_lucro = total_vendas / len(self.dados['vendas']) if len(self.dados['vendas']) > 0 else 0
        
        relatorio = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           💰 ANÁLISE DE LUCRO SIMPLES                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

💰 O QUE VOCÊ FATUROU:
   • Total de Vendas: R$ {total_vendas:,.2f}
   • Número de Vendas: {len(self.dados['vendas'])} transações
   • Ticket Médio: R$ {ticket_medio_lucro:.2f} por venda

💸 O QUE VOCÊ GASTOU:
   • Total de Despesas: R$ {total_despesas:,.2f}
   • Número de Despesas: {len(self.dados['despesas'])} registros

📈 SEU LUCRO REAL:
   • Lucro: R$ {saldo_final:,.2f}
   • Margem de Lucro: {(saldo_final/total_vendas*100):.1f}%""" if total_vendas > 0 else f"""
📈 SEU LUCRO REAL:
   • Lucro: R$ {saldo_final:,.2f}
   • Margem de Lucro: N/A (sem vendas no período)
"""
        relatorio += """
   • Fórmula: VENDAS - DESPESAS = LUCRO

🎯 INDICADORES DE PERFORMANCE:
   • Eficiência de Vendas: {'✅ ALTA' if margem_lucro > 40 else '⚠️ MÉDIA' if margem_lucro > 20 else '❌ BAIXA'}
   • Controle de Custos: {'✅ BOM' if total_despesas < total_vendas * 0.3 else '⚠️ REGULAR' if total_despesas < total_vendas * 0.5 else '❌ ALTO'}
   • Rentabilidade: {'✅ EXCELENTE' if saldo_final > total_vendas * 0.3 else '✅ BOA' if saldo_final > total_vendas * 0.15 else '⚠️ REGULAR' if saldo_final > 0 else '❌ PREJUÍZO'}

💡 RECOMENDAÇÕES:
"""
        
        if margem_lucro < 20:
            relatorio += "   • ⚠️ Margem de lucro baixa - considere ajustar preços ou reduzir custos\n"
        if total_despesas > total_vendas * 0.4:
            relatorio += "   • ⚠️ Despesas altas - revise gastos operacionais\n"
        if saldo_final < 0:
            relatorio += "   • ❌ Prejuízo detectado - ação imediata necessária\n"
        else:
            relatorio += "   • ✅ Operação saudável - mantenha o controle\n"
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_diario(self):
        """Gera relatório das vendas do dia"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        vendas_hoje = [venda for venda in self.dados['vendas'] if venda['data'].startswith(hoje)]
        despesas_hoje = [despesa for despesa in self.dados['despesas'] if despesa['data'].startswith(hoje)]
        
        total_vendas_hoje = sum(self.get_valor_cobrado(venda) for venda in vendas_hoje)
        total_despesas_hoje = sum(despesa['valor'] for despesa in despesas_hoje)
        
        # Análise por espetinho hoje
        vendas_por_espetinho_hoje = {}
        for venda in vendas_hoje:
            if 'espetinho' in venda:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho_hoje:
                    vendas_por_espetinho_hoje[espetinho] = {'quantidade': 0, 'valor': 0}
                vendas_por_espetinho_hoje[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho_hoje[espetinho]['valor'] += self.get_valor_cobrado(venda)
        
        relatorio = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           📅 RELATÓRIO DIÁRIO - {hoje}                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 RESUMO DO DIA:
   • Vendas: {len(vendas_hoje)} transações
   • Faturamento: R$ {total_vendas_hoje:,.2f}
   • Despesas: R$ {total_despesas_hoje:,.2f}
   • Saldo do Dia: R$ {total_vendas_hoje - total_despesas_hoje:,.2f}

🍖 VENDAS POR ESPETINHO HOJE:
"""
        
        if vendas_por_espetinho_hoje:
            for espetinho, dados in sorted(vendas_por_espetinho_hoje.items(), 
                                         key=lambda x: x[1]['quantidade'], reverse=True):
                ticket_medio = dados['valor'] / dados['quantidade'] if dados['quantidade'] > 0 else 0
                relatorio += f"   • {espetinho}: {dados['quantidade']} unid. | R$ {dados['valor']:,.2f} | Ticket: R$ {ticket_medio:.2f}\n"
        else:
            relatorio += "   • Nenhuma venda registrada hoje\n"
        
        # Quebra por tipo de consumo (local, entrega, interno)
        consumo_por_tipo = {'local': 0, 'entrega': 0, 'interno': 0}
        for venda in vendas_hoje:
            tipo_consumo = venda.get('tipo_consumo', 'local')
            if tipo_consumo in consumo_por_tipo:
                consumo_por_tipo[tipo_consumo] += venda.get('quantidade', 0)

        relatorio += """
📌 CONSUMO POR TIPO:
   • Local: {local} unidades
   • Entrega: {entrega} unidades
   • Interno: {interno} unidades
""".format(**consumo_por_tipo)
        
        # Calcular ticket médio com proteção contra divisão por zero
        ticket_medio_hoje = total_vendas_hoje / len(vendas_hoje) if len(vendas_hoje) > 0 else 0
        
        relatorio += f"""
📈 COMPARAÇÃO COM MÉDIA:
   • Ticket Médio Hoje: R$ {ticket_medio_hoje:.2f} por venda
   • Status: {'✅ BOM DIA' if total_vendas_hoje > 0 else '⚠️ SEM VENDAS'}
"""
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_mobile(self):
        """Gera relatório específico de vendas mobile"""
        # Filtrar vendas mobile
        vendas_mobile = [venda for venda in self.dados['vendas'] if venda.get('origem') == 'mobile']
        
        if not vendas_mobile:
            relatorio = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           📱 RELATÓRIO DE VENDAS MOBILE                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

❌ Nenhuma venda mobile encontrada!
💡 Lance vendas pelo celular para ver os dados aqui.
            """
        else:
            # Calcular totais mobile (usando valor cobrado)
            total_vendas_mobile = sum(self.get_valor_cobrado(venda) for venda in vendas_mobile)
            total_quantidade_mobile = sum(venda['quantidade'] for venda in vendas_mobile)
            
            # Análise por espetinho mobile
            vendas_por_espetinho_mobile = {}
            for venda in vendas_mobile:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho_mobile:
                    vendas_por_espetinho_mobile[espetinho] = {
                        'quantidade': 0, 'valor_total': 0, 'vendas': []
                    }
                vendas_por_espetinho_mobile[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho_mobile[espetinho]['valor_total'] += self.get_valor_cobrado(venda)
                vendas_por_espetinho_mobile[espetinho]['vendas'].append(venda)
            
            # Encontrar mais vendido mobile
            mais_vendido_mobile = max(vendas_por_espetinho_mobile.items(), 
                                    key=lambda x: x[1]['quantidade']) if vendas_por_espetinho_mobile else ("Nenhum", {'quantidade': 0, 'valor_total': 0})
            
            relatorio = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           📱 RELATÓRIO DE VENDAS MOBILE                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 RESUMO GERAL MOBILE:
   • Total de Vendas: {len(vendas_mobile)} transações
   • Quantidade Total: {total_quantidade_mobile} unidades
   • Faturamento Total: R$ {total_vendas_mobile:,.2f}
   • Ticket Médio: R$ {total_vendas_mobile/len(vendas_mobile):.2f} por venda

🏆 DESTAQUE MOBILE:
   • Mais Vendido: {mais_vendido_mobile[0]} ({mais_vendido_mobile[1]['quantidade']} unidades)

📱 VENDAS POR ESPETINHO (MOBILE):
"""
            
            # Listar vendas por espetinho mobile
            for espetinho, dados in sorted(vendas_por_espetinho_mobile.items(), 
                                         key=lambda x: x[1]['quantidade'], reverse=True):
                ticket_medio = dados['valor_total'] / dados['quantidade'] if dados['quantidade'] > 0 else 0
                relatorio += f"""
🍖 {espetinho.upper()}
   • Quantidade: {dados['quantidade']} unidades
   • Faturamento: R$ {dados['valor_total']:,.2f}
   • Ticket Médio: R$ {ticket_medio:.2f}
   • Vendas: {len(dados['vendas'])} transações
"""
            
            # Listar todas as vendas mobile (detalhado)
            relatorio += f"""
📋 HISTÓRICO DETALHADO (MOBILE):
"""
            for venda in sorted(vendas_mobile, key=lambda x: x['data'], reverse=True):
                relatorio += f"   • {venda['data']} | {venda['espetinho']} | {venda['quantidade']}x | R$ {venda['total']:.2f}\n"
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_desktop(self):
        """Gera relatório específico de vendas desktop"""
        # Filtrar vendas desktop
        vendas_desktop = [venda for venda in self.dados['vendas'] if venda.get('origem') == 'desktop']
        
        if not vendas_desktop:
            relatorio = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          💻 RELATÓRIO DE VENDAS DESKTOP                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

❌ Nenhuma venda desktop encontrada!
💡 Lance vendas pelo sistema desktop para ver os dados aqui.
            """
        else:
            # Calcular totais desktop (usando valor cobrado)
            total_vendas_desktop = sum(self.get_valor_cobrado(venda) for venda in vendas_desktop)
            total_quantidade_desktop = sum(venda['quantidade'] for venda in vendas_desktop)
            
            # Análise por espetinho desktop
            vendas_por_espetinho_desktop = {}
            for venda in vendas_desktop:
                espetinho = venda['espetinho']
                if espetinho not in vendas_por_espetinho_desktop:
                    vendas_por_espetinho_desktop[espetinho] = {
                        'quantidade': 0, 'valor_total': 0, 'vendas': []
                    }
                vendas_por_espetinho_desktop[espetinho]['quantidade'] += venda['quantidade']
                vendas_por_espetinho_desktop[espetinho]['valor_total'] += self.get_valor_cobrado(venda)
                vendas_por_espetinho_desktop[espetinho]['vendas'].append(venda)
            
            # Encontrar mais vendido desktop
            mais_vendido_desktop = max(vendas_por_espetinho_desktop.items(), 
                                     key=lambda x: x[1]['quantidade']) if vendas_por_espetinho_desktop else ("Nenhum", {'quantidade': 0, 'valor_total': 0})
            
            relatorio = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          💻 RELATÓRIO DE VENDAS DESKTOP                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 RESUMO GERAL DESKTOP:
   • Total de Vendas: {len(vendas_desktop)} transações
   • Quantidade Total: {total_quantidade_desktop} unidades
   • Faturamento Total: R$ {total_vendas_desktop:,.2f}
   • Ticket Médio: R$ {total_vendas_desktop/len(vendas_desktop):.2f} por venda

🏆 DESTAQUE DESKTOP:
   • Mais Vendido: {mais_vendido_desktop[0]} ({mais_vendido_desktop[1]['quantidade']} unidades)

💻 VENDAS POR ESPETINHO (DESKTOP):
"""
            
            # Listar vendas por espetinho desktop
            for espetinho, dados in sorted(vendas_por_espetinho_desktop.items(), 
                                         key=lambda x: x[1]['quantidade'], reverse=True):
                ticket_medio = dados['valor_total'] / dados['quantidade'] if dados['quantidade'] > 0 else 0
                relatorio += f"""
🍖 {espetinho.upper()}
   • Quantidade: {dados['quantidade']} unidades
   • Faturamento: R$ {dados['valor_total']:,.2f}
   • Ticket Médio: R$ {ticket_medio:.2f}
   • Vendas: {len(dados['vendas'])} transações
"""
            
            # Listar todas as vendas desktop (detalhado)
            relatorio += f"""
📋 HISTÓRICO DETALHADO (DESKTOP):
"""
            for venda in sorted(vendas_desktop, key=lambda x: x['data'], reverse=True):
                relatorio += f"   • {venda['data']} | {venda['espetinho']} | {venda['quantidade']}x | R$ {venda['total']:.2f}\n"
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
    
    def gerar_relatorio_vendas_por_hora(self):
        """Gera relatório de vendas agrupadas por hora do dia"""
        # Agrupar vendas por hora
        vendas_por_hora = {}
        
        for venda in self.dados['vendas']:
            try:
                # Extrair hora da data (formato: DD/MM/YYYY HH:MM)
                data_hora = venda['data']
                if ' ' in data_hora:
                    hora = data_hora.split(' ')[1].split(':')[0]  # Pega apenas a hora
                else:
                    continue
                
                hora_int = int(hora)
                
                if hora_int not in vendas_por_hora:
                    vendas_por_hora[hora_int] = {
                        'quantidade': 0,
                        'valor_total': 0,
                        'vendas': 0
                    }
                
                vendas_por_hora[hora_int]['quantidade'] += venda['quantidade']
                vendas_por_hora[hora_int]['valor_total'] += self.get_valor_cobrado(venda)
                vendas_por_hora[hora_int]['vendas'] += 1
                
            except (ValueError, IndexError):
                continue
        
        # Ordenar por hora
        horas_ordenadas = sorted(vendas_por_hora.keys())
        
        # Calcular totais gerais
        total_geral_vendas = sum(dados['vendas'] for dados in vendas_por_hora.values())
        total_geral_quantidade = sum(dados['quantidade'] for dados in vendas_por_hora.values())
        total_geral_valor = sum(dados['valor_total'] for dados in vendas_por_hora.values())
        
        # Encontrar horários de pico
        hora_pico_vendas = max(vendas_por_hora.keys(), key=lambda h: vendas_por_hora[h]['vendas']) if vendas_por_hora else 0
        hora_pico_valor = max(vendas_por_hora.keys(), key=lambda h: vendas_por_hora[h]['valor_total']) if vendas_por_hora else 0
        
        # Gerar relatório
        relatorio = f"""
🕐 RELATÓRIO DE VENDAS POR HORA
{'='*50}

📊 RESUMO GERAL:
• Total de Vendas: {total_geral_vendas}
• Total de Unidades: {total_geral_quantidade}
• Faturamento Total: R$ {total_geral_valor:.2f}

🏆 HORÁRIOS DE PICO:
• Maior Número de Vendas: {hora_pico_vendas:02d}:00 ({vendas_por_hora[hora_pico_vendas]['vendas']} vendas)
• Maior Faturamento: {hora_pico_valor:02d}:00 (R$ {vendas_por_hora[hora_pico_valor]['valor_total']:.2f})

📈 DETALHAMENTO POR HORA:
{'Hora':<6} {'Vendas':<8} {'Unidades':<10} {'Faturamento':<12} {'% Vendas':<10}
{'-'*60}
"""
        
        for hora in horas_ordenadas:
            dados = vendas_por_hora[hora]
            percentual_vendas = (dados['vendas'] / total_geral_vendas * 100) if total_geral_vendas > 0 else 0
            
            relatorio += f"{hora:02d}:00  {dados['vendas']:<8} {dados['quantidade']:<10} R$ {dados['valor_total']:<10.2f} {percentual_vendas:<9.1f}%\n"
        
        # Adicionar análise de períodos
        relatorio += f"\n📊 ANÁLISE POR PERÍODOS:\n"
        relatorio += f"{'-'*40}\n"
        
        # Manhã (06:00 - 11:59)
        manha_vendas = sum(vendas_por_hora.get(h, {}).get('vendas', 0) for h in range(6, 12))
        manha_valor = sum(vendas_por_hora.get(h, {}).get('valor_total', 0) for h in range(6, 12))
        
        # Tarde (12:00 - 17:59)
        tarde_vendas = sum(vendas_por_hora.get(h, {}).get('vendas', 0) for h in range(12, 18))
        tarde_valor = sum(vendas_por_hora.get(h, {}).get('valor_total', 0) for h in range(12, 18))
        
        # Noite (18:00 - 23:59)
        noite_vendas = sum(vendas_por_hora.get(h, {}).get('vendas', 0) for h in range(18, 24))
        noite_valor = sum(vendas_por_hora.get(h, {}).get('valor_total', 0) for h in range(18, 24))
        
        # Madrugada (00:00 - 05:59)
        madrugada_vendas = sum(vendas_por_hora.get(h, {}).get('vendas', 0) for h in range(0, 6))
        madrugada_valor = sum(vendas_por_hora.get(h, {}).get('valor_total', 0) for h in range(0, 6))
        
        relatorio += f"🌅 Manhã (06:00-11:59): {manha_vendas} vendas | R$ {manha_valor:.2f}\n"
        relatorio += f"☀️  Tarde (12:00-17:59): {tarde_vendas} vendas | R$ {tarde_valor:.2f}\n"
        relatorio += f"🌆 Noite (18:00-23:59): {noite_vendas} vendas | R$ {noite_valor:.2f}\n"
        relatorio += f"🌙 Madrugada (00:00-05:59): {madrugada_vendas} vendas | R$ {madrugada_valor:.2f}\n"
        
        # Recomendações
        relatorio += f"\n💡 RECOMENDAÇÕES:\n"
        relatorio += f"{'-'*30}\n"
        
        if hora_pico_vendas >= 18:
            relatorio += f"• Foque no horário noturno ({hora_pico_vendas:02d}:00) - maior movimento\n"
        elif hora_pico_vendas >= 12:
            relatorio += f"• Foque no horário da tarde ({hora_pico_vendas:02d}:00) - maior movimento\n"
        else:
            relatorio += f"• Foque no horário da manhã ({hora_pico_vendas:02d}:00) - maior movimento\n"
        
        if manha_vendas < tarde_vendas and manha_vendas < noite_vendas:
            relatorio += f"• Considere estratégias para aumentar vendas na manhã\n"
        if noite_vendas > tarde_vendas and noite_vendas > manha_vendas:
            relatorio += f"• Horário noturno é o mais lucrativo - mantenha foco\n"
        
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, relatorio)
        
        # Mostrar gráfico visual
        self.mostrar_grafico_vendas_por_hora(vendas_por_hora, horas_ordenadas)
    
    def mostrar_grafico_vendas_por_hora(self, vendas_por_hora, horas_ordenadas):
        """Mostra gráfico visual de vendas por hora"""
        # Criar janela do gráfico
        janela_grafico = tk.Toplevel(self.root)
        janela_grafico.title("📊 Gráfico de Vendas por Hora")
        janela_grafico.geometry("1000x600")
        janela_grafico.configure(bg='#f0f0f0')
        
        # Centralizar janela
        janela_grafico.transient(self.root)
        janela_grafico.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(janela_grafico)
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(frame_principal, text="📊 RELATÓRIO DE VENDAS POR HORA", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 10))
        
        # Frame do gráfico
        frame_grafico = ttk.Frame(frame_principal)
        frame_grafico.pack(fill='both', expand=True)
        
        # Canvas para desenhar o gráfico
        canvas = tk.Canvas(frame_grafico, bg='white', width=900, height=400)
        canvas.pack(pady=10)
        
        # Calcular dimensões do gráfico
        largura_canvas = 900
        altura_canvas = 400
        margem_esquerda = 80
        margem_direita = 20
        margem_superior = 20
        margem_inferior = 60
        
        largura_util = largura_canvas - margem_esquerda - margem_direita
        altura_util = altura_canvas - margem_superior - margem_inferior
        
        # Encontrar valor máximo para escala
        if vendas_por_hora:
            valor_max = max(dados['valor_total'] for dados in vendas_por_hora.values())
            # Arredondar para cima para escala mais limpa
            valor_max = ((int(valor_max) // 50) + 1) * 50
        else:
            valor_max = 100
        
        # Desenhar eixos
        canvas.create_line(margem_esquerda, margem_superior, margem_esquerda, altura_canvas - margem_inferior, width=2, fill='black')
        canvas.create_line(margem_esquerda, altura_canvas - margem_inferior, largura_canvas - margem_direita, altura_canvas - margem_inferior, width=2, fill='black')
        
        # Desenhar grade e labels do eixo Y
        for i in range(0, int(valor_max) + 1, 50):
            y = altura_canvas - margem_inferior - (i / valor_max) * altura_util
            canvas.create_line(margem_esquerda - 5, y, margem_esquerda, y, width=1, fill='gray')
            canvas.create_text(margem_esquerda - 10, y, text=str(i), anchor='e', font=('Arial', 10))
        
        # Desenhar barras
        if horas_ordenadas:
            largura_barra = largura_util / len(horas_ordenadas) * 0.8
            espacamento = largura_util / len(horas_ordenadas) * 0.2
            
            for i, hora in enumerate(horas_ordenadas):
                dados = vendas_por_hora[hora]
                valor = dados['valor_total']
                
                # Calcular posição da barra
                x_inicio = margem_esquerda + i * (largura_barra + espacamento) + espacamento/2
                x_fim = x_inicio + largura_barra
                
                # Calcular altura da barra
                altura_barra = (valor / valor_max) * altura_util
                y_inicio = altura_canvas - margem_inferior - altura_barra
                y_fim = altura_canvas - margem_inferior
                
                # Desenhar barra
                cor_barra = '#4CAF50' if valor == max(dados['valor_total'] for dados in vendas_por_hora.values()) else '#2196F3'
                canvas.create_rectangle(x_inicio, y_inicio, x_fim, y_fim, fill=cor_barra, outline='black', width=1)
                
                # Adicionar valor no topo da barra
                canvas.create_text(x_inicio + largura_barra/2, y_inicio - 10, 
                                 text=f"R$ {valor:.0f}", font=('Arial', 9, 'bold'), fill='black')
                
                # Adicionar label da hora
                canvas.create_text(x_inicio + largura_barra/2, altura_canvas - margem_inferior + 20, 
                                 text=f"{hora:02d}:00", font=('Arial', 10), fill='black')
        
        # Legenda
        frame_legenda = ttk.Frame(frame_principal)
        frame_legenda.pack(pady=10)
        
        ttk.Label(frame_legenda, text="Total de Vendas (R$)", font=('Arial', 12, 'bold')).pack(side='left')
        canvas_legenda = tk.Canvas(frame_legenda, width=20, height=15, bg='white')
        canvas_legenda.pack(side='left', padx=(10, 0))
        canvas_legenda.create_rectangle(2, 2, 18, 13, fill='#2196F3', outline='black')
        
        # Botão fechar
        ttk.Button(frame_principal, text="Fechar", command=janela_grafico.destroy).pack(pady=10)
    
    def limpar_campos_venda(self):
        """Limpa os campos do formulário de venda"""
        self.combo_espetinho.set('')
        self.entry_qtd_venda.delete(0, 'end')
        self.entry_qtd_venda.insert(0, "1")  # Valor padrão
        self.entry_valor_venda.delete(0, 'end')
        self.label_total.config(text="R$ 0,00")
        self.var_alterar_estoque.set(True)  # Resetar checkbox
        # Manter data atual para próxima venda
        self.entry_data_venda.delete(0, 'end')
        self.entry_data_venda.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    def limpar_campos_despesa(self):
        """Limpa os campos do formulário de despesa"""
        self.entry_desc_despesa.delete(0, 'end')
        self.entry_valor_despesa.delete(0, 'end')
        # Manter data atual para próxima despesa
        self.entry_data_despesa.delete(0, 'end')
        self.entry_data_despesa.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    def atualizar_lista_espetinhos(self):
        """Atualiza a lista de espetinhos"""
        # Limpar lista atual
        for item in self.tree_espetinhos.get_children():
            self.tree_espetinhos.delete(item)
        
        # Adicionar espetinhos
        for nome, dados in self.dados['espetinhos'].items():
            custo = dados['custo']
            venda = dados['valor']
            lucro = venda - custo
            
            # Calcular Markup: ((Venda - Custo) / Custo) * 100
            markup = (lucro / custo * 100) if custo > 0 else 0
            
            # Calcular Margem: ((Venda - Custo) / Venda) * 100
            margem = (lucro / venda * 100) if venda > 0 else 0
            
            self.tree_espetinhos.insert('', 'end', values=(
                nome,
                f"R$ {custo:.2f}",
                f"R$ {venda:.2f}",
                f"R$ {lucro:.2f}",
                f"{markup:.1f}%",
                f"{margem:.1f}%",
                f"{dados['estoque']} unid."
            ))
    
    def atualizar_combo_espetinhos(self):
        """Atualiza o combobox de espetinhos para vendas"""
        lista_espetinhos = list(self.dados['espetinhos'].keys())
        self.combo_espetinho['values'] = lista_espetinhos
    
    def atualizar_combo_estoque(self):
        """Atualiza o combobox de espetinhos para estoque"""
        lista_espetinhos = list(self.dados['espetinhos'].keys())
        self.combo_estoque['values'] = lista_espetinhos
    
    def atualizar_combo_custo(self):
        """Atualiza o combobox de espetinhos para custo"""
        lista_espetinhos = list(self.dados['espetinhos'].keys())
        self.combo_custo['values'] = lista_espetinhos
    
    def on_espetinho_selected(self, event):
        """Quando um espetinho é selecionado na venda"""
        espetinho = self.combo_espetinho.get()
        if espetinho in self.dados['espetinhos']:
            valor = self.dados['espetinhos'][espetinho]['valor']
            self.entry_valor_venda.config(state='normal')
            self.entry_valor_venda.delete(0, 'end')
            self.entry_valor_venda.insert(0, f"{valor:.2f}")
            self.entry_valor_venda.config(state='readonly')
            self.calcular_total_venda()
    
    def calcular_total_venda(self):
        """Calcula o total da venda"""
        try:
            quantidade = int(self.entry_qtd_venda.get())
            valor_unitario = float(self.entry_valor_venda.get())
            total = quantidade * valor_unitario
            self.label_total.config(text=f"R$ {total:.2f}")
        except:
            self.label_total.config(text="R$ 0,00")
    
    def definir_data_atual(self):
        """Define a data/hora atual no campo de vendas"""
        self.entry_data_venda.delete(0, 'end')
        self.entry_data_venda.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    def definir_data_atual_despesa(self):
        """Define a data/hora atual no campo de despesas"""
        self.entry_data_despesa.delete(0, 'end')
        self.entry_data_despesa.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    def definir_data_atual_edicao(self, entry_widget):
        """Define a data/hora atual no campo de edição"""
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    def abrir_calendario_venda(self):
        """Abre o calendário para seleção de data de venda"""
        calendario = CalendarioWidget(self.root, self.entry_data_venda, 
                                    cores=self.cores, incluir_hora=True)
        calendario.mostrar_calendario()
    
    def abrir_calendario_despesa(self):
        """Abre o calendário para seleção de data de despesa"""
        calendario = CalendarioWidget(self.root, self.entry_data_despesa, 
                                    cores=self.cores, incluir_hora=True)
        calendario.mostrar_calendario()
    
    def abrir_calendario_edicao(self, entry_widget):
        """Abre o calendário para edição de data"""
        calendario = CalendarioWidget(self.root, entry_widget, 
                                    cores=self.cores, incluir_hora=True)
        calendario.mostrar_calendario()
    
    def configurar_scroll_mouse(self, widget):
        """Configura o scroll com mouse wheel para um widget"""
        def _on_mousewheel(event):
            widget.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            widget.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            widget.unbind_all("<MouseWheel>")
        
        # Bind quando o mouse entra no widget
        widget.bind('<Enter>', _bind_to_mousewheel)
        # Unbind quando o mouse sai do widget
        widget.bind('<Leave>', _unbind_from_mousewheel)
    
    def adicionar_estoque(self):
        """Adiciona estoque para um espetinho"""
        try:
            espetinho = self.combo_estoque.get()
            quantidade = int(self.entry_qtd_estoque.get())
            
            if not espetinho:
                messagebox.showerror("Erro", "Selecione um espetinho!")
                return
            
            if quantidade < 0:
                messagebox.showerror("Erro", "Quantidade não pode ser negativa!")
                return
            
            # Adicionar ao estoque
            self.dados['espetinhos'][espetinho]['estoque'] += quantidade
            
            if self.salvar_dados():
                self.atualizar_lista_espetinhos()
                self.atualizar_dashboard()
                self.entry_qtd_estoque.delete(0, 'end')
                if quantidade > 0:
                    self.mostrar_notificacao_sucesso(f"✅ Adicionado {quantidade} unidades de {espetinho} ao estoque!")
                elif quantidade == 0:
                    self.mostrar_notificacao_sucesso(f"✅ Estoque de {espetinho} mantido em {self.dados['espetinhos'][espetinho]['estoque']} unidades!")
                else:
                    self.mostrar_notificacao_sucesso(f"✅ Removido {abs(quantidade)} unidades de {espetinho} do estoque!")
            
        except ValueError:
            self.mostrar_notificacao_erro("❌ Quantidade deve ser um número!")
        except Exception as e:
            self.mostrar_notificacao_erro(f"❌ Erro ao adicionar estoque: {str(e)}")
    
    def atualizar_custo(self):
        """Atualiza o custo de um espetinho"""
        try:
            espetinho = self.combo_custo.get()
            novo_custo = float(self.entry_novo_custo.get().replace(',', '.'))
            
            if not espetinho:
                messagebox.showerror("Erro", "Selecione um espetinho!")
                return
            
            if novo_custo < 0:
                messagebox.showerror("Erro", "Custo não pode ser negativo!")
                return
            
            # Atualizar custo
            self.dados['espetinhos'][espetinho]['custo'] = novo_custo
            
            if self.salvar_dados():
                self.atualizar_lista_espetinhos()
                self.atualizar_dashboard()
                self.entry_novo_custo.delete(0, 'end')
                self.mostrar_notificacao_sucesso(f"✅ Custo do {espetinho} atualizado para R$ {novo_custo:.2f}!")
            
        except ValueError:
            self.mostrar_notificacao_erro("❌ Custo deve ser um número!")
        except Exception as e:
            self.mostrar_notificacao_erro(f"❌ Erro ao atualizar custo: {str(e)}")
    
    def zerar_todo_estoque(self):
        """Zera o estoque de todos os espetinhos"""
        if messagebox.askyesno("Confirmar", "⚠️ Tem certeza que deseja ZERAR o estoque de TODOS os espetinhos?\n\nEsta ação não pode ser desfeita!"):
            try:
                # Zerar estoque de todos os espetinhos
                for espetinho in self.dados['espetinhos']:
                    self.dados['espetinhos'][espetinho]['estoque'] = 0
                
                if self.salvar_dados():
                    self.atualizar_lista_espetinhos()
                    self.atualizar_dashboard()
                    self.mostrar_notificacao_sucesso("✅ Estoque de TODOS os espetinhos foi zerado!")
                else:
                    self.mostrar_notificacao_erro("❌ Erro ao salvar dados!")
                    
            except Exception as e:
                self.mostrar_notificacao_erro(f"❌ Erro ao zerar estoque: {str(e)}")
    
    def zerar_estoque_individual(self):
        """Zera o estoque de um espetinho específico"""
        try:
            espetinho = self.combo_estoque.get()
            
            if not espetinho:
                self.mostrar_notificacao_erro("❌ Selecione um espetinho!")
                return
            
            estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
            
            if messagebox.askyesno("Confirmar", f"⚠️ Tem certeza que deseja ZERAR o estoque de {espetinho}?\n\nEstoque atual: {estoque_atual} unidades"):
                # Zerar estoque do espetinho selecionado
                self.dados['espetinhos'][espetinho]['estoque'] = 0
                
                if self.salvar_dados():
                    self.atualizar_lista_espetinhos()
                    self.atualizar_dashboard()
                    self.mostrar_notificacao_sucesso(f"✅ Estoque de {espetinho} foi zerado!")
                else:
                    self.mostrar_notificacao_erro("❌ Erro ao salvar dados!")
                    
        except Exception as e:
            self.mostrar_notificacao_erro(f"❌ Erro ao zerar estoque: {str(e)}")
    
    def mostrar_tooltip_markup_simples(self):
        """Mostra tooltip explicativo sobre Markup"""
        tooltip = tk.Toplevel(self.root)
        tooltip.title("📊 Markup")
        tooltip.geometry("400x300")
        tooltip.configure(bg=self.cores['fundo_secundario'])
        tooltip.resizable(False, False)
        
        # Centralizar tooltip
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
        tooltip.geometry(f"400x300+{x}+{y}")
        
        # Conteúdo do tooltip
        frame = tk.Frame(tooltip, bg=self.cores['fundo_secundario'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(frame, text="📊 MARKUP", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_secundario'])
        titulo.pack(pady=(0, 15))
        
        # Explicação
        explicacao = """
💡 O que é Markup?

Markup é quanto você "marca" em cima do 
custo do produto para chegar no preço 
de venda.

📐 Fórmula:
((Venda - Custo) ÷ Custo) × 100

📝 Exemplo Prático:
• Custo: R$ 3,00
• Venda: R$ 6,00
• Markup: ((6 - 3) ÷ 3) × 100 = 100%

🎯 O que significa:
"Eu vendo por 100% a mais do que paguei"

✅ Vantagem:
Fácil de calcular e entender
        """
        
        label_explicacao = tk.Label(frame, 
                                   text=explicacao,
                                   font=self.fonte_principal,
                                   fg=self.cores['texto_principal'],
                                   bg=self.cores['fundo_secundario'],
                                   justify='left')
        label_explicacao.pack(fill='both', expand=True)
        
        # Botão fechar
        btn_fechar = tk.Button(frame, text="✅ Entendi!", 
                              command=tooltip.destroy,
                              bg=self.cores['destaque'],
                              fg=self.cores['fundo_principal'],
                              font=self.fonte_principal,
                              relief='flat',
                              padx=20,
                              pady=10)
        btn_fechar.pack(pady=(15, 0))
    
    def mostrar_tooltip_margem_simples(self):
        """Mostra tooltip explicativo sobre Margem"""
        tooltip = tk.Toplevel(self.root)
        tooltip.title("🎯 Margem")
        tooltip.geometry("400x300")
        tooltip.configure(bg=self.cores['fundo_secundario'])
        tooltip.resizable(False, False)
        
        # Centralizar tooltip
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
        tooltip.geometry(f"400x300+{x}+{y}")
        
        # Conteúdo do tooltip
        frame = tk.Frame(tooltip, bg=self.cores['fundo_secundario'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(frame, text="🎯 MARGEM", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_secundario'])
        titulo.pack(pady=(0, 15))
        
        # Explicação
        explicacao = """
💡 O que é Margem?

Margem é quanto de lucro você tem 
sobre o preço de venda.

📐 Fórmula:
((Venda - Custo) ÷ Venda) × 100

📝 Exemplo Prático:
• Custo: R$ 3,00
• Venda: R$ 6,00
• Margem: ((6 - 3) ÷ 6) × 100 = 50%

🎯 O que significa:
"50% do preço de venda é lucro"

✅ Vantagem:
Mostra a rentabilidade real do produto
        """
        
        label_explicacao = tk.Label(frame, 
                                   text=explicacao,
                                   font=self.fonte_principal,
                                   fg=self.cores['texto_principal'],
                                   bg=self.cores['fundo_secundario'],
                                   justify='left')
        label_explicacao.pack(fill='both', expand=True)
        
        # Botão fechar
        btn_fechar = tk.Button(frame, text="✅ Entendi!", 
                              command=tooltip.destroy,
                              bg=self.cores['destaque'],
                              fg=self.cores['fundo_principal'],
                              font=self.fonte_principal,
                              relief='flat',
                              padx=20,
                              pady=10)
        btn_fechar.pack(pady=(15, 0))
    
    def editar_venda(self):
        """Edita uma venda selecionada"""
        selecionado = self.tree_vendas.selection()
        if not selecionado:
            self.mostrar_notificacao_erro("❌ Selecione uma venda para editar!")
            return
        
        # Obter o item selecionado
        item = self.tree_vendas.item(selecionado[0])
        valores = item['values']
        
        # Usar uma abordagem mais simples: encontrar por índice na lista
        # Obter todos os itens da treeview
        items = self.tree_vendas.get_children()
        indice_selecionado = items.index(selecionado[0])
        
        # Verificar se o índice é válido
        if indice_selecionado < len(self.dados['vendas']):
            venda = self.dados['vendas'][indice_selecionado]
            self.criar_janela_edicao_venda(indice_selecionado, venda)
        else:
            self.mostrar_notificacao_erro("❌ Índice de venda inválido!")
    
    def excluir_venda(self):
        """Exclui uma venda selecionada"""
        selecionado = self.tree_vendas.selection()
        if not selecionado:
            self.mostrar_notificacao_erro("❌ Selecione uma venda para excluir!")
            return
        
        # Confirmar exclusão com modal moderno
        self.modal.mostrar_modal_confirmacao(
            "⚠️ Confirmar Exclusão", 
            "Tem certeza que deseja excluir esta venda?",
            callback_sim=lambda: self._confirmar_exclusao_venda()
        )
    
    def _confirmar_exclusao_venda(self):
        """Confirma a exclusão da venda"""
        try:
            # Obter item selecionado
            selecionado = self.tree_vendas.selection()
            if not selecionado:
                return
            
            # Usar a mesma abordagem simples: encontrar por índice na lista
            items = self.tree_vendas.get_children()
            indice_selecionado = items.index(selecionado[0])
            
            # Verificar se o índice é válido
            if indice_selecionado < len(self.dados['vendas']):
                venda = self.dados['vendas'][indice_selecionado]
                
                # Se for venda com espetinho e alterou estoque, devolver ao estoque
                if 'espetinho' in venda and venda.get('alterou_estoque', True):
                    espetinho = venda['espetinho']
                    quantidade = venda['quantidade']
                    self.dados['espetinhos'][espetinho]['estoque'] += quantidade
                
                # Remover venda
                del self.dados['vendas'][indice_selecionado]
                
                if self.salvar_dados():
                    self.atualizar_lista_vendas()
                    self.atualizar_lista_espetinhos()
                    self.atualizar_dashboard()
                    self.modal.mostrar_modal_sucesso("✅ Sucesso", "Venda excluída com sucesso!")
            else:
                self.modal.mostrar_modal_erro("❌ Erro", "Índice de venda inválido!")
        except Exception as e:
            self.modal.mostrar_modal_erro("❌ Erro", f"Erro ao excluir venda: {str(e)}")
    
    def editar_despesa(self):
        """Edita uma despesa selecionada"""
        selecionado = self.tree_despesas.selection()
        if not selecionado:
            self.modal.mostrar_modal_erro("❌ Erro", "Selecione uma despesa para editar!")
            return
        
        # Obter índice da despesa selecionada
        item = self.tree_despesas.item(selecionado[0])
        valores = item['values']
        
        # Encontrar a despesa nos dados
        for i, despesa in enumerate(self.dados['despesas']):
            if (despesa['data'] == valores[0] and 
                despesa['descricao'] == valores[1] and
                f"R$ {despesa['valor']:.2f}" == valores[2]):
                
                # Criar janela de edição
                self.criar_janela_edicao_despesa(i, despesa)
                return
        
        messagebox.showerror("Erro", "Despesa não encontrada!")
    
    def excluir_despesa(self):
        """Exclui uma despesa selecionada"""
        selecionado = self.tree_despesas.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma despesa para excluir!")
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta despesa?"):
            # Obter índice da despesa selecionada
            item = self.tree_despesas.item(selecionado[0])
            valores = item['values']
            
            # Encontrar e remover a despesa
            for i, despesa in enumerate(self.dados['despesas']):
                if (despesa['data'] == valores[0] and 
                    despesa['descricao'] == valores[1] and
                    f"R$ {despesa['valor']:.2f}" == valores[2]):
                    
                    # Remover despesa
                    del self.dados['despesas'][i]
                    
                    if self.salvar_dados():
                        self.atualizar_lista_despesas()
                        messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")
                    return
            
            messagebox.showerror("Erro", "Despesa não encontrada!")
    
    def criar_janela_edicao_venda(self, indice, venda):
        """Cria janela para editar venda"""
        janela = tk.Toplevel(self.root)
        janela.title("✏️ Editar Venda")
        janela.geometry("450x400")
        janela.configure(bg=self.cores['fundo_principal'])
        janela.grab_set()  # Modal
        
        # Centralizar janela
        janela.transient(self.root)
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 225
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        janela.geometry(f"450x400+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(janela)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título moderno
        titulo = tk.Label(frame, text="✏️ EDITAR VENDA", 
                         font=self.fonte_titulo, 
                         fg=self.cores['destaque'], 
                         bg=self.cores['fundo_principal'])
        titulo.pack(pady=(0, 20))
        
        # Campo de data/hora
        ttk.Label(frame, text="Data/Hora:", font=self.fonte_principal).pack(anchor='w', pady=(0, 5))
        frame_data = ttk.Frame(frame)
        frame_data.pack(fill='x', pady=(0, 10))
        
        entry_data = ttk.Entry(frame_data, width=20, style='Modern.TEntry')
        entry_data.pack(side='left', padx=(0, 5))
        entry_data.insert(0, venda['data'])
        
        # Botão do calendário
        ttk.Button(frame_data, text="📅", command=lambda: self.abrir_calendario_edicao(entry_data), style='Secondary.TButton').pack(side='left', padx=(0, 5))
        
        # Botão para usar data atual
        ttk.Button(frame_data, text="🕐 Agora", command=lambda: self.definir_data_atual_edicao(entry_data), style='Secondary.TButton').pack(side='left')
        
        # Campo de espetinho
        ttk.Label(frame, text="Espetinho:", font=self.fonte_principal).pack(anchor='w', pady=(0, 5))
        combo_edit = ttk.Combobox(frame, width=30, state='readonly', style='Modern.TCombobox')
        combo_edit.pack(fill='x', pady=(0, 10))
        combo_edit['values'] = list(self.dados['espetinhos'].keys())
        combo_edit.set(venda.get('espetinho', ''))
        
        # Campo de quantidade
        ttk.Label(frame, text="Quantidade:", font=self.fonte_principal).pack(anchor='w', pady=(0, 5))
        entry_qtd = ttk.Entry(frame, width=30, style='Modern.TEntry')
        entry_qtd.pack(fill='x', pady=(0, 10))
        entry_qtd.insert(0, str(venda['quantidade']))
        
        # Campo de valor unitário
        ttk.Label(frame, text="Valor Unitário:", font=self.fonte_principal).pack(anchor='w', pady=(0, 5))
        entry_valor = ttk.Entry(frame, width=30, style='Modern.TEntry')
        entry_valor.pack(fill='x', pady=(0, 20))
        entry_valor.insert(0, str(venda['valor_unitario']))
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill='x', pady=10)
        
        def salvar_edicao():
            try:
                espetinho = combo_edit.get()
                quantidade = int(entry_qtd.get())
                valor_unitario = float(entry_valor.get().replace(',', '.'))
                data_venda = entry_data.get().strip()
                
                if not espetinho:
                    self.mostrar_notificacao_erro("❌ Selecione um espetinho!")
                    return
                
                if quantidade <= 0:
                    self.mostrar_notificacao_erro("❌ Quantidade deve ser maior que zero!")
                    return
                
                # Validar data/hora
                if not data_venda:
                    self.mostrar_notificacao_erro("❌ Data/hora é obrigatória!")
                    return
                
                try:
                    # Validar formato da data
                    datetime.strptime(data_venda, '%d/%m/%Y %H:%M')
                except ValueError:
                    self.mostrar_notificacao_erro("❌ Formato de data inválido! Use DD/MM/AAAA HH:MM")
                    return
                
                # Calcular diferença no estoque apenas se a venda altera estoque
                if venda.get('alterou_estoque', True):
                    quantidade_antiga = venda['quantidade']
                    diferenca = quantidade - quantidade_antiga
                    
                    # Verificar se há estoque suficiente
                    estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
                    if estoque_atual < diferenca:
                        self.mostrar_notificacao_erro(f"❌ Estoque insuficiente! Disponível: {estoque_atual} unidades")
                        return
                    
                    # Atualizar estoque
                    self.dados['espetinhos'][espetinho]['estoque'] -= diferenca
                
                # Atualizar venda
                self.dados['vendas'][indice] = {
                    'data': data_venda,
                    'espetinho': espetinho,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'total': quantidade * valor_unitario,
                    'alterou_estoque': venda.get('alterou_estoque', True)
                }
                
                if self.salvar_dados():
                    self.atualizar_lista_vendas()
                    self.atualizar_lista_espetinhos()
                    self.atualizar_dashboard()
                    janela.destroy()
                    self.mostrar_notificacao_sucesso("✅ Venda editada com sucesso!")
                
            except ValueError:
                self.mostrar_notificacao_erro("❌ Valores inválidos!")
            except Exception as e:
                self.mostrar_notificacao_erro(f"❌ Erro ao editar venda: {str(e)}")
        
        ttk.Button(frame_botoes, text="💾 Salvar", command=salvar_edicao, style='Modern.TButton').pack(side='left', padx=10)
        ttk.Button(frame_botoes, text="❌ Cancelar", command=janela.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def criar_janela_edicao_despesa(self, indice, despesa):
        """Cria janela para editar despesa"""
        janela = tk.Toplevel(self.root)
        janela.title("Editar Despesa")
        janela.geometry("400x250")
        janela.grab_set()  # Modal
        
        # Frame principal
        frame = ttk.Frame(janela)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Editar Despesa", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Campos de edição
        ttk.Label(frame, text="Descrição:").pack(anchor='w')
        entry_desc = ttk.Entry(frame, width=30)
        entry_desc.pack(fill='x', pady=5)
        entry_desc.insert(0, despesa['descricao'])
        
        ttk.Label(frame, text="Valor:").pack(anchor='w')
        entry_valor = ttk.Entry(frame, width=30)
        entry_valor.pack(fill='x', pady=5)
        entry_valor.insert(0, str(despesa['valor']))
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill='x', pady=10)
        
        def salvar_edicao():
            try:
                descricao = entry_desc.get().strip()
                valor = float(entry_valor.get().replace(',', '.'))
                
                if not descricao:
                    messagebox.showerror("Erro", "Descrição é obrigatória!")
                    return
                
                # Atualizar despesa
                self.dados['despesas'][indice] = {
                    'data': despesa['data'],
                    'descricao': descricao,
                    'valor': valor
                }
                
                if self.salvar_dados():
                    self.atualizar_lista_despesas()
                    janela.destroy()
                    messagebox.showinfo("Sucesso", "Despesa editada com sucesso!")
                
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar despesa: {str(e)}")
        
        ttk.Button(frame_botoes, text="Salvar", command=salvar_edicao).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side='left', padx=5)
    
    def filtrar_vendas(self):
        """Filtra vendas por período"""
        try:
            data_inicial = self.entry_data_inicial.get().strip()
            data_final = self.entry_data_final.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar vendas
            vendas_filtradas = []
            for venda in self.dados['vendas']:
                data_venda = datetime.strptime(venda['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_venda <= data_fim:
                    vendas_filtradas.append(venda)
            
            # Atualizar lista
            self.atualizar_lista_vendas_filtrada(vendas_filtradas)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar vendas: {str(e)}")
    
    def mostrar_todas_vendas(self):
        """Mostra todas as vendas"""
        self.atualizar_lista_vendas()
    
    def filtrar_despesas(self):
        """Filtra despesas por período"""
        try:
            data_inicial = self.entry_data_inicial_despesa.get().strip()
            data_final = self.entry_data_final_despesa.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar despesas
            despesas_filtradas = []
            for despesa in self.dados['despesas']:
                data_despesa = datetime.strptime(despesa['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_despesa <= data_fim:
                    despesas_filtradas.append(despesa)
            
            # Atualizar lista
            self.atualizar_lista_despesas_filtrada(despesas_filtradas)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar despesas: {str(e)}")
    
    def mostrar_todas_despesas(self):
        """Mostra todas as despesas"""
        self.atualizar_lista_despesas()
    
    def gerar_relatorio_periodo(self):
        """Gera relatório para um período específico"""
        try:
            data_inicial = self.entry_data_inicial_rel.get().strip()
            data_final = self.entry_data_final_rel.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar vendas e despesas
            vendas_periodo = []
            despesas_periodo = []
            
            for venda in self.dados['vendas']:
                data_venda = datetime.strptime(venda['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_venda <= data_fim:
                    vendas_periodo.append(venda)
            
            for despesa in self.dados['despesas']:
                data_despesa = datetime.strptime(despesa['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_despesa <= data_fim:
                    despesas_periodo.append(despesa)
            
            # Calcular totais (usando valor cobrado)
            total_vendas = sum(self.get_valor_cobrado(venda) for venda in vendas_periodo)
            total_despesas = sum(despesa['valor'] for despesa in despesas_periodo)
            saldo = total_vendas - total_despesas
            
            # Calcular custo total das vendas do período
            total_custo_vendas = 0
            for venda in vendas_periodo:
                if 'espetinho' in venda:
                    espetinho = venda['espetinho']
                    quantidade = venda['quantidade']
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += quantidade * custo_unitario
            
            lucro_bruto = total_vendas - total_custo_vendas
            margem_lucro = (lucro_bruto / total_vendas * 100) if total_vendas > 0 else 0
            
            resumo = f"""
RELATÓRIO FINANCEIRO - PERÍODO: {data_inicial} a {data_final}

RECEITAS:
Total de Vendas: R$ {total_vendas:.2f}

CUSTOS:
Custo Total das Vendas: R$ {total_custo_vendas:.2f}
Outras Despesas: R$ {total_despesas:.2f}

LUCRO:
Lucro Bruto: R$ {lucro_bruto:.2f}
Margem de Lucro: {margem_lucro:.1f}%
Saldo do Período: R$ {saldo:.2f}

QUANTIDADES:
Vendas: {len(vendas_periodo)} transações
Despesas: {len(despesas_periodo)} registros
            """
            
            self.label_resumo.config(text=resumo)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_fechamento_mensal(self):
        """Gera relatório de fechamento mensal (por competência) e grava resumo no JSON"""
        try:
            data_final_str = self.entry_data_final_rel.get().strip()
            data_inicial_str = self.entry_data_inicial_rel.get().strip()

            # Usar data final como referência; se vazia, usar inicial
            data_ref_str = data_final_str or data_inicial_str
            if not data_ref_str:
                messagebox.showerror("Erro", "Preencha pelo menos a Data Final para definir o mês.")
                return

            dt_ref = datetime.strptime(data_ref_str, '%d/%m/%Y')
            ano = dt_ref.year
            mes = dt_ref.month
            competencia = f"{ano:04d}-{mes:02d}"

            # Filtrar vendas do mês pela competência (se existir) ou pela data
            vendas_mes = []
            for venda in self.dados['vendas']:
                comp_venda = venda.get('competencia')
                if comp_venda:
                    if comp_venda == competencia:
                        vendas_mes.append(venda)
                else:
                    # Fallback para vendas antigas: usar data string
                    try:
                        data_str = venda.get('data', '').split(' ')[0]
                        dt_venda = datetime.strptime(data_str, '%d/%m/%Y')
                        if dt_venda.year == ano and dt_venda.month == mes:
                            vendas_mes.append(venda)
                    except Exception:
                        continue

            # Filtrar despesas do mês
            despesas_mes = []
            for despesa in self.dados['despesas']:
                try:
                    data_str = despesa.get('data', '').split(' ')[0]
                    dt_desp = datetime.strptime(data_str, '%d/%m/%Y')
                    if dt_desp.year == ano and dt_desp.month == mes:
                        despesas_mes.append(despesa)
                except Exception:
                    continue

            # Totais principais
            total_cobrado = sum(self.get_valor_cobrado(v) for v in vendas_mes)
            total_bonificacoes_valor_tabela = sum(v.get('total', 0) for v in vendas_mes if v.get('tipo_venda') == 'bonificacao')
            qtd_bonificada = sum(v.get('quantidade', 0) for v in vendas_mes if v.get('tipo_venda') == 'bonificacao')

            # Consumo por tipo (quantidade e valor cobrado)
            consumo_por_tipo = {
                'local': {'qtd': 0, 'valor': 0.0},
                'entrega': {'qtd': 0, 'valor': 0.0},
                'interno': {'qtd': 0, 'valor': 0.0},
            }
            for v in vendas_mes:
                tipo = v.get('tipo_consumo', 'local')
                if tipo in consumo_por_tipo:
                    consumo_por_tipo[tipo]['qtd'] += v.get('quantidade', 0)
                    consumo_por_tipo[tipo]['valor'] += self.get_valor_cobrado(v)

            # Custo das vendas no mês
            total_custo_vendas = 0.0
            for v in vendas_mes:
                espetinho = v.get('espetinho')
                if espetinho and espetinho in self.dados['espetinhos']:
                    custo_unit = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += custo_unit * v.get('quantidade', 0)

            total_despesas = sum(d['valor'] for d in despesas_mes)

            lucro_bruto = total_cobrado - total_custo_vendas
            margem_bruta = (lucro_bruto / total_cobrado * 100) if total_cobrado > 0 else 0
            saldo_final = total_cobrado - total_despesas

            # Ticket médio (só vendas pagas)
            qtd_vendas_pagas = sum(1 for v in vendas_mes if self.get_valor_cobrado(v) > 0)
            ticket_medio = total_cobrado / qtd_vendas_pagas if qtd_vendas_pagas > 0 else 0

            # Resumo textual
            nome_mes = [
                'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ][mes-1]

            resumo = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📅 FECHAMENTO MENSAL - {nome_mes}/{ano} ({competencia})                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

📌 RESUMO GERAL:
   • Vendas: {len(vendas_mes)} lançamentos (pagas + bonificações)
   • Despesas: {len(despesas_mes)} registros

💰 FATURAMENTO (PAGO):
   • Total Cobrado: R$ {total_cobrado:,.2f}
   • Ticket Médio (pagas): R$ {ticket_medio:,.2f}

🎁 BONIFICAÇÕES:
   • Quantidade Bonificada: {qtd_bonificada} unidades
   • Valor de Tabela Bonificado: R$ {total_bonificacoes_valor_tabela:,.2f}

📦 CONSUMO POR TIPO:
   • Local:   {consumo_por_tipo['local']['qtd']} unid. | R$ {consumo_por_tipo['local']['valor']:,.2f}
   • Entrega: {consumo_por_tipo['entrega']['qtd']} unid. | R$ {consumo_por_tipo['entrega']['valor']:,.2f}
   • Interno: {consumo_por_tipo['interno']['qtd']} unid. | R$ {consumo_por_tipo['interno']['valor']:,.2f}

💸 CUSTOS E DESPESAS:
   • Custo dos Espetinhos Vendidos: R$ {total_custo_vendas:,.2f}
   • Outras Despesas (caixa):       R$ {total_despesas:,.2f}

📈 RESULTADO DO MÊS:
   • Lucro Bruto (Vendas - Custo): R$ {lucro_bruto:,.2f}
   • Margem Bruta: {margem_bruta:.1f}%{" (sobre o que foi cobrado)" if total_cobrado > 0 else ""}
   • Saldo Final (Cobrado - Despesas): R$ {saldo_final:,.2f}
   • Status: {'✅ LUCRO' if saldo_final > 0 else '❌ PREJUÍZO' if saldo_final < 0 else '⚖️ NO ZERO A ZERO'}
"""

            # Mostrar no painel de texto
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(1.0, resumo)

            # Gravar fechamento no JSON para histórico
            fechamentos = self.dados.get('fechamentos_mensais', {})
            fechamentos[competencia] = {
                'ano': ano,
                'mes': mes,
                'nome_mes': nome_mes,
                'total_cobrado': total_cobrado,
                'total_bonificacoes_valor_tabela': total_bonificacoes_valor_tabela,
                'qtd_bonificada': qtd_bonificada,
                'consumo_por_tipo': consumo_por_tipo,
                'total_custo_vendas': total_custo_vendas,
                'total_despesas': total_despesas,
                'lucro_bruto': lucro_bruto,
                'margem_bruta': margem_bruta,
                'saldo_final': saldo_final,
                'ticket_medio': ticket_medio,
                'qtd_vendas': len(vendas_mes),
                'qtd_despesas': len(despesas_mes),
                'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            self.dados['fechamentos_mensais'] = fechamentos
            self.salvar_dados()

        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar fechamento mensal: {str(e)}")
    
    def gerar_relatorio_fechamentos_mensais(self):
        """Mostra um comparativo de todos os fechamentos mensais já gravados"""
        fechamentos = self.dados.get('fechamentos_mensais', {})
        if not fechamentos:
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(1.0, "❌ Ainda não há fechamentos mensais gravados.\n\nUse o botão '📅 Fechamento Mensal' para gerar o primeiro.")
            return

        # Ordenar por competência (AAAAMM)
        competencias_ordenadas = sorted(fechamentos.keys())

        linhas = []
        linhas.append("╔════════════════════════════════════════════════════════════════════╗")
        linhas.append("║                  📚 HISTÓRICO DE FECHAMENTOS MENSAIS               ║")
        linhas.append("╚════════════════════════════════════════════════════════════════════╝")
        linhas.append("")

        linhas.append(f"{'Comp.':<8} {'Mês/Ano':<12} {'Faturado':>12} {'Despesas':>12} {'Saldo':>12} {'Bonif. Tbl':>12}")
        linhas.append("-" * 70)

        total_faturado = 0.0
        total_despesas = 0.0
        total_saldo = 0.0
        total_bonif = 0.0

        for comp in competencias_ordenadas:
            f = fechamentos.get(comp, {})
            nome_mes = f.get('nome_mes', '')
            ano = f.get('ano', '')
            faturado = float(f.get('total_cobrado', 0))
            despesas = float(f.get('total_despesas', 0))
            saldo = float(f.get('saldo_final', faturado - despesas))
            bonif = float(f.get('total_bonificacoes_valor_tabela', 0))

            total_faturado += faturado
            total_despesas += despesas
            total_saldo += saldo
            total_bonif += bonif

            linhas.append(f"{comp:<8} {nome_mes}/{ano:<10} R$ {faturado:>9.2f} R$ {despesas:>9.2f} R$ {saldo:>9.2f} R$ {bonif:>9.2f}")

        linhas.append("-" * 70)
        linhas.append(f"{'TOTAL':<20} R$ {total_faturado:>9.2f} R$ {total_despesas:>9.2f} R$ {total_saldo:>9.2f} R$ {total_bonif:>9.2f}")
        linhas.append("")

        # Pequena análise
        linhas.append("📈 RESUMO RÁPIDO:")
        linhas.append(f"   • Meses fechados: {len(competencias_ordenadas)}")
        linhas.append(f"   • Média de faturamento/mês: R$ {(total_faturado/len(competencias_ordenadas)):.2f}")
        linhas.append(f"   • Média de saldo/mês:       R$ {(total_saldo/len(competencias_ordenadas)):.2f}")

        texto = "\n".join(linhas)
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, texto)
    
    def atualizar_lista_vendas_filtrada(self, vendas_filtradas):
        """Atualiza a lista de vendas com dados filtrados"""
        # Limpar lista atual
        for item in self.tree_vendas.get_children():
            self.tree_vendas.delete(item)
        
        # Adicionar vendas filtradas
        for venda in vendas_filtradas:
            descricao = venda.get('espetinho', venda.get('descricao', ''))
            origem = venda.get('origem', 'desktop')
            origem_emoji = "📱 MOBILE" if origem == 'mobile' else "💻 DESKTOP"
            
            self.tree_vendas.insert('', 'end', values=(
                venda['data'],
                descricao,
                venda['quantidade'],
                f"R$ {venda['valor_unitario']:.2f}",
                f"R$ {venda['total']:.2f}",
                origem_emoji
            ))
    
    def atualizar_lista_despesas_filtrada(self, despesas_filtradas):
        """Atualiza a lista de despesas com dados filtrados"""
        # Limpar lista atual
        for item in self.tree_despesas.get_children():
            self.tree_despesas.delete(item)
        
        # Adicionar despesas filtradas
        for despesa in despesas_filtradas:
            self.tree_despesas.insert('', 'end', values=(
                despesa['data'],
                despesa['descricao'],
                f"R$ {despesa['valor']:.2f}"
            ))
    
    def executar(self):
        """Executa o sistema"""
        # Debug: mostrar dados carregados
        print("=== DADOS CARREGADOS ===")
        print(f"Total de vendas: {len(self.dados['vendas'])}")
        print(f"Total de despesas: {len(self.dados['despesas'])}")
        print(f"Total de espetinhos: {len(self.dados['espetinhos'])}")
        print("========================")
        
        self.root.mainloop()

if __name__ == "__main__":
    sistema = SistemaEspetinho()
    sistema.executar()

                    diferenca = quantidade - quantidade_antiga
                    
                    # Verificar se há estoque suficiente
                    estoque_atual = self.dados['espetinhos'][espetinho]['estoque']
                    if estoque_atual < diferenca:
                        self.mostrar_notificacao_erro(f"❌ Estoque insuficiente! Disponível: {estoque_atual} unidades")
                        return
                    
                    # Atualizar estoque
                    self.dados['espetinhos'][espetinho]['estoque'] -= diferenca
                
                # Atualizar venda
                self.dados['vendas'][indice] = {
                    'data': data_venda,
                    'espetinho': espetinho,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'total': quantidade * valor_unitario,
                    'alterou_estoque': venda.get('alterou_estoque', True)
                }
                
                if self.salvar_dados():
                    self.atualizar_lista_vendas()
                    self.atualizar_lista_espetinhos()
                    self.atualizar_dashboard()
                    janela.destroy()
                    self.mostrar_notificacao_sucesso("✅ Venda editada com sucesso!")
                
            except ValueError:
                self.mostrar_notificacao_erro("❌ Valores inválidos!")
            except Exception as e:
                self.mostrar_notificacao_erro(f"❌ Erro ao editar venda: {str(e)}")
        
        ttk.Button(frame_botoes, text="💾 Salvar", command=salvar_edicao, style='Modern.TButton').pack(side='left', padx=10)
        ttk.Button(frame_botoes, text="❌ Cancelar", command=janela.destroy, style='Secondary.TButton').pack(side='left', padx=10)
    
    def criar_janela_edicao_despesa(self, indice, despesa):
        """Cria janela para editar despesa"""
        janela = tk.Toplevel(self.root)
        janela.title("Editar Despesa")
        janela.geometry("400x250")
        janela.grab_set()  # Modal
        
        # Frame principal
        frame = ttk.Frame(janela)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Editar Despesa", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Campos de edição
        ttk.Label(frame, text="Descrição:").pack(anchor='w')
        entry_desc = ttk.Entry(frame, width=30)
        entry_desc.pack(fill='x', pady=5)
        entry_desc.insert(0, despesa['descricao'])
        
        ttk.Label(frame, text="Valor:").pack(anchor='w')
        entry_valor = ttk.Entry(frame, width=30)
        entry_valor.pack(fill='x', pady=5)
        entry_valor.insert(0, str(despesa['valor']))
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill='x', pady=10)
        
        def salvar_edicao():
            try:
                descricao = entry_desc.get().strip()
                valor = float(entry_valor.get().replace(',', '.'))
                
                if not descricao:
                    messagebox.showerror("Erro", "Descrição é obrigatória!")
                    return
                
                # Atualizar despesa
                self.dados['despesas'][indice] = {
                    'data': despesa['data'],
                    'descricao': descricao,
                    'valor': valor
                }
                
                if self.salvar_dados():
                    self.atualizar_lista_despesas()
                    janela.destroy()
                    messagebox.showinfo("Sucesso", "Despesa editada com sucesso!")
                
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar despesa: {str(e)}")
        
        ttk.Button(frame_botoes, text="Salvar", command=salvar_edicao).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side='left', padx=5)
    
    def filtrar_vendas(self):
        """Filtra vendas por período"""
        try:
            data_inicial = self.entry_data_inicial.get().strip()
            data_final = self.entry_data_final.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar vendas
            vendas_filtradas = []
            for venda in self.dados['vendas']:
                data_venda = datetime.strptime(venda['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_venda <= data_fim:
                    vendas_filtradas.append(venda)
            
            # Atualizar lista
            self.atualizar_lista_vendas_filtrada(vendas_filtradas)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar vendas: {str(e)}")
    
    def mostrar_todas_vendas(self):
        """Mostra todas as vendas"""
        self.atualizar_lista_vendas()
    
    def filtrar_despesas(self):
        """Filtra despesas por período"""
        try:
            data_inicial = self.entry_data_inicial_despesa.get().strip()
            data_final = self.entry_data_final_despesa.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar despesas
            despesas_filtradas = []
            for despesa in self.dados['despesas']:
                data_despesa = datetime.strptime(despesa['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_despesa <= data_fim:
                    despesas_filtradas.append(despesa)
            
            # Atualizar lista
            self.atualizar_lista_despesas_filtrada(despesas_filtradas)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar despesas: {str(e)}")
    
    def mostrar_todas_despesas(self):
        """Mostra todas as despesas"""
        self.atualizar_lista_despesas()
    
    def gerar_relatorio_periodo(self):
        """Gera relatório para um período específico"""
        try:
            data_inicial = self.entry_data_inicial_rel.get().strip()
            data_final = self.entry_data_final_rel.get().strip()
            
            if not data_inicial or not data_final:
                messagebox.showerror("Erro", "Preencha as datas inicial e final!")
                return
            
            # Converter datas para datetime
            data_ini = datetime.strptime(data_inicial, '%d/%m/%Y')
            data_fim = datetime.strptime(data_final, '%d/%m/%Y')
            
            # Filtrar vendas e despesas
            vendas_periodo = []
            despesas_periodo = []
            
            for venda in self.dados['vendas']:
                data_venda = datetime.strptime(venda['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_venda <= data_fim:
                    vendas_periodo.append(venda)
            
            for despesa in self.dados['despesas']:
                data_despesa = datetime.strptime(despesa['data'].split(' ')[0], '%d/%m/%Y')
                if data_ini <= data_despesa <= data_fim:
                    despesas_periodo.append(despesa)
            
            # Calcular totais (usando valor cobrado)
            total_vendas = sum(self.get_valor_cobrado(venda) for venda in vendas_periodo)
            total_despesas = sum(despesa['valor'] for despesa in despesas_periodo)
            saldo = total_vendas - total_despesas
            
            # Calcular custo total das vendas do período
            total_custo_vendas = 0
            for venda in vendas_periodo:
                if 'espetinho' in venda:
                    espetinho = venda['espetinho']
                    quantidade = venda['quantidade']
                    custo_unitario = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += quantidade * custo_unitario
            
            lucro_bruto = total_vendas - total_custo_vendas
            margem_lucro = (lucro_bruto / total_vendas * 100) if total_vendas > 0 else 0
            
            resumo = f"""
RELATÓRIO FINANCEIRO - PERÍODO: {data_inicial} a {data_final}

RECEITAS:
Total de Vendas: R$ {total_vendas:.2f}

CUSTOS:
Custo Total das Vendas: R$ {total_custo_vendas:.2f}
Outras Despesas: R$ {total_despesas:.2f}

LUCRO:
Lucro Bruto: R$ {lucro_bruto:.2f}
Margem de Lucro: {margem_lucro:.1f}%
Saldo do Período: R$ {saldo:.2f}

QUANTIDADES:
Vendas: {len(vendas_periodo)} transações
Despesas: {len(despesas_periodo)} registros
            """
            
            self.label_resumo.config(text=resumo)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_fechamento_mensal(self):
        """Gera relatório de fechamento mensal (por competência) e grava resumo no JSON"""
        try:
            data_final_str = self.entry_data_final_rel.get().strip()
            data_inicial_str = self.entry_data_inicial_rel.get().strip()

            # Usar data final como referência; se vazia, usar inicial
            data_ref_str = data_final_str or data_inicial_str
            if not data_ref_str:
                messagebox.showerror("Erro", "Preencha pelo menos a Data Final para definir o mês.")
                return

            dt_ref = datetime.strptime(data_ref_str, '%d/%m/%Y')
            ano = dt_ref.year
            mes = dt_ref.month
            competencia = f"{ano:04d}-{mes:02d}"

            # Filtrar vendas do mês pela competência (se existir) ou pela data
            vendas_mes = []
            for venda in self.dados['vendas']:
                comp_venda = venda.get('competencia')
                if comp_venda:
                    if comp_venda == competencia:
                        vendas_mes.append(venda)
                else:
                    # Fallback para vendas antigas: usar data string
                    try:
                        data_str = venda.get('data', '').split(' ')[0]
                        dt_venda = datetime.strptime(data_str, '%d/%m/%Y')
                        if dt_venda.year == ano and dt_venda.month == mes:
                            vendas_mes.append(venda)
                    except Exception:
                        continue

            # Filtrar despesas do mês
            despesas_mes = []
            for despesa in self.dados['despesas']:
                try:
                    data_str = despesa.get('data', '').split(' ')[0]
                    dt_desp = datetime.strptime(data_str, '%d/%m/%Y')
                    if dt_desp.year == ano and dt_desp.month == mes:
                        despesas_mes.append(despesa)
                except Exception:
                    continue

            # Totais principais
            total_cobrado = sum(self.get_valor_cobrado(v) for v in vendas_mes)
            total_bonificacoes_valor_tabela = sum(v.get('total', 0) for v in vendas_mes if v.get('tipo_venda') == 'bonificacao')
            qtd_bonificada = sum(v.get('quantidade', 0) for v in vendas_mes if v.get('tipo_venda') == 'bonificacao')

            # Consumo por tipo (quantidade e valor cobrado)
            consumo_por_tipo = {
                'local': {'qtd': 0, 'valor': 0.0},
                'entrega': {'qtd': 0, 'valor': 0.0},
                'interno': {'qtd': 0, 'valor': 0.0},
            }
            for v in vendas_mes:
                tipo = v.get('tipo_consumo', 'local')
                if tipo in consumo_por_tipo:
                    consumo_por_tipo[tipo]['qtd'] += v.get('quantidade', 0)
                    consumo_por_tipo[tipo]['valor'] += self.get_valor_cobrado(v)

            # Custo das vendas no mês
            total_custo_vendas = 0.0
            for v in vendas_mes:
                espetinho = v.get('espetinho')
                if espetinho and espetinho in self.dados['espetinhos']:
                    custo_unit = self.dados['espetinhos'][espetinho]['custo']
                    total_custo_vendas += custo_unit * v.get('quantidade', 0)

            total_despesas = sum(d['valor'] for d in despesas_mes)

            lucro_bruto = total_cobrado - total_custo_vendas
            margem_bruta = (lucro_bruto / total_cobrado * 100) if total_cobrado > 0 else 0
            saldo_final = total_cobrado - total_despesas

            # Ticket médio (só vendas pagas)
            qtd_vendas_pagas = sum(1 for v in vendas_mes if self.get_valor_cobrado(v) > 0)
            ticket_medio = total_cobrado / qtd_vendas_pagas if qtd_vendas_pagas > 0 else 0

            # Resumo textual
            nome_mes = [
                'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
            ][mes-1]

            resumo = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📅 FECHAMENTO MENSAL - {nome_mes}/{ano} ({competencia})                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

📌 RESUMO GERAL:
   • Vendas: {len(vendas_mes)} lançamentos (pagas + bonificações)
   • Despesas: {len(despesas_mes)} registros

💰 FATURAMENTO (PAGO):
   • Total Cobrado: R$ {total_cobrado:,.2f}
   • Ticket Médio (pagas): R$ {ticket_medio:,.2f}

🎁 BONIFICAÇÕES:
   • Quantidade Bonificada: {qtd_bonificada} unidades
   • Valor de Tabela Bonificado: R$ {total_bonificacoes_valor_tabela:,.2f}

📦 CONSUMO POR TIPO:
   • Local:   {consumo_por_tipo['local']['qtd']} unid. | R$ {consumo_por_tipo['local']['valor']:,.2f}
   • Entrega: {consumo_por_tipo['entrega']['qtd']} unid. | R$ {consumo_por_tipo['entrega']['valor']:,.2f}
   • Interno: {consumo_por_tipo['interno']['qtd']} unid. | R$ {consumo_por_tipo['interno']['valor']:,.2f}

💸 CUSTOS E DESPESAS:
   • Custo dos Espetinhos Vendidos: R$ {total_custo_vendas:,.2f}
   • Outras Despesas (caixa):       R$ {total_despesas:,.2f}

📈 RESULTADO DO MÊS:
   • Lucro Bruto (Vendas - Custo): R$ {lucro_bruto:,.2f}
   • Margem Bruta: {margem_bruta:.1f}%{" (sobre o que foi cobrado)" if total_cobrado > 0 else ""}
   • Saldo Final (Cobrado - Despesas): R$ {saldo_final:,.2f}
   • Status: {'✅ LUCRO' if saldo_final > 0 else '❌ PREJUÍZO' if saldo_final < 0 else '⚖️ NO ZERO A ZERO'}
"""

            # Mostrar no painel de texto
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(1.0, resumo)

            # Gravar fechamento no JSON para histórico
            fechamentos = self.dados.get('fechamentos_mensais', {})
            fechamentos[competencia] = {
                'ano': ano,
                'mes': mes,
                'nome_mes': nome_mes,
                'total_cobrado': total_cobrado,
                'total_bonificacoes_valor_tabela': total_bonificacoes_valor_tabela,
                'qtd_bonificada': qtd_bonificada,
                'consumo_por_tipo': consumo_por_tipo,
                'total_custo_vendas': total_custo_vendas,
                'total_despesas': total_despesas,
                'lucro_bruto': lucro_bruto,
                'margem_bruta': margem_bruta,
                'saldo_final': saldo_final,
                'ticket_medio': ticket_medio,
                'qtd_vendas': len(vendas_mes),
                'qtd_despesas': len(despesas_mes),
                'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            self.dados['fechamentos_mensais'] = fechamentos
            self.salvar_dados()

        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar fechamento mensal: {str(e)}")
    
    def gerar_relatorio_fechamentos_mensais(self):
        """Mostra um comparativo de todos os fechamentos mensais já gravados"""
        fechamentos = self.dados.get('fechamentos_mensais', {})
        if not fechamentos:
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(1.0, "❌ Ainda não há fechamentos mensais gravados.\n\nUse o botão '📅 Fechamento Mensal' para gerar o primeiro.")
            return

        # Ordenar por competência (AAAAMM)
        competencias_ordenadas = sorted(fechamentos.keys())

        linhas = []
        linhas.append("╔════════════════════════════════════════════════════════════════════╗")
        linhas.append("║                  📚 HISTÓRICO DE FECHAMENTOS MENSAIS               ║")
        linhas.append("╚════════════════════════════════════════════════════════════════════╝")
        linhas.append("")

        linhas.append(f"{'Comp.':<8} {'Mês/Ano':<12} {'Faturado':>12} {'Despesas':>12} {'Saldo':>12} {'Bonif. Tbl':>12}")
        linhas.append("-" * 70)

        total_faturado = 0.0
        total_despesas = 0.0
        total_saldo = 0.0
        total_bonif = 0.0

        for comp in competencias_ordenadas:
            f = fechamentos.get(comp, {})
            nome_mes = f.get('nome_mes', '')
            ano = f.get('ano', '')
            faturado = float(f.get('total_cobrado', 0))
            despesas = float(f.get('total_despesas', 0))
            saldo = float(f.get('saldo_final', faturado - despesas))
            bonif = float(f.get('total_bonificacoes_valor_tabela', 0))

            total_faturado += faturado
            total_despesas += despesas
            total_saldo += saldo
            total_bonif += bonif

            linhas.append(f"{comp:<8} {nome_mes}/{ano:<10} R$ {faturado:>9.2f} R$ {despesas:>9.2f} R$ {saldo:>9.2f} R$ {bonif:>9.2f}")

        linhas.append("-" * 70)
        linhas.append(f"{'TOTAL':<20} R$ {total_faturado:>9.2f} R$ {total_despesas:>9.2f} R$ {total_saldo:>9.2f} R$ {total_bonif:>9.2f}")
        linhas.append("")

        # Pequena análise
        linhas.append("📈 RESUMO RÁPIDO:")
        linhas.append(f"   • Meses fechados: {len(competencias_ordenadas)}")
        linhas.append(f"   • Média de faturamento/mês: R$ {(total_faturado/len(competencias_ordenadas)):.2f}")
        linhas.append(f"   • Média de saldo/mês:       R$ {(total_saldo/len(competencias_ordenadas)):.2f}")

        texto = "\n".join(linhas)
        self.text_resumo.delete(1.0, tk.END)
        self.text_resumo.insert(1.0, texto)
    
    def atualizar_lista_vendas_filtrada(self, vendas_filtradas):
        """Atualiza a lista de vendas com dados filtrados"""
        # Limpar lista atual
        for item in self.tree_vendas.get_children():
            self.tree_vendas.delete(item)
        
        # Adicionar vendas filtradas
        for venda in vendas_filtradas:
            descricao = venda.get('espetinho', venda.get('descricao', ''))
            origem = venda.get('origem', 'desktop')
            origem_emoji = "📱 MOBILE" if origem == 'mobile' else "💻 DESKTOP"
            
            self.tree_vendas.insert('', 'end', values=(
                venda['data'],
                descricao,
                venda['quantidade'],
                f"R$ {venda['valor_unitario']:.2f}",
                f"R$ {venda['total']:.2f}",
                origem_emoji
            ))
    
    def atualizar_lista_despesas_filtrada(self, despesas_filtradas):
        """Atualiza a lista de despesas com dados filtrados"""
        # Limpar lista atual
        for item in self.tree_despesas.get_children():
            self.tree_despesas.delete(item)
        
        # Adicionar despesas filtradas
        for despesa in despesas_filtradas:
            self.tree_despesas.insert('', 'end', values=(
                despesa['data'],
                despesa['descricao'],
                f"R$ {despesa['valor']:.2f}"
            ))
    
    def executar(self):
        """Executa o sistema"""
        # Debug: mostrar dados carregados
        print("=== DADOS CARREGADOS ===")
        print(f"Total de vendas: {len(self.dados['vendas'])}")
        print(f"Total de despesas: {len(self.dados['despesas'])}")
        print(f"Total de espetinhos: {len(self.dados['espetinhos'])}")
        print("========================")
        
        self.root.mainloop()

if __name__ == "__main__":
    sistema = SistemaEspetinho()
    sistema.executar()
