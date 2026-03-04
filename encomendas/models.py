from django.db import models
from django.utils import timezone
from clientes.models import Cliente
# Removido import direto para evitar circularidade
# from contratos.models import Contrato

class EncomendaSurf(models.Model):
    # Relacionamentos
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='encomendas_surf')
    contrato = models.OneToOneField('contratos.Contrato', on_delete=models.SET_NULL, null=True, blank=True, related_name='ficha_surf')
    
    # Seção 1: Dados Básicos
    peso = models.CharField(max_length=50, verbose_name="Peso")
    altura = models.CharField(max_length=50, verbose_name="Altura")
    
    TIPO_PRANCHA_CHOICES = [
        ('SHORTBOARD', 'Shortboard (Pranchinha)'),
        ('FISH', 'Fish'),
        ('LONGBOARD', 'Longboard'),
        ('FAN_BOARD', 'Fan Board'),
        ('STAND_UP', 'Stand Up'),
    ]
    tipo_prancha = models.CharField(max_length=20, choices=TIPO_PRANCHA_CHOICES, verbose_name="Tipo de Prancha")

    # Seção 2/3: Configurações Técnicas (Quilhas, Fundo, Rabeta)
    QUILHAS_CHOICES = [
        ('TRI', 'Triquilhas (Convencional)'),
        ('BI', 'Biquilha'),
        ('QUADRI', 'Quadriquilha'),
        ('MULTI', 'Multiquilha (Tri ou Quadri)'),
    ]
    quilhas = models.CharField(max_length=10, choices=QUILHAS_CHOICES, verbose_name="Quilhas")

    FUNDO_CHOICES = [
        ('FLAT', 'Flat'),
        ('CONCAVE', 'Concave'),
        ('DOUBLE_CONCAVE', 'Double Concave'),
        ('THREE_CONCAVE', 'Three Concave'),
        ('CANALETA_CENTRAL', 'Canaleta - Centralizada'),
        ('CANALETA_QUILHAS', 'Canaleta - Entre Quilhas'),
    ]
    tipo_fundo = models.CharField(max_length=20, choices=FUNDO_CHOICES, verbose_name="Tipo de Fundo")

    RABETA_CHOICES = [
        ('PIN', 'Pin'),
        ('ROUND', 'Round'),
        ('SQUARE', 'Square'),
        ('SQUASH', 'Squash'),
        ('KING_SCRON', 'King Scron'),
        ('DIMON', 'Dimon'),
        ('SWALLOW', 'Swallow'),
        ('HALF_MOON', 'Half Moon Tail'),
        ('WING', 'Wing'),
        ('DOUBLE_WING', 'Double Wing'),
        ('ROUND_SQUASH', 'Round Squash'),
    ]
    rabeta = models.CharField(max_length=20, choices=RABETA_CHOICES, verbose_name="Rabeta")

    tamanho = models.CharField(max_length=50, verbose_name="Tamanho da Prancha")
    
    # Seção 4/5/6: Fan Board / Stand Up / Longboard (Modelos específicos)
    MODELO_EXT_CHOICES = [
        ('INICIANTE', 'Iniciante'),
        ('ESCOLINHA', 'Escolinha'),
        ('SEMI_PROGRESSIVO', 'Semi-Progressivo'),
        ('REMADA', 'Remada'),
        ('INTERMEDIARIO', 'Intermediário'),
        ('SURF', 'Surf'),
        ('CLASSICO', 'Clássico'),
        ('PROGRESSIVO', 'Progressivo'),
    ]
    modelo_especifico = models.CharField(max_length=20, choices=MODELO_EXT_CHOICES, null=True, blank=True)

    # Seção 15: Características Gerais
    BORDA_CHOICES = [
        ('FINA', 'Borda Fina'),
        ('MEDIA', 'Borda Média'),
        ('GROSSA', 'Borda Grossa'),
    ]
    bordas = models.CharField(max_length=10, choices=BORDA_CHOICES, verbose_name="Bordas")

    LAMINACAO_CHOICES = [
        ('FORTE', 'Forte (Mais Pesada)'),
        ('NORMAL', 'Normal'),
        ('COMPETICAO', 'Competição'),
        ('POLIDA', 'Polida'),
    ]
    tipo_laminacao = models.CharField(max_length=20, choices=LAMINACAO_CHOICES, verbose_name="Tipo de Laminação")

    COPINHO_CHOICES = [
        ('FUSION', 'Fusion'),
        ('FCS2', 'FCS-II'),
        ('FUTURE', 'Future Fins'),
    ]
    copinho = models.CharField(max_length=10, choices=COPINHO_CHOICES, verbose_name="Tipo de Copinho")

    # Seção 16: Pintura
    pintura_desejada = models.BooleanField(default=False, verbose_name="Deseja Pintura?")
    TIPO_PINTURA_CHOICES = [
        ('SIMPLES_FUNDO', 'Simples - Apenas Fundo'),
        ('SIMPLES_BORDAS', 'Simples - Apenas Bordas'),
        ('SIMPLES_DECK', 'Simples - Deck'),
        ('SIMPLES_FUNDO_DECK', 'Simples - Fundo e Deck'),
        ('ARTISTICA', 'Pintura Artística (Abstrato/Complexo)'),
    ]
    tipo_pintura = models.CharField(max_length=20, choices=TIPO_PINTURA_CHOICES, null=True, blank=True)
    
    CORES_CHOICES = [
        ('1', 'Uma Cor'),
        ('2', 'Duas Cores'),
        ('3', 'Três Cores'),
        ('4+', 'Mais que Três'),
    ]
    quantidade_cores = models.CharField(max_length=5, choices=CORES_CHOICES, null=True, blank=True)
    
    link_imagem_pintura = models.URLField(max_length=500, null=True, blank=True, verbose_name="Link da Imagem")
    pintura_arquivo = models.FileField(upload_to='encomendas/pinturas/', null=True, blank=True, verbose_name="Desenho da Pintura (Anexo)")
    
    # Seção Final: Arquivos Técnicos
    shape_3d_arquivo = models.FileField(upload_to='encomendas/shapes_3d/', null=True, blank=True, verbose_name="Projeto Shape 3D")
    
    # Controle e Status
    STATUS_ENCOMENDA_CHOICES = [
        ('FILA', 'Em Fila'),
        ('PRODUCAO', 'Em Produção'),
        ('FINALIZADA', 'Finalizada'),
        ('ENTREGUE', 'Entregue'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_ENCOMENDA_CHOICES, default='FILA', verbose_name="Status da Encomenda")
    data_encomenda = models.DateField(default=timezone.now, verbose_name="Data da Encomenda")
    data_previsao_entrega = models.DateField(null=True, blank=True, verbose_name="Previsão de Entrega")
    
    # Seção Financeira
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Total")
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor de Entrada")
    valor_restante = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Restante")
    venda_lancada = models.BooleanField(default=False, verbose_name="Venda Lançada no Financeiro")
    data_fechamento = models.DateTimeField(null=True, blank=True, verbose_name="Data de Fechamento")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_recebido(self):
        from decimal import Decimal
        entrada = self.valor_entrada or Decimal('0.00')
        if not self.pk:
            return entrada
        pagos = self.pagamentos.aggregate(models.Sum('valor'))['valor__sum'] or Decimal('0.00')
        return entrada + pagos

    @property
    def calculo_restante(self):
        from decimal import Decimal
        total = self.valor_total or Decimal('0.00')
        return total - self.total_recebido

    def save(self, *args, **kwargs):
        # Sincroniza o campo físico do banco com o cálculo para buscas/filtros
        self.valor_restante = self.calculo_restante
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ficha {self.tipo_prancha} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Encomenda de Prancha"
        verbose_name_plural = "Encomendas de Pranchas"
