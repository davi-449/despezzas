# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from djangosige.apps.vendas.models import ItensVenda, Pagamento

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

REPORT_FONT = 'Times'
REPORT_FONT_BOLD = REPORT_FONT + '-Bold'

class VendaReport:
    def __init__(self, venda):
        self.venda = venda
        self.doc = SimpleDocTemplate("venda.pdf", pagesize=A4)
        self.styles = self.get_styles()
        self.elements = []

    def get_styles(self):
        styles = []
        styles.append(ParagraphStyle(name='Normal', fontName=REPORT_FONT, fontSize=10, leading=12))
        styles.append(ParagraphStyle(name='Bold', fontName=REPORT_FONT_BOLD, fontSize=10, leading=12))
        return styles

    def build(self):
        self.topo_pagina()
        self.dados_cliente()
        self.banda_produtos()
        self.dados_produtos()
        self.totais_venda()
        self.banda_pagamento()
        self.dados_pagamento()
        self.observacoes()
        self.banda_foot()
        self.doc.build(self.elements)

    def topo_pagina(self):
        txt = Paragraph('Relatorio de venda', self.styles[1])
        txt.wrapOn(self.doc, 19.4 * cm, 0.8 * cm)
        txt.drawHeight = 0.8 * cm
        txt.drawWidth = 19.4 * cm
        self.elements.append(txt)

        txt = Paragraph('Página 1 de 1', self.styles[0])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 2
        self.elements.append(txt)

        self.elements.append(Spacer(1, 0.3 * cm))

    def dados_cliente(self):
        txt = Paragraph(self.venda.cliente.nome_razao_social, self.styles[1])
        txt.wrapOn(self.doc, 8 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 8 * cm
        self.elements.append(txt)

        if self.venda.cliente.pessoa_juridica:
            txt = Paragraph(self.venda.cliente.pessoa_juridica.format_cnpj, self.styles[1])
            txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
            txt.drawHeight = 0.5 * cm
            txt.drawWidth = 4 * cm
            self.elements.append(txt)

            txt = Paragraph(self.venda.cliente.pessoa_juridica.format_ie, self.styles[1])
            txt.wrapOn(self.doc, 6.4 * cm, 0.5 * cm)
            txt.drawHeight = 0.5 * cm
            txt.drawWidth = 6.4 * cm
            self.elements.append(txt)
        else:
            txt = Paragraph(self.venda.cliente.pessoa_fisica.format_cpf, self.styles[1])
            txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
            txt.drawHeight = 0.5 * cm
            txt.drawWidth = 4 * cm
            self.elements.append(txt)

            txt = Paragraph(self.venda.cliente.pessoa_fisica.format_rg, self.styles[1])
            txt.wrapOn(self.doc, 6.4 * cm, 0.5 * cm)
            txt.drawHeight = 0.5 * cm
            txt.drawWidth = 6.4 * cm
            self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.endereco_padrao.format_endereco, self.styles[0])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.endereco_padrao.municipio, self.styles[0])
        txt.wrapOn(self.doc, 8 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 8 * cm
        self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.endereco_padrao.uf, self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.endereco_padrao.cep, self.styles[0])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.telefone_padrao.telefone, self.styles[0])
        txt.wrapOn(self.doc, 8 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 8 * cm
        self.elements.append(txt)

        txt = Paragraph(self.venda.cliente.email_padrao.email, self.styles[0])
        txt.wrapOn(self.doc, 11.3 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 11.3 * cm
        self.elements.append(txt)

    def banda_produtos(self):
        data = []
        for item in self.venda.itensvenda_set.all():
            data.append([item.produto.codigo, item.produto.descricao, item.produto.format_unidade, item.format_quantidade, item.format_valor_unit, item.format_desconto, item.format_total])
        table = Table(data, style=[('GRID', (0, 0), (-1, -1), 0.5), ('FONTNAME', (0, 0), (-1, 0), REPORT_FONT_BOLD), ('FONTSIZE', (0, 0), (-1, -1), 9)])
        self.elements.append(table)

    def dados_produtos(self):
        pass

    def totais_venda(self):
        txt = Paragraph('Totais', self.styles[1])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 1
        self.elements.append(txt)

        txt = Paragraph('Frete: R$ ' + self.venda.format_frete, self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph('Seguro: R$ ' + self.venda.format_seguro, self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph('Despesas: R$ ' + self.venda.format_despesas, self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph('Desconto: R$ ' + self.venda.format_desconto, self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph('Impostos: R$ ' + self.venda.format_impostos, self.styles[0])
        txt.wrapOn(self.doc, 3.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 3.4 * cm
        self.elements.append(txt)

        txt = Paragraph('Total sem impostos: R$ ' + self.venda.format_total_sem_imposto, self.styles[0])
        txt.wrapOn(self.doc, 13.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 13.4 * cm
        txt.alignment = 2
        self.elements.append(txt)

        txt = Paragraph('Total: R$ ' + self.venda.format_valor_total, self.styles[1])
        txt.wrapOn(self.doc, 5.6 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 5.6 * cm
        txt.alignment = 2
        self.elements.append(txt)

    def banda_pagamento(self):
        txt = Paragraph('Pagamento', self.styles[1])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 1
        self.elements.append(txt)

        txt = Paragraph('Forma: ' + self.venda.cond_pagamento.get_forma_display(), self.styles[0])
        txt.wrapOn(self.doc, 4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 4 * cm
        self.elements.append(txt)

        txt = Paragraph('Nº de parcelas: ' + str(self.venda.cond_pagamento.n_parcelas), self.styles[0])
        txt.wrapOn(self.doc, 3 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 3 * cm
        self.elements.append(txt)

    def dados_pagamento(self):
        data = []
        for pagamento in self.venda.pagamento_set.all():
            data.append([pagamento.indice_parcela, pagamento.format_vencimento, pagamento.format_valor_parcela])
        table = Table(data, style=[('GRID', (0, 0), (-1, -1), 0.5), ('FONTNAME', (0, 0), (-1, 0), REPORT_FONT_BOLD), ('FONTSIZE', (0, 0), (-1, -1), 9)])
        self.elements.append(table)

    def observacoes(self):
        txt = Paragraph('Observações', self.styles[1])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 1
        self.elements.append(txt)

        txt = Paragraph(self.venda.observacoes, self.styles[0])
        txt.wrapOn(self.doc, 19.4 * cm, 2 * cm)
        txt.drawHeight = 2 * cm
        txt.drawWidth = 19.4 * cm
        self.elements.append(txt)

    def banda_foot(self):
        txt = Paragraph('Gerado por djangoSIGE', self.styles[1])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 0
        self.elements.append(txt)

        txt = Paragraph('Data da impressão: ' + self.venda.data_emissao.strftime('%d/%m/%Y'), self.styles[0])
        txt.wrapOn(self.doc, 19.4 * cm, 0.5 * cm)
        txt.drawHeight = 0.5 * cm
        txt.drawWidth = 19.4 * cm
        txt.alignment = 2
        self.elements.append(txt)

# Exemplo de uso:
#venda = VendaReport(venda)
#venda.build()