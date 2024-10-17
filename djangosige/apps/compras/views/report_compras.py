# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from djangosige.apps.compras.models import ItensCompra, Pagamento


class CompraReport(object):

    def __init__(self, compra_id, *args, **kwargs):
        self.title = _('Relatorio de compra')

        self.filename = 'compra_report.pdf'
        self.doc = SimpleDocTemplate(self.filename, pagesize=A4)
        self.elements = []

        self.dados_fornecedor = DadosFornecedor()
        self.dados_produtos = DadosProdutosCompra(compra_id)
        self.dados_pagamento = DadosPagamentoCompra(compra_id)

        self.build()

    def build(self):
        self.elements.append(Paragraph(self.title, ParagraphStyle(name='Title1', fontName='Helvetica-Bold', fontSize=16)))
        self.elements.append(Spacer(0, 0.5 * cm))

        self.elements.extend(self.dados_fornecedor.elements)
        self.elements.extend(self.dados_produtos.elements)
        self.elements.extend(self.dados_pagamento.elements)

        self.doc.build(self.elements)


class DadosFornecedor(object):

    def __init__(self):
        self.ender_info = False
        self.elements = []

        self.fornecedor = None  # Isso deve ser passado ou atribuído corretamente
        txt = Paragraph(_('Fornecedor: ') + self.fornecedor.nome_razao_social if self.fornecedor else '', ParagraphStyle(name='Fornecedor', fontName='Helvetica-Bold', fontSize=12))
        txt.wrapOn(None, 19.4 * cm, 0.5 * cm)  # Não usamos 'self.doc' aqui
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 1
        self.elements.append(txt)

        self.height = 2.7 * cm

    def inserir_informacoes_pj(self):
        if self.fornecedor and hasattr(self.fornecedor, 'pessoa_jur_info'):
            txt = Paragraph(_('CNPJ: ') + self.fornecedor.pessoa_jur_info.format_cnpj, ParagraphStyle(name='Fornecedor', fontName='Helvetica-Bold', fontSize=10))
            self.elements.append(txt)

            txt = Paragraph(_('IE: ') + self.fornecedor.pessoa_jur_info.format_ie, ParagraphStyle(name='Fornecedor', fontName='Helvetica-Bold', fontSize=10))
            self.elements.append(txt)

    def inserir_informacoes_pf(self):
        if self.fornecedor and hasattr(self.fornecedor, 'pessoa_fis_info'):
            txt = Paragraph(_('CPF: ') + self.fornecedor.pessoa_fis_info.format_cpf, ParagraphStyle(name='Fornecedor', fontName='Helvetica-Bold', fontSize=10))
            self.elements.append(txt)

            txt = Paragraph(_('RG: ') + self.fornecedor.pessoa_fis_info.format_rg, ParagraphStyle(name='Fornecedor', fontName='Helvetica-Bold', fontSize=10))
            self.elements.append(txt)

    def inserir_informacoes_endereco(self):
        if self.fornecedor and hasattr(self.fornecedor, 'endereco_padrao'):
            self.ender_info = True
            txt = Paragraph(_('Endereço: ') + self.fornecedor.endereco_padrao.format_endereco, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)

            txt = Paragraph(_('Cidade: ') + self.fornecedor.endereco_padrao.municipio, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)

            txt = Paragraph(_('UF: ') + self.fornecedor.endereco_padrao.uf, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)

            txt = Paragraph(_('CEP: ') + self.fornecedor.endereco_padrao.cep, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)

    def inserir_informacoes_telefone(self):
        if self.fornecedor and hasattr(self.fornecedor, 'telefone_padrao'):
            txt = Paragraph(_('Telefone: ') + self.fornecedor.telefone_padrao.telefone, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)

    def inserir_informacoes_email(self):
        if self.fornecedor and hasattr(self.fornecedor, 'email_padrao'):
            txt = Paragraph(_('Email: ') + self.fornecedor.email_padrao.email, ParagraphStyle(name='Fornecedor', fontName='Helvetica', fontSize=10))
            self.elements.append(txt)


class DadosProdutosCompra(object):

    def __init__(self, compra_id):
        self.elements = []

        # Função lambda corrigida
        self.get_queryset = lambda compra_id: ItensCompra.objects.filter(compra_id=compra_id) or []

        # Consulta os itens de compra
        self.data = self.get_queryset(compra_id)

        # Cria a tabela de produtos
        self.table = Table([[u'Produto', u'Quantidade', u'Valor Unit.', u'Valor Total']], colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm])

        # Preenche a tabela com os dados dos produtos
        for item in self.data:
            self.table._argW.append([item.produto.descricao, str(item.quantidade), str(item.valor_unit), str(item.valor_total)])

        # Estilo da tabela
        self.table.setStyle(TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
             ('FONTSIZE', (0, 0), (-1, -1), 8),
             ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
             ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
             ('ALIGN', (3, 0), (3, -1), 'RIGHT')]))

        # Adiciona a tabela aos elementos
        self.elements.append(self.table)


class DadosPagamentoCompra(object):

    def __init__(self, compra_id):
        self.elements = []

        # Função lambda corrigida
        self.get_queryset = lambda compra_id: Pagamento.objects.filter(compra_id=compra_id) or []

        # Consulta os pagamentos
        self.data = self.get_queryset(compra_id)

        # Cria a tabela de pagamentos
        self.table = Table([[u'Forma de Pagamento', u'Valor', u'Vencimento', u'Status']], colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm])

        # Preenche a tabela com os dados dos pagamentos
        for item in self.data:
            self.table.append([item.forma_pagamento.nome, str(item.valor), str(item.data_vencimento), item.get_status_display()])

        # Estilo da tabela
        self.table.setStyle(TableStyle(
            [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
             ('FONTSIZE', (0, 0), (-1, -1), 8),
             ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
             ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
             ('ALIGN', (3, 0), (3, -1), 'RIGHT')]))

        # Adiciona a tabela aos elementos
        self.elements.append(self.table)

